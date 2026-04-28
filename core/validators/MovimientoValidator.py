from pydantic import model_validator
from typing import Optional
from core.models.Plataforma import Plataforma
from api.schemas.PermutacionSchema import PermutacionCreate
from api.schemas.MovimientoSchema import MovimientoCreate
from fastapi import HTTPException

class MovimientoValidator():
  
    @staticmethod
    def validar_permutacion(origen: Plataforma, destino: Plataforma, permutacion):

        if not origen or not destino:
            raise HTTPException(status_code=404, detail="Plataforma no encontrada")

        if origen.saldo < permutacion.monto :
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

        if origen.id == destino.id:
            raise HTTPException(status_code=400, detail="No se puede permutar a la misma plataforma")
        
        if origen.nombre == "dolares" or destino.nombre == "dolares":
            raise HTTPException(status_code=400, detail="Para permutar dólares, utiliza la ruta de permutación de dólar")

    @staticmethod
    def validar_permutacion_dolar( origen: Plataforma, destino: Plataforma, permutacion: PermutacionCreate, cambio_dolar: float, movimiento: str):
        if not origen or not destino:
            raise HTTPException(status_code=404, detail="Plataforma no encontrada")
        
        if origen.id == destino.id:
            raise HTTPException(status_code=400, detail="No se puede permutar a la misma plataforma")
        
        if origen.nombre != "dolares" and destino.nombre != "dólares":
            raise HTTPException(status_code=400, detail="en esta ruta solo se pueden permutar dólares")
        
        if movimiento == "compra" and origen.saldo < permutacion.monto * cambio_dolar:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

        if movimiento == "venta" and origen.saldo < permutacion.monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente") 

    def validar_movimiento(movimiento: MovimientoCreate, plataforma: Plataforma):
        if movimiento.tipo not in ["ingreso", "gasto"]:
            raise HTTPException(status_code=400, detail="Tipo de movimiento inválido")
        
        if movimiento.tipo == "gasto" and (not movimiento.descripcion or not movimiento.categoria):
            raise HTTPException(status_code=400, detail="Los gastos deben tener descripción y categoría")
        
        if movimiento.plataforma_id is None:
            raise HTTPException(status_code=400, detail="El movimiento debe tener una plataforma asociada")
        
        if not plataforma:
            raise HTTPException(status_code=404, detail="plataforma no encontrada")
        
        if movimiento.tipo == "gasto" and plataforma.saldo < movimiento.monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        
        if movimiento.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto no puede ser negativo o cero")