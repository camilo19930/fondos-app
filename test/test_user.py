import pytest
from fastapi.testclient import TestClient
from app import app  # Ajusta esta línea si es necesario
from unittest.mock import patch
from models.user import User
from bson import ObjectId
from unittest.mock import MagicMock

client = TestClient(app)

# Datos de prueba
mock_user_data = {
    "name": "John",
    "email": "john.doe@example.com",
    "password": "test1234",
    "telefono": "3111234567",
    "saldo": 1213
}

@pytest.fixture
def mock_db(mocker):
    # Mockea la colección de usuarios
    mock_collection = mocker.patch("config.db.conn.local.user")
    yield mock_collection

def test_create_user(mock_db):
    # Configura el mock para que devuelva un ID de usuario simulado
    mock_db.insert_one.return_value.inserted_id = ObjectId("60c72b2f4f1a2c001c8f4e69")
    mock_db.find_one.return_value = {
        "_id": ObjectId("60c72b2f4f1a2c001c8f4e69"),
        "name": "John",
        "email": "john.doe@example.com",
        "telefono": "3111234567"
    }
    
    response = client.post("/users", json=mock_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == mock_user_data["name"]
    assert data["email"] == mock_user_data["email"]
    assert "id" in data

def test_get_all_users(mock_db):
    # Configura el mock para que devuelva una lista de usuarios
    mock_db.find.return_value = [
        {"_id": ObjectId("60c72b2f4f1a2c001c8f4e69"), "name": "John"},
        {"_id": ObjectId("60c72b2f4f1a2c001c8f4e70"), "name": "Jane"},
    ]
    
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
