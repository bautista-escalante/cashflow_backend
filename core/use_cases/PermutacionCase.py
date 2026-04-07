from sqlalchemy.orm import Session
from datetime import date
import requests

from core.models.Plataforma import Plataforma
from api.schemas.PermutacionSchema import PermutacionCreate
from core.validators.MovimientoValidator import MovimientoValidator
from api.schemas.PermutacionSchema import PermutacionResponse
from core.models.Movimiento import Movimiento


class PermutacionCase:

    def generar_permutaciones(self, db:Session, permutacion: PermutacionCreate):

        origen = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_origen_id
        ).first()

        destino = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_destino_id
        ).first()

        MovimientoValidator.validar_permutacion(origen, destino, permutacion)
   
        origen.saldo -= permutacion.monto
        destino.saldo += permutacion.monto

        db.add(Movimiento(
            tipo=permutacion.tipo,
            monto=permutacion.monto,
            fecha=date.today(),
            descripcion=f"cambio de {origen.nombre} a {destino.nombre}",
            plataforma_origen_id=origen.id,
            plataforma_destino_id=destino.id
        ))

        db.commit()

        return permutacion
        
    def permutar_dolar(self, db:Session, permutacion: PermutacionCreate):
        origen = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_origen_id
        ).first()

        destino = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_destino_id
        ).first()
        
        movimiento = "compra" if destino.nombre == "dolares" else "venta"
        dolares = requests.get("https://dolarapi.com/v1/dolares/blue").json()
 
        if movimiento == "compra":
            MovimientoValidator.validar_permutacion_dolar(origen, destino, permutacion, dolares["venta"], movimiento)

            origen.saldo -= permutacion.monto * dolares["venta"]
            destino.saldo += permutacion.monto 

        elif movimiento == "venta":
            MovimientoValidator.validar_permutacion_dolar(origen, destino, permutacion, dolares["compra"], movimiento)

            origen.saldo -= permutacion.monto 
            destino.saldo += permutacion.monto * dolares["compra"]

        db.add(Movimiento(
            tipo=permutacion.tipo,
            monto=permutacion.monto,
            fecha= date.today(),
            descripcion=f"{movimiento} de {origen.nombre} a {destino.nombre} a razon de {dolares['venta'] if movimiento == 'compra' else dolares['compra']} cada dólar",
            plataforma_origen_id=origen.id,
            plataforma_destino_id=destino.id
        ))

        db.commit()

        return PermutacionResponse(
            id=0,
            tipo=permutacion.tipo,
            monto=permutacion.monto,
            fecha=permutacion.fecha,
            plataforma_origen_id=permutacion.plataforma_origen_id,
            plataforma_destino_id=permutacion.plataforma_destino_id,
            valor_cambio=dolares["venta"] if movimiento == "compra" else dolares["compra"]
        )