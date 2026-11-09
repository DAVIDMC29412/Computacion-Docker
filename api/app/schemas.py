from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RepuestoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    tipo: str = Field(..., min_length=2, max_length=50)
    marca: str = Field(..., min_length=1, max_length=80)
    referencia: Optional[str] = Field(None, max_length=80)
    vehiculo: str = Field(..., min_length=2, max_length=120)
    posicion: str = Field(..., min_length=2, max_length=30)
    precio: float = Field(..., ge=0)
    stock: int = Field(0, ge=0)


class RepuestoCreate(RepuestoBase):
    pass


class RepuestoUpdate(RepuestoBase):
    pass


class RepuestoOut(RepuestoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
