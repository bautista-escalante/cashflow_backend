from sqlalchemy.orm import Session
from fastapi import HTTPException

from core.models.Plataforma import Plataforma
from api.schemas.PlataformaSchema import PlataformaCreate, PlataformaResponse
from core.validators.PlataformaValidator import PlataformaValidator
import datetime

class PlataformaCase:

    def crear_plataforma(self, db: Session, plataforma: PlataformaCreate, id_usuario):
        
        PlataformaValidator.validar_plataforma(db, plataforma, id_usuario)
        
        plataforma_db = Plataforma(plataforma.nombre, plataforma.saldo, datetime.datetime.now(), id_usuario)
        
        db.add(plataforma_db)
        db.commit()
        db.refresh(plataforma_db)
        
        return PlataformaResponse.model_validate(plataforma_db)

    def obtener_plataformas(self, db: Session, id):
        plataformas = db.query(Plataforma).filter(Plataforma.id_usuario == id).all()
        
        if not plataformas:
            raise HTTPException("platafomas no encontradas")

        return plataformas

    def obtener_plataforma(self, db: Session, nombre: str, id_usuario):
        
        plataforma = db.query(Plataforma).filter(Plataforma.nombre == nombre, Plataforma.id_usuario == id_usuario).first()
        
        if not plataforma:
            raise HTTPException(status_code=404, detail="Plataforma no encontrada.")
        
        return plataforma