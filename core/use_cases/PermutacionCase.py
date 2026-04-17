from sqlalchemy.orm import Session
from datetime import date
import requests

from core.models.Plataforma import Plataforma
from api.schemas.PermutacionSchema import PermutacionCreate
from core.validators.MovimientoValidator import MovimientoValidator
from api.schemas.PermutacionSchema import PermutacionResponse
from core.models.Movimiento import Movimiento


class PermutacionCase:

    def generar_permutaciones(self, db:Session, permutacion: PermutacionCreate, id_usuario):

        origen = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_origen_id,
            Plataforma.id_usuario == id_usuario
        ).first()

        destino = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_destino_id
        ).first()

        MovimientoValidator.validar_permutacion(origen, destino, permutacion)
   
        origen.saldo -= permutacion.monto
        destino.saldo += permutacion.monto

        movimiento_db = Movimiento(
            tipo=permutacion.tipo,
            monto=permutacion.monto,
            fecha=date.today(),
            descripcion=f"cambio de {origen.nombre} a {destino.nombre}",
            plataforma_origen_id=origen.id,
            plataforma_destino_id=destino.id,
            usuario_id = id_usuario
        )
        print(movimiento_db.__dict__)
        db.add(movimiento_db)
        db.commit()
        db.refresh(movimiento_db)

        return PermutacionResponse.model_validate(movimiento_db)
        
    def permutar_dolar(self, db:Session, permutacion: PermutacionCreate, id_usuario):
        origen = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_origen_id,
            Plataforma.id_usuario == id_usuario
        ).first()

        destino = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_destino_id,
            Plataforma.id_usuario == id_usuario
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
    

        movimiento_obj = Movimiento(
            tipo=permutacion.tipo,
            monto=permutacion.monto,
            fecha= date.today(),
            descripcion=f"{movimiento} de {origen.nombre} a {destino.nombre} a razon de {dolares['venta'] if movimiento == 'compra' else dolares['compra']} cada dólar",
            plataforma_origen_id=origen.id,
            plataforma_destino_id=destino.id,
            usuario_id = id_usuario
        )
        print(movimiento_obj)

        db.add(movimiento_obj)

        db.commit()

        return PermutacionResponse(
            id=0,
            tipo=permutacion.tipo,
            monto=permutacion.monto,
            fecha=date.today(),
            plataforma_origen_id=permutacion.plataforma_origen_id,
            plataforma_destino_id=permutacion.plataforma_destino_id,
            valor_cambio=dolares["venta"] if movimiento == "compra" else dolares["compra"],
            usuario_id = id_usuario
        )