from fastapi import FastAPI
from api.routes.Movimiento_routes import Movimiento

app = FastAPI()

app.include_router(Movimiento)

""" 
desde el frontend me llega 
    tipo -> ingreso, gasto o permutacion
    categoria -> essencial, gusto, ahorro
    monto -> numero
    descripcion -> string para gastos e ingresos
    plataforma -> efectivo, tarjeta, billetera virtual, dolares

deberia crear una cuenta para que los dema snop vean mi informacion, 
pero por ahora lo dejamos asi

agregamos fecha 

agregamos el nuevo movimiento a la base de datos,
y devolvemos el total final al frontend

si es una permutacion se resta el monto a la plataforma origen y se suma a la plataforma destino, 
y se devuelve el total final al frontend

rutas:

agregrar movimiento -> POST /movimiento
obtener movimientos -> GET /movimientos
obtener evolucion -> GET /movimientos/evolucion trae los totales atravez de los dias ? 

obtener resumen -> GET /resumen

obtener plataformas -> GET /plataformas -> para saber cuento tenes en una en especial 

obtener permutacion -> POST /permutacion 

con estos datos podemos hacer un dashboard con el total de ingresos, gastos, y el balance final, 
ademas de un grafico con la evolucion del balance a lo largo del tiempo

esto entra en use cases:
    DEBERIA OBTENER EL VALOR QUE HAY EN DICHAS PLATAFORMAS  
    restarle el monto a la plataforma origen y sumarle el monto a la plataforma destino,
    y devolver el total final
        
    si es de efectivo a dolar o viceversa, 
    deberia hacer la conversion segun el valor del dolar al momento de la permutacion
        
    deberia guardar un registro de la permutacion en la base de datos?
        
"""