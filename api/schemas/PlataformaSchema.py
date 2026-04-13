from pydantic import BaseModel


class PlataformaCreate(BaseModel):
    nombre: str
    saldo: float
    usuario_id: int

class PlataformaResponse(PlataformaCreate):
    id: int
    saldo: float

    class Config:
        from_attributes = True