from fastapi import Depends
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.use_cases.PermutacionCase import PermutacionCase
from api.schemas.PermutacionSchema import PermutacionCreate, PermutacionResponse
from infrastructure.database.db import get_db
from infrastructure.service.AuthService import AuthService


permutacion_case = PermutacionCase()
Permutacion_routes = APIRouter()

# realizar una permutacion entre plataformas
@Permutacion_routes.post("/permutacion") 
def realizar_permutacion(permutacion: PermutacionCreate, db: Session = Depends(get_db), 
    response_model=PermutacionResponse, payload=Depends(AuthService.validar_token)):

    return permutacion_case.generar_permutaciones(db, permutacion, payload["user_id"])


@Permutacion_routes.post("/permutacion_dolar") 
def realizar_permutacion(permutacion: PermutacionCreate, db: Session = Depends(get_db), 
    response_model=PermutacionResponse, payload=Depends(AuthService.validar_token)):

    return permutacion_case.permutar_dolar(db, permutacion, payload["user_id"])
