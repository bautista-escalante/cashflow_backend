from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioAuth, UsuarioResponse
from infrastructure.database.db import get_db
from core.models.Usuario import Usuario
from core.use_cases.UsuarioCase import UsuarioCase
from infrastructure.service.AuthService import AuthService

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])
usuario_case = UsuarioCase()
dependencies=[Depends(AuthService.validar_token)]

@usuario_router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    
    return usuario_case.crear_usuario(usuario, db)

@usuario_router.get("/", response_model=UsuarioResponse)
def obtener_usuario(payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):
    
    return usuario_case.obtener_usuario(payload["user_id"], db)

@usuario_router.put("/", response_model=UsuarioResponse)
def actualizar_usuario(clave:str, payload=Depends(AuthService.validar_token), db: Session = Depends(get_db)):
    
    return usuario_case.actualizar_usuario(clave, payload["user_id"], db)

@usuario_router.delete("/")
def eliminar_usuario(db: Session = Depends(get_db), payload=Depends(AuthService.validar_token)):
    
    return usuario_case.eliminar_usuario(payload["user_id"], db)

@usuario_router.post("/auth")
def autenticar_usuario(usuario_auth: UsuarioAuth, db: Session = Depends(get_db)):
    
    return usuario_case.autenticar_usuario(usuario_auth.email, usuario_auth.clave, db) 