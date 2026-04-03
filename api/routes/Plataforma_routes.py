from fastapi import APIRouter

plataforma_routes = APIRouter()

plataforma_routes.post("/plataforma") # agregar una nueva plataforma
def agregar_plataforma():
    pass

plataforma_routes.get("/plataformas") # traer todas las plataformas y su saldo
def obtener_plataformas():
    pass

plataforma_routes.get("/plataforma/{nombre}") # traer el saldo de una plataforma específica
def obtener_saldo(nombre):
    pass