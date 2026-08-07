import random
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from infrastructure.database.db import Base

from core.models.Usuario import Usuario
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento

from api.schemas.UsuarioSchema import UsuarioCreate

from core.use_cases.UsuarioCase import UsuarioCase

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def usuario_prueba(db):
    num = random.randint(1, 1000)
    usuario_case = UsuarioCase()
    usuario_prueba = UsuarioCreate(
        nombre=f"Usuario fixture {num}",
        email=f"usuario.{num}@example.com",
        clave="clave_de_prueba"
    )
    usuario_prueba = usuario_case.crear_usuario(usuario_prueba, db)

    return usuario_prueba
