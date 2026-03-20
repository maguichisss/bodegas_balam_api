from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .. import crud, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TipoProductoRead)
def create_tipo_producto(tipo_producto: schemas.TipoProductoCreate, db: Session = Depends(get_db)):
    return crud.tipo_producto_crud.create(db, obj_in=tipo_producto)


@router.get("/", response_model=List[schemas.TipoProductoRead])
def read_tipos_producto(
    skip: int = 0,
    limit: int = 100,
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    tipo_producto: Optional[str] = Query(None, description="Filter by tipo_producto (exact match)"),
    tipo_producto__contains: Optional[str] = Query(None, description="Filter by tipo_producto contains"),
    tipo_producto__startswith: Optional[str] = Query(None, description="Filter by tipo_producto starts with"),
    tipo_producto__endswith: Optional[str] = Query(None, description="Filter by tipo_producto ends with"),
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
    if tipo_producto is not None:
        filters["tipo_producto"] = {"eq": tipo_producto}
    if tipo_producto__contains is not None:
        filters.setdefault("tipo_producto", {})["contains"] = tipo_producto__contains
    if tipo_producto__startswith is not None:
        filters.setdefault("tipo_producto", {})["startswith"] = tipo_producto__startswith
    if tipo_producto__endswith is not None:
        filters.setdefault("tipo_producto", {})["endswith"] = tipo_producto__endswith

    if filters:
        return crud.tipo_producto_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.tipo_producto_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.TipoProductoRead)
def read_tipo_producto(id: int, db: Session = Depends(get_db)):
    db_tipo = crud.tipo_producto_crud.get(db, id=id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de producto not found")
    return db_tipo


@router.put("/{id}", response_model=schemas.TipoProductoRead)
def update_tipo_producto(id: int, tipo_producto: schemas.TipoProductoCreate, db: Session = Depends(get_db)):
    db_tipo = crud.tipo_producto_crud.get(db, id=id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de producto not found")
    return crud.tipo_producto_crud.update(db, db_obj=db_tipo, obj_in=tipo_producto)


@router.delete("/{id}", response_model=schemas.TipoProductoRead)
def delete_tipo_producto(id: int, db: Session = Depends(get_db)):
    db_tipo = crud.tipo_producto_crud.get(db, id=id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de producto not found")
    return crud.tipo_producto_crud.remove(db, id=id)
