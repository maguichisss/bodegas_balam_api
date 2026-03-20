# Bodegas Balam API - Code Documentation

## Table of Contents

1. [Project Structure](#project-structure)
2. [app/__init__.py](#app__init__py)
3. [app/db/db.py - Database Configuration](#appdbdbpy---database-configuration)
4. [app/models/models.py - ORM Models](#appmodelsmodelspy---orm-models)
5. [app/schemas/schemas.py - Pydantic Schemas](#appschemasschemaspy---pydantic-schemas)
6. [app/crud/crud.py - Database Operations](#appcrudcrudpy---database-operations)
7. [app/routers/*.py - API Endpoints](#approuterspy---api-endpoints)
8. [app/main.py - Application Entry Point](#appmainpy---application-entry-point)
9. [Data Flow](#data-flow)

---

## Project Structure

```
app/
├── __init__.py           (empty)
├── main.py               (FastAPI application entry point)
├── crud/
│   ├── __init__.py
│   └── crud.py           (CRUD operations base class + entity-specific instances)
├── db/
│   ├── __init__.py
│   └── db.py             (Database connection & session management)
├── models/
│   ├── __init__.py
│   └── models.py         (SQLAlchemy ORM models)
├── routers/
│   ├── __init__.py
│   ├── tipos_producto.py (Router for TipoProducto endpoints)
│   ├── tiendas.py        (Router for Tienda endpoints)
│   ├── estatus.py        (Router for Estatus endpoints)
│   ├── vendedores.py     (Router for Vendedor endpoints)
│   ├── productos.py      (Router for Producto endpoints)
│   ├── compras.py        (Router for Compra endpoints)
│   ├── inventario.py     (Router for Inventario endpoints)
│   └── ventas.py         (Router for Venta endpoints)
└── schemas/
    ├── __init__.py
    └── schemas.py         (Pydantic schemas for validation)
```

---

## app/__init__.py

Placeholder file that marks `app/` as a Python package.

---

## app/db/db.py - Database Configuration

```python
from sqlalchemy import create_engine          # Creates database connection
from sqlalchemy.ext.declarative import declarative_base  # Base class for ORM models
from sqlalchemy.orm import sessionmaker       # Creates session factory
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/bodegas_balam")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

| Line | Code | Description |
|------|------|-------------|
| 6 | `DATABASE_URL` | Reads from env var; defaults to local PostgreSQL |
| 8 | `engine` | Connection pool to PostgreSQL |
| 9 | `SessionLocal` | Factory producing `Session` objects |
| 11 | `Base` | Declarative base all ORM models inherit from |

### SessionLocal

| Parameter | Value | Behavior |
|-----------|-------|---------|
| `autocommit` | `False` | Must explicitly call `.commit()` to save changes |
| `autoflush` | `False` | Changes aren't auto-flushed before queries |
| `bind` | `engine` | Uses the database connection pool |

### get_db() Dependency

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- **FastAPI dependency** that creates a new session per request
- Yields to route handler
- Closes in `finally`, ensuring cleanup even on errors

---

## app/models/models.py - ORM Models

All models inherit from `Base` (declarative base). Each has:
- `__tablename__` — actual table name in DB
- `id` — auto-incrementing primary key
- `created_at` / `updated_at` — timestamps auto-set by `func.now()`
- Relationships defined with `relationship()`

### Entities Overview

| Model | Table | Purpose |
|-------|-------|---------|
| **TipoProducto** | `tipos_producto` | Product categories (e.g., "Bebidas", "Snacks") |
| **Tienda** | `tiendas` | Store/shop names |
| **Estatus** | `estatus` | Status catalog (e.g., "Pendiente", "Completado") |
| **Vendedor** | `vendedores` | Salespeople (`unique=True` prevents duplicates) |
| **Producto** | `productos` | Products with name, presentation, alias, type FK, reference price |
| **Compra** | `compras` | Purchase orders linking product, store, status with quantity & unit price |
| **Inventario** | `inventario` | Inventory batches tracking stock from purchases |
| **Venta** | `ventas` | Sales transactions with seller commission & payment method |

### Key Column Types

| Type | Usage |
|------|-------|
| `Integer` | Primary keys, quantities |
| `String(n)` | Text fields with max length |
| `Numeric(p, s)` | Decimal numbers (precision, scale) |
| `Boolean` | True/False flags |
| `Date` | Calendar dates |
| `DateTime` | Timestamps |
| `Text` | Long text (unlimited) |
| `ForeignKey` | References other tables |

### Relationship Patterns

```python
# One-to-Many: TipoProducto → Producto
productos = relationship("Producto", back_populates="tipo")

# Many-to-One: Compra → Producto (reverse)
producto = relationship("Producto", back_populates="compras")

# One Compra → many Inventario batches
inventarios = relationship("Inventario", back_populates="compra")
```

## app/schemas/schemas.py - Pydantic Schemas

Each entity has three schema variants:

### Schema Pattern

```python
class TipoProductoBase(BaseModel):      # Fields for creation
    tipo_producto: str

class TipoProductoCreate(TipoProductoBase):  # Inherits all fields (empty body)
    pass

class TipoProductoRead(TipoProductoBase):    # Response includes id + timestamps
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}  # ORM → Pydantic conversion
```

### Schema Types

| Schema | Purpose | Fields |
|--------|---------|--------|
| **Base** | Core data fields | Just the data columns |
| **Create** | POST body | Inherits Base |
| **Read** | GET response | Base + id + timestamps + nested relationships |

### Important Configurations

#### from_attributes = True
Allows conversion from SQLAlchemy ORM objects to Pydantic models automatically.

#### Nested Relationships
```python
class CompraRead(CompraBase):
    id: int
    created_at: datetime
    updated_at: datetime
    producto: Optional[ProductoRead] = None      # Nested object
    tienda: Optional[TiendaRead] = None           # Nested object
    estatus: Optional[EstatusRead] = None         # Nested object
```

---

## app/crud/crud.py - Database Operations

### Type Variables

```python
ModelType = TypeVar("ModelType", bound=Base)           # Any SQLAlchemy model
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # Any Pydantic Create schema
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # Any Pydantic Update schema
```

Enable type-safe generic programming — `CRUDBase` works with any model/schema.

### OPERATORS Dictionary

Maps operator names to SQLAlchemy filter functions:

| Operator | SQL Equivalent | Example |
|----------|----------------|---------|
| `eq` | `==` | Exact match |
| `ne` | `!=` | Not equal |
| `gt` | `>` | Greater than |
| `gte` | `>=` | Greater than or equal |
| `lt` | `<` | Less than |
| `lte` | `<=` | Less than or equal |
| `like` | `ILIKE %value%` | Case-insensitive substring |
| `contains` | `ILIKE %value%` | Case-insensitive substring |
| `startswith` | `ILIKE value%` | Prefix match |
| `endswith` | `ILIKE %value` | Suffix match |
| `not_like` | `NOT ILIKE` | Exclusion |
| `in` | `IN (...)` | Multiple values (comma or list) |
| `not_in` | `NOT IN (...)` | Exclusion list |
| `is_null` | `IS NULL` / `IS NOT NULL` | Null check |

### CRUDBase Class Methods

| Method | Description |
|--------|-------------|
| `get(db, id)` | Fetch single record by ID |
| `get_multi(db, skip, limit, filters)` | Paginated list with simple `filter_by` |
| `get_filtered(db, skip, limit, filters)` | **Dynamic filtering** with operator support |
| `get_selected(db, skip, limit, filters, fields)` | Select specific columns, return as dicts |
| `create(db, obj_in)` | Insert new record |
| `update(db, db_obj, obj_in)` | Update existing record (partial updates via `exclude_unset=True`) |
| `remove(db, id)` | Delete record by ID |

### get_filtered() Logic

```python
def get_filtered(self, db, skip, limit, filters, fields):
    query = db.query(self.model)
    conditions = []

    if filters:
        for field, params in filters.items():      # e.g., {"precio_referencia": {"gt": 100}}
            if hasattr(self.model, field):         # Verify column exists
                column = getattr(self.model, field)  # Get SQLAlchemy column object
                for op, value in params.items():   # e.g., "gt": 100
                    if op in OPERATORS:
                        conditions.append(OPERATORS[op](column, value))  # Build filter

    if conditions:
        query = query.filter(and_(*conditions))   # AND all conditions

    return query.offset(skip).limit(limit).all()
```

---

## app/routers/*.py - API Endpoints

### Common Structure

Every router has 5 endpoints:

| Method | Path | Function | Description |
|--------|------|----------|-------------|
| `POST` | `/` | `create_*` | Create new record |
| `GET` | `/` | `read_*s` | List with filtering & pagination |
| `GET` | `/{id}` | `read_*` | Get single record |
| `PUT` | `/{id}` | `update_*` | Update existing record |
| `DELETE` | `/{id}` | `delete_*` | Remove record |

### Dependency Injection Pattern

```python
def read_tipos_producto(..., db: Session = Depends(get_db)):
```

- `Depends(get_db)` tells FastAPI to inject a database session automatically
- The session is created per request and closed after response

### Dynamic Filter Building

```python
filters: Dict[str, Dict[str, Any]] = {}

if id is not None:
    filters["id"] = {"eq": id}           # Exact match: id == value
if id__gt is not None:
    filters.setdefault("id", {})["gt"] = id__gt  # Greater than: id > value
if tipo_producto__contains is not None:
    filters.setdefault("tipo_producto", {})["contains"] = tipo_producto__contains
```

Builds a filter dictionary passed to `crud.get_filtered()`.

### Error Handling Pattern

```python
@router.get("/{id}")
def read_tipo_producto(id: int, db: Session = Depends(get_db)):
    db_tipo = crud.tipo_producto_crud.get(db, id=id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de producto not found")
    return db_tipo
```

- Fetches record by ID
- Returns **404 Not Found** if doesn't exist
- Returns the record on success

### Products Router Special Features

```python
PRODUCTO_BASICO = ["id", "producto", "presentacion"]
PRODUCTO_DETALLE = ["id", "producto", "presentacion", "alias", "id_tipo", "precio_referencia", "url_image"]
```

Supports:
- **`modo=basico`** or **`modo=detalle`** — predefined field sets
- **`campos=`** — custom comma-separated field selection
- Uses `crud.get_selected()` for column projection

---

## app/main.py - Application Entry Point

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from . import models
from .routers import tipos_producto, tiendas, estatus, vendedores, productos, compras, inventario, ventas
```

### Table Creation

```python
models.Base.metadata.create_all(bind=engine)
```

On startup, creates all database tables if they don't exist.

### FastAPI Instance

```python
app = FastAPI(redirect_slashes=False)
```

- `redirect_slashes=False` — `/tipos_producto` and `/tipos_producto/` are treated as different routes

### CORS Middleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins
    allow_credentials=True,    # Allow cookies/auth headers
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],       # Allow all headers
)
```

Enables cross-origin requests from any frontend.

### Router Registration

```python
app.include_router(tipos_producto.router, prefix="/tipos_producto", tags=["tipos_producto"])
app.include_router(tiendas.router, prefix="/tiendas", tags=["tiendas"])
app.include_router(estatus.router, prefix="/estatus", tags=["estatus"])
app.include_router(vendedores.router, prefix="/vendedores", tags=["vendedores"])
app.include_router(productos.router, prefix="/productos", tags=["productos"])
app.include_router(compras.router, prefix="/compras", tags=["compras"])
app.include_router(inventario.router, prefix="/inventario", tags=["inventario"])
app.include_router(ventas.router, prefix="/ventas", tags=["ventas"])
```

Each router is included with a prefix and tag for OpenAPI docs.

### Root Endpoint

```python
@app.get("/")
def read_root():
    return {"message": "Bodegas Balam API"}
```

Health check / welcome message endpoint.

---

## Data Flow

### Architecture Layers

```
┌─────────────────────────────────────────┐
│              HTTP Request               │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Routers (app/routers/*.py)           │
│    - Validates parameters               │
│    - Builds filter dictionaries          │
│    - Returns Pydantic responses          │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    CRUD (app/crud/crud.py)              │
│    - Executes database operations       │
│    - Builds dynamic queries              │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Models (app/models/models.py)        │
│    - SQLAlchemy ORM entities            │
│    - Relationship definitions           │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Database (PostgreSQL)                │
└─────────────────────────────────────────┘
```

### Request/Response Flow Example (POST /compras)

```
POST /compras {"id_producto": 1, "cantidad": 100, ...}
    │
    ▼
CompraCreate schema validates JSON
    │
    ▼
compra_crud.create(db, obj_in=pydantic_obj)
    │
    ▼
Creates Compra ORM object from Pydantic data
    │
    ▼
db.add() → db.commit() → db.refresh()
    │
    ▼
Returns CompraRead schema (with nested producto, tienda, estatus)
    │
    ▼
JSON response to client
```

### Database Relationships Diagram

```
┌─────────────┐       ┌─────────────┐
│TipoProducto │──1:N──│   Producto   │
└─────────────┘       └──────┬──────┘
                             │
                             │ N:1
                             ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Tienda    │──1:N──│   Compra    │──1:N──│ Inventario  │
└─────────────┘       └──────┬──────┘       └──────┬──────┘
                             │                    │
                             │ N:1                │ N:1
                             ▼                    ▼
                       ┌─────────────┐       ┌─────────────┐
                       │   Estatus   │       │    Venta    │
                       └─────────────┘       └──────┬──────┘
                                                    │
                       ┌─────────────┐              │ N:1
                       │  Vendedor   │──────────────┘
                       └─────────────┘
```

---

## API Usage Examples

### Create a Product Type
```bash
POST /tipos_producto
{"tipo_producto": "Bebidas"}
```

### List Products with Filters
```bash
GET /productos?precio_referencia__gte=100&modo=detalle
```

### Get Single Record
```bash
GET /productos/1
```

### Update a Record
```bash
PUT /tiendas/1
{"tienda": "Sucursal Norte"}
```

### Delete a Record
```bash
DELETE /estatus/3
```
