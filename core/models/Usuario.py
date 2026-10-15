from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.database.db import Base

class Usuario(Base):
    
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    clave = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    fecha = Column(DateTime)
    eliminado_el = Column(DateTime, nullable=True)
    
    def __init__(self, id: int, nombre: str, clave: str, email: str):
        
        self.id = id
        self.nombre = nombre
        self.clave = clave
        self.email = email
        self.eliminado_el = None