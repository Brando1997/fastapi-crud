# API CRUD de Items con FastAPI

Este proyecto es un ejemplo educativo de una API REST para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre una lista de "items" almacenada en memoria. Está construido con FastAPI y utiliza Pydantic para la validación de datos.

## Características

- **Crear** un nuevo item.
- **Leer** la lista completa de items.
- **Leer** un item específico por su ID.
- **Actualizar** un item existente por su ID (reemplazo total con PUT).
- **Eliminar** un item por su ID.
- Documentación de API interactiva y automática (generada por Swagger UI y ReDoc).
- "Base de datos" en memoria que se reinicia cada vez que se detiene la aplicación.
- Endpoint de utilidad para cargar datos de ejemplo (`/_seed`).

## Requisitos

- Python 3.8+
- `pip` y `venv`

## Instalación y Configuración

1.  **Clona o descarga este repositorio.**

2.  **Crea y activa un entorno virtual:**

    ```bash
    # En Windows
    python -m venv .venv
    .\.venv\Scripts\Activate

    # En macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instala las dependencias:**

    Con el entorno virtual activado, ejecuta el siguiente comando para instalar FastAPI y Uvicorn (el servidor ASGI):

    ```bash
    pip install fastapi "uvicorn[standard]"
    ```

## Cómo ejecutar la aplicación

Una vez instaladas las dependencias, puedes iniciar el servidor de desarrollo con el siguiente comando:

```bash
uvicorn main:app --reload
```

-   `main`: Se refiere al archivo `main.py`.
-   `app`: Es el objeto `FastAPI` creado dentro de `main.py`.
-   `--reload`: Hace que el servidor se reinicie automáticamente cada vez que detecta un cambio en el código.

El servidor estará disponible en `http://127.0.0.1:8000`.

## Uso de la API

Una vez que el servidor esté en funcionamiento, puedes interactuar con la API:

-   **Documentación Interactiva (Swagger UI):** Abre tu navegador y ve a `http://127.0.0.1:8000/docs`. Desde esta interfaz puedes ver todos los endpoints, sus parámetros y probarlos directamente.

-   **Documentación Alternativa (ReDoc):** También puedes visitar `http://127.0.0.1:8000/redoc`.

-   **Endpoints Principales:**
    - `POST /items/`: Crea un nuevo item.
    - `GET /items/`: Obtiene todos los items.
    - `GET /items/{item_id}`: Obtiene un item por su ID.
    - `PUT /items/{item_id}`: Actualiza un item por su ID.
    - `DELETE /items/{item_id}`: Elimina un item por su ID.
