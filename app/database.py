# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1) PostgreSQL URL (Render te proporcionó dos; usamos la externa para acceso desde tu app)
#    Puedes poner aquí directamente tu URL o, preferible, definirla en ENVIRONMENT VARIABLE.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://almapaid_user:7iXZmLPXzDBuDg9u8Lxa5O8xWkELLvg7@dpg-d11bhhumcj7s73a2g1og-a.oregon-postgres.render.com/almapaid"
)

# 2) Crear el engine de SQLAlchemy apuntando a Postgres
engine = create_engine(DATABASE_URL)

# 3) SessionLocal será la fábrica de sesiones para PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4) Base declarativa para los modelos
Base = declarative_base()

