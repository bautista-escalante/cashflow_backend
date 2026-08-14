
from core.models.Usuario import Usuario
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento


def test_database_connection(db):
    assert db is not None


def test_database_tables(db):
    assert db.query(Usuario).all() is not None
    assert db.query(Plataforma).all() is not None
    assert db.query(Movimiento).all() is not None