from fastapi import Request
from fastapi.responses import RedirectResponse
from .database import SessionLocal

def get_db():
    """
    Abre una sesión de BD, la cede (yield) para que FastAPI la injete
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
    - Si existe, devuelve ese valor (por ejemplo, el email o ID del admin).
    """
    admin_user = request.session.get("admin")
    if not admin_user:
        return RedirectResponse(url="/login", status_code=302)
    return admin_user

