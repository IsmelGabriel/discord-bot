from utils.db import conectar

def get_prompt(server_id=None, name="default"):
    """Obtiene el prompt de un servidor. Si no existe, usa el prompt global."""
    conn = conectar()
    if not conn:
        return "You are a helpful assistant."

    try:
        with conn.cursor() as cur:
            # 1️⃣ Buscar prompt del servidor específico
            cur.execute(
                "SELECT content FROM prompts WHERE server_id = %s AND name = %s LIMIT 1;",
                (server_id, name),
            )
            result = cur.fetchone()

            if result:
                return result[0]

            # 2️⃣ Si no existe, buscar el prompt global (server_id IS NULL)
            cur.execute(
                "SELECT content FROM prompts WHERE server_id IS NULL AND name = %s LIMIT 1;",
                (name,),
            )
            result = cur.fetchone()
            return result[0] if result else "You are a helpful assistant."
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el prompt: {e}")
        return "You are a helpful assistant."
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
                DO UPDATE SET content = EXCLUDED.content, updated_at = NOW();
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
