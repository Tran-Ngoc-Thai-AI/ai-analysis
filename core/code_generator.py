from utils.openai_client import call_openai
from utils import prompt_templates as pt


def generate_analysis_code(reasoning_output, df, eda_context=None):
    intent = reasoning_output["intent"]
    analysis_plan = reasoning_output["analysis_plan"]

    if intent == "churn":
        prompt = pt.CHURN_CODE_PROMPT
    elif intent == "sales":
        prompt = pt.SALES_CODE_PROMPT
    elif intent == "anomaly":
        prompt = pt.ANOMALY_CODE_PROMPT
    else:
        prompt = pt.GENERIC_CODE_PROMPT

    final_prompt = prompt.format(
        analysis_plan=analysis_plan,
        columns=list(df.columns),
        eda_context=eda_context or {}
    )

    return call_openai(final_prompt)
