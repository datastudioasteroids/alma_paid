# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy import text
from .database import Base, engine
from . import models          # Para que SQLAlchemy registre todos los modelos
from .routes import landing, admin
from .auth import router as auth_router

def ensure_last_paid_column_exists():
    """
    Chequea en information_schema si existe students.last_paid_date.
    Si no existe, ejecuta ALTER TABLE para crearla.
    """
    with engine.connect() as conn:
        # 1) Verificar si la columna ya existe:
        resultado = conn.execute(
            text(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'students' AND column_name = 'last_paid_date';
                """
            )
        )
        if resultado.fetchone() is None:
            # 2) Si no existe, la agregamos:
            conn.execute(
                text("ALTER TABLE students ADD COLUMN last_paid_date DATE;")
            )

# 1) Primero, nos aseguramos de que la columna exista en la BD:
ensure_last_paid_column_exists()

# 2) Luego creamos las tablas que falten (sin alterar las ya existentes):
Base.metadata.create_all(bind=engine)

# 3) Inicializamos la aplicación FastAPI
app = FastAPI()

# 4) Middleware de sesión (para proteger rutas admin, etc.)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"
)

# 5) Montar directorio estático
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 6) Incluir routers
app.include_router(landing.router)   # Rutas públicas ("/", "/create_preference", etc.)
app.include_router(auth_router)      # Ruta de login/logout
app.include_router(admin.router)     # Rutas administrativas bajo "/admin"

# 7) (Opcional) Ruta raíz para redirigir o mensaje
@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}

