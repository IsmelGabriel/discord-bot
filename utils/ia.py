from openai import OpenAi
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

ia_client = OpenAi(api_key=openai_api_key)

def generate_response(prompt: str) -> str:
    response = ia_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content']
