from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from infrastructure.database.db import get_db
from api.schemas.PlataformaSchema import PlataformaCreate, PlataformaResponse
from core.use_cases.PlataformaCase import PlataformaCase
from infrastructure.service.AuthService import AuthService

plataforma_routes = APIRouter(prefix="/plataformas", tags=["plataformas"])
plataforma_case = PlataformaCase()

@plataforma_routes.post("/", response_model=PlataformaResponse)
def agregar_plataforma(plataforma: PlataformaCreate, 
    payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):
        
    return plataforma_case.crear_plataforma(db, plataforma, payload["user_id"])
    
@plataforma_routes.get("/", response_model=list[PlataformaResponse])
def obtener_plataformas(payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):
        
    return plataforma_case.obtener_plataformas(db, payload["user_id"])

@plataforma_routes.get("/{nombre}", response_model=PlataformaResponse)
def obtener_plataforma(nombre: str, 
    payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):

    return plataforma_case.obtener_plataforma(db, nombre.lower().strip(), payload["user_id"])
    