import pytest
from fastapi.testclient import TestClient
from app import app
from unittest import mock
from bson import ObjectId

client = TestClient(app)

# Datos mockeados
mock_users = [
    {
        "id": "66f48e60ff4f5823b82c2c77",
        "idFondo": "66f48e60ff4f5823b82c2c77",
        "nombreFondo": "FPV_BTG_PACTUAL_RECAUDADORA",
        "fechaVinculación": "2024-09-27T14:29:18.378000",
        "monto": 75000.0,
        "estado": False,
        "montoInicial": 76000.0,
        "historicoId": "66f70755fc834575bc534143"
    },
    {
        "id": "66f4a6193c38b9fcd7a3c445",
        "idFondo": "66f4a6193c38b9fcd7a3c445",
        "nombreFondo": "DEUDAPRIVADA",
        "fechaVinculación": "2024-09-27T14:29:11.189000",
        "monto": 50000.0,
        "estado": True,
        "montoInicial": 449000.0,
        "historicoId": "66f70767fc834575bc534145"
    }
]
mock_user = {
    "_id": ObjectId("64cf8f9b6f9a4c3b52d5f9e1"),
    "name": "Camilo",
    "email": "edwinbp20@gmail.com",
    "telefono": "3117018113",
    "fondo_actual": [],
    "historico": [],
    "saldo": 5000000
}

@mock.patch("routes.user.get_users_db")  # Ajusta esta línea según la importación real
def test_find_all_users(mock_response):
    mock_response.return_value = mock_users
    mock_response = client.get("/users")
    print(mock_response)
    assert mock_response.status_code == 200
    # assert mock_response.json() == mock_users


@mock.patch("routes.user.get_users_db")  # Asegúrate de que esta ruta sea correcta
def test_create_user(mock_get_users_db):
    # Datos de entrada del nuevo usuario
    user_data = {
        "name": "Camilo",
        "email": "edwinbp20@gmail.com",
        "telefono": "3117018113",
        "fondo_actual": [],
        "historico": [],
        "password": "test",
        "saldo": 5000000  # Cambiado a un número en lugar de cadena
    }

    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_users_db.return_value = mock_db
    
    # Simulamos que insert_one() devuelve un objeto con un _id
    mock_db.insert_one.return_value.inserted_id = "64cf8f9b6f9a4c3b52d5f9e1"
    
    # Simulamos que find_one() devuelve el nuevo usuario creado
    mock_db.find_one.return_value = {
        "_id": "64cf8f9b6f9a4c3b52d5f9e1",
        "name": "Camilo",
        "email": "edwinbp20@gmail.com",
        "telefono": "3117018113",
        "fondo_actual": [],
        "historico": [],
        "password": "test",
        "saldo": 5000000  # Cambiado a número
    }

    # Llamamos al endpoint para crear el usuario
    response = client.post("/users", json=user_data)

    # Verificamos la respuesta
    assert response.status_code == 200
    
    response_data = response.json()
    
    # Verificamos campos individuales en la respuesta
    assert response_data["name"] == "Camilo"
    assert response_data["email"] == "edwinbp20@gmail.com"
    assert response_data["telefono"] == "3117018113"
    assert response_data["fondo_actual"] == []
    assert response_data["historico"] == []
    assert response_data["password"] == "test"
    assert response_data["saldo"] == 5000000  # Comparar como número
    assert "id" in response_data  # Verificamos que el campo 'id' esté presente


mock_user = {
    "_id": ObjectId("66f48e60ff4f5823b82c2c77"),
    "name": "Camilo",
    "email": "edwinbp20@gmail.com",
    "telefono": "3117018113",
    "fondo_actual": [],
    "historico": [],
    "saldo": 5000000
}

# Simulamos el comportamiento de userEntity para que devuelva lo que esperamos
def mock_user_entity(user):
    return {
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "telefono": user["telefono"],
        "fondo_actual": user["fondo_actual"],
        "historico": user["historico"],
        "saldo": user["saldo"]
    }

