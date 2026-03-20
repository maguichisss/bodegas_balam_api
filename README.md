# Bodegas Balam API

FastAPI REST API para gestion de inventarios y ventas de bebidas.

## Endpoints

| Metodo | Endpoint | Descripcion |
|--------|---------|-------------|
| GET | `/tipos_producto/` | Listar tipos de producto |
| POST | `/tipos_producto/` | Crear tipo de producto |
| GET | `/tipos_producto/{id}` | Obtener tipo de producto |
| PUT | `/tipos_producto/{id}` | Actualizar tipo de producto |
| DELETE | `/tipos_producto/{id}` | Eliminar tipo de producto |
| GET | `/tiendas/` | Listar tiendas |
| POST | `/tiendas/` | Crear tienda |
| GET | `/tiendas/{id}` | Obtener tienda |
| PUT | `/tiendas/{id}` | Actualizar tienda |
| DELETE | `/tiendas/{id}` | Eliminar tienda |
| GET | `/estatus/` | Listar estatus |
| POST | `/estatus/` | Crear estatus |
| GET | `/estatus/{id}` | Obtener estatus |
| PUT | `/estatus/{id}` | Actualizar estatus |
| DELETE | `/estatus/{id}` | Eliminar estatus |
| GET | `/vendedores/` | Listar vendedores |
| POST | `/vendedores/` | Crear vendedor |
| GET | `/vendedores/{id}` | Obtener vendedor |
| PUT | `/vendedores/{id}` | Actualizar vendedor |
| DELETE | `/vendedores/{id}` | Eliminar vendedor |
| GET | `/productos/` | Listar productos |
| POST | `/productos/` | Crear producto |
| GET | `/productos/{id}` | Obtener producto |
| PUT | `/productos/{id}` | Actualizar producto |
| DELETE | `/productos/{id}` | Eliminar producto |
| GET | `/compras/` | Listar compras |
| POST | `/compras/` | Crear compra |
| GET | `/compras/{id}` | Obtener compra |
| PUT | `/compras/{id}` | Actualizar compra |
| DELETE | `/compras/{id}` | Eliminar compra |
| GET | `/inventario/` | Listar inventario |
| POST | `/inventario/` | Crear inventario |
| GET | `/inventario/{id}` | Obtener inventario |
| PUT | `/inventario/{id}` | Actualizar inventario |
| DELETE | `/inventario/{id}` | Eliminar inventario |
| GET | `/ventas/` | Listar ventas |
| POST | `/ventas/` | Crear venta |
| GET | `/ventas/{id}` | Obtener venta |
| PUT | `/ventas/{id}` | Actualizar venta |
| DELETE | `/ventas/{id}` | Eliminar venta |

## Filtros Query Parameters

Todos los endpoints GET soportan los siguientes query parameters:

### Paginacion

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Numero de registros a omitir |
| `limit` | int | 100 | Limite de registros a retornar |

### Operadores de Filtro

| Operador | Descripcion | Ejemplo |
|----------|-------------|---------|
| `__eq` | Igual (default) | `?producto=tequila` |
| `__ne` | Diferente | `?estatus__ne=pendiente` |
| `__gt` | Mayor que | `?precio__gt=100` |
| `__gte` | Mayor o igual | `?stock__gte=10` |
| `__lt` | Menor que | `?stock__lt=5` |
| `__lte` | Menor o igual | `?precio__lte=50` |
| `__like` | LIKE (case-insensitive) | `?producto__like=cuervo` |
| `__contains` | Contains (case-insensitive) | `?producto__contains=tequila` |
| `__startswith` | Comienza con | `?producto__startswith=jose` |
| `__endswith` | Termina con | `?producto__endswith=ml` |
| `__not_like` | NOT LIKE | `?producto__not_like=generico` |
| `__in` | IN (comma-separated) | `?id__in=1,2,3` |
| `__not_in` | NOT IN | `?id__not_in=4,5,6` |
| `__is_null` | IS NULL | `?alias__is_null=true` |

### Seleccion de Campos

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `modo` | string | Modo predefinido: `basico`, `detallado` |
| `campos` | string | Campos a retornar (comma-separated) |

**Modos disponibles:**

| Modo | Campos incluidos |
|------|-----------------|
| `basico` | id, campo_principal |
| `detallado` | id, campo_principal, campos_adicionales |

**Ejemplos:**

```bash
# Respuesta basica
GET /productos/?modo=basico

# Respuesta con mas campos
GET /productos/?modo=detallado

# Seleccionar campos especificos
GET /productos/?campos=id,producto,precio_referencia

# Combinar con filtros
GET /productos/?modo=basico&precio_referencia__gt=100

# Seleccionar campos con filtros
GET /productos/?campos=id,producto,presentacion&producto__like=cuervo
```

## Configuracion

