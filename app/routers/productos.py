from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from .. import crud, schemas
from ..db import get_db

router = APIRouter()

PRODUCTO_BASICO = ["id", "producto", "presentacion"]
PRODUCTO_DETALLE = ["id", "producto", "presentacion", "alias", "id_tipo", "precio_referencia", "url_image"]


@router.post("/", response_model=schemas.ProductoRead)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.producto_crud.create(db, obj_in=producto)


@router.get("/", response_model=Union[List[schemas.ProductoRead], List[Dict[str, Any]]])
def read_productos(
    skip: int = 0,
    limit: int = 100,
    modo: Optional[str] = Query(None, description="Modo de respuesta: basico, detalle"),
    campos: Optional[str] = Query(None, description="Campos a retornar (comma-separated)"),
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    id__in: Optional[str] = Query(None, description="Filter by id in (comma-separated values)"),
    producto: Optional[str] = Query(None, description="Filter by producto (exact match)"),
    producto__contains: Optional[str] = Query(None, description="Filter by producto contains"),
    producto__like: Optional[str] = Query(None, description="Filter by producto LIKE (case-insensitive)"),
    producto__startswith: Optional[str] = Query(None, description="Filter by producto starts with"),
    producto__endswith: Optional[str] = Query(None, description="Filter by producto ends with"),
    presentacion: Optional[str] = Query(None, description="Filter by presentacion (exact match)"),
    presentacion__contains: Optional[str] = Query(None, description="Filter by presentacion contains"),
    alias: Optional[str] = Query(None, description="Filter by alias (exact match)"),
    alias__contains: Optional[str] = Query(None, description="Filter by alias contains"),
    id_tipo: Optional[int] = Query(None, description="Filter by id_tipo (exact match)"),
    precio_referencia: Optional[Decimal] = Query(None, description="Filter by precio_referencia (exact match)"),
    precio_referencia__gt: Optional[Decimal] = Query(None, description="Filter by precio_referencia > value"),
    precio_referencia__gte: Optional[Decimal] = Query(None, description="Filter by precio_referencia >= value"),
    precio_referencia__lt: Optional[Decimal] = Query(None, description="Filter by precio_referencia < value"),
    precio_referencia__lte: Optional[Decimal] = Query(None, description="Filter by precio_referencia <= value"),
    db: Session = Depends(get_db),
):
    filters: Dict[str, Dict[str, Any]] = {}
    fields: Optional[List[str]] = None

    if modo == "basico":
        fields = PRODUCTO_BASICO
    elif modo == "detalle":
        fields = PRODUCTO_DETALLE
    elif campos:
        fields = [f.strip() for f in campos.split(",")]

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
    if producto is not None:
        filters["producto"] = {"eq": producto}
    if producto__contains is not None:
        filters.setdefault("producto", {})["contains"] = producto__contains
    if producto__like is not None:
        filters.setdefault("producto", {})["like"] = producto__like
    if producto__startswith is not None:
        filters.setdefault("producto", {})["startswith"] = producto__startswith
    if producto__endswith is not None:
        filters.setdefault("producto", {})["endswith"] = producto__endswith
    if presentacion is not None:
        filters["presentacion"] = {"eq": presentacion}
    if presentacion__contains is not None:
        filters.setdefault("presentacion", {})["contains"] = presentacion__contains
    if alias is not None:
        filters["alias"] = {"eq": alias}
    if alias__contains is not None:
        filters.setdefault("alias", {})["contains"] = alias__contains
    if id_tipo is not None:
        filters["id_tipo"] = {"eq": id_tipo}
    if precio_referencia is not None:
        filters["precio_referencia"] = {"eq": precio_referencia}
    if precio_referencia__gt is not None:
        filters.setdefault("precio_referencia", {})["gt"] = precio_referencia__gt
    if precio_referencia__gte is not None:
        filters.setdefault("precio_referencia", {})["gte"] = precio_referencia__gte
    if precio_referencia__lt is not None:
        filters.setdefault("precio_referencia", {})["lt"] = precio_referencia__lt
    if precio_referencia__lte is not None:
        filters.setdefault("precio_referencia", {})["lte"] = precio_referencia__lte

    if fields:
        return crud.producto_crud.get_selected(db, skip=skip, limit=limit, filters=filters, fields=fields)
    if filters:
        return crud.producto_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.producto_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.ProductoRead)
def read_producto(id: int, db: Session = Depends(get_db)):
    db_producto = crud.producto_crud.get(db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return db_producto


@router.put("/{id}", response_model=schemas.ProductoRead)
def update_producto(id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.producto_crud.get(db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return crud.producto_crud.update(db, db_obj=db_producto, obj_in=producto)


@router.delete("/{id}", response_model=schemas.ProductoRead)
def delete_producto(id: int, db: Session = Depends(get_db)):
    db_producto = crud.producto_crud.get(db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return crud.producto_crud.remove(db, id=id)
