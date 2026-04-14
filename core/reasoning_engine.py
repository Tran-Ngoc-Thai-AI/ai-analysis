from core.intent_detector import detect_intent
from utils.openai_client import call_openai
from utils import prompt_templates as pt


def ai_reasoning(user_prompt, eda_context, eda_summary=None):
    """Generate analysis plan using both concise summary and structured EDA."""

    intent = detect_intent(user_prompt)

    if intent == "churn":
        prompt = pt.CHURN_REASONING_PROMPT
    elif intent == "sales":
        prompt = pt.SALES_REASONING_PROMPT
    elif intent == "anomaly":
        prompt = pt.ANOMALY_REASONING_PROMPT
    else:
        prompt = pt.GENERIC_REASONING_PROMPT

    eda_summary_text = eda_summary or "(chưa có tóm tắt EDA)"
    combined_eda_context = (
        f"Tóm tắt EDA (ngắn gọn, ưu tiên nếu nhất quán):\n{eda_summary_text}\n\n"
        f"Ngữ cảnh EDA chi tiết (ưu tiên số liệu thật, không bịa cột ngoài danh sách):\n{eda_context}"
    )

    final_prompt = prompt.format(
        user_prompt=user_prompt,
        eda_context=combined_eda_context
    )

    analysis_plan = call_openai(final_prompt)

    return {
        "intent": intent,
        "analysis_plan": analysis_plan
    }
