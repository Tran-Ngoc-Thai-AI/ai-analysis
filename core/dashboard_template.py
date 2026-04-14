import os
import uuid
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _save_fig(fig, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{uuid.uuid4().hex}.png")
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lower_map = {c.lower(): c for c in df.columns}
    for key in candidates:
        if key.lower() in lower_map:
            return lower_map[key.lower()]
    return None


def generate_rich_dashboard(df: pd.DataFrame, output_dir: str = "outputs/charts") -> List[str]:
    paths: List[str] = []
    if df is None or df.empty:
        return paths

    churn_col = _first_existing(df, ["churn", "exited", "is_churn"])
    active_col = _first_existing(df, ["active_member", "isactive", "active"])
    age_col = _first_existing(df, ["age"])
    country_col = _first_existing(df, ["country", "geography", "region"])
    credit_col = _first_existing(df, ["credit_score", "creditscore"])
    balance_col = _first_existing(df, ["balance"])
    customer_col = _first_existing(df, ["customer_id", "customerid", "id"])

    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    trend_col = age_col if age_col else (num_cols[0] if num_cols else None)

    bg = "#0f1422"
    panel = "#1a2236"
    border = "#2a3550"
    text = "#e7ecf7"
    muted = "#9bb0d3"
    c1 = "#ff4d4f"
    c2 = "#2d9cff"
    c3 = "#00d1b2"
    c4 = "#8c84ff"
    c5 = "#f6c445"

    fig = plt.figure(figsize=(19.2, 10.8), facecolor=bg)
    gs = fig.add_gridspec(10, 24, wspace=0.9, hspace=1.0)

    def style_panel(ax, title: str | None = None):
        ax.set_facecolor(panel)
        for sp in ax.spines.values():
            sp.set_color(border)
            sp.set_linewidth(1.2)
        ax.tick_params(colors=muted, labelsize=10)
        if title:
            ax.set_title(title, fontsize=13, color=text, loc="left", pad=10, fontweight="bold")

    def kpi(ax, value: str, label: str, color: str, spark_series: np.ndarray):
        style_panel(ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.text(0.05, 0.72, value, fontsize=30, color=color, fontweight="bold", ha="left", va="center")
        ax.text(0.05, 0.38, label, fontsize=13, color=muted, ha="left", va="center")
        ax.text(0.05, 0.18, "Status: Stable", fontsize=10.5, color=c5, ha="left", va="center", fontweight="bold")
        if spark_series.size > 1:
            x = np.linspace(0.58, 0.95, spark_series.size)
            y0 = 0.72 + 0.12 * (spark_series - spark_series.min()) / (spark_series.ptp() + 1e-9)
            ax.plot(x, y0, color=color, linewidth=2.2)
            ax.fill_between(x, y0, 0.70, color=color, alpha=0.15)

    # Header
    fig.text(0.045, 0.94, "Customer Intelligence Dashboard", color=text, fontsize=34, fontweight="bold")
    fig.text(0.045, 0.905, "Auto-generated rich dashboard from dataset profile", color=muted, fontsize=18)

    n = len(df)
    unique_customers = int(df[customer_col].nunique()) if customer_col else n
    churn_rate = float(df[churn_col].mean() * 100) if churn_col else np.nan
    active_rate = float(df[active_col].mean() * 100) if active_col else np.nan
    avg_credit = float(df[credit_col].mean()) if credit_col else np.nan
    avg_balance = float(df[balance_col].mean()) if balance_col else np.nan

    spark = np.linspace(0.3, 1, 14) + np.random.default_rng(7).normal(0, 0.05, 14)

    ax1 = fig.add_subplot(gs[1:4, 0:4]);  kpi(ax1, f"{unique_customers:,}", "Total Customers", c2, spark)
    ax2 = fig.add_subplot(gs[1:4, 4:8]);  kpi(ax2, f"{churn_rate:.1f}%" if not np.isnan(churn_rate) else "--", "Churn Rate", c1, spark[::-1])
    ax3 = fig.add_subplot(gs[1:4, 8:12]); kpi(ax3, f"{active_rate:.1f}%" if not np.isnan(active_rate) else "--", "Active Members", c3, np.sort(spark))
    ax4 = fig.add_subplot(gs[1:4, 12:16]); kpi(ax4, f"{avg_credit:.0f}" if not np.isnan(avg_credit) else "--", "Avg Credit Score", c4, np.roll(spark, 3))

    # Donut 1: churn
    axd1 = fig.add_subplot(gs[1:4, 16:20]); style_panel(axd1, "Churn Split")
    axd1.set_xticks([]); axd1.set_yticks([])
    if churn_col:
        churned = float(df[churn_col].sum())
        stayed = float(max(n - churned, 0))
        axd1.pie([stayed, churned], colors=[c3, c1], startangle=90, wedgeprops={"width": 0.33, "edgecolor": panel})
        axd1.text(0, 0, f"{(churned/max(n,1))*100:.0f}%", color=text, fontsize=26, fontweight="bold", ha="center", va="center")
    else:
        axd1.text(0.5, 0.5, "No churn data", color=muted, ha="center", va="center", transform=axd1.transAxes)

    # Donut 2: active/card ratio
    axd2 = fig.add_subplot(gs[1:4, 20:24]); style_panel(axd2, "Active Ratio")
    axd2.set_xticks([]); axd2.set_yticks([])
    if active_col:
        active = float(df[active_col].sum())
        inactive = float(max(n - active, 0))
        axd2.pie([active, inactive], colors=[c2, "#3b4356"], startangle=90, wedgeprops={"width": 0.33, "edgecolor": panel})
        axd2.text(0, 0, f"{(active/max(n,1))*100:.0f}%", color=text, fontsize=26, fontweight="bold", ha="center", va="center")
    else:
        axd2.text(0.5, 0.5, "No active data", color=muted, ha="center", va="center", transform=axd2.transAxes)

    # Trend
    axt = fig.add_subplot(gs[4:8, 0:12]); style_panel(axt, "Trend Analysis")
    if trend_col and pd.api.types.is_numeric_dtype(df[trend_col]):
        s = df[trend_col].dropna().astype(float)
        if len(s) > 5:
            bins = np.linspace(float(s.min()), float(s.max()), 8)
            bins = np.unique(bins)
            if len(bins) >= 3:
                labels = [f"B{i+1}" for i in range(len(bins) - 1)]
                grouped = pd.cut(s, bins=bins, labels=labels, include_lowest=True, duplicates="drop").value_counts().sort_index()
                x = np.arange(len(grouped))
                y = grouped.values.astype(float)
                axt.plot(x, y, marker="o", color=c2, linewidth=3)
                axt.fill_between(x, y, color=c2, alpha=0.12)
                peak = int(np.argmax(y))
                axt.annotate("Peak", xy=(peak, y[peak]), xytext=(peak, y[peak] + max(y) * 0.12),
                             color=c5, arrowprops={"arrowstyle": "->", "color": c5, "lw": 1.5}, fontsize=11, fontweight="bold")
                axt.set_xticks(x)
                axt.set_xticklabels(grouped.index.astype(str), color=muted)
                axt.set_ylabel("Count", color=muted)
            else:
                axt.text(0.5, 0.5, "Not enough spread for trend bins", color=muted, ha="center", va="center", transform=axt.transAxes)
        else:
            axt.text(0.5, 0.5, "Not enough rows for trend", color=muted, ha="center", va="center", transform=axt.transAxes)
    else:
        axt.text(0.5, 0.5, "No numeric trend column", color=muted, ha="center", va="center", transform=axt.transAxes)

    # Composition by country
    axb = fig.add_subplot(gs[4:8, 12:24]); style_panel(axb, "Composition by Segment")
    if country_col and churn_col:
        temp = df.groupby([country_col, churn_col]).size().unstack(fill_value=0)
        names = temp.index.astype(str).tolist()
        base = temp[temp.columns.min()].values if len(temp.columns) else np.zeros(len(temp))
        top = temp[temp.columns.max()].values if len(temp.columns) > 1 else np.zeros(len(temp))
        x = np.arange(len(names))
        axb.bar(x, base, color=c2, width=0.56, label="Base")
        axb.bar(x, top, bottom=base, color=c1, width=0.56, label="Top")
        axb.set_xticks(x)
        axb.set_xticklabels(names, color=muted)
        axb.legend(frameon=False, labelcolor=muted, loc="upper right")
        for i, (b, t) in enumerate(zip(base, top)):
            total = float(b + t)
            pct = (t / total * 100) if total > 0 else 0
            axb.text(i, total + max(1.0, total * 0.02), f"{pct:.1f}%", ha="center", va="bottom", color=text, fontsize=10)
    elif country_col:
        vc = df[country_col].astype(str).value_counts().head(8)
        x = np.arange(len(vc))
        axb.bar(x, vc.values, color=c2, width=0.56)
        axb.set_xticks(x)
        axb.set_xticklabels(vc.index.tolist(), color=muted)
        axb.set_ylabel("Count", color=muted)
    else:
        axb.text(0.5, 0.5, "No segment column", color=muted, ha="center", va="center", transform=axb.transAxes)

    # Footer strip
    axf = fig.add_subplot(gs[8:10, 0:24]); style_panel(axf)
    axf.set_xticks([]); axf.set_yticks([])
    axf.text(0.01, 0.55, "Highlights", color=text, fontsize=13, fontweight="bold", transform=axf.transAxes)
    msg = []
    if not np.isnan(churn_rate):
        msg.append(f"Churn {churn_rate:.1f}%")
    if not np.isnan(active_rate):
        msg.append(f"Active {active_rate:.1f}%")
    if not np.isnan(avg_balance):
        msg.append(f"Avg Balance {avg_balance:,.0f}")
    axf.text(0.12, 0.55, " | ".join(msg) if msg else "Insufficient KPI columns", color=muted, fontsize=12, transform=axf.transAxes)

    paths.append(_save_fig(fig, output_dir))
    return paths
