import logging
import mysql.connector
from datetime import datetime
import os
import re

# 🔧 Variables de entorno
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "discord_logs")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")

# 🔍 Detecta tipo de contenido en el mensaje
def detect_content_type(message: str):
    if not message or message.strip() == "":
        return "vacio"
    if re.search(r"(https?:\/\/[^\s]+(\.png|\.jpg|\.jpeg|\.gif))", message, re.IGNORECASE):
        return "imagen"
    if re.search(r"(https?:\/\/[^\s]+(\.mp4|\.mov|\.avi|\.webm))", message, re.IGNORECASE):
        return "video"
    if re.search(r"(https?:\/\/[^\s]+)", message):
        return "link"
    return "texto"

# 🧱 Clase para guardar logs en MySQL
class MySQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        try:
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            self.cursor = self.conn.cursor()
            print("✅ Conectado a MySQL correctamente.")
        except mysql.connector.Error as err:
            print(f"❌ Error al conectar con MySQL: {err}")

    def emit(self, record):
        try:
            log_data = record.msg if isinstance(record.msg, dict) else {}

            level = record.levelname
            server_id = log_data.get("server_id")
            author_id = log_data.get("author_id")
            author_name = log_data.get("author_name")
            message = log_data.get("message", "")
            content_type = detect_content_type(message)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            query = """
                INSERT INTO logs (level, server_id, author_id, author_name, message, content_type, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (level, server_id, author_id, author_name, message, content_type, timestamp)

            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error al guardar log en MySQL: {e}")

# 🧩 Configurar el logger
def setup_logger():
    logger = logging.getLogger("bot_logger")
    logger.setLevel(logging.INFO)

    # 📦 Muestra los logs en consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))

    # 💾 Guarda los logs en MySQL
    mysql_handler = MySQLHandler()

    # Evita agregar múltiples handlers duplicados
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(mysql_handler)

    return logger
