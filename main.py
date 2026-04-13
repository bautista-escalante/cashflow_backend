from fastapi import FastAPI
from api.routes.Movimiento_routes import Movimiento_routes
from api.routes.Plataforma_routes import plataforma_routes
from api.routes.permutacion_routes import Permutacion_routes
from api.routes.usuario_routes import usuario_router


from infrastructure.database.db import engine, Base
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Movimiento_routes)
app.include_router(plataforma_routes)
app.include_router(Permutacion_routes)
app.include_router(usuario_router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

