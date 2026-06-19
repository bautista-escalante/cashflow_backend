from pydantic import BaseModel
from typing import Optional
from datetime import date


class PermutacionCreate(BaseModel):

    tipo: str = "permutacion"
    monto: float
    plataforma_origen_id: int
    plataforma_destino_id: int

class PermutacionResponse(BaseModel):
    id: int
    tipo: str
    monto: float
    descripcion: str
    fecha: date
    plataforma_origen_id: int
    plataforma_destino_id: int
    valor_cambio: Optional[float] = None

    class Config:
        from_attributes = True