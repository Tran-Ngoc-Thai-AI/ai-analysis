from openai import AzureOpenAI
import os

input_api_key = "Thêm API key của bạn vào đây hoặc đặt biến môi trường AZURE_OPENAI_API_KEY"
input_azure_endpoint = "Thêm endpoint của bạn vào đây hoặc đặt biến môi trường AZURE_OPENAI_ENDPOINT"
input_model = "Thêm tên model của bạn vào đây hoặc đặt biến môi trường AZURE_OPENAI_DEPLOYMENT"

client = AzureOpenAI(
    api_key=input_api_key or os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=input_azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-06-01"
)

def call_openai(prompt: str) -> str:
    model = input_model or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        # temperature=0.2
    )
    return response.choices[0].message.content