@mock.patch("routes.user.get_users_db")  # Asegúrate de que esta ruta sea correcta
@mock.patch("routes.user.userEntity", side_effect=mock_user_entity)  # Mockeamos userEntity
def test_find_user_success(mock_user_entity, mock_get_users_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_users_db.return_value = mock_db
    
    # Simulamos que find_one() devuelve el usuario encontrado
    mock_db.find_one.return_value = mock_user
    
    # Llamamos al endpoint para buscar el usuario
    response = client.get(f"/users/{mock_user['_id']}")  # Usamos el ID del mock_user

    # Verificamos la respuesta
    assert response.status_code == 200
    response_data = response.json()
    
    # Verificamos que los datos devueltos sean correctos
    # assert response_data["_id"] == str(mock_user["_id"])  # Asegúrate de comparar como cadenas
    # assert response_data["name"] == mock_user["name"]
    # assert response_data["email"] == mock_user["email"]
    
# @mock.patch("routes.user.get_users_db")  # Asegúrate de que esta ruta sea correcta
# def test_find_user_exception(mock_get_users_db):
#     # Creamos un mock para la base de datos
#     mock_db = mock.MagicMock()
#     mock_get_users_db.return_value = mock_db
    
#     # Simulamos que find_one() lanza una excepción
#     mock_db.find_one.side_effect = Exception("Database error")
    
#     # Llamamos al endpoint para buscar el usuario
#     response = client.get(f"/users/{ObjectId()}")
    
#     # Verificamos que la respuesta sea un error 500
#     assert response.status_code == 500
#     assert response.json() == {'detail': {'error': 'Database error'}}

@mock.patch("routes.user.get_users_db")  # Asegúrate de que esta ruta sea correcta
def test_update_user_success(mock_get_users_db):
    # Datos de entrada para actualizar el usuario
    user_data = {
        "name": "Camilo",
        "email": "camilo@example.com",
        "telefono": "3117018113",
        "fondo_actual": [],
        "historico": [],
        "saldo": 5000,
        "password": "test"
    }

    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_users_db.return_value = mock_db

    # Simulamos que find_one_and_update() y find_one() funcionan correctamente
    mock_db.find_one_and_update.return_value = None  # No necesitamos el resultado aquí
    mock_db.find_one.return_value = {
        "_id": ObjectId("66f48e60ff4f5823b82c2c77"),
        "name": "Camilo",
        "email": "camilo@example.com",
        "telefono": "3117018113",
        "fondo_actual": [],
        "historico": [],
        "saldo": 5000,
        "password": "test"
    }

    # Llamamos al endpoint para actualizar el usuario
    response = client.put(f"/users/66f88f2546522bf035c17dda", json=user_data)

    # Verificamos la respuesta
    assert response.status_code == 200
    response_data = response.json()

    # Verificamos que los datos devueltos sean correctos
    assert response_data["name"] == "Camilo"
    assert response_data["email"] == "camilo@example.com"
    assert response_data["telefono"] == "3117018113"
    assert response_data["saldo"] == 5000
    
    
# @mock.patch("routes.user.get_users_db")  # Asegúrate de que esta ruta sea correcta
# def test_update_user_exception(mock_get_users_db):
#     # Datos de entrada para actualizar el usuario
#     user_data = {
#         "name": "Camilo",
#         "email": "camilo@example.com",
#         "telefono": "3117018113",
#         "fondo_actual": [],
#         "historico": [],
#         "saldo": 5000,
#         "password": "test"
#     }

#     # Creamos un mock para la base de datos
#     mock_db = mock.MagicMock()
#     mock_get_users_db.return_value = mock_db

#     # Simulamos que find_one_and_update() lanza una excepción
#     mock_db.find_one_and_update.side_effect = Exception("Database error")

#     # Llamamos al endpoint para actualizar el usuario
#     response = client.put(f"/users/66f88ec5642e0a5ae2372e7b", json=user_data)

#     # Verificamos que la respuesta sea un error 500
#     assert response.status_code == 500
#     assert response.json() == {'detail': {'error': 'Database error'}}

@mock.patch("routes.user.get_users_db")  # Asegúrate de que esta ruta sea correcta
def test_delete_user_success(mock_get_users_db):
    # Creamos un mock para la base de datos
    mock_db = mock.MagicMock()
    mock_get_users_db.return_value = mock_db

    # Simulamos que find_one_and_delete() devuelve el usuario encontrado
    mock_db.find_one_and_delete.return_value = {
        "_id": ObjectId("66f48e60ff4f5823b82c2c77"),
        "name": "Camilo",
        "email": "camilo@example.com"
    }

    # Llamamos al endpoint para eliminar el usuario
    response = client.delete(f"/users/66f88ec5642e0a5ae2372e7b")

    # Verificamos la respuesta
    assert response.status_code == 204
    assert response.content == b''