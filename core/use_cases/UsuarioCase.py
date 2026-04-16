from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from core.models.Usuario import Usuario
from infrastructure.service.AuthService import AuthService
from core.validators.UsuarioValidator import UsuarioValidator
from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioResponse

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioCase:

    def crear_usuario(self, usuario: UsuarioCreate, db: Session):
        UsuarioValidator.validar_usuario(usuario, db)
        
        Usuario_nuevo = Usuario(
            id=None, 
            nombre=usuario.nombre, 
            clave=crypt_context.hash(usuario.clave), 
            email=usuario.email
        )
        db.add(Usuario_nuevo)
        db.commit()
        db.refresh(Usuario_nuevo)

        return UsuarioResponse.model_validate(Usuario_nuevo)

    def obtener_usuario(self, usuario_id: int, db: Session):
        
        usuario = UsuarioValidator.verificar_usuario_existe(usuario_id, db)
        
        return UsuarioResponse.model_validate(usuario)

    def actualizar_usuario(self, clave, id, db: Session):
        
        UsuarioValidator.verificar_clave_distinta(id, clave, db, crypt_context)
    
        usuario_db = db.query(Usuario).filter(
            Usuario.id == id,
            Usuario.eliminado_el.is_(None)
        ).first()

        usuario_db.clave = crypt_context.hash(clave)

        db.commit()
        db.refresh(usuario_db)

        return UsuarioResponse.model_validate(usuario_db)

    def eliminar_usuario(self, usuario_id: int, db: Session):
        usuario_db = UsuarioValidator.verificar_usuario_existe(usuario_id, db)

        usuario_db.eliminado_el = datetime.utcnow()

        db.commit()
        db.refresh(usuario_db)

        return {"detail": "Usuario eliminado exitosamente."}

    def autenticar_usuario(self, email: str, clave: str, db: Session):

        usuario_db = db.query(Usuario).filter(Usuario.email == email, Usuario.eliminado_el.is_(None)).first()

        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
        if not crypt_context.verify(clave, usuario_db.clave):
            raise HTTPException(status_code=401, detail="clave incorrecta.")

        token = AuthService.generar_token(usuario_db.id)

        return {"access_token": token, "token_type": "bearer"}