import time
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Repuesto
from .schemas import RepuestoCreate, RepuestoOut, RepuestoUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Espera a que MySQL esté listo y crea las tablas
    retries = 10
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            retries -= 1
            time.sleep(3)
    yield


app = FastAPI(
    title="API Repuestos de Suspensión",
    version="2.0.0",
    description="CRUD de repuestos de suspensión (FastAPI + MySQL).",
    lifespan=lifespan,
)


def obtener_o_404(db: Session, repuesto_id: int) -> Repuesto:
    repuesto = db.get(Repuesto, repuesto_id)
    if repuesto is None:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    return repuesto


@app.get("/api/health")
def health():
    return {"status": "ok"}


# ---------- VER (listar todos, con búsqueda y filtro opcional) ----------
@app.get("/api/repuestos", response_model=List[RepuestoOut])
def listar_repuestos(
    q: Optional[str] = Query(None, description="Buscar por nombre, marca, vehículo o referencia"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo"),
    db: Session = Depends(get_db),
):
    consulta = db.query(Repuesto)
    if q:
        patron = f"%{q}%"
        consulta = consulta.filter(
            or_(
                Repuesto.nombre.ilike(patron),
                Repuesto.marca.ilike(patron),
                Repuesto.vehiculo.ilike(patron),
                Repuesto.referencia.ilike(patron),
            )
        )
    if tipo:
        consulta = consulta.filter(Repuesto.tipo == tipo)
    return consulta.order_by(Repuesto.id.desc()).all()


# ---------- VER (uno) ----------
@app.get("/api/repuestos/{repuesto_id}", response_model=RepuestoOut)
def ver_repuesto(repuesto_id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, repuesto_id)


# ---------- AGREGAR ----------
@app.post("/api/repuestos", response_model=RepuestoOut, status_code=status.HTTP_201_CREATED)
def crear_repuesto(datos: RepuestoCreate, db: Session = Depends(get_db)):
    repuesto = Repuesto(**datos.model_dump())
    db.add(repuesto)
    db.commit()
    db.refresh(repuesto)
    return repuesto


# ---------- EDITAR ----------
@app.put("/api/repuestos/{repuesto_id}", response_model=RepuestoOut)
def editar_repuesto(repuesto_id: int, datos: RepuestoUpdate, db: Session = Depends(get_db)):
    repuesto = obtener_o_404(db, repuesto_id)
    for campo, valor in datos.model_dump().items():
        setattr(repuesto, campo, valor)
    db.commit()
    db.refresh(repuesto)
    return repuesto


# ---------- ELIMINAR ----------
@app.delete("/api/repuestos/{repuesto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_repuesto(repuesto_id: int, db: Session = Depends(get_db)):
    repuesto = obtener_o_404(db, repuesto_id)
    db.delete(repuesto)
    db.commit()
    return None
