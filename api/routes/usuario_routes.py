from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioResponse
from infrastructure.database.db import get_db
from core.models.Usuario import Usuario
from core.use_cases.UsuarioCase import UsuarioCase

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])
usuario_case = UsuarioCase()

@usuario_router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    
    return usuario_case.crear_usuario(usuario, db)


