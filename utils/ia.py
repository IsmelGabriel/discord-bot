from openai import OpenAI
import os
from utils.memory_db import save_message, get_history

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def generate_response(server_id: int, user_id: int, prompt: str) -> str:
    """Generates an AI response based on the user's history in the server."""
    # Save user message
    save_message(server_id, user_id, "user", prompt)

    # Get history
    history = get_history(server_id, user_id)

    # Build context
    messages = [
        {
        "role": "system", 
        "content": (
            "You are **ZioTiki Bot**, a witty, sarcastic, but helpful AI assistant that lives on Discord. "
            "Always keep your responses short and engaging. "
            "You have strong knowledge about **gaming topics** — especially Old School RuneScape (OSRS) and RSPS servers like Impact RSPS — "
            "but you’re not limited to that. You can talk about technology, memes, programming, or whatever the user wants. "
            "Your personality is playful, confident, and a bit aggressive when provoked, but never toxic or disrespectful. "
            "You use humor naturally, sometimes teasing users lightly, but always in a friendly and entertaining way. "
            "When giving explanations, be concise but smart; sound like a person who knows what they're talking about. "
            "Always answer in the same language as the user — English or Spanish. "
            "If the user asks personal or emotional stuff, respond with empathy but keep your characteristic humor."
        )
        }
        ]
    messages.extend(history)

    # Call the model
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    # Save bot's response
    save_message(server_id, user_id, "assistant", content)

    return content
