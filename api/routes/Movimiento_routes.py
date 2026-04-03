from fastapi import FastAPI, APIRouter

Movimiento_routes = APIRouter()

Movimiento_routes.post("/movimiento")
def agregar_movimiento():
    pass

Movimiento_routes.get("/movimientos") # trar todos los movimientos
def obtener_movimientos():
    pass


Movimiento_routes.get("/movimientos/evolucion") # traer la evolucion de los movimientos a lo largo del tiempo
def obtener_evolucion():
    pass

Movimiento_routes.get("/resumen") # traer el resumen de los movimientos, total de ingresos y gastos
def obtener_resumen():
    pass