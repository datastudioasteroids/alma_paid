# app/database.py

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------
# 1) Leer y saneamiento de la URL de conexión a Postgres
# ----------------------------------------------------------------------
raw_url = os.getenv(
    "DATABASE_URL",
    # Esta es solo la URL por defecto para desarrollo.
    # En producción, Render inyecta DATABASE_URL en las Environment Variables.
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@\
dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)
DATABASE_URL = raw_url.strip()
if not DATABASE_URL:
    sys.stderr.write("ERROR: DATABASE_URL no está definida o quedó vacía después de strip().\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 2) Crear el engine de SQLAlchemy apuntando a la URL limpia
# ----------------------------------------------------------------------
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    sys.stderr.write(f"ERROR: No se pudo crear el engine con DATABASE_URL:\n{e}\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 3) Intentar ALTER TABLE para agregar last_paid_date si falta
# ----------------------------------------------------------------------
#    - Si la tabla 'students' existe pero no tiene la columna, la añadimos.
#    - Si falla porque la tabla no existe aún, capturamos el error y seguimos.
with engine.connect() as conn:
    try:
        conn.execute(
            text("""
                ALTER TABLE students
                ADD COLUMN IF NOT EXISTS last_paid_date DATE;
            """)
        )
    except Exception as alter_err:
        # La tabla 'students' aún no existe → más adelante la crea create_all()
        sys.stderr.write(f"WARNING: No se pudo agregar last_paid_date (puede que la tabla 'students' no exista aún):\n{alter_err}\n")

# ----------------------------------------------------------------------
# 4) Importar Base para crear tablas nuevas (si no existen)
# ----------------------------------------------------------------------
#    Hacemos la importación aquí para evitar dependencias cíclicas.
from .models import *  # Para que SQLAlchemy conozca todos los modelos y Base.metadata
from .models import Base as ModelsBase

# ----------------------------------------------------------------------
# 5) Crear las tablas definidas en los modelos si no existieran
# ----------------------------------------------------------------------
#    Esto crea 'students' con last_paid_date integrado si la tabla no existía.
ModelsBase.metadata.create_all(bind=engine)

# ----------------------------------------------------------------------
# 6) Configurar SessionLocal y exportar Base para usarse en el resto de la app
# ----------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = ModelsBase

