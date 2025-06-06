# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# Importamos engine y Base desde database.py
from .database import engine, Base

# Importar modelos aquí, para que SQLAlchemy conozca todas las tablas
from . import models

# Para enviar consultas SQL crudas
from sqlalchemy import text

# ----------------------------------------------------------------------
# 1) Asegurarnos de que la columna 'last_paid_date' exista en la tabla 'students'
# ----------------------------------------------------------------------
# Ejecutamos ALTER TABLE ... ADD COLUMN IF NOT EXISTS
# Si la tabla 'students' aún no existe, este bloque fallará y lo capturamos.
with engine.connect() as conn:
    try:
        conn.execute(
            text("""
                ALTER TABLE students
                ADD COLUMN IF NOT EXISTS last_paid_date DATE;
            """)
        )
    except Exception as alter_err:
        # Si falla (por ejemplo, porque 'students' no existe), lo ignoramos.
        # Luego create_all() creará la tabla completa con last_paid_date.
        print(f"WARNING: No se pudo agregar last_paid_date (tal vez 'students' no existe aún): {alter_err}")

# ----------------------------------------------------------------------
# 2) Crear todas las tablas que falten (students, courses, enrollments, payments, etc.)
# ----------------------------------------------------------------------
# Esto crea la tabla 'students' con 'last_paid_date' integrada si no existía
Base.metadata.create_all(bind=engine)


# ----------------- Definición de la app FastAPI -----------------

app = FastAPI()

# Middleware de sesión (para ensure_admin en rutas admin)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"
)

# Montar carpeta de archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir routers
from .routes import landing, admin
from .auth import router as auth_router

app.include_router(landing.router)   # Rutas públicas ("/", "/create_preference", "/payment/...")
app.include_router(auth_router)      # Rutas de login/logout
app.include_router(admin.router)     # Rutas administrativas bajo "/admin"

# Ruta raíz opcional
@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}


