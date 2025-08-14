from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 1️⃣ GET / retorna 200
def test_root():
    response = client.get("/")
    assert response.status_code == 200

# 2️⃣ POST /items/ con datos válidos
def test_create_item_valid():
    new_item = {"id": 1, "nombre": "Pan", "precio": 2.5}
    response = client.post("/items/", json=new_item)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Pan"

# 3️⃣ POST /items/ con datos inválidos (falla)
def test_create_item_invalid():
    invalid_item = {"nombre": "Leche"}  # Falta 'id' y 'precio'
    response = client.post("/items/", json=invalid_item)
    assert response.status_code == 422  # error de validación
