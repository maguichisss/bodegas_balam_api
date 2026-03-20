from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from .. import crud, schemas
from ..db import get_db

router = APIRouter()

VENTA_BASICO = ["id", "cantidad_vendida", "precio_venta"]
VENTA_DETALLE = ["id", "cantidad_vendida", "precio_venta"]


@router.post("/", response_model=schemas.VentaRead)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    return crud.venta_crud.create(db, obj_in=venta)


@router.get("/", response_model=Union[List[schemas.VentaRead], List[Dict[str, Any]]])
def read_ventas(
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
    id_inventario: Optional[int] = Query(None, description="Filter by id_inventario (exact match)"),
    id_vendedor: Optional[int] = Query(None, description="Filter by id_vendedor (exact match)"),
    cantidad_vendida: Optional[int] = Query(None, description="Filter by cantidad_vendida (exact match)"),
    cantidad_vendida__gt: Optional[int] = Query(None, description="Filter by cantidad_vendida > value"),
    cantidad_vendida__gte: Optional[int] = Query(None, description="Filter by cantidad_vendida >= value"),
    cantidad_vendida__lt: Optional[int] = Query(None, description="Filter by cantidad_vendida < value"),
    cantidad_vendida__lte: Optional[int] = Query(None, description="Filter by cantidad_vendida <= value"),
    precio_venta: Optional[Decimal] = Query(None, description="Filter by precio_venta (exact match)"),
    precio_venta__gt: Optional[Decimal] = Query(None, description="Filter by precio_venta > value"),
    precio_venta__gte: Optional[Decimal] = Query(None, description="Filter by precio_venta >= value"),
    precio_venta__lt: Optional[Decimal] = Query(None, description="Filter by precio_venta < value"),
    precio_venta__lte: Optional[Decimal] = Query(None, description="Filter by precio_venta <= value"),
    total_venta: Optional[Decimal] = Query(None, description="Filter by total_venta (exact match)"),
    total_venta__gt: Optional[Decimal] = Query(None, description="Filter by total_venta > value"),
    total_venta__gte: Optional[Decimal] = Query(None, description="Filter by total_venta >= value"),
    total_venta__lt: Optional[Decimal] = Query(None, description="Filter by total_venta < value"),
    total_venta__lte: Optional[Decimal] = Query(None, description="Filter by total_venta <= value"),
    metodo_pago: Optional[str] = Query(None, description="Filter by metodo_pago (exact match)"),
    metodo_pago__contains: Optional[str] = Query(None, description="Filter by metodo_pago contains"),
    db: Session = Depends(get_db),
):
    filters: Dict[str, Dict[str, Any]] = {}
    fields: Optional[List[str]] = None

    if modo == "basico":
        fields = VENTA_BASICO
    elif modo == "detalle":
        fields = VENTA_DETALLE
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
    if id_inventario is not None:
        filters["id_inventario"] = {"eq": id_inventario}
    if id_vendedor is not None:
        filters["id_vendedor"] = {"eq": id_vendedor}
    if cantidad_vendida is not None:
        filters["cantidad_vendida"] = {"eq": cantidad_vendida}
    if cantidad_vendida__gt is not None:
        filters.setdefault("cantidad_vendida", {})["gt"] = cantidad_vendida__gt
    if cantidad_vendida__gte is not None:
        filters.setdefault("cantidad_vendida", {})["gte"] = cantidad_vendida__gte
    if cantidad_vendida__lt is not None:
        filters.setdefault("cantidad_vendida", {})["lt"] = cantidad_vendida__lt
    if cantidad_vendida__lte is not None:
        filters.setdefault("cantidad_vendida", {})["lte"] = cantidad_vendida__lte
    if precio_venta is not None:
        filters["precio_venta"] = {"eq": precio_venta}
    if precio_venta__gt is not None:
        filters.setdefault("precio_venta", {})["gt"] = precio_venta__gt
    if precio_venta__gte is not None:
        filters.setdefault("precio_venta", {})["gte"] = precio_venta__gte
    if precio_venta__lt is not None:
        filters.setdefault("precio_venta", {})["lt"] = precio_venta__lt
    if precio_venta__lte is not None:
        filters.setdefault("precio_venta", {})["lte"] = precio_venta__lte
    if total_venta is not None:
        filters["total_venta"] = {"eq": total_venta}
    if total_venta__gt is not None:
        filters.setdefault("total_venta", {})["gt"] = total_venta__gt
    if total_venta__gte is not None:
        filters.setdefault("total_venta", {})["gte"] = total_venta__gte
    if total_venta__lt is not None:
        filters.setdefault("total_venta", {})["lt"] = total_venta__lt
    if total_venta__lte is not None:
        filters.setdefault("total_venta", {})["lte"] = total_venta__lte
    if metodo_pago is not None:
        filters["metodo_pago"] = {"eq": metodo_pago}
    if metodo_pago__contains is not None:
        filters.setdefault("metodo_pago", {})["contains"] = metodo_pago__contains

    if fields:
        return crud.venta_crud.get_selected(db, skip=skip, limit=limit, filters=filters, fields=fields)
    if filters:
        return crud.venta_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.venta_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.VentaRead)
def read_venta(id: int, db: Session = Depends(get_db)):
    db_venta = crud.venta_crud.get(db, id=id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return db_venta


@router.put("/{id}", response_model=schemas.VentaRead)
def update_venta(id: int, venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    db_venta = crud.venta_crud.get(db, id=id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return crud.venta_crud.update(db, db_obj=db_venta, obj_in=venta)


@router.delete("/{id}", response_model=schemas.VentaRead)
def delete_venta(id: int, db: Session = Depends(get_db)):
    db_venta = crud.venta_crud.get(db, id=id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return crud.venta_crud.remove(db, id=id)
