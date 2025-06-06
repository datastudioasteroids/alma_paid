# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# 1) Importar engine, Base y modelos
from .database import engine, Base
from . import models   # para que SQLAlchemy conozca todas las tablas

from sqlalchemy import text

app = FastAPI()

# ----------------------------------------------------------------------
# 2) Evento de arranque: correr migración ANTES de exponer rutas
# ----------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    print(">>> STARTUP: asegurando columna last_paid_date …")
    with engine.connect() as conn:
        try:
            conn.execute(
                text("""
                    ALTER TABLE students
                    ADD COLUMN IF NOT EXISTS last_paid_date DATE;
                """)
            )
            print(">>> last_paid_date: columna confirmada o ya existía.")
        except Exception as alter_err:
            # Si 'students' no existe aún (primer deploy), se ignora el error.
            print(f">>> WARNING: No se pudo agregar last_paid_date: {alter_err}")

    # Crear tablas nuevas que falten (incluye students con su columna)
    Base.metadata.create_all(bind=engine)
    print(">>> create_all(): tablas creadas o ya existentes.")

# ----------------------------------------------------------------------
# 3) Middleware de sesión (mantener tal cual, solo cambia la clave)
# ----------------------------------------------------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key="UNA_CADENA_MUY_LARGA_Y_AZAR_QUE_CAMBIES_POR_PRODUCCIÓN"
)

# ----------------------------------------------------------------------
# 4) Montar estáticos y enrutadores *después* del evento de startup
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



