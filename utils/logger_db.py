import os
import re
import psycopg2
from datetime import datetime

# Conexión a la base de datos en Render usando variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", 5432)



def conectar():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        return None


def detectar_tipo_contenido(mensaje):
    """Detecta si el mensaje contiene imagen, video o link."""
    if re.search(r'(https?:\/\/.*\.(?:png|jpg|jpeg|gif|webp))', mensaje):
        return "imagen"
    elif re.search(r'(https?:\/\/.*\.(?:mp4|mov|avi|mkv))', mensaje):
        return "video"
    elif re.search(r'https?:\/\/', mensaje):
        return "link"
    elif mensaje.strip() == "":
        return "vacío"
    else:
        return "texto"


def guardar_log(level, server_id, author_id, author_name, mensaje):
    conn = conectar()
    if not conn:
        return

    tipo = detectar_tipo_contenido(mensaje)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO logs (level, server_id, author_id, author_name, message, content_type, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (level, server_id, author_id, author_name, mensaje, tipo, fecha_hora))
            conn.commit()
            print(f"[{fecha_hora}] ({level}) {author_name}: {mensaje} [{tipo}]")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el log: {e}")
    finally:
        conn.close()
