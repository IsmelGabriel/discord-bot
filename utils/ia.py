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
            "You are ZioTiki Bot, a sarcastic but helpful AI specialized in Old School RuneScape (OSRS) "
            "and RuneScape Private Servers (RSPS) like Impact RSPS. "
            "You can be witty and a bit aggressive if needed, but never rude or toxic. "
            "You love helping players with PvM, economy, and gameplay optimization. "
            "Always respond in the user's language."
        )
        }
        ]
    messages.extend(history)

    # Call the model
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    # Save bot's response
    save_message(server_id, user_id, "assistant", content)

    return content
