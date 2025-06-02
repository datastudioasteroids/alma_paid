# app/deps.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base
from fastapi import Request
from fastapi.responses import RedirectResponse

# Ruta a tu archivo SQLite (puede ser relativa o absoluta)
DATABASE_URL = "sqlite:///./alma_paid.db"

# Crear el engine y el SessionLocal
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Abre una sesión de DB, la cede (yield) para que FastAPI la injete
    en dependencias, y la cierra al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_admin(request: Request):
    """
    Comprueba si existe `request.session['admin']`.
    - Si no existe, redirige a /login.
    - Si existe, devuelve el valor (normalmente el email del admin).
    """
    admin_user = request.session.get("admin")
    if not admin_user:
        return RedirectResponse(url="/login", status_code=302)
    return admin_user

