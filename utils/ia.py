from openai import OpenAI
import os
from utils.memory_db import save_message, get_history

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def generate_response(user_id: int, prompt: str) -> str:
    # Save the user's message
    save_message(user_id, "user", prompt)

    # Get history from the database
    history = get_history(user_id)

    # Build the context
    messages = [{"role": "system", "content": "You are ZioTiki Bot, a helpful assistant for Discord."}]
    messages.extend(history)

    # Call the model
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    # Save the bot's response
    save_message(user_id, "assistant", content)

    return content
