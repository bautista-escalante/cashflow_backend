from core.models.Usuario import Usuario
from api.schemas.UsuarioSchema import UsuarioCreate

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

    @staticmethod
    def verificar_usuario_existe(usuario_id: int, db: Session):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.eliminado_el.is_(None)).first()
        if not usuario:
            
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

        return usuario
    
    @staticmethod
    def verificar_clave_distinta(usuario_id: int, clave, db: Session, crypt_context):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.eliminado_el.is_(None)).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

        if len(clave) < 8:
            raise HTTPException(status_code=400, detail="La nueva clave debe tener al menos 8 caracteres.")

        if crypt_context.verify(clave, usuario.clave):
            raise HTTPException(status_code=400, detail="La nueva clave debe ser diferente a la actual.")