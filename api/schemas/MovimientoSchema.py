from pydantic import BaseModel
from typing import Optional
from datetime import date


class MovimientoCreate(BaseModel):
    
    tipo: str  # ingreso | gasto | permutacion
    monto: float
    plataforma_id: int = None
    descripcion: Optional[str] = None
    fecha: Optional[date] = None
    categoria: Optional[str] = None
    usuario_id: int

class MovimientoResponse(MovimientoCreate):
    id: int

    class Config:
        from_attributes = True