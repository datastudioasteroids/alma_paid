# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# 1) Importamos engine y Base desde database.py
from .database import engine, Base

# 2) Importamos modelos para que Base conozca las tablas (incluyendo Student con last_paid_date)
from . import models

from sqlalchemy import text

app = FastAPI()

# ----------------------------------------------------------------------
# Evento de arranque:
#   - Agrega la columna last_paid_date si faltara
#   - Crea tablas que aún no existan
# ----------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    print(">>> STARTUP: corrigiendo esquema de 'students' …")
    with engine.connect() as conn:
        try:
            conn.execute(
                text("""
                    ALTER TABLE students
                    ADD COLUMN IF NOT EXISTS last_paid_date DATE;
                """)
            )
            print(">>> last_paid_date: columna asegurada o ya existía.")
        except Exception as alter_err:
            # Si la tabla 'students' no existe, ignoramos (create_all() la creará completa).
            print(f">>> WARNING: No se pudo agregar last_paid_date: {alter_err}")

    # Crear tablas nuevas que falten (incluye 'students' con last_paid_date si no existía)
    Base.metadata.create_all(bind=engine)
    print(">>> create_all(): tablas creadas o ya existentes.")

# ----------------------------------------------------------------------
# Middleware de sesión (mantén tu clave secreta aquí)
# ----------------------------------------------------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key="UNA_CADENA_MUY_LARGA_Y_SECRETA_PARA_PRODUCCION"
)

# ----------------------------------------------------------------------
# Montar estáticos y agregar routers (después del evento de startup)
# ----------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")

from .routes import landing, admin
from .auth import router as auth_router

app.include_router(landing.router)
app.include_router(auth_router)
app.include_router(admin.router)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}


