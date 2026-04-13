from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from infrastructure.database.db import Base

class Plataforma(Base):
    __tablename__ = 'plataformas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    saldo = Column(Float)
    fecha = Column(DateTime)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))

    def __init__(self, nombre: str, saldo: float, fecha, id_usuario: int):
        self.nombre = nombre.lower().strip()
        self.saldo = saldo
        self.fecha = fecha
        self.id_usuario = id_usuario