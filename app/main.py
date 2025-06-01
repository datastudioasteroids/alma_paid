# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .routes import landing, admin
from .auth import router as auth_router  # Importamos el router de auth

app = FastAPI()

# 1) Middleware de sesión (necesario para request.session)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"  # Usa una clave aleatoria y secreta
)

# 2) Archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 3) Routers
app.include_router(landing.router)   # Rutas públicas: / y /search y /pay
app.include_router(auth_router)      # Rutas de autenticación: /login y /logout
app.include_router(admin.router)     # Panel protegido: /admin/...

# (Opcional) Ruta raíz
@app.get("/")
async def root_redirect():
    """
    Si alguien entra a "/", lo redirigimos a la landing.
    De hecho, landing.router define GET "/" también, así que no es estrictamente necesario.
    """
    return {"message": "Visita / para ir a la página principal."}
