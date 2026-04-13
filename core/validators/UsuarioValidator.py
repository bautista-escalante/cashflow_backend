from core.models.Usuario import Usuario
from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioResponse

from fastapi import HTTPException
from sqlalchemy.orm import Session


class UsuarioValidator:
    
    @staticmethod
    def validar_usuario(usuario: UsuarioCreate, db: Session):
        
        if len(usuario.clave) < 8:
            raise HTTPException(status_code=400, detail="La clave debe tener al menos 8 caracteres.")
        
        if not usuario.nombre.strip():
            raise HTTPException(status_code=400, detail="El nombre no puede estar vacío.")
        
        if db.query(Usuario).filter(Usuario.email == usuario.email).first():
            raise HTTPException(status_code=400, detail="El email ya está en uso.")

        if db.query(Usuario).filter(Usuario.nombre == usuario.nombre).first():
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")
