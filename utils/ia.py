from openai import OpenAI
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

ia_client = OpenAI(api_key=openai_api_key)

def generate_response(prompt: str) -> str:
    response = ia_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": (
                                            "Your name is ZioTiki Bot.",
                                            "You are a helpful assistant in discord with multiple users.",
                                            "Provide clear and concise answers to user questions."
                                            )
             },
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content
