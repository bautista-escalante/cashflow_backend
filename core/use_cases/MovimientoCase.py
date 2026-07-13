from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from itertools import groupby
from datetime import date
from fastapi import HTTPException

import datetime
import requests

from core.models.Movimiento import Movimiento
from api.schemas.MovimientoSchema import MovimientoCreate
from core.validators.MovimientoValidator import MovimientoValidator
from core.models.Plataforma import Plataforma
from api.schemas.MovimientoSchema import MovimientoResponse
from api.schemas.PermutacionSchema import PermutacionResponse


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

        if movimiento.tipo == "gasto":  
            plataforma.saldo -= movimiento.monto
            
        elif movimiento.tipo == "ingreso":
            plataforma.saldo += movimiento.monto
            
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

        movimientos_validados = []
        for m in movimiento_db:
            if(m.tipo != "permutacion"):
                movimientos_validados.append(MovimientoResponse.model_validate(m))
            else:
                movimientos_validados.append(PermutacionResponse.model_validate(m))

        return movimientos_validados

    def obtener_gastos(self, db: Session, anio: int, mes: int, categoria: str, incluir_dolares: bool, id_usuario: int) -> list[MovimientoResponse]:

        if not (1 <= mes <= 12):
            raise HTTPException(status_code=400, detail="mes no válido")
        if anio < 2000:
            raise HTTPException(status_code=400, detail="año no válido")

        movimientos = db.query(Movimiento).filter(
            Movimiento.usuario_id == id_usuario,
            Movimiento.categoria == categoria,
            extract("month", Movimiento.fecha) == mes,
            extract("year", Movimiento.fecha) == anio,
        ).all()
            

        if not movimientos:
            # si noy movimietos solamente devolvemos una lista vacia
            return []
            #raise HTTPException(status_code=404, detail="sin movimientos para ese período")

        return [MovimientoResponse.model_validate(m) for m in movimientos]

    def delete_movimiento(self, db: Session, movimiento_id: int, id_usuario):
        movimiento_db = db.query(Movimiento).filter(
            Movimiento.id == movimiento_id,
            Movimiento.usuario_id == id_usuario
            ).first()

        if not movimiento_db:
            raise HTTPException(status_code=404, detail="no hay movimientos")
        
        db.delete(movimiento_db)
        db.commit()

    
    def obtener_evolucion(self, db: Session, usuario_id, mes, anio, incluir_dolares):
        query = db.query(Movimiento).join(
            Plataforma, Movimiento.plataforma_id == Plataforma.id
        ).filter(
            Movimiento.usuario_id == usuario_id,
            extract("month", Movimiento.fecha) == mes,
            extract("year", Movimiento.fecha) == anio,
        )

        if not incluir_dolares:
            query = query.filter(Plataforma.nombre != "dolares")

        movimientos = query.order_by(Movimiento.fecha).all()

        plataformas = db.query(Plataforma).filter(
            Plataforma.id_usuario == usuario_id
        ).all()

        saldo_plataformas = 0
        for p in plataformas:
            if p.nombre != "dolares":
                saldo_plataformas += p.saldo
            elif incluir_dolares:
                dolares = requests.get("https://dolarapi.com/v1/dolares/blue").json()
                saldo_plataformas += p.saldo * dolares["compra"]

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
                "saldo": saldo_acumulado + saldo_plataformas,
            })

        return evolucion