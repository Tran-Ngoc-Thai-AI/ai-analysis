
import re
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid
import traceback


def clean_code(code: str) -> str:
    code = re.sub(r"```(?:python)?", "", code)
    code = re.sub(r"```", "", code)
    return code.strip()


# ✅ NEW: AST Transformer để fix duplicate kwargs (đặc biệt là color)
class FixDuplicateKwargs(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)

        seen = set()
        new_keywords = []

        for kw in node.keywords:
            if kw.arg is None:
                new_keywords.append(kw)
                continue

            # nếu bị trùng (vd color), chỉ giữ cái đầu
            if kw.arg in seen:
                continue

            seen.add(kw.arg)
            new_keywords.append(kw)

        node.keywords = new_keywords
        return node


def sanitize_generated_code(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code

    filtered_body = []
    blocked_names = {"df", "save_fig", "pd", "plt", "np"}

    for node in tree.body:
        # ❌ Drop plt.style.use(...)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "use"
                and isinstance(func.value, ast.Attribute)
                and func.value.attr == "style"
                and isinstance(func.value.value, ast.Name)
                and func.value.value.id == "plt"
            ):
                continue

        # ❌ Block redefining save_fig
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "save_fig":
            continue

        # ❌ Block override injected vars
        assigned_names = set()
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    assigned_names.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assigned_names.add(node.target.id)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            assigned_names.add(node.target.id)

        if assigned_names & blocked_names:
            continue

        # ❌ Block numpy import
        if isinstance(node, ast.Import):
            names = {n.name.split(".")[0] for n in node.names}
            if "numpy" in names:
                continue

        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] == "numpy":
                continue

        filtered_body.append(node)

    tree.body = filtered_body

    # ✅ APPLY FIX duplicate kwargs
    tree = FixDuplicateKwargs().visit(tree)
    ast.fix_missing_locations(tree)

    return ast.unparse(tree)


def patch_ptp_calls(code: str) -> str:
    pattern = re.compile(r"(\b[\w\.]+\b)\.ptp\(([^)]*)\)")
    pattern_numpy = re.compile(r"\bnumpy\.ptp\(([^)]*)\)")

    def repl(m):
        expr = m.group(1)
        args = m.group(2).strip()
        return f"np.ptp({expr}, {args})" if args else f"np.ptp({expr})"

    code = pattern.sub(repl, code)
    code = pattern_numpy.sub(lambda m: f"np.ptp({m.group(1)})", code)
    return code


def run_visualization(code, df, output_dir="outputs/charts"):
    os.makedirs(output_dir, exist_ok=True)

    old_rc = plt.rcParams.copy()

    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except Exception:
        plt.style.use("default")

    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.edgecolor": "#222",
        "axes.labelcolor": "#111",
        "xtick.color": "#111",
        "ytick.color": "#111",
        "grid.color": "#d6d6d6",
        "text.color": "#111",
    })

    chart_paths = []

    def save_fig(fig):
        try:
            for ax in fig.get_axes():
                ax.set_facecolor("white")
        except Exception:
            pass

        fig.patch.set_facecolor("white")

        try:
            fig.tight_layout(pad=1.2)
        except Exception:
            pass

        path = os.path.join(output_dir, f"{uuid.uuid4().hex}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        chart_paths.append(path)

    # ✅ SAFE pandas.cut
    original_pd_cut = pd.cut
    original_pd_qcut = pd.qcut

    def safe_pd_cut(*args, **kwargs):
        try:
            return original_pd_cut(*args, **kwargs)
        except ValueError as e:
            if "Bin edges must be unique" not in str(e):
                raise

            retry_kwargs = dict(kwargs)
            retry_kwargs["duplicates"] = "drop"

            try:
                return original_pd_cut(*args, **retry_kwargs)
            except ValueError:
                retry_kwargs.pop("labels", None)
                return original_pd_cut(*args, **retry_kwargs)

    # ✅ SAFE pandas.qcut
    def safe_pd_qcut(*args, **kwargs):
        try:
            return original_pd_qcut(*args, **kwargs)
        except ValueError as e:
            if "Bin edges must be unique" not in str(e):
                raise

            retry_kwargs = dict(kwargs)
            retry_kwargs["duplicates"] = "drop"

            try:
                return original_pd_qcut(*args, **retry_kwargs)
            except ValueError:
                # labels thường bị lệch số lượng khi duplicates='drop'
                retry_kwargs.pop("labels", None)
                return original_pd_qcut(*args, **retry_kwargs)

    class PandasProxy:
        def __getattr__(self, name):
            if name == "cut":
                return safe_pd_cut
            if name == "qcut":
                return safe_pd_qcut
            return getattr(pd, name)

    def safe_np_ptp(a, axis=None, out=None, **kwargs):
        try:
            arr = np.asarray(pd.to_numeric(a, errors="coerce"))
            arr = arr[~np.isnan(arr)]
            if arr.size == 0:
                return 0
            return float(np.nanmax(arr) - np.nanmin(arr))
        except Exception:
            return 0

    class NumpyProxy:
        def __getattr__(self, name):
            if name == "ptp":
                return safe_np_ptp
            return getattr(np, name)

    env = {
        "df": df,
        "pd": PandasProxy(),
        "np": NumpyProxy(),
        "plt": plt,
        "save_fig": save_fig
    }

    clean = clean_code(code)
    clean = patch_ptp_calls(clean)
    safe_code = sanitize_generated_code(clean)

    try:
        exec(safe_code, env, env)
    except Exception:
        # Dump generated code + traceback để debug đúng dòng lỗi khi exec thất bại.
        debug_dir = os.path.join(output_dir, "_debug")
        os.makedirs(debug_dir, exist_ok=True)
        debug_base = uuid.uuid4().hex

        code_path = os.path.join(debug_dir, f"failed_vis_code_{debug_base}.py")
        trace_path = os.path.join(debug_dir, f"failed_vis_trace_{debug_base}.txt")

        numbered_lines = [f"{i:04d}: {line}" for i, line in enumerate(safe_code.splitlines(), start=1)]

        with open(code_path, "w", encoding="utf-8") as f:
            f.write("\n".join(numbered_lines))

        with open(trace_path, "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())

        raise
    finally:
        plt.rcParams.update(old_rc)

    return chart_paths

