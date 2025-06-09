# migrate_add_description.py

import os
from sqlalchemy import create_engine, text

# Usar misma URL que el resto de la app
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)

engine = create_engine(DATABASE_URL)

# Ejecutar el ALTER TABLE directamente en PostgreSQL
with engine.connect() as connection:
    try:
        connection.execute(text("ALTER TABLE courses ADD COLUMN description TEXT DEFAULT '';"))
        print("✅ Columna 'description' agregada correctamente en 'courses'.")
    except Exception as e:
        print("⚠️ No se pudo agregar la columna (quizás ya existe):", e)
