from sqlalchemy.orm import Session
from fastapi import HTTPException

from core.models.Plataforma import Plataforma
from api.schemas.PlataformaSchema import PlataformaCreate
from core.validators.PlataformaValidator import PlataformaValidator
import datetime

class PlataformaCase:

    def crear_plataforma(self, db: Session, plataforma: PlataformaCreate):
        
        PlataformaValidator.validar_plataforma(db, plataforma)
        
        plataforma_db = Plataforma(plataforma.nombre, plataforma.saldo, datetime.datetime.now())
        
        db.add(plataforma_db)
        db.commit()
        db.refresh(plataforma_db)
        
        return plataforma_db

    def obtener_plataformas(self, db: Session):
        return db.query(Plataforma).all()

    def obtener_plataforma(self, db: Session, nombre: str):
        
        plataforma = db.query(Plataforma).filter(Plataforma.nombre == nombre).first()
        
        if not plataforma:
            raise HTTPException(status_code=404, detail="Plataforma no encontrada.")
        
        return plataforma