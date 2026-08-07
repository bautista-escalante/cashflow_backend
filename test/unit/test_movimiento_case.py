from core.use_cases.MovimientoCase import movimientoCase
from infrastructure.database.db import get_db
from core.models.Plataforma import Plataforma
from api.schemas.MovimientoSchema import MovimientoCreate
import datetime

movimiento_case = movimientoCase()

class TestAgregarMovimiento:
    def test_agregar_movimiento_gasto(self, db, usuario_prueba, plataforma_prueba):
        
        movimiento = MovimientoCreate(
            tipo="gasto",
            monto=100.0,
            plataforma_id=plataforma_prueba.id,
            descripcion="gasto de prueba",
            categoria="Alimentos"
        )

        saldo_inicial = db.query(Plataforma).filter(Plataforma.id == plataforma_prueba.id).first().saldo

        movimiento_case.agregar_movimiento(db, movimiento, id_usuario=usuario_prueba.id)

        saldo_final = db.query(Plataforma).filter(Plataforma.id == plataforma_prueba.id).first().saldo

        assert saldo_final == (saldo_inicial - 100.0)


    def test_agregar_movimiento_ingreso(self, db, usuario_prueba, plataforma_prueba):
        movimiento = MovimientoCreate(
            tipo="ingreso",
            monto=100.0,
            plataforma_id=plataforma_prueba.id,
            descripcion="ingreso de prueba",
        )

        saldo_inicial = db.query(Plataforma).filter(Plataforma.id == plataforma_prueba.id).first().saldo

        movimiento_case.agregar_movimiento(db,  movimiento, id_usuario=usuario_prueba.id)

        saldo_final = db.query(Plataforma).filter(Plataforma.id == plataforma_prueba.id).first().saldo

        assert saldo_final == (saldo_inicial + 100.0)


class TestObtenerMovimientos:
    def test_obtener_movimientos(self, db, usuario_prueba, plataforma_prueba):
        
        movimiento = MovimientoCreate(
            tipo="gasto",
            monto=50.0,
            plataforma_id=plataforma_prueba.id,
            descripcion="gasto de prueba",
            categoria="Transporte"
        )
        movimiento_case.agregar_movimiento(db, movimiento, id_usuario=usuario_prueba.id)

        movimientos = movimiento_case.obtener_movimientos(db, "gasto", id_usuario=usuario_prueba.id)

        assert len(movimientos) > 0

class TestObtenerGastos:
    def test_obtener_gastos(self, db, usuario_prueba, plataforma_prueba):
        
        gasto = MovimientoCreate(
            tipo="gasto",
            monto=50.0,
            plataforma_id=plataforma_prueba.id,
            descripcion="gasto de prueba",
            categoria="Entretenimiento"
        )
        movimiento_case.agregar_movimiento(db, gasto, id_usuario=usuario_prueba.id)

        ingreso = MovimientoCreate(
            tipo="ingreso",
            monto=200.0,
            plataforma_id=plataforma_prueba.id,
            descripcion="ingreso de prueba",
            categoria="Salario"
        )
        movimiento_case.agregar_movimiento(db, ingreso, id_usuario=usuario_prueba.id)

        gastos = movimiento_case.obtener_gastos(db, datetime.date.today().year, datetime.date.today().month, 
                                                "Transporte", id_usuario=usuario_prueba.id)

        assert all(gasto.tipo == "gasto" for gasto in gastos)