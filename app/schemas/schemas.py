from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# Base Schemas
class TipoProductoBase(BaseModel):
    tipo_producto: str

class TipoProductoCreate(TipoProductoBase):
    pass

class TipoProductoRead(TipoProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class TiendaBase(BaseModel):
    tienda: str

class TiendaCreate(TiendaBase):
    pass

class TiendaRead(TiendaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class EstatusBase(BaseModel):
    estatus: str

class EstatusCreate(EstatusBase):
    pass

class EstatusRead(EstatusBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class VendedorBase(BaseModel):
    vendedor: str

class VendedorCreate(VendedorBase):
    pass

class VendedorRead(VendedorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProductoBase(BaseModel):
    producto: str
    presentacion: Optional[str] = None
    alias: Optional[str] = None
    id_tipo: int
    precio_referencia: Optional[Decimal] = None
    url_image: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tipo: Optional[TipoProductoRead] = None

    model_config = {"from_attributes": True}

class CompraBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    id_tienda: int
    fecha_recibido: Optional[date] = None
    estatus_id: int

class CompraCreate(CompraBase):
    pass

class CompraRead(CompraBase):
    id: int
    created_at: datetime
    updated_at: datetime
    producto: Optional[ProductoRead] = None
    tienda: Optional[TiendaRead] = None
    estatus: Optional[EstatusRead] = None

    model_config = {"from_attributes": True}

class InventarioBase(BaseModel):
    id_compra: int
    stock_inicial: int
    stock_actual: int
    vendidos: Optional[int] = 0
    precio_minimo: Optional[Decimal] = None
    precio_recomendado: Optional[Decimal] = None
    activo: Optional[bool] = True

class InventarioCreate(InventarioBase):
    pass

class InventarioRead(InventarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    compra: Optional[CompraRead] = None

    model_config = {"from_attributes": True}

class VentaBase(BaseModel):
    id_inventario: int
    cantidad_vendida: int
    precio_venta: Decimal
    total_venta: Decimal
    fecha: date
    id_vendedor: int
    metodo_pago: Optional[str] = None
    comision_vendedor: Optional[Decimal] = None
    costo_unitario_lote: Optional[Decimal] = None

class VentaCreate(VentaBase):
    pass

class VentaRead(VentaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    inventario: Optional[InventarioRead] = None
    vendedor: Optional[VendedorRead] = None

    model_config = {"from_attributes": True}
