# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine
from . import models          # Importamos modelos para que SQLAlchemy conozca todas las tablas
from .routes import landing, admin
from .auth import router as auth_router

# 1) Antes de crear todas las tablas, chequeamos/creamos la columna 'last_paid_date' en students
def ensure_last_paid_column_exists():
    """
    Se conecta directamente con engine y checa en information_schema si la columna students.last_paid_date existe.
    Si no existe, la agrega con ALTER TABLE.
    """
    # Conexión "raw" a la base de datos
    with engine.connect() as conn:
        # Buscamos en information_schema.columns
        resultado = conn.execute(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'students' AND column_name = 'last_paid_date';
            """
        )
        if resultado.fetchone() is None:
            # Si no encontramos el registro, agregamos la columna
            conn.execute(
                "ALTER TABLE students ADD COLUMN last_paid_date DATE;"
            )


# 2) Ejecutamos la función de "migración ligera" ANTES de create_all
ensure_last_paid_column_exists()

# 3) Luego, creamos las tablas (sólo las que falten)
Base.metadata.create_all(bind=engine)

# 4) Inicializamos FastAPI
app = FastAPI()

# 5) Middleware de sesión (necesario para ensure_admin)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"
)

# 6) Montamos recursos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 7) Incluir routers
app.include_router(landing.router)   # Rutas públicas: "/", "/create_preference", "/payment/..."
app.include_router(auth_router)      # Rutas de login/logout
app.include_router(admin.router)     # Rutas administrativas protegidas bajo "/admin"

# 8) (Opcional) Ruta raíz para redirigir o mostrar un mensaje
@app.get("/", include_in_schema=False)
async def root_redirect():
    # landing.router ya define GET "/", así que esto es opcional.
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}


