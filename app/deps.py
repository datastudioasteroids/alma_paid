# app/deps.py
from fastapi import Request
from fastapi.responses import RedirectResponse
from .database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    """
    Crea una sesión de DB, la yield para que la use FastAPI y la cierre al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_admin(request: Request):
    """
    Comprueba si existe request.session['admin'].
    Si no existe, redirige a /login.
    Si existe, devuelve el valor (normalmente el email del admin).
    """
    admin_user = request.session.get("admin")
    if not admin_user:
        return RedirectResponse(url="/login", status_code=302)
    return admin_user
