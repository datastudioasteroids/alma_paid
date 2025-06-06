# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# Importamos engine y Base desde database.py
from .database import engine, Base

# Importamos los modelos para que SQLAlchemy conozca todas las tablas
from . import models

# Para ejecutar SQL crudo
from sqlalchemy import text

app = FastAPI()

# ----------------------------------------------------------------------
# 1) Evento de arranque: aseguramos que last_paid_date exista en 'students'
# ----------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    # a) Agregar columna si falta
    with engine.connect() as conn:
        try:
            conn.execute(
                text("""
                    ALTER TABLE students
                    ADD COLUMN IF NOT EXISTS last_paid_date DATE;
                """)
            )
        except Exception as alter_err:
            # Si la tabla 'students' no existe aún, lo ignoramos.
            print(f"WARNING: No se pudo agregar last_paid_date (posiblemente 'students' no existe): {alter_err}")

    # b) Crear tablas que falten (incluyendo 'students' completo en un primer deploy)
    Base.metadata.create_all(bind=engine)


# ----------------- Configuración de la app -----------------

# Middleware de sesión (necesario para ensure_admin)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"
)

# Montar carpeta de archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir routers (después de la migración)
from .routes import landing, admin
from .auth import router as auth_router

app.include_router(landing.router)   # Rutas públicas
app.include_router(auth_router)      # Login/logout
app.include_router(admin.router)     # Rutas admin (/admin)

# Ruta raíz opcional
@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}



