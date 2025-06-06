# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1) Lectura de la URL de conexión a Postgres (Render provee esta ENV var por defecto).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)

# 2) Creamos el engine apuntando a esa URL
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    # Si la URL está mal formateada, levantamos un error claro
    raise RuntimeError(f"ERROR: No se pudo crear el engine con DATABASE_URL:\n  Value: {DATABASE_URL}\n  Detalle: {e}")

# 3) SessionLocal seguirá siendo la "fábrica" de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4) Base declarativa para todos los modelos
Base = declarative_base()


