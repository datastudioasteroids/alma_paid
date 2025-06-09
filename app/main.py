# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine
from . import models  # Asegura que los modelos se registren en Base
from .routes import landing, admin
from .auth import router as auth_router

# Crear tablas automáticamente al iniciar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware de sesiones (necesario para autenticación en /admin)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"  # 🔐 ¡Cámbialo en producción!
)

# Archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registrar endpoints
app.include_router(landing.router)
app.include_router(auth_router)
app.include_router(admin.router)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}



