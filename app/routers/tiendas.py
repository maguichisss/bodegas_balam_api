from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .. import crud, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TiendaRead)
def create_tienda(tienda: schemas.TiendaCreate, db: Session = Depends(get_db)):
    return crud.tienda_crud.create(db, obj_in=tienda)


@router.get("/", response_model=List[schemas.TiendaRead])
def read_tiendas(
    skip: int = 0,
    limit: int = 100,
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    tienda: Optional[str] = Query(None, description="Filter by tienda (exact match)"),
    tienda__contains: Optional[str] = Query(None, description="Filter by tienda contains"),
    tienda__startswith: Optional[str] = Query(None, description="Filter by tienda starts with"),
    tienda__endswith: Optional[str] = Query(None, description="Filter by tienda ends with"),
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
    if tienda is not None:
        filters["tienda"] = {"eq": tienda}
    if tienda__contains is not None:
        filters.setdefault("tienda", {})["contains"] = tienda__contains
    if tienda__startswith is not None:
        filters.setdefault("tienda", {})["startswith"] = tienda__startswith
    if tienda__endswith is not None:
        filters.setdefault("tienda", {})["endswith"] = tienda__endswith

    if filters:
        return crud.tienda_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.tienda_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.TiendaRead)
def read_tienda(id: int, db: Session = Depends(get_db)):
    db_tienda = crud.tienda_crud.get(db, id=id)
    if db_tienda is None:
        raise HTTPException(status_code=404, detail="Tienda not found")
    return db_tienda


@router.put("/{id}", response_model=schemas.TiendaRead)
def update_tienda(id: int, tienda: schemas.TiendaCreate, db: Session = Depends(get_db)):
    db_tienda = crud.tienda_crud.get(db, id=id)
    if db_tienda is None:
        raise HTTPException(status_code=404, detail="Tienda not found")
    return crud.tienda_crud.update(db, db_obj=db_tienda, obj_in=tienda)


@router.delete("/{id}", response_model=schemas.TiendaRead)
def delete_tienda(id: int, db: Session = Depends(get_db)):
    db_tienda = crud.tienda_crud.get(db, id=id)
    if db_tienda is None:
        raise HTTPException(status_code=404, detail="Tienda not found")
    return crud.tienda_crud.remove(db, id=id)
