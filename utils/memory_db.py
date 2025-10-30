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

def save_message(server_id: int, user_id: int, role: str, content: str):
    """Saves a message in the database."""
    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO memories (server_id, user_id, role, content) VALUES (%s, %s, %s, %s)",
                (server_id, user_id, role, content)
            )
            conn.commit()

def get_history(server_id: int, user_id: int):
    """Gets the conversation history of a user within a server."""
    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT role, content FROM memories WHERE server_id = %s AND user_id = %s ORDER BY id ASC",
                (server_id, user_id)
            )
            return cur.fetchall()

def clear_history(server_id: int, user_id: int):
    """Clears a user's memory in a specific server."""
    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM memories WHERE server_id = %s AND user_id = %s", (server_id, user_id))
            conn.commit()
