from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.db import Base

class Movimiento(Base):
    __tablename__ = 'movimientos'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50))
    monto = Column(Float)
    fecha = Column(DateTime)
    descripcion = Column(String(200))
    categoria = Column(String(100))

    plataforma_id = Column(Integer, ForeignKey('plataformas.id'))
    plataforma_origen_id = Column(Integer, ForeignKey('plataformas.id'))
    plataforma_destino_id = Column(Integer, ForeignKey('plataformas.id'))
    
    plataforma = relationship("Plataforma", foreign_keys=[plataforma_id])
    plataforma_origen = relationship("Plataforma", foreign_keys=[plataforma_origen_id])
    plataforma_destino = relationship("Plataforma", foreign_keys=[plataforma_destino_id])
    