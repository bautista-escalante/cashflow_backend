from core.models.Plataforma import Plataforma
from api.schemas.PlataformaSchema import PlataformaCreate
from sqlalchemy.orm import Session

class PlataformaValidator:
    @staticmethod
    def validar_plataforma(db: Session, plataforma: PlataformaCreate):
        if not plataforma.nombre:
            raise ValueError("El nombre es obligatorio.")
        
        if plataforma.saldo < 0:
            raise ValueError("El saldo no puede ser negativo.")
        
        if db.query(Plataforma).filter(Plataforma.nombre == plataforma.nombre).first():
            raise ValueError("Ya existe una plataforma con ese nombre.")
