from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, String

from .database import Base


class Repuesto(Base):
    """Repuesto de suspensión (amortiguadores, espirales, bujes, rótulas, etc.)."""

    __tablename__ = "repuestos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    tipo = Column(String(50), nullable=False)          # Amortiguador, Espiral, Buje...
    marca = Column(String(80), nullable=False)          # Monroe, KYB, Gabriel...
    referencia = Column(String(80), nullable=True)      # Código del fabricante
    vehiculo = Column(String(120), nullable=False)      # Ej: Chevrolet Spark GT 2015
    posicion = Column(String(30), nullable=False)       # Delantero, Trasero, Kit completo
    precio = Column(Numeric(12, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    creado = Column(DateTime, default=datetime.utcnow)
    actualizado = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
