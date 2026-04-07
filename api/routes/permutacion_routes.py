from fastapi import Depends
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.use_cases.PermutacionCase import PermutacionCase
from api.schemas.PermutacionSchema import PermutacionCreate, PermutacionResponse
from infrastructure.database.db import get_db


permutacion_case = PermutacionCase()
Permutacion_routes = APIRouter()

# realizar una permutacion entre plataformas
@Permutacion_routes.post("/permutacion") 
def realizar_permutacion(permutacion: PermutacionCreate, db: Session = Depends(get_db), response_model=PermutacionResponse):
    try:
        return permutacion_case.generar_permutaciones(db, permutacion)
    
    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@Permutacion_routes.post("/permutacion_dolar") 
def realizar_permutacion(permutacion: PermutacionCreate, db: Session = Depends(get_db), response_model=PermutacionResponse):
    try:
        return permutacion_case.permutar_dolar(db, permutacion)

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})