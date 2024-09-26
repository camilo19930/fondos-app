import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app  # Asegúrate de que este es el nombre correcto del archivo principal

client = TestClient(app)

@pytest.fixture
def mock_fund_data():
    return {
        "id": "66f48e60ff4f5823b82c2c77",
        "name": "Fund Test",
        "minimum_amount": 1000.0,
        "description": "This is a test fund"
    }

# Test para obtener todos los fondos
def test_find_all_funds(mock_fund_data):
    with patch('config.db.conn.local.fund.find', return_value=[mock_fund_data()]):
        response = client.get("/funds")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Fund Test"

# Test para crear un fondo
def test_create_fund(mock_fund_data):
    with patch('config.db.conn.local.fund.insert_one') as mock_insert:
        mock_insert.return_value.inserted_id = "1"
        with patch('config.db.conn.local.fund.find_one') as mock_find_one:
            mock_find_one.return_value = {**mock_fund_data(), "_id": "1"}
            response = client.post("/funds", json=mock_fund_data())
            assert response.status_code == 200
            assert response.json()["name"] == "Fund Test"

# # Test para obtener un fondo por ID
# def test_find_fund(mock_fund_data):
#     fund_id = "1"
#     with patch('config.db.conn.local.fund.find_one') as mock_find_one:
#         mock_find_one.return_value = {**mock_fund_data(), "_id": fund_id}
#         response = client.get(f"/funds/{fund_id}")
#         assert response.status_code == 200
#         assert response.json()["name"] == "Fund Test"

# # Test para actualizar un fondo
# def test_update_fund(mock_fund_data):
#     fund_id = "1"
#     updated_data = {**mock_fund_data(), "name": "Updated Fund"}
#     with patch('config.db.conn.local.fund.find_one_and_update') as mock_update:
#         with patch('config.db.conn.local.fund.find_one') as mock_find_one:
#             mock_find_one.return_value = {**updated_data, "_id": fund_id}
#             response = client.put(f"/funds/{fund_id}", json=updated_data)
#             assert response.status_code == 200
#             assert response.json()["name"] == "Updated Fund"

# # Test para eliminar un fondo
# def test_delete_fund(mock_fund_data):
#     fund_id = "1"
#     with patch('config.db.conn.local.fund.find_one_and_delete') as mock_delete:
#         mock_delete.return_value = {**mock_fund_data(), "_id": fund_id}
#         response = client.delete(f"/funds/{fund_id}")
#         assert response.status_code == 204
