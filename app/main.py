# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine
from .routes import landing, admin
from .auth import router as auth_router  # tu módulo de autenticación

# 1) Crear (si no existen) todas las tablas definidas en Base.metadata sobre Postgres
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2) Middleware de sesiones (necesario para ensure_admin)
app.add_middleware(
    SessionMiddleware,
    secret_key="TU_CLAVE_SECRETA_ALEATORIA"  # reemplázala por algo secreto
)

# 3) Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 4) Incluir routers
app.include_router(landing.router)   # rutas públicas: "/", "/create_preference", "/payment/..."
app.include_router(auth_router)      # rutas de login/logout
app.include_router(admin.router)     # rutas administrativas bajo "/admin"

# 5) (Opcional) ruta raíz
@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}

