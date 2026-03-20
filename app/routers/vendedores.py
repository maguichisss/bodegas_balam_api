from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .. import crud, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.VendedorRead)
def create_vendedor(vendedor: schemas.VendedorCreate, db: Session = Depends(get_db)):
    return crud.vendedor_crud.create(db, obj_in=vendedor)


@router.get("/", response_model=List[schemas.VendedorRead])
def read_vendedores(
    skip: int = 0,
    limit: int = 100,
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    vendedor: Optional[str] = Query(None, description="Filter by vendedor (exact match)"),
    vendedor__contains: Optional[str] = Query(None, description="Filter by vendedor contains"),
    vendedor__startswith: Optional[str] = Query(None, description="Filter by vendedor starts with"),
    vendedor__endswith: Optional[str] = Query(None, description="Filter by vendedor ends with"),
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
    if vendedor is not None:
        filters["vendedor"] = {"eq": vendedor}
    if vendedor__contains is not None:
        filters.setdefault("vendedor", {})["contains"] = vendedor__contains
    if vendedor__startswith is not None:
        filters.setdefault("vendedor", {})["startswith"] = vendedor__startswith
    if vendedor__endswith is not None:
        filters.setdefault("vendedor", {})["endswith"] = vendedor__endswith

    if filters:
        return crud.vendedor_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.vendedor_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.VendedorRead)
def read_vendedor(id: int, db: Session = Depends(get_db)):
    db_vendedor = crud.vendedor_crud.get(db, id=id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor not found")
    return db_vendedor


@router.put("/{id}", response_model=schemas.VendedorRead)
def update_vendedor(id: int, vendedor: schemas.VendedorCreate, db: Session = Depends(get_db)):
    db_vendedor = crud.vendedor_crud.get(db, id=id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor not found")
    return crud.vendedor_crud.update(db, db_obj=db_vendedor, obj_in=vendedor)


@router.delete("/{id}", response_model=schemas.VendedorRead)
def delete_vendedor(id: int, db: Session = Depends(get_db)):
    db_vendedor = crud.vendedor_crud.get(db, id=id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor not found")
    return crud.vendedor_crud.remove(db, id=id)
