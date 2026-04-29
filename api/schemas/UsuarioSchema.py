from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    clave: str


class UsuarioAuth(BaseModel):
    email: EmailStr
    clave: str
    
class UpdatePassword(BaseModel):
    clave: str


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True