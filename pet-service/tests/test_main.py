from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_pets():
    response = client.get("/pets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_pet():
    response = client.post("/pets", json={
        "name": "Charlie",
        "allergies": ["Getreide"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charlie"