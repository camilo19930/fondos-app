import pytest
from fastapi.testclient import TestClient
from app import app
from unittest import mock
from bson import ObjectId

client = TestClient(app)

# Datos mockeados
mock_funds = [
    {"_id": "1", "name": "Fondo A", "amount": 10000},
    {"_id": "2", "name": "Fondo B", "amount": 20000},
]
mock_fund_data = {
    "_id": "64cf8f9b6f9a4c3b52d5f9e1",
    "name": "FPV_BTG_PACTUAL_DINAMICA testtsss",
    "category": "FPV",
    "minimum_amount": 100000,
    "initial_amount": 1000000
}
mock_created_fund = {
    "id": "64cf8f9b6f9a4c3b52d5f9e1",
    "name": "FPV_BTG_PACTUAL_DINAMICA testtsss",
    "category": "FPV",
    "minimum_amount": 100000.0
}
mock_fund = {
    "id": ObjectId("66f89e625c6dd828ab2e3067"),
    "name": "FPV_BTG_PACTUAL_DINAMICA",
    "category": "FPV",
    "minimum_amount": 100000.0
}


@mock.patch("routes.fund.get_finds_db")  # Asegúrate de que esta ruta sea correcta
def test_find_all_funds_success(mock_get_funds_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_funds_db.return_value = mock_db
    
    # Simulamos que find() devuelve una lista de fondos
    mock_db.find.return_value = mock_funds

    # Llamamos al endpoint para obtener todos los fondos
    response = client.get("/funds")

    # Verificamos la respuesta
    assert response.status_code == 200
    # assert response.json() == mock_funds

@mock.patch("routes.fund.get_finds_db")  # Asegúrate de que esta ruta sea correcta
def test_create_fund_success(mock_get_funds_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_funds_db.return_value = mock_db

    # Simulamos que insert_one() devuelve un objeto con un _id
    mock_db.insert_one.return_value.inserted_id = "64cf8f9b6f9a4c3b52d5f9e1"

    # Simulamos que find_one() devuelve el nuevo fondo creado
    mock_db.find_one.return_value = mock_created_fund

    # Llamamos al endpoint para crear el fondo
    response = client.post("/funds", json=mock_fund_data)
    response_data = response.json()
    # Verificamos la respuesta
    assert response.status_code == 200
    assert response_data["category"] == "FPV"
    
    
@mock.patch("routes.fund.get_finds_db")  # Asegúrate de que esta ruta sea correcta
def test_find_fund_success(mock_get_funds_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_funds_db.return_value = mock_db
    
    # Simulamos que find_one() devuelve el fondo encontrado
    mock_db.find_one.return_value = mock_fund
    
    # Llamamos al endpoint para buscar el fondo
    response = client.get(f"/funds/66f48e60ff4f5823b82c2c77")

    # Verificamos la respuesta
    assert response.status_code == 200
    response_data = response.json()

    # Verificamos que los datos devueltos sean correctos
    assert response_data["name"] == mock_fund["name"]
    
@mock.patch("routes.fund.get_finds_db")  # Asegúrate de que esta ruta sea correcta
def test_update_fund_success(mock_get_funds_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_funds_db.return_value = mock_db
    
    # Simulamos que find_one_and_update() no lanza excepciones
    mock_db.find_one_and_update.return_value = mock_fund
    
    # Simulamos que find_one() devuelve el fondo actualizado
    mock_db.find_one.return_value = {
        "_id": ObjectId("64cf8f9b6f9a4c3b52d5f9e1"),
        "name": "FPV_BTG_PACTUAL_DINAMICA",
        "category": "FPV",
        "minimum_amount": 75000,
        "initial_amount": 76000
    }
    updated_fund_data = {
    "name": "FPV_BTG_PACTUAL_DINAMICA",
    "category": "FPV",
    "minimum_amount": 75000,
    "initial_amount": 76000
}
    # Llamamos al endpoint para actualizar el fondo
    response = client.put(f"/funds/66f48e60ff4f5823b82c2c77", json=updated_fund_data)

    # Verificamos la respuesta
    assert response.status_code == 200
    response_data = response.json()

    # Verificamos que los datos devueltos sean correctos
    # assert response_data["_id"] == str(mock_fund["_id"])  # Convertimos ObjectId a string
    assert response_data["name"] == updated_fund_data["name"]
    assert response_data["minimum_amount"] == updated_fund_data["minimum_amount"]
    
    
@mock.patch("routes.fund.get_finds_db")  # Asegúrate de que esta ruta sea correcta
def test_delete_fund_success(mock_get_users_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_users_db.return_value = mock_db
    
    # Simulamos que find_one_and_delete() no lanza excepciones y devuelve el fondo eliminado
    mock_db.find_one_and_delete.return_value = mock_fund

    # Llamamos al endpoint para eliminar el fondo
    response = client.delete(f"/funds/66f8a0c377f6c573e54662f5")

    # Verificamos la respuesta
    assert response.status_code == 204  # Verificamos que el código de estado sea 204 No Content
