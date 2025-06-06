# app/database.py

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------
# 1) Lectura y saneamiento de la URL de conexión
# ----------------------------------------------------------------------
raw_url = os.getenv(
    "DATABASE_URL",
    # URL por defecto (pero en producción siempre vendrá desde Render)
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)
DATABASE_URL = raw_url.strip()
if not DATABASE_URL:
    sys.stderr.write("ERROR: DATABASE_URL no está definida o quedó vacía después de strip().\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 2) Crear el engine de SQLAlchemy apuntando a PostgreSQL
# ----------------------------------------------------------------------
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    sys.stderr.write(f"ERROR: No se pudo crear el engine con DATABASE_URL:\n{e}\n")
    sys.exit(1)

# ----------------------------------------------------------------------
# 3) Asegurarnos de que la columna `last_paid_date` exista en Postgres
# ----------------------------------------------------------------------
# Ejecutamos un ALTER TABLE ... ADD COLUMN IF NOT EXISTS justo al iniciar
# (esto no afecta tablas que ya tienen la columna; en otras, la crea).
with engine.connect() as conn:
    try:
        conn.execute(
            text("""
                ALTER TABLE students
                ADD COLUMN IF NOT EXISTS last_paid_date DATE;
            """)
        )
    except Exception as alter_err:
        # Si hubiese algún problema (e.g. la tabla ni siquiera existe), lo notificamos
        sys.stderr.write(f"WARNING: No se pudo asegurarse la columna last_paid_date:\n{alter_err}\n")
        # No hacemos sys.exit(1) porque quizá estemos en la primera creación de tablas.
        # La siguiente llamada a create_all() resolverá la creación de tablas nuevas.

# ----------------------------------------------------------------------
# 4) SessionLocal y Base declarativa
# ----------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

