from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from api.schemas.MovimientoSchema import MovimientoCreate, MovimientoResponse
from core.use_cases.MovimientoCase import movimientoCase
from infrastructure.database.db import get_db

Movimiento_routes = APIRouter()
movimiento_case = movimientoCase()

@Movimiento_routes.post("/movimiento", response_model=MovimientoResponse)
def agregar_movimiento(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    try:
        return movimiento_case.agregar_movimiento(db, movimiento)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@Movimiento_routes.get("/movimientos", response_model=list[MovimientoResponse]) # trar todos los movimientos
def obtener_movimientos(db: Session = Depends(get_db)):
    try:
        return movimiento_case.obtener_movimientos(db, "todos")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@Movimiento_routes.get("/movimientos/gastos", response_model=list[MovimientoResponse])
def obtener_gastos(db: Session = Depends(get_db)):
    try:
        return movimiento_case.obtener_movimientos(db, "gasto")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@Movimiento_routes.get("/movimientos/ingresos", response_model=list[MovimientoResponse])
def obtener_ingresos(db: Session = Depends(get_db)):
    try:
        return movimiento_case.obtener_movimientos(db, "ingreso")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# traer la evolucion de los movimientos a lo largo del tiempo
@Movimiento_routes.get("/movimientos/evolucion") 
def obtener_evolucion(db: Session = Depends(get_db)):
    try:
        return movimiento_case.obtener_evolucion(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@Movimiento_routes.get("/movimiento/{movimiento_id}")
def obtener_movimiento_por_id(movimiento_id: int, db: Session = Depends(get_db)):
    try:
        return movimiento_case.get_movimiento_by_id(db, movimiento_id)
       
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def eliminar_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    try:
        movimiento_case.delete_movimiento(db, movimiento_id)
        return JSONResponse({"mensaje": "Movimiento eliminado"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))