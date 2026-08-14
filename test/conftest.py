import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from infrastructure.database.db import Base, get_db

from core.models.Usuario import Usuario
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento

from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioResponse
from api.schemas.PlataformaSchema import PlataformaCreate

from core.use_cases.UsuarioCase import UsuarioCase
from core.use_cases.PlataformaCase import PlataformaCase


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
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
    uuid = uuid4().hex
    usuario_case = UsuarioCase()
    usuario_prueba = UsuarioCreate(
        nombre=f"Usuario fixture {uuid}",
        email=f"usuario.{uuid}@example.com",
        clave="clave_de_prueba"
    )
    usuario_prueba = usuario_case.crear_usuario(usuario_prueba, db)

    return usuario_prueba


@pytest.fixture
def plataforma_prueba(db, usuario_prueba: UsuarioResponse):

    plataforma_case = PlataformaCase()
    plataforma_prueba = PlataformaCreate(
        nombre="efectivo",
        saldo=100.0
    )
    plataforma_prueba = plataforma_case.crear_plataforma(db, plataforma_prueba, usuario_prueba.id)

    return plataforma_prueba

@pytest.fixture
def client(db):
    
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()