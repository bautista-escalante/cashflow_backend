from core.use_cases.MovimientoCase import movimientoCase
from infrastructure.database.db import get_db
from core.models.Plataforma import Plataforma
from api.schemas.MovimientoSchema import MovimientoCreate

movimiento_case = movimientoCase()

class TestAgregarMovimiento:
    def test_agregar_movimiento_gasto(self):
        db=get_db()

        movimiento = MovimientoCreate(
            tipo="gasto",
            monto=100.0,
            plataforma_id=1,
            descripcion="gasto de prueba",
            categoria="Alimentos"
        )

        saldo_inicial = db.query(Plataforma).filter(Plataforma.id == 1).first().saldo

        movimiento_case.agregar_movimiento(db, movimiento, id_usuario=1)

        saldo_final = db.query(Plataforma).filter(Plataforma.id == 1).first().saldo

        assert saldo_final == (saldo_inicial - 100.0)

    def test_agregar_movimiento_ingreso(self):
        db=get_db()

        saldo_inicial = db.query(Plataforma).filter(Plataforma.id == 1).first().saldo

        movimiento_case.agregar_movimiento(
            db, 
            movimiento={
            "tipo": "ingreso",
            "monto": 100.0,
            "plataforma_id": 1,
            "descripcion": "ingreso de prueba",
            "categoria": "Alimentos"}, 
            id_usuario=1)

        saldo_final = db.query(Plataforma).filter(Plataforma.id == 1).first().saldo

        assert saldo_final == (saldo_inicial + 100.0)


class TestObtenerMovimientos:
    ...

class TestObtenerGastos:
    ...

class TestDeleteMovimiento:
    ...

class TestObtenerEvolucion:
    ...