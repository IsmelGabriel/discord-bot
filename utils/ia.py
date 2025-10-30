from openai import OpenAI
import os
from utils.memory import add_message, get_history

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def generate_response(user_id: int, prompt: str) -> str:
    # Save user message to memory
    add_message(user_id, "user", prompt)

    # Prepare messages for the API call
    messages = [{"role": "system", "content": "You are ZioTiki Bot, a helpful assistant on Discord."}]
    messages.extend(get_history(user_id))

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()

    # Save assistant response to memory
    add_message(user_id, "assistant", content)

    return content
