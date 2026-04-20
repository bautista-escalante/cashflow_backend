from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from api.routes.Movimiento_routes import Movimiento_routes
from api.routes.Plataforma_routes import plataforma_routes
from api.routes.permutacion_routes import Permutacion_routes
from api.routes.usuario_routes import usuario_router


from infrastructure.database.db import engine, Base
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Movimiento_routes)
app.include_router(plataforma_routes)
app.include_router(Permutacion_routes)
app.include_router(usuario_router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

