# app/database.py

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) Leemos DATABASE_URL **solo** desde Variable de Entorno.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    sys.stderr.write("ERROR: DATABASE_URL no está definida. Debes configurarla en Render (Settings → Environment).\n")
    sys.exit(1)

# 2) Creamos el engine. Si es inválida, sale un error legible.
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    sys.stderr.write(f"ERROR: No se pudo crear el engine con DATABASE_URL:\n  {DATABASE_URL}\n  Detalle: {e}\n")
    sys.exit(1)

# 3) SessionLocal y Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

