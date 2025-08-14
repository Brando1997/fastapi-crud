from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    new_item = {"id": 10, "name": "Pan", "price": 5.0}
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    assert response.json()["name"] == "Pan"

def test_create_item_missing_data():
    incomplete_item = {"name": "Leche"}  # Falta 'id' y 'price'
    response = client.post("/items", json=incomplete_item)
    assert response.status_code == 422  # Código de error de validación de FastAPI

