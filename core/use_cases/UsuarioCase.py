from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

import os
from dotenv import load_dotenv

from core.models.Usuario import Usuario
from api.schemas.UsuarioSchema import UsuarioCreate, UsuarioModify, UsuarioResponse
from core.validators.UsuarioValidator import UsuarioValidator


load_dotenv()
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
        
        UsuarioValidator.verificar_usuario_existe(usuario_id, db)
        
        return db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.eliminado_el.is_(None)).first()

    def actualizar_usuario(self, usuario: UsuarioModify, db: Session):
        
        UsuarioValidator.verificar_clave_distinta(usuario.id, usuario, db, crypt_context)
    
        usuario_db = db.query(Usuario).filter(
            Usuario.id == usuario.id,
            Usuario.eliminado_el.is_(None)
        ).first()

        usuario_db.clave = crypt_context.hash(usuario.clave)

        db.commit()
        db.refresh(usuario_db)

        return usuario_db

    def eliminar_usuario(self, usuario_id: int, db: Session):
        UsuarioValidator.verificar_usuario_existe(usuario_id, db)

        usuario_db = db.query(Usuario).filter(
            Usuario.id == usuario_id, 
            Usuario.eliminado_el.is_(None)
        ).first()

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

        print(os.getenv("SECRET_KEY"))
        token = encode(
            {
                "user_id": usuario_db.id,
                "exp": datetime.utcnow() + timedelta(hours=1)
            }, 
            os.getenv("SECRET_KEY"), 
            algorithm=os.getenv("ALGORITHM"))

        return {"access_token": token, "token_type": "bearer"}