import streamlit as st
from core.data_loader import load_data
from core.eda_engine import run_eda
from core.reasoning_engine import ai_reasoning
from core.code_generator import generate_analysis_code
from core.visualization import run_visualization
from core.insight_generator import generate_insight
from core.report_generator import build_report_html
from utils.prompt_templates import (
    EDA_SUMMARY_PROMPT,
    # AI_REASONING_EXPLANATION_PROMPT,
    REPAIR_DASHBOARD_PROMPT,
    DASHBOARD_PROMPT
)
from utils.openai_client import call_openai


st.set_page_config(page_title="AI Data Analysis Automation", layout="wide")
st.title("🤖 AI Tự động Phân tích Dữ liệu")

uploaded_file = st.file_uploader("📂 Upload data (CSV / Excel)", type=["csv", "xlsx"])
user_prompt = st.text_area("✍️ Nhập nhu cầu phân tích", height=120)

# =========================
# ANALYZE BUTTON
# =========================
if uploaded_file and user_prompt and st.button("🚀 Analyze"):
    with st.spinner("AI đang phân tích dữ liệu..."):
        df = load_data(uploaded_file) 
        eda_context = run_eda(df)
        # Giữ bản EDA rút gọn để giảm token nhưng vẫn đủ fact cho reasoning
        eda_context_light = {
            "schema": eda_context.get("schema"),
            "data_quality": eda_context.get("data_quality"),
            "distribution": {
                "describe": eda_context.get("distribution", {}).get("describe"),
                "skewness": eda_context.get("distribution", {}).get("skewness"),
            },
            # Chỉ lấy tối đa 3 biến phân loại đầu tiên để tránh phình prompt
            "categorical_summary": dict(list(eda_context.get("categorical_summary", {}).items())[:3]),
        }

        # ---- Auto EDA summary
        eda_summary = call_openai(
            EDA_SUMMARY_PROMPT.format(eda_context=eda_context)
        )

        # ---- AI reasoning plan (summary + slim context)
        analysis_plan = ai_reasoning(
            user_prompt,
            eda_context=eda_context_light,
            eda_summary=eda_summary
        )

        # ---- Reasoning explanation
        # reasoning_text = call_openai(
        #     AI_REASONING_EXPLANATION_PROMPT.format(
        #         analysis_plan=analysis_plan
        #     )
        # )

        # ---- Generate charts (analysis plan + EDA context gọn)
        code = generate_analysis_code(analysis_plan, df, eda_context_light)
        chart_paths = run_visualization(code, df)
        dashboard_code = call_openai(
            DASHBOARD_PROMPT.format(
                eda_context=eda_context_light,
                analysis_plan=analysis_plan,
                columns=list(df.columns)
            )
        )
        dashboard_paths = run_visualization(dashboard_code, df)
        if not dashboard_paths:
            repaired_dashboard_code = call_openai(
                REPAIR_DASHBOARD_PROMPT.format(
                    dashboard_code=dashboard_code,
                    columns=list(df.columns)
                )
            )
            dashboard_paths = run_visualization(repaired_dashboard_code, df)
            dashboard_code = repaired_dashboard_code

        # ---- Insight
        insight_text = generate_insight(
            analysis_plan,
            eda_context=eda_context,
            eda_summary=eda_summary
        )

        # ---- SAVE ALL TO SESSION_STATE
        st.session_state["df"] = df
        st.session_state["eda_summary"] = eda_summary
        st.session_state["analysis_plan"] = analysis_plan
        # st.session_state["reasoning_text"] = reasoning_text
        st.session_state["chart_paths"] = chart_paths
        st.session_state["dashboard_code"] = dashboard_code
        st.session_state["dashboard_paths"] = dashboard_paths
        st.session_state["insight_text"] = insight_text
        st.session_state["Ketluan"] = """Hệ thống phân tích dữ liệu tự động bằng AI cho phép thực hiện toàn bộ quy trình từ khám phá dữ liệu, suy luận phân tích, trực quan hóa cho đến sinh báo cáo mà không cần can thiệp thủ công.

Giải pháp này giúp rút ngắn thời gian phân tích, nâng cao khả năng phát hiện insight và hỗ trợ hiệu quả cho việc ra quyết định dựa trên dữ liệu trong doanh nghiệp.
"""

# =========================
# RENDER DASHBOARD (ALWAYS FROM SESSION_STATE)
# =========================
# =========================
# RENDER DASHBOARD (REPORT VIEWER)
# =========================
if "df" in st.session_state:

    # ===== HEADER =====
    st.markdown("## 📄 BÁO CÁO PHÂN TÍCH DỮ LIỆU TỰ ĐỘNG BẰNG AI")
    st.caption(
        "Hệ thống: Upload → Dashboard -> Auto EDA → Charts → Insight → PDF  \n"
        "Báo cáo được sinh hoàn toàn tự động bằng AI."
    )
    st.divider()

    # ===== SECTION 1: DASHBOARD =====
    if "dashboard_paths" in st.session_state:
        st.markdown("## 1️⃣ Dashboard phân tích dữ liệu")
        if st.session_state["dashboard_paths"]:
            for i, p in enumerate(st.session_state["dashboard_paths"], start=1):
                st.markdown(f"**Hình {i}: Dashboard phân tích dữ liệu**")
                st.image(p, use_column_width=True)
        else:
            st.warning(
                "Chưa sinh được hình dashboard từ code LLM. "
                "Bạn có thể bấm Analyze lại hoặc điều chỉnh prompt phân tích."
            )
            if st.session_state.get("dashboard_code"):
                with st.expander("Xem code dashboard LLM để debug"):
                    st.code(st.session_state["dashboard_code"], language="python")
        st.divider()

    # ===== SECTION 2: DATA OVERVIEW =====
    st.markdown("## 2️⃣ Tổng quan dữ liệu")
    st.markdown(f"""
- **Số dòng dữ liệu:** {len(st.session_state["df"])}
- **Số cột dữ liệu:** {len(st.session_state["df"].columns)}
- **Danh sách cột:** {", ".join(st.session_state["df"].columns)}
""")
    st.divider()

    # ===== SECTION 3: AUTO EDA =====
    if st.session_state.get("eda_summary"):
        st.markdown("## 3️⃣ Phân tích dữ liệu thăm dò (Auto EDA)")
        st.markdown(st.session_state["eda_summary"])
        st.divider()

    # ===== SECTION 4: CHARTS =====
    if st.session_state.get("chart_paths"):
        st.markdown("## 4️⃣ Biểu đồ phân tích dữ liệu")
        for i, p in enumerate(st.session_state["chart_paths"], start=1):
            st.markdown(f"**Hình {i}: Biểu đồ phân tích dữ liệu**")
            st.image(p, use_column_width=True)
        st.divider()


    # ===== SECTION 4: AI REASONING =====
    # if st.session_state.get("reasoning_text"):
    #     st.markdown("## 4️⃣ Giải thích suy luận của AI")
    #     st.markdown(st.session_state["reasoning_text"])
    #     st.divider()

    # ===== SECTION 5: INSIGHT =====
    if st.session_state.get("insight_text"):
        st.markdown("## 5️⃣ Nhận định & Insight từ AI")
        st.markdown(st.session_state["insight_text"])
        st.divider()

    # ===== SECTION 6: CONCLUSION =====
    st.markdown("## 6️⃣ Kết luận")
    st.markdown(st.session_state["Ketluan"])


# =========================
# EXPORT HTML REPORT
# =========================
# if all(k in st.session_state for k in [
#     "df", "chart_paths", "dashboard_paths", "insight_text", "eda_summary"
# ]):
#     html_text = build_report_html(
#         df=st.session_state["df"],
#         eda_summary=st.session_state["eda_summary"],
#         dashboard_paths=st.session_state["dashboard_paths"],
#         chart_paths=st.session_state["chart_paths"],
#         insight_text=st.session_state["insight_text"],
#         ketluan=st.session_state["Ketluan"]
#     )
#     html_bytes = html_text.encode("utf-8")

#     st.download_button(
#         "🧾 Download HTML Report",
#         data=html_bytes,
#         file_name="ai_data_report.html",
#         mime="text/html"
#     )
