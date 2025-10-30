import psycopg2
import os

# Conexión a la base de datos usando las variables internas de Render
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "dpg-d41dqo9r0fns73cbvt00-a"),  # cambia si tu host es distinto
    dbname=os.getenv("DB_NAME", "discord_logs"),
    user=os.getenv("DB_USER", "ziotiki"),
    password=os.getenv("DB_PASS", "TU_CONTRASEÑA_AQUÍ"),
    port=5432
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(20),
    server_id BIGINT,
    author_id BIGINT,
    author_name VARCHAR(100),
    message TEXT,
    content_type VARCHAR(20),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cur.close()
conn.close()
print("✅ Tabla 'logs' creada correctamente.")
