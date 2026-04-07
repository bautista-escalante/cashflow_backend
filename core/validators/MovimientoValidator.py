from pydantic import model_validator
from typing import Optional
from core.models.Plataforma import Plataforma
from api.schemas.PermutacionSchema import PermutacionCreate
from api.schemas.MovimientoSchema import MovimientoCreate

class MovimientoValidator():
  
    
    @staticmethod
    def validar_permutacion(origen: Plataforma, destino: Plataforma, permutacion):

        if not origen or not destino:
            raise ValueError("Plataforma no encontrada")

        if origen.saldo < permutacion.monto :
            raise ValueError("Saldo insuficiente")

        if origen.id == destino.id:
            raise ValueError("No se puede permutar a la misma plataforma")
        
        if origen.nombre == "dolares" or destino.nombre == "dolares":
            raise ValueError("Para permutar dólares, utiliza la ruta de permutación de dólar")

    @staticmethod
    def validar_permutacion_dolar( origen: Plataforma, destino: Plataforma, permutacion: PermutacionCreate, cambio_dolar: float, movimiento: str):
        if not origen or not destino:
            raise ValueError("Plataforma no encontrada")
        
        if origen.id == destino.id:
            raise ValueError("No se puede permutar a la misma plataforma")
        
        if origen.nombre != "dolares" and destino.nombre != "dolares":
            raise ValueError("en esta ruta solo se pueden permutar dólares")
        
        if movimiento == "compra" and origen.saldo < permutacion.monto * cambio_dolar:
            raise ValueError("Saldo insuficiente")

        if movimiento == "venta" and origen.saldo < permutacion.monto:
            raise ValueError("Saldo insuficiente") 
        
    def validar_movimiento(movimiento: MovimientoCreate, plataforma: Plataforma):
        if movimiento.tipo not in ["ingreso", "gasto", "permutacion"]:
            raise ValueError("Tipo de movimiento inválido")
        
        if movimiento.tipo == "gasto" and (not movimiento.descripcion or not movimiento.categoria):
            raise ValueError("Los gastos deben tener descripción y categoría")
        
        if movimiento.plataforma_id is None:
            raise ValueError("El movimiento debe tener una plataforma asociada")
        
        if movimiento.tipo == "gasto" and plataforma.saldo < movimiento.monto:
            raise ValueError("Saldo insuficiente")
        
        if movimiento.monto <= 0:
            raise ValueError("El monto no puede ser negativo o cero")