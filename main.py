from typing import List
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="CRUD de Items en memoria",
    description=(
        "Ejemplo educativo de CRUD con FastAPI usando almacenamiento en memoria. "
        "Incluye validaciones básicas y códigos de estado adecuados."
    ),
    version="1.0.0",
)

# =============================
# 1) Modelos de datos (Pydantic)
# =============================

class Item(BaseModel):
    """Modelo completo para crear/actualizar items.

    Notas:
    - Usamos 'id' como clave única para simplificar.
    - 'nombre' no debe ser vacío.
    - 'precio' debe ser >= 0.
    """

    id: int = Field(..., ge=1, description="Identificador único (>= 1)")
    nombre: str = Field(..., min_length=1, description="Nombre del item")
    precio: float = Field(..., ge=0, description="Precio del item (>= 0)")


# =============================
# 2) "Base de datos" en memoria
# =============================
# Podríamos usar un dict {id: Item} para O(1), pero mantenemos una lista
# para hacerlo muy explícito y didáctico.
items_db: List[Item] = []


def _find_index_by_id(item_id: int) -> int:
    """Devuelve el índice del item con ese id o -1 si no existe."""
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            return idx
    return -1


# =============================
# 3) Endpoints CRUD
# =============================

# CREATE (POST)
@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Crear un nuevo item",
)
def crear_item(item: Item):
    """Crea un item nuevo si el id no existe.

    - 409 si el id ya existe (conflicto)
    """
    if _find_index_by_id(item.id) != -1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="El ID ya existe"
        )
    items_db.append(item)
    return item


# READ (GET) - todos
@app.get(
    "/items/",
    response_model=List[Item],
    tags=["items"],
    summary="Listar todos los items",
)
def obtener_items():
    return items_db


# READ (GET) - uno
@app.get(
    "/items/{item_id}",
    response_model=Item,
    tags=["items"],
    summary="Obtener un item por id",
)
def obtener_item(
    item_id: int = Path(..., ge=1, description="ID del item a buscar (>= 1)")
):
    idx = _find_index_by_id(item_id)
    if idx == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return items_db[idx]


# UPDATE (PUT) - reemplazo total
@app.put(
    "/items/{item_id}",
    response_model=Item,
    tags=["items"],
    summary="Actualizar (reemplazar) un item por id",
)
def actualizar_item(
    item_id: int = Path(..., ge=1, description="ID del item a actualizar (>= 1)"),
    item_actualizado: Item = ...,
):
    """PUT = Reemplazo total del recurso.

    Reglas que aplicamos:
    - El id del path **debe** coincidir con el id del body para evitar ambigüedad.
    - 404 si no existe.
    """
    if item_id != item_actualizado.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El id del path y del body deben coincidir",
        )

    idx = _find_index_by_id(item_id)
    if idx == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    items_db[idx] = item_actualizado
    return item_actualizado


# DELETE (DELETE)
@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["items"],
    summary="Eliminar un item por id",
)
def eliminar_item(
    item_id: int = Path(..., ge=1, description="ID del item a eliminar (>= 1)")
):
    idx = _find_index_by_id(item_id)
    if idx == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    # Eliminar y devolver 204 (sin cuerpo)
    del items_db[idx]
    return None


# (Opcional) Semilla de datos para probar más fácil
@app.post(
    "/_seed",
    tags=["utils"],
    summary="Cargar datos de ejemplo en memoria",
)
def seed_data():
    items_db.clear()
    items_db.extend(
        [
            Item(id=1, nombre="Pan", precio=2.5),
            Item(id=2, nombre="Leche", precio=7.0),
            Item(id=3, nombre="Huevos", precio=12.0),
        ]
    )
    return {"mensaje": "Datos de ejemplo cargados", "total": len(items_db)}