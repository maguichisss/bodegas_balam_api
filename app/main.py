from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from . import models
from .routers import tipos_producto, tiendas, estatus, vendedores, productos, compras, inventario, ventas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tipos_producto.router, prefix="/tipos_producto", tags=["tipos_producto"])
app.include_router(tiendas.router, prefix="/tiendas", tags=["tiendas"])
app.include_router(estatus.router, prefix="/estatus", tags=["estatus"])
app.include_router(vendedores.router, prefix="/vendedores", tags=["vendedores"])
app.include_router(productos.router, prefix="/productos", tags=["productos"])
app.include_router(compras.router, prefix="/compras", tags=["compras"])
app.include_router(inventario.router, prefix="/inventario", tags=["inventario"])
app.include_router(ventas.router, prefix="/ventas", tags=["ventas"])

@app.get("/")
def read_root():
    return {"message": "Bodegas Balam API"}
