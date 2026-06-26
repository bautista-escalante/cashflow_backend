from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Optional, Union
from datetime import datetime

from api.schemas.MovimientoSchema import MovimientoCreate, MovimientoResponse
from api.schemas.PermutacionSchema import PermutacionResponse
from core.use_cases.MovimientoCase import movimientoCase
from infrastructure.database.db import get_db
from infrastructure.service.AuthService import AuthService

Movimiento_routes = APIRouter(prefix="/movimientos", tags=["movimientos"])
movimiento_case = movimientoCase()

@Movimiento_routes.post("/", response_model=MovimientoResponse)
def agregar_movimiento( movimiento: MovimientoCreate, 
    payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):

    return movimiento_case.agregar_movimiento(db, movimiento, payload["user_id"])

@Movimiento_routes.get("/", response_model=list[Union[MovimientoResponse, PermutacionResponse]]) # trar todos los movimientos
def obtener_movimientos(payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):

    return movimiento_case.obtener_movimientos(db, "todos", payload["user_id"])

@Movimiento_routes.get("/gastos", response_model=list[MovimientoResponse])
def obtener_gastos( 
    mes: int, anio: int, categoria: str, payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):
    
    return movimiento_case.obtener_gastos(db, anio, mes, categoria, payload["user_id"])

@Movimiento_routes.get("/ingresos", response_model=list[MovimientoResponse])
def obtener_ingresos(payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):

    return movimiento_case.obtener_movimientos(db, "ingreso", payload["user_id"])

@Movimiento_routes.get("/evolucion") 
def obtener_evolucion(payload=Depends(AuthService.validar_token), db: Session = Depends(get_db),  
    mes: Optional[int] = Query(default=None, ge=1, le=12), anio: Optional[int] = Query(default=None, ge=2000, le=2100),
   ):

    return movimiento_case.obtener_evolucion(db, payload["user_id"], mes, anio) 

@Movimiento_routes.delete("/") 
def eliminar_movimiento(movimiento_id: int,
    payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):

    movimiento_case.delete_movimiento(db, movimiento_id, payload["user_id"])
    return JSONResponse({"mensaje": "Movimiento eliminado"}, status_code=200)