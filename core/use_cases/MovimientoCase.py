from sqlalchemy.orm import Session
from itertools import groupby
from datetime import date
from fastapi import HTTPException

from core.models.Movimiento import Movimiento
from api.schemas.MovimientoSchema import MovimientoCreate
from core.validators.MovimientoValidator import MovimientoValidator
from core.models.Plataforma import Plataforma
from api.schemas.MovimientoSchema import MovimientoResponse


class movimientoCase:

    def agregar_movimiento(self, db: Session, movimiento: MovimientoCreate, id_usuario):
        
        plataforma = db.query(Plataforma).filter(
            Plataforma.id == movimiento.plataforma_id, 
            Plataforma.id_usuario == id_usuario
            ).first()

        MovimientoValidator.validar_movimiento(movimiento, plataforma)

        nuevo_movimiento = Movimiento(
            tipo=movimiento.tipo,
            monto=movimiento.monto,
            fecha=date.today(),
            descripcion=movimiento.descripcion,
            categoria=movimiento.categoria,
            plataforma_id=movimiento.plataforma_id,
            usuario_id = id_usuario
        )

        db.add(nuevo_movimiento)
        db.commit()
        db.refresh(nuevo_movimiento)

        return MovimientoResponse.model_validate(nuevo_movimiento)

    def obtener_movimientos(self, db: Session, tipo: str, id_usuario):

        if not tipo in ["gasto", "permutacion", "ingreso", "todos"]:
            raise HTTPException(status_code=400, detail="tipo de movimiento erroneo")

        if tipo == "todos":
            movimiento_db = db.query(Movimiento).filter(
                Movimiento.usuario_id == id_usuario
                ).all()

        else:
            movimiento_db = db.query(Movimiento).filter(
                Movimiento.tipo == tipo, 
                Movimiento.usuario_id == id_usuario
                ).all()

        if not movimiento_db:
            raise HTTPException(status_code=404, detail="no hay movimientos")

        return [MovimientoResponse.model_validate(m) for m in movimiento_db]

    def delete_movimiento(self, db: Session, movimiento_id: int, id_usuario):
        movimiento_db = db.query(Movimiento).filter(
            Movimiento.id == movimiento_id,
            Movimiento.usuario_id == id_usuario
            ).first()

        if not movimiento_db:
            raise HTTPException(status_code=404, detail="no hay movimientos")
        
        db.delete(movimiento_db)
        db.commit()

    def obtener_evolucion(self, db: Session, usuario_id):
        movimientos = db.query(Movimiento).filter(
            Movimiento.usuario_id == usuario_id).order_by(
            Movimiento.fecha
            ).all()
    
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