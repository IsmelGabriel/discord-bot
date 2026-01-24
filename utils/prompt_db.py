from utils.db import conectar
from datetime import datetime

def get_prompt(server_id=None, name="default"):
    """Obtiene el prompt de un servidor. Si no existe, usa el prompt global."""
    conn = conectar()
    if not conn:
        return "You are a helpful assistant."

    try:
        with conn.cursor() as cur:
            # Buscar prompt del servidor específico (solo por server_id primero)
            if server_id is not None:
                # Primero intenta buscar con server_id y name
                cur.execute(
                    "SELECT content FROM prompts WHERE server_id = %s AND name = %s LIMIT 1;",
                    (server_id, name),
                )
                result = cur.fetchone()

                if result:
                    return result[0]

                # Si no encuentra, buscar cualquier prompt del servidor (por si cambió el name)
                cur.execute(
                    "SELECT content FROM prompts WHERE server_id = %s LIMIT 1;",
                    (server_id,),
                )
                result = cur.fetchone()

                if result:
                    return result[0]

            # Si no existe, buscar el prompt global (server_id IS NULL)
            cur.execute(
                "SELECT content FROM prompts WHERE server_id IS NULL AND name = %s LIMIT 1;",
                (name,),
            )
            result = cur.fetchone()
            return result[0] if result else (
                "Eres un bot en un servidor de Discord relacionado con RuneScape. "
                "Respondes con sarcasmo y humor negro, pero a veces das buenos consejos. "
                "Te adaptas a las conversaciones y respondes según el humor y la toxicidad del chat. "
                "No eres sensible a los insultos y si te atacan, los destruyes con humor ácido."
                )
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el prompt: {e}")
        return (
                "Eres un bot en un servidor de Discord relacionado con RuneScape. "
                "Respondes con sarcasmo y humor negro, pero a veces das buenos consejos. "
                "Te adaptas a las conversaciones y respondes según el humor y la toxicidad del chat. "
                "No eres sensible a los insultos y si te atacan, los destruyes con humor ácido."
                )
    finally:
        conn.close()


def update_prompt(server_id, name, content):
    """Crea o actualiza un prompt de un servidor."""
    conn = conectar()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO prompts (server_id, name, content)
                VALUES (%s, %s, %s)
                ON CONFLICT (server_id, name)
                DO UPDATE SET content = EXCLUDED.content, update_at = NOW();
                """,
                (server_id, name, content),
            )
            conn.commit()
            print(f"[PROMPT] '{name}' actualizado para server {server_id or 'global'}.")
            return True
    except Exception as e:
        print(f"[ERROR] No se pudo actualizar el prompt: {e}")
        return False
    finally:
        conn.close()
