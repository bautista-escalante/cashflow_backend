from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from infrastructure.database.db import get_db
from api.schemas.PlataformaSchema import PlataformaCreate, PlataformaResponse
from core.use_cases.PlataformaCase import PlataformaCase

plataforma_routes = APIRouter()
plataforma_case = PlataformaCase()

@plataforma_routes.post("/plataforma", status_code=201, response_model=PlataformaResponse)
def agregar_plataforma(plataforma: PlataformaCreate, db: Session = Depends(get_db)):
    try:
        return plataforma_case.crear_plataforma(db, plataforma)
    
    except ValueError as ve:
        return JSONResponse({"error": str(ve)}, status_code=400)
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@plataforma_routes.get("/plataformas", response_model=list[PlataformaResponse])
def obtener_plataformas(db: Session = Depends(get_db)):
    try:
        return plataforma_case.obtener_plataformas(db)
    
    except ValueError as ve:
        return JSONResponse({"error": str(ve)}, status_code=400) 
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@plataforma_routes.get("/plataforma/{nombre}", response_model=PlataformaResponse)
def obtener_plataforma(nombre: str, db: Session = Depends(get_db)):
    try:
        return plataforma_case.obtener_plataforma(db, nombre.lower().strip())
    
    except ValueError as ve:
        return JSONResponse({"error": str(ve)}, status_code=400)
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)