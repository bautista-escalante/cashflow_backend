from sqlalchemy.orm import Session
from itertools import groupby
from datetime import date

from core.models.Movimiento import Movimiento
from api.schemas.MovimientoSchema import MovimientoCreate
from core.validators.MovimientoValidator import MovimientoValidator
from core.models.Plataforma import Plataforma


class movimientoCase:

    def agregar_movimiento(self, db: Session, movimiento: MovimientoCreate):
        
        plataforma = db.query(Plataforma).filter(Plataforma.id == movimiento.plataforma_id).first()
        MovimientoValidator.validar_movimiento(movimiento, plataforma)

        nuevo_movimiento = Movimiento(
            tipo=movimiento.tipo,
            monto=movimiento.monto,
            fecha=date.today(),
            descripcion=movimiento.descripcion,
            categoria=movimiento.categoria,
            plataforma_id=movimiento.plataforma_id
        )

        db.add(nuevo_movimiento)
        db.commit()
        db.refresh(nuevo_movimiento)

        return nuevo_movimiento

    def obtener_movimientos(self, db: Session, tipo: str):
        if tipo == "todos":
            return db.query(Movimiento).all()
        else:
            return db.query(Movimiento).filter(Movimiento.tipo == tipo).all()

    def get_movimiento_by_id(self, db: Session, movimiento_id: int):
        return db.query(Movimiento).filter(Movimiento.id == movimiento_id).first()

    def delete_movimiento(self, db: Session, movimiento_id: int):
        movimiento = self.get_movimiento_by_id(db, movimiento_id)
        if movimiento:
            db.delete(movimiento)
            db.commit()

    def obtener_evolucion(self, db: Session):
        movimientos = db.query(Movimiento).order_by(Movimiento.fecha).all()
        evolucion = []
        saldo_acumulado = 0

        for fecha, grupo in groupby(movimientos, key=lambda m: m.fecha):
            for movimiento in grupo:
                if movimiento.tipo == "ingreso":
                    saldo_acumulado += movimiento.monto
                elif movimiento.tipo == "gasto":
                    saldo_acumulado -= movimiento.monto

            evolucion.append({
                "fecha": fecha,
                "saldo": saldo_acumulado
            })

        return evolucion