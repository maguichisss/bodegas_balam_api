from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from decimal import Decimal
from .. import crud, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.InventarioRead)
def create_inventario(inventario: schemas.InventarioCreate, db: Session = Depends(get_db)):
    return crud.inventario_crud.create(db, obj_in=inventario)


@router.get("/", response_model=List[schemas.InventarioRead])
def read_inventarios(
    skip: int = 0,
    limit: int = 100,
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    id__in: Optional[str] = Query(None, description="Filter by id in (comma-separated values)"),
    id_compra: Optional[int] = Query(None, description="Filter by id_compra (exact match)"),
    stock_actual: Optional[int] = Query(None, description="Filter by stock_actual (exact match)"),
    stock_actual__gt: Optional[int] = Query(None, description="Filter by stock_actual > value"),
    stock_actual__gte: Optional[int] = Query(None, description="Filter by stock_actual >= value"),
    stock_actual__lt: Optional[int] = Query(None, description="Filter by stock_actual < value"),
    stock_actual__lte: Optional[int] = Query(None, description="Filter by stock_actual <= value"),
    stock_inicial: Optional[int] = Query(None, description="Filter by stock_inicial (exact match)"),
    stock_inicial__gt: Optional[int] = Query(None, description="Filter by stock_inicial > value"),
    stock_inicial__gte: Optional[int] = Query(None, description="Filter by stock_inicial >= value"),
    stock_inicial__lt: Optional[int] = Query(None, description="Filter by stock_inicial < value"),
    stock_inicial__lte: Optional[int] = Query(None, description="Filter by stock_inicial <= value"),
    precio_minimo: Optional[Decimal] = Query(None, description="Filter by precio_minimo (exact match)"),
    precio_minimo__gt: Optional[Decimal] = Query(None, description="Filter by precio_minimo > value"),
    precio_minimo__gte: Optional[Decimal] = Query(None, description="Filter by precio_minimo >= value"),
    precio_minimo__lt: Optional[Decimal] = Query(None, description="Filter by precio_minimo < value"),
    precio_minimo__lte: Optional[Decimal] = Query(None, description="Filter by precio_minimo <= value"),
    activo: Optional[bool] = Query(None, description="Filter by activo (exact match)"),
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
    if id_compra is not None:
        filters["id_compra"] = {"eq": id_compra}
    if stock_actual is not None:
        filters["stock_actual"] = {"eq": stock_actual}
    if stock_actual__gt is not None:
        filters.setdefault("stock_actual", {})["gt"] = stock_actual__gt
    if stock_actual__gte is not None:
        filters.setdefault("stock_actual", {})["gte"] = stock_actual__gte
    if stock_actual__lt is not None:
        filters.setdefault("stock_actual", {})["lt"] = stock_actual__lt
    if stock_actual__lte is not None:
        filters.setdefault("stock_actual", {})["lte"] = stock_actual__lte
    if stock_inicial is not None:
        filters["stock_inicial"] = {"eq": stock_inicial}
    if stock_inicial__gt is not None:
        filters.setdefault("stock_inicial", {})["gt"] = stock_inicial__gt
    if stock_inicial__gte is not None:
        filters.setdefault("stock_inicial", {})["gte"] = stock_inicial__gte
    if stock_inicial__lt is not None:
        filters.setdefault("stock_inicial", {})["lt"] = stock_inicial__lt
    if stock_inicial__lte is not None:
        filters.setdefault("stock_inicial", {})["lte"] = stock_inicial__lte
    if precio_minimo is not None:
        filters["precio_minimo"] = {"eq": precio_minimo}
    if precio_minimo__gt is not None:
        filters.setdefault("precio_minimo", {})["gt"] = precio_minimo__gt
    if precio_minimo__gte is not None:
        filters.setdefault("precio_minimo", {})["gte"] = precio_minimo__gte
    if precio_minimo__lt is not None:
        filters.setdefault("precio_minimo", {})["lt"] = precio_minimo__lt
    if precio_minimo__lte is not None:
        filters.setdefault("precio_minimo", {})["lte"] = precio_minimo__lte
    if activo is not None:
        filters["activo"] = {"eq": activo}

    if filters:
        return crud.inventario_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.inventario_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.InventarioRead)
def read_inventario(id: int, db: Session = Depends(get_db)):
    db_inventario = crud.inventario_crud.get(db, id=id)
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario not found")
    return db_inventario


@router.put("/{id}", response_model=schemas.InventarioRead)
def update_inventario(id: int, inventario: schemas.InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = crud.inventario_crud.get(db, id=id)
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario not found")
    return crud.inventario_crud.update(db, db_obj=db_inventario, obj_in=inventario)


@router.delete("/{id}", response_model=schemas.InventarioRead)
def delete_inventario(id: int, db: Session = Depends(get_db)):
    db_inventario = crud.inventario_crud.get(db, id=id)
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario not found")
    return crud.inventario_crud.remove(db, id=id)
