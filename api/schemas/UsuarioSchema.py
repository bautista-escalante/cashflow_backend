from pydantic import BaseModel, EmailStr

class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    clave: str

    class Config:
        orm_mode = True
        
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    clave: str
 
class UsuarioModify(BaseModel):
    id: int
    clave: str

class UsuarioResponse(UsuarioCreate):
    id: int

    class Config:
        from_attributes = True