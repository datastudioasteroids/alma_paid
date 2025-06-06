# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine
from . import models          # para que Base.metadata conozca todos los modelos
from .routes import landing, admin
from .auth import router as auth_router

# 1) Crea tablas que falten (solo crea las que no existan; no borra nada)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2) Middleware de sesiones (solo para `/admin`)
app.add_middleware(
    SessionMiddleware,
    secret_key="CAMBIÁ_ESTA_CLAVE_POR_ALGO_AZAR"
)

# 3) Montar estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 4) Incluir routers
app.include_router(landing.router)
app.include_router(auth_router)
app.include_router(admin.router)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Visita / para ir a la página principal de AlmaPaid."}


