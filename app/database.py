from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ruta a tu base de datos SQLite (puedes cambiarla si usas otro RDBMS)
SQLALCHEMY_DATABASE_URL = "sqlite:///./alma_paid.db"

# El parámetro connect_args={"check_same_thread": False} es necesario para SQLite en aplicaciones multihilo
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal será la “fábrica” de sesiones que usarán todos los routers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para declarar modelos
Base = declarative_base()

