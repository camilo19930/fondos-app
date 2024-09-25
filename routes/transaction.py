from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from models.transaction import Transaction
from models.user import User
from models.fund import Fund
from schemas.transaction import transactionEntity, transactionsEntity
from schemas.fund import fundEntity, fundsEntity
from bson import ObjectId
from datetime import datetime

transaction = APIRouter()

@transaction.get('/transaction')
def find_all_transaction():
    return transactionsEntity(conn.local.fondos.find())

# # Endpoint para actualizar el fondo actual y registrar el histórico
# @transaction.put("/transaction/{id_usuario}/fondo_actual")
# async def actualizar_fondo_actual2(id_usuario: str, fondo: Fund):
#     # Convertir el id de usuario a ObjectId si es necesario
#     if not ObjectId.is_valid(id_usuario):
#         raise HTTPException(status_code=400, detail="ID de usuario no válido")
    
#     # Buscar el usuario por id
#     usuario = conn.local.user.find_one({"_id": ObjectId(id_usuario)})
#     if not usuario:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
#     # Verificar si el usuario tiene un fondo_actual registrado
#     if "fondo_actual" in usuario and usuario["fondo_actual"]:
#         # Guardar el fondo actual en el histórico antes de actualizar
#         historico = {
#             "idFondo": usuario["fondo_actual"].get("idFondo", ""),
#             "nombreFondo": usuario["fondo_actual"].get("nombreFondo", ""),
#             "fechaVinculación": usuario["fondo_actual"].get("fechaVinculación", ""),
#             "monto": usuario["fondo_actual"].get("monto", 0)
#         }
        
#         # Actualizar el campo historico del usuario
#         conn.local.user.update_one(
#             {"_id": ObjectId(id_usuario)},
#             {"$set": {"historico": historico}}
#         )

#     # Actualizar el campo fondo_actual del usuario con el nuevo fondo
#     fondo_actualizado = {
#         "idFondo": str(ObjectId()),  # Puedes generar un ID único si lo necesitas
#         "nombreFondo": fondo.name,
#         "fechaVinculación": datetime.now(),
#         "monto": fondo.minimun_amount
#     }

#     # Actualizar el usuario en la base de datos
#     conn.local.user.update_one(
#         {"_id": ObjectId(id_usuario)},
#         {"$set": {"fondo_actual": fondo_actualizado}}
#     )

#     return {"mensaje": "Fondo actual y histórico actualizados exitosamente"}


# Endpoint para actualizar el fondo actual y agregar al histórico
@transaction.put("/transaction/{id_usuario}/fondo_actual")
async def actualizar_fondo_actual(id_usuario: str, fondo: Fund):
    # Convertir el id de usuario a ObjectId si es necesario
    if not ObjectId.is_valid(id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")
    
    # Buscar el usuario por id
    usuario = conn.local.user.find_one({"_id": ObjectId(id_usuario)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if int(usuario['saldo']) < int(fondo.minimun_amount):
        raise HTTPException(status_code=400, detail="El saldo del cliente es menor que el saldo minímo del fondo")

    # Preparar el nuevo fondo_actual
    nuevo_fondo_actual = {
        "idFondo": fondo.id,  # Generar un ID único para el fondo
        "nombreFondo": fondo.name,
        "fechaVinculación": datetime.now(),
        "monto": fondo.minimun_amount
    }

    # Si existe un fondo_actual, mover el último fondo al histórico
    if "fondo_actual" in usuario and usuario["fondo_actual"]:
        ultimo_fondo = usuario["fondo_actual"][-1]  # Obtener el último fondo actual
        historico_item = {
            "idFondo": ultimo_fondo.get("idFondo", ""),
            "nombreFondo": ultimo_fondo.get("nombreFondo", ""),
            "fechaVinculación": ultimo_fondo.get("fechaVinculación", ""),
            "monto": ultimo_fondo.get("monto", 0)
        }
        
        # Insertar el item en el array de historico
        conn.local.user.update_one(
            {"_id": ObjectId(id_usuario)},
            {"$push": {"historico": historico_item}}  # Agregar al array de histórico
        )

    # Agregar el nuevo fondo al array fondo_actual
    conn.local.user.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"fondo_actual": nuevo_fondo_actual}}  # Agregar al array de fondo_actual
    )

    return {"mensaje": "Fondo actual y histórico actualizados exitosamente"}