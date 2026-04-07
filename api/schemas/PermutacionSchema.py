from pydantic import BaseModel
from typing import Optional
from datetime import date


class PermutacionCreate(BaseModel):

    tipo: str = "permutacion"
    monto: float
    fecha: date
    plataforma_origen_id: int
    plataforma_destino_id: int

class PermutacionResponse(PermutacionCreate):
    id: int
    valor_cambio: Optional[float] = None

    class Config:
        from_attributes = True