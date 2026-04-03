from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MovimientoBase(BaseModel):
    
    tipo: str  # ingreso | gasto | permutacion
    monto: float
    fecha: datetime
    descripcion: Optional[str] = None
    categoria: Optional[str] = None

class MovimientoCreate(MovimientoBase):
    plataforma_id: Optional[int] = None
    plataforma_origen_id: Optional[int] = None
    plataforma_destino_id: Optional[int] = None
    
class MovimientoResponse(MovimientoBase):
    id: int

    class Config:
        from_attributes = True