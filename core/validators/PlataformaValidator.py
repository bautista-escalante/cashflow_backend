from core.models.Plataforma import Plataforma
from api.schemas.PlataformaSchema import PlataformaCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func

class PlataformaValidator:
    @staticmethod
    def validar_plataforma(db: Session, plataforma: PlataformaCreate):
        if not plataforma.nombre:
            raise HTTPException(status_code=400, detail="El nombre es obligatorio.")
        
        if plataforma.saldo < 0:
            raise HTTPException(status_code=400, detail="El saldo no puede ser negativo.")
        
        if db.query(Plataforma).filter(
            func.lower(func.trim(Plataforma.nombre)) == plataforma.nombre.strip().lower()
        ).first():
            raise HTTPException(status_code=400, detail="Ya existe una plataforma con ese nombre.")
