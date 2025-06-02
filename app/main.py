# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine
from .routes import landing, admin
from .auth import router as auth_router  # Importamos las rutas de autenticación

# 1) Crear tablas si no existen (incluyendo la nueva tabla "payments")
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2) Middleware de sesión (necesario para usar request.session en ensure_admin)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"  # Reemplazá por un string aleatorio y secreto
)

# 3) Montar carpeta de archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 4) Incluir routers
app.include_router(landing.router)   # Rutas públicas: "/", "/create_preference", "/payment/..."
app.include_router(auth_router)      # Rutas de login/logout
app.include_router(admin.router)     # Rutas administrativas protegidas bajo "/admin"

# 5) (Opcional) Ruta raíz que redirige o muestra un mensaje
@app.get("/", include_in_schema=False)
async def root_redirect():
    # Puesto que landing.router ya define GET "/", esto es opcional.
    # Podrías redirigir directamente a "/": return RedirectResponse(url="/")
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}
