import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger():
    # Crear carpeta logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Ruta base del archivo de logs
    log_path = "logs/bot.log"

    # Crear el manejador rotativo
    handler = TimedRotatingFileHandler(
        log_path,
        when="D",          # "D" = días
        interval=15,       # Cada 15 días se crea un nuevo archivo
        backupCount=0,     # Cuántos archivos antiguos conservar (ajústalo)
        encoding="utf-8"
    )

    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    # Configurar el logger principal
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # También mostrar logs en consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
