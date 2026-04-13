from sqlalchemy.orm import Session
from core.models.Usuario import Usuario
from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioResponse
from core.validators.UsuarioValidator import UsuarioValidator

from passlib.context import CryptContext

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
        pass

    def actualizar_usuario(self, usuario_id: int,  usuario: UsuarioCreate, db: Session):
        pass

    def eliminar_usuario(self, usuario_id: int, db: Session):
        pass
