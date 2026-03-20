from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class TipoProducto(Base):
    __tablename__ = "tipos_producto"
    id = Column(Integer, primary_key=True, index=True)
    tipo_producto = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    productos = relationship("Producto", back_populates="tipo")

class Tienda(Base):
    __tablename__ = "tiendas"
    id = Column(Integer, primary_key=True, index=True)
    tienda = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    compras = relationship("Compra", back_populates="tienda")

class Estatus(Base):
    __tablename__ = "estatus"
    id = Column(Integer, primary_key=True, index=True)
    estatus = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    compras = relationship("Compra", back_populates="estatus")

class Vendedor(Base):
    __tablename__ = "vendedores"
    id = Column(Integer, primary_key=True, index=True)
    vendedor = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ventas = relationship("Venta", back_populates="vendedor")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(255), nullable=False)
    presentacion = Column(String(20))
    alias = Column(String(30))
    id_tipo = Column(Integer, ForeignKey("tipos_producto.id"))
    precio_referencia = Column(Numeric(10, 2))
    url_image = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tipo = relationship("TipoProducto", back_populates="productos")
    compras = relationship("Compra", back_populates="producto")

class Compra(Base):
    __tablename__ = "compras"
    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    id_tienda = Column(Integer, ForeignKey("tiendas.id"))
    fecha_recibido = Column(Date)
    estatus_id = Column(Integer, ForeignKey("estatus.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    producto = relationship("Producto", back_populates="compras")
    tienda = relationship("Tienda", back_populates="compras")
    estatus = relationship("Estatus", back_populates="compras")
    inventarios = relationship("Inventario", back_populates="compra")

class Inventario(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, index=True)
    id_compra = Column(Integer, ForeignKey("compras.id"))
    stock_inicial = Column(Integer, nullable=False)
    stock_actual = Column(Integer, nullable=False)
    vendidos = Column(Integer, default=0)
    precio_minimo = Column(Numeric(10, 2))
    precio_recomendado = Column(Numeric(10, 2))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    compra = relationship("Compra", back_populates="inventarios")
    ventas = relationship("Venta", back_populates="inventario")

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    id_inventario = Column(Integer, ForeignKey("inventario.id"))
    cantidad_vendida = Column(Integer, nullable=False)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    total_venta = Column(Numeric(10, 2), nullable=False)
    fecha = Column(Date, nullable=False)
    id_vendedor = Column(Integer, ForeignKey("vendedores.id"))
    metodo_pago = Column(String(50))
    comision_vendedor = Column(Numeric(10, 2))
    costo_unitario_lote = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    inventario = relationship("Inventario", back_populates="ventas")
    vendedor = relationship("Vendedor", back_populates="ventas")
