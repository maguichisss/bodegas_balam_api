from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .. import crud, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.EstatusRead)
def create_estatus(estatus: schemas.EstatusCreate, db: Session = Depends(get_db)):
    return crud.estatus_crud.create(db, obj_in=estatus)


@router.get("/", response_model=List[schemas.EstatusRead])
def read_estatuses(
    skip: int = 0,
    limit: int = 100,
    id: Optional[int] = Query(None, description="Filter by id (exact match)"),
    id__gt: Optional[int] = Query(None, description="Filter by id > value"),
    id__gte: Optional[int] = Query(None, description="Filter by id >= value"),
    id__lt: Optional[int] = Query(None, description="Filter by id < value"),
    id__lte: Optional[int] = Query(None, description="Filter by id <= value"),
    estatus: Optional[str] = Query(None, description="Filter by estatus (exact match)"),
    estatus__contains: Optional[str] = Query(None, description="Filter by estatus contains"),
    estatus__startswith: Optional[str] = Query(None, description="Filter by estatus starts with"),
    estatus__endswith: Optional[str] = Query(None, description="Filter by estatus ends with"),
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
    if estatus is not None:
        filters["estatus"] = {"eq": estatus}
    if estatus__contains is not None:
        filters.setdefault("estatus", {})["contains"] = estatus__contains
    if estatus__startswith is not None:
        filters.setdefault("estatus", {})["startswith"] = estatus__startswith
    if estatus__endswith is not None:
        filters.setdefault("estatus", {})["endswith"] = estatus__endswith

    if filters:
        return crud.estatus_crud.get_filtered(db, skip=skip, limit=limit, filters=filters)
    return crud.estatus_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.EstatusRead)
def read_estatus(id: int, db: Session = Depends(get_db)):
    db_estatus = crud.estatus_crud.get(db, id=id)
    if db_estatus is None:
        raise HTTPException(status_code=404, detail="Estatus not found")
    return db_estatus


@router.put("/{id}", response_model=schemas.EstatusRead)
def update_estatus(id: int, estatus: schemas.EstatusCreate, db: Session = Depends(get_db)):
    db_estatus = crud.estatus_crud.get(db, id=id)
    if db_estatus is None:
        raise HTTPException(status_code=404, detail="Estatus not found")
    return crud.estatus_crud.update(db, db_obj=db_estatus, obj_in=estatus)


@router.delete("/{id}", response_model=schemas.EstatusRead)
def delete_estatus(id: int, db: Session = Depends(get_db)):
    db_estatus = crud.estatus_crud.get(db, id=id)
    if db_estatus is None:
        raise HTTPException(status_code=404, detail="Estatus not found")
    return crud.estatus_crud.remove(db, id=id)
