import re
from datetime import datetime
from utils.db import execute_query

def detectar_tipo_contenido(mensaje: str) -> str:
    """Detecta si el mensaje contiene imagen, video, link o texto."""
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


def guardar_log(level: str, server_id: int, author_id: int, author_name: str, mensaje: str):
    """Guarda un log en la base de datos."""
    tipo = detectar_tipo_contenido(mensaje)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = """
        INSERT INTO logs (level, server_id, author_id, author_name, message, content_type, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    params = (level, server_id, author_id, author_name, mensaje, tipo, fecha_hora)

    execute_query(query, params)

    print(f"[{fecha_hora}] ({level}) {author_name}: {mensaje} [{tipo}]")
