from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from decimal import Decimal
from .. import crud, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.CompraRead)
def create_compra(compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    return crud.compra_crud.create(db, obj_in=compra)


@router.get("/", response_model=List[schemas.CompraRead])
def read_compras(
    skip: int = 0,
    limit: int = 100,
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    id__in: Optional[str] = Query(None, description="Filter by id in (comma-separated values)"),
    id_producto: Optional[int] = Query(None, description="Filter by id_producto (exact match)"),
    cantidad: Optional[int] = Query(None, description="Filter by cantidad (exact match)"),
    cantidad__gt: Optional[int] = Query(None, description="Filter by cantidad > value"),
    cantidad__gte: Optional[int] = Query(None, description="Filter by cantidad >= value"),
    cantidad__lt: Optional[int] = Query(None, description="Filter by cantidad < value"),
    cantidad__lte: Optional[int] = Query(None, description="Filter by cantidad <= value"),
    precio_unitario: Optional[Decimal] = Query(None, description="Filter by precio_unitario (exact match)"),
    precio_unitario__gt: Optional[Decimal] = Query(None, description="Filter by precio_unitario > value"),
    precio_unitario__gte: Optional[Decimal] = Query(None, description="Filter by precio_unitario >= value"),
    precio_unitario__lt: Optional[Decimal] = Query(None, description="Filter by precio_unitario < value"),
    precio_unitario__lte: Optional[Decimal] = Query(None, description="Filter by precio_unitario <= value"),
    id_tienda: Optional[int] = Query(None, description="Filter by id_tienda (exact match)"),
    estatus_id: Optional[int] = Query(None, description="Filter by estatus_id (exact match)"),
    db: Session = Depends(get_db),
):
    filters: Dict[str, Dict[str, Any]] = {}

    if id is not None:
        filters["id"] = {"eq": id}
    if id__gt is not None:
        filters.setdefault("id", {})["gt"] = id__gt
    if id__gte is not None:
        filters.setdefault("id", {})["gte"] = id__gte
    if id__lt is not None:
        filters.setdefault("id", {})["lt"] = id__lt
    if id__lte is not None:
        filters.setdefault("id", {})["lte"] = id__lte
    if id__in is not None:
        filters.setdefault("id", {})["in"] = id__in
    if id_producto is not None:
        filters["id_producto"] = {"eq": id_producto}
    if cantidad is not None:
        filters["cantidad"] = {"eq": cantidad}
    if cantidad__gt is not None:
        filters.setdefault("cantidad", {})["gt"] = cantidad__gt
    if cantidad__gte is not None:
        filters.setdefault("cantidad", {})["gte"] = cantidad__gte
    if cantidad__lt is not None:
        filters.setdefault("cantidad", {})["lt"] = cantidad__lt
    if cantidad__lte is not None:
        filters.setdefault("cantidad", {})["lte"] = cantidad__lte
    if precio_unitario is not None:
        filters["precio_unitario"] = {"eq": precio_unitario}
    if precio_unitario__gt is not None:
        filters.setdefault("precio_unitario", {})["gt"] = precio_unitario__gt
    if precio_unitario__gte is not None:
        filters.setdefault("precio_unitario", {})["gte"] = precio_unitario__gte
    if precio_unitario__lt is not None:
        filters.setdefault("precio_unitario", {})["lt"] = precio_unitario__lt
    if precio_unitario__lte is not None:
        filters.setdefault("precio_unitario", {})["lte"] = precio_unitario__lte
    if id_tienda is not None:
        filters["id_tienda"] = {"eq": id_tienda}
    if estatus_id is not None:
        filters["estatus_id"] = {"eq": estatus_id}

    if filters:
        return crud.compra_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.compra_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.CompraRead)
def read_compra(id: int, db: Session = Depends(get_db)):
    db_compra = crud.compra_crud.get(db, id=id)
    if db_compra is None:
        raise HTTPException(status_code=404, detail="Compra not found")
    return db_compra


@router.put("/{id}", response_model=schemas.CompraRead)
def update_compra(id: int, compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    db_compra = crud.compra_crud.get(db, id=id)
    if db_compra is None:
        raise HTTPException(status_code=404, detail="Compra not found")
    return crud.compra_crud.update(db, db_obj=db_compra, obj_in=compra)


@router.delete("/{id}", response_model=schemas.CompraRead)
def delete_compra(id: int, db: Session = Depends(get_db)):
    db_compra = crud.compra_crud.get(db, id=id)
    if db_compra is None:
        raise HTTPException(status_code=404, detail="Compra not found")
    return crud.compra_crud.remove(db, id=id)
