# app/database.py

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------------------------------------------------------
# 1) Leer y limpiar la URL de conexión a Postgres de la variable de entorno
# ----------------------------------------------------------------------
raw_url = os.getenv(
    "DATABASE_URL",
    # Esta URL solo se usa en desarrollo local si no existe VARIABLE de entorno.
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@\
dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)
DATABASE_URL = raw_url.strip()
if not DATABASE_URL:
    sys.stderr.write("ERROR: DATABASE_URL no está definida o quedó vacía después de strip().\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 2) Crear el engine de SQLAlchemy
# ----------------------------------------------------------------------
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    sys.stderr.write(f"ERROR: No se pudo crear el engine con la URL:\n{e}\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 3) Configurar SessionLocal y Base
# ----------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