Variables de entorno:

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://postgres:password@localhost/bodegas_balam` | URL de conexion a PostgreSQL |

## Ejemplos con curl

### Tipos de Producto

```bash
# Listar todos los tipos de producto
curl -X GET "http://localhost:9000/tipos_producto/"

# Crear tipo de producto
curl -X POST "http://localhost:9000/tipos_producto/" \
  -H "Content-Type: application/json" \
  -d '{"tipo_producto": "ron"}'

# Obtener tipo de producto por ID
curl -X GET "http://localhost:9000/tipos_producto/1"

# Actualizar tipo de producto
curl -X PUT "http://localhost:9000/tipos_producto/1" \
  -H "Content-Type: application/json" \
  -d '{"tipo_producto": "whisky premium"}'

# Eliminar tipo de producto
curl -X DELETE "http://localhost:9000/tipos_producto/1"
```

### Tiendas

```bash
# Listar tiendas
curl -X GET "http://localhost:9000/tiendas/"

# Crear tienda
curl -X POST "http://localhost:9000/tiendas/" \
  -H "Content-Type: application/json" \
  -d '{"tienda": "Bodega Centro"}'
```

### Vendedores

```bash
# Listar vendedores activos
curl -X GET "http://localhost:9000/vendedores/?vendedor__contains=mau"

# Crear vendedor
curl -X POST "http://localhost:9000/vendedores/" \
  -H "Content-Type: application/json" \
  -d '{"vendedor": "JUAN"}'
```

### Productos

```bash
# Listar todos los productos
curl -X GET "http://localhost:9000/productos/"

# Modo basico (solo campos esenciales)
curl -X GET "http://localhost:9000/productos/?modo=basico"

# Modo detallado (mas campos)
curl -X GET "http://localhost:9000/productos/?modo=detallado"

# Seleccionar campos especificos
curl -X GET "http://localhost:9000/productos/?campos=id,producto,precio_referencia"

# Buscar producto por nombre (LIKE case-insensitive)
curl -X GET "http://localhost:9000/productos/?producto__like=cuervo"

# Productos que comienzan con "jose"
curl -X GET "http://localhost:9000/productos/?producto__startswith=jose"

# Productos que terminan con "ml"
curl -X GET "http://localhost:9000/productos/?producto__endswith=ml"

# Productos con precio mayor a 100
curl -X GET "http://localhost:9000/productos/?precio_referencia__gt=100"

# Productos sin alias (IS NULL)
curl -X GET "http://localhost:9000/productos/?alias__is_null=true"

# Combinacion de filtros
curl -X GET "http://localhost:9000/productos/?id_tipo=1&precio_referencia__gte=50&producto__contains=reposado"

# Modo basico + filtro
curl -X GET "http://localhost:9000/productos/?modo=basico&precio_referencia__gt=100"

# Campos especificos + filtro
curl -X GET "http://localhost:9000/productos/?campos=id,producto,presentacion&producto__like=cuervo"

# Crear producto
curl -X POST "http://localhost:9000/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "producto": "Herradura Plata - 750ml",
    "presentacion": "750ml",
    "id_tipo": 1,
    "precio_referencia": 450.00
  }'
```

### Inventario

```bash
# Listar inventario
curl -X GET "http://localhost:9000/inventario/"

# Inventario con stock bajo
curl -X GET "http://localhost:9000/inventario/?stock_actual__lt=10"

# Inventario activo de un producto especifico
curl -X GET "http://localhost:9000/inventario/?id_compra=5&activo=true"

# Inventario con IDs en lista
curl -X GET "http://localhost:9000/inventario/?id__in=1,2,3"

# Crear registro de inventario
curl -X POST "http://localhost:9000/inventario/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_compra": 1,
    "stock_inicial": 12,
    "stock_actual": 12,
    "precio_minimo": 80.00,
    "precio_recomendado": 100.00
  }'
```

### Ventas

```bash
# Listar ventas
curl -X GET "http://localhost:9000/ventas/"

# Ventas con precio mayor a 100
curl -X GET "http://localhost:9000/ventas/?precio_venta__gt=100"

# Ventas por rango de precio
curl -X GET "http://localhost:9000/ventas/?precio_venta__gte=100&precio_venta__lte=500"

# Ventas por vendedor
curl -X GET "http://localhost:9000/ventas/?id_vendedor=1"

# Ventas con pago en efectivo
curl -X GET "http://localhost:9000/ventas/?metodo_pago=efectivo"

# Crear venta
curl -X POST "http://localhost:9000/ventas/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_inventario": 1,
    "cantidad_vendida": 2,
    "precio_venta": 95.00,
    "total_venta": 190.00,
    "fecha": "2026-03-19",
    "id_vendedor": 1,
    "metodo_pago": "efectivo"
  }'
```

## Configuracion

```bash
docker compose up --build
```
