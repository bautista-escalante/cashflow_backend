from pydantic import model_validator
from typing import Optional
from api.schemas.MovimientoSchema import MovimientoBase

class MovimientoValidator(MovimientoBase):
    plataforma_id: Optional[int] = None
    plataforma_origen_id: Optional[int] = None
    plataforma_destino_id: Optional[int] = None

    @model_validator(mode="after")
    def validar_movimiento(self):
        if self.tipo in ["ingreso", "gasto"]:
            if not self.plataforma_id:
                raise ValueError("plataforma_id es obligatorio")

        if self.tipo == "permutacion":
            if not self.plataforma_origen_id or not self.plataforma_destino_id:
                raise ValueError("origen y destino son obligatorios")

        return self
    
    @staticmethod
    def validar_permutacion(self, origen, destino, permutacion):
        if self.tipo == "permutacion":
            if not self.plataforma_origen_id or not self.plataforma_destino_id:
                raise ValueError("origen y destino son obligatorios")
        
        if not origen or not destino:
            raise ValueError("Plataforma no encontrada")

        if origen.saldo < permutacion.monto:
            raise ValueError("Saldo insuficiente")
        
        if origen.id == destino.id:
            raise ValueError("No se puede permutar a la misma plataforma")