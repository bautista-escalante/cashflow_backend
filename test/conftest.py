import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from infrastructure.database.db import Base

from core.models.Usuario import Usuario
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento

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