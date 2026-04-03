from pydantic import BaseModel


class PlataformaCreate(BaseModel):
    nombre: str
    saldo_inicial: float

class PlataformaResponse(PlataformaCreate):
    id: int
    saldo_actual: float

    class Config:
        from_attributes = True