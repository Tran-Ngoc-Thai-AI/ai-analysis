from utils.openai_client import call_openai
from utils import prompt_templates as pt


def generate_insight(reasoning_output, eda_context=None, eda_summary=None):
    """Compose an insight prompt enriched with the latest EDA summary."""

    intent = reasoning_output["intent"]
    analysis_plan = reasoning_output["analysis_plan"]

    if intent == "churn":
        prompt = pt.CHURN_INSIGHT_PROMPT
    elif intent == "sales":
        prompt = pt.SALES_INSIGHT_PROMPT
    elif intent == "anomaly":
        prompt = pt.ANOMALY_INSIGHT_PROMPT
    else:
        return "No specific insights generated."

    # Prefer the human-readable EDA summary; fallback to raw context string.
    eda_text = eda_summary or eda_context or "(không có thông tin EDA)"

    final_prompt = (
        f"{prompt}\n\n"
        f"Kế hoạch phân tích:\n{analysis_plan}\n\n"
        f"Tóm tắt EDA:\n{eda_text}"
    )

    return call_openai(final_prompt)
