import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import closing

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432)
}

def save_message(user_id: int, role: str, content: str):
    """Saves a message in the database."""
    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO memories (user_id, role, content) VALUES (%s, %s, %s)",
                (user_id, role, content)
            )
            conn.commit()

def get_history(user_id: int):
    """Gets the conversation history of a user."""
    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT role, content FROM memories WHERE user_id = %s ORDER BY id ASC",
                (user_id,)
            )
            return cur.fetchall()

def clear_history(user_id: int):
    """Clears the user's memory."""
    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM memories WHERE user_id = %s", (user_id,))
            conn.commit()
