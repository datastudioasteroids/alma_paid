# app/database.py

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------
# 1) Lectura y saneamiento de la URL de conexión
# ----------------------------------------------------------------------
# Preferimos obtener la URL de entorno; si no existe, usamos la cadena por defecto.
raw_url = os.getenv(
    "DATABASE_URL",
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)

# Aplicamos strip() para eliminar espacios o saltos de línea accidentales al inicio o final.
DATABASE_URL = raw_url.strip()

# Si, tras hacer strip(), la URL queda vacía o no válida, detenemos la aplicación.
if not DATABASE_URL:
    sys.stderr.write("ERROR: DATABASE_URL no está definida o quedó vacía después de strip().\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 2) Crear el engine de SQLAlchemy apuntando a PostgreSQL
# ----------------------------------------------------------------------
# Al pasar DATABASE_URL limpia, evitamos errores de 'database does not exist'
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    sys.stderr.write(f"ERROR: No se pudo crear el engine con DATABASE_URL:\n{e}\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 3) SessionLocal: fábrica de sesiones para PostgreSQL
# ----------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------------------------------------------------
# 4) Base declarativa para los modelos
# ----------------------------------------------------------------------
Base = declarative_base()

