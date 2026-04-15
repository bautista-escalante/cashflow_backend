from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioModify, UsuarioAuth, UsuarioResponse
from infrastructure.database.db import get_db
from core.models.Usuario import Usuario
from core.use_cases.UsuarioCase import UsuarioCase

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])
usuario_case = UsuarioCase()

@usuario_router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    
    return usuario_case.crear_usuario(usuario, db)

@usuario_router.get("/", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    
    return usuario_case.obtener_usuario(usuario_id, db)

@usuario_router.put("/", response_model=UsuarioResponse)
def actualizar_usuario(usuario: UsuarioModify, db: Session = Depends(get_db)):
    
    return usuario_case.actualizar_usuario(usuario, db)

@usuario_router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    
    return usuario_case.eliminar_usuario(usuario_id, db)

@usuario_router.post("/auth")
def autenticar_usuario(usuario_auth: UsuarioAuth, db: Session = Depends(get_db)):
    
    return usuario_case.autenticar_usuario(usuario_auth.email, usuario_auth.clave, db) 