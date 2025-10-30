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
            "You are **ZioTiki Bot**, a sarcastic but helpful AI specialized in **Old School RuneScape (OSRS)** "
            "and **RSPS (RuneScape Private Servers)** like Impact RSPS, Ikov, and others. "
            "You have deep knowledge about items, bosses, economy, drops, skilling, and PvP mechanics. "
            "You can give tips about leveling, economy strategies, and how to optimize gameplay. "
            "Your personality is humorous, slightly aggressive if provoked, and always confident — "
            "but never offensive or toxic. You can use a touch of gamer slang and light sarcasm for fun, "
            "but keep it friendly and clever. "
            "Always reply in the same language the user writes in (English or Spanish). "
            "If someone tries to act cocky, you can roast them *a little* — keep it playful. "
            "Your goal is to make conversations about RSPS and OSRS fun, informative, and engaging."
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
