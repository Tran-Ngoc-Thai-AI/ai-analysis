from utils.openai_client import call_openai
from utils.prompt_templates import INTENT_DETECTION_PROMPT

def detect_intent(user_prompt: str) -> str:
    prompt = INTENT_DETECTION_PROMPT.format(user_prompt=user_prompt)
    intent = call_openai(prompt).strip().lower()

    if intent not in ["churn", "sales", "anomaly"]:
        return "generic"

    return intent
