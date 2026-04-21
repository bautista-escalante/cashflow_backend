from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from api.routes.Movimiento_routes import Movimiento_routes
from api.routes.Plataforma_routes import plataforma_routes
from api.routes.permutacion_routes import Permutacion_routes
from api.routes.usuario_routes import usuario_router
from fastapi.exceptions import RequestValidationError

from infrastructure.database.db import engine, Base
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento
from core.exceptions import validation_exception_handler

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://cashflow-frontend-eight.vercel.app",
    "capacitor://localhost",
    "http://localhost",
]


app.add_exception_handler(RequestValidationError, validation_exception_handler)

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

