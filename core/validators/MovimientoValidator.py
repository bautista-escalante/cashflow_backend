from pydantic import model_validator
from typing import Optional
from api.schemas.MovimientoSchema import MovimientoBase
from core.models.Plataforma import Plataforma
from api.schemas.PermutacionSchema import PermutacionCreate

class MovimientoValidator(MovimientoBase):
    plataforma_id: Optional[int] = None
    plataforma_origen_id: Optional[int] = None
    plataforma_destino_id: Optional[int] = None
    
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
        
        print(movimiento)
        if movimiento == "compra" and origen.saldo < permutacion.monto * cambio_dolar:
            raise ValueError("Saldo insuficiente")

        if movimiento == "venta" and origen.saldo < permutacion.monto:
            raise ValueError("Saldo insuficiente") 