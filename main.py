from fastapi import FastAPI
from api.routes.Movimiento import Movimiento_path

app = FastAPI()

app.include_router(Movimiento_path)

""" 
desde el frontend me llega 
    tipo -> ingreso, gasto o permutacion
    categoria -> essencial, gusto, ahorro
    monto -> numero
    descripcion -> string para gastos e ingresos
    plataforma -> efectivo, tarjeta, billetera virtual, dolares

agregamos fecha 

agregamos el nuevo movimiento a la base de datos,
y devolvemos el total final al frontend

si es una permutacion se resta el monto a la plataforma origen y se suma a la plataforma destino, 
y se devuelve el total final al frontend

rutas:

agregrar movimiento -> POST /movimiento
obtener evolucion -> GET /movimientos
obtener evolucion -> GET /movimientos/evolucion

obtener resumen -> GET /resumen

obtener plataformas -> GET /plataformas -> para saber cuento tenes en una en especial 

obtener permutacion -> POST /permutacion 

con estos datos podemos hacer un dashboard con el total de ingresos, gastos, y el balance final, 
ademas de un grafico con la evolucion del balance a lo largo del tiempo


"""