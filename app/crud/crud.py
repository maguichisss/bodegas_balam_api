from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

from ..models import models
Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


OPERATORS = {
    "eq": lambda c, v: c == v,
    "ne": lambda c, v: c != v,
    "gt": lambda c, v: c > v,
    "gte": lambda c, v: c >= v,
    "lt": lambda c, v: c < v,
    "lte": lambda c, v: c <= v,
    "like": lambda c, v: c.ilike(f"%{v}%"),
    "contains": lambda c, v: c.ilike(f"%{v}%"),
    "startswith": lambda c, v: c.ilike(f"{v}%"),
    "endswith": lambda c, v: c.ilike(f"%{v}"),
    "not_like": lambda c, v: ~c.ilike(f"%{v}%"),
    "in": lambda c, v: c.in_(v.split(",")) if isinstance(v, str) else c.in_(v),
    "not_in": lambda c, v: ~c.in_(v.split(",")) if isinstance(v, str) else ~c.in_(v),
    "is_null": lambda c, v: c.is_(None) if v else c.isnot(None),
}


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]:
        query = db.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return query.offset(skip).limit(limit).all()

    def get_filtered(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Dict[str, Any]]] = None,
        fields: Optional[List[str]] = None,
    ) -> List[ModelType]:
        query = db.query(self.model)
        conditions = []

        if filters:
            for field, params in filters.items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    for op, value in params.items():
                        if op in OPERATORS:
                            conditions.append(OPERATORS[op](column, value))

        if conditions:
            query = query.filter(and_(*conditions))

        return query.offset(skip).limit(limit).all()

    def get_selected(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Dict[str, Any]]] = None,
        fields: Optional[List[str]] = None,
    ) -> List[Any]:
        columns = []
        valid_fields = []

        if fields:
            for f in fields:
                if hasattr(self.model, f):
                    columns.append(getattr(self.model, f))
                    valid_fields.append(f)
        else:
            columns = [getattr(self.model, f) for f in dir(self.model) if not f.startswith('_') and not callable(getattr(self.model, f))]
            valid_fields = [f for f in dir(self.model) if not f.startswith('_') and not callable(getattr(self.model, f))]

        query = db.query(*columns) if columns else db.query(self.model)
        conditions = []

        if filters:
            for field, params in filters.items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    for op, value in params.items():
                        if op in OPERATORS:
                            conditions.append(OPERATORS[op](column, value))

        if conditions:
            query = query.filter(and_(*conditions))

        results = query.offset(skip).limit(limit).all()

        if fields and not columns:
            return results

        return [
            {k: float(v) if isinstance(v, Decimal) else v for k, v in zip(valid_fields, row)}
            for row in results
        ]

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class TipoProductoCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.TipoProducto)


class TiendaCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Tienda)


class EstatusCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Estatus)


class VendedorCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Vendedor)


class ProductoCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Producto)


class CompraCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Compra)


class InventarioCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Inventario)


class VentaCRUD(CRUDBase):
    def __init__(self):
        super().__init__(models.Venta)


tipo_producto_crud = TipoProductoCRUD()
tienda_crud = TiendaCRUD()
estatus_crud = EstatusCRUD()
vendedor_crud = VendedorCRUD()
producto_crud = ProductoCRUD()
compra_crud = CompraCRUD()
inventario_crud = InventarioCRUD()
venta_crud = VentaCRUD()
