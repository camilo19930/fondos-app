import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from models.transaction import Transaction
from models.user import User
from models.fund import Fund
from schemas.transaction import transactionEntity, transactionsEntity
from schemas.fund import fundEntity, fundsEntity
from bson import ObjectId
from datetime import datetime
from models.transaction import FondoCancelacion
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

transaction = APIRouter()
# Endpoint para actualizar el fondo actual y agregar al histórico
@transaction.put("/transaction/fondo_actual/{id_usuario}")
async def actualizar_fondo_actual(id_usuario: str, fondo: Fund):
    # Convertir el id de usuario a ObjectId si es necesario
    if not ObjectId.is_valid(id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")
    
    # Buscar el usuario por id
    usuario = conn.local.user.find_one({"_id": ObjectId(id_usuario)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar si el saldo del usuario es suficiente
    if float(fondo.initial_amount) < float(fondo.minimum_amount) or float(usuario['saldo']) < float(fondo.initial_amount):
        raise HTTPException(status_code=400, detail="El saldo del cliente es menor que el saldo mínimo del fondo")
    
    nuevo_saldo = float(usuario['saldo']) - float(fondo.initial_amount)
    
    # Actualizar el saldo del usuario
    conn.local.user.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$set": {"saldo": nuevo_saldo}}  # Actualizar el campo saldo con el nuevo valor
    )
    
    # Preparar el nuevo fondo_actual
    nuevo_fondo_actual = {
        "idFondo": fondo.id,  # Mantiene el ID existente del fondo
        "nombreFondo": fondo.name,
        "fechaVinculación": datetime.now(),
        "monto": fondo.minimum_amount,
        "estado": True,
        "montoInicial": fondo.initial_amount,
        "historicoId": str(ObjectId())  # Generar un nuevo ID único para el histórico
    }
    
    # Actualizar el fondo_actual
    conn.local.user.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"fondo_actual": nuevo_fondo_actual}}  # Agregar al array de fondo_actual
    )
    
    # Insertar el item en el array de historico
    conn.local.user.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"historico": nuevo_fondo_actual}}  # Agregar al array de histórico
    )
    
    enviar_correo(usuario['email'], 'ejecución exitosa', 'Mensaje de exito')
    return {"mensaje": "Fondo actual y histórico actualizados exitosamente"}


# Endpoint para cambiar el estado del fondo a False y moverlo a histórico
@transaction.put("/transaction/cancelar_fondo/{id_usuario}")
async def cancelar_fondo(id_usuario: str, fondo_data: FondoCancelacion):
    # Verificar si el ID de usuario es válido
    if not ObjectId.is_valid(id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")

    # Buscar el usuario por ID
    usuario = conn.local.user.find_one({"_id": ObjectId(id_usuario)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Buscar el fondo en fondo_actual que coincida con el idFondo y aún no esté cancelado
    fondo_a_cancelar = None
    for fondo in usuario.get("fondo_actual", []):
        if fondo["idFondo"] == fondo_data.idFondo and fondo.get("estado", True):
            fondo_a_cancelar = fondo
            break
    
    if not fondo_a_cancelar:
        raise HTTPException(status_code=404, detail="Fondo no encontrado o ya cancelado")

    # Cambiar el estado del fondo a False
    fondo_a_cancelar["estado"] = False
    saldo = float(usuario['saldo']) + float(fondo_a_cancelar["monto"])
    print(saldo)
    # Eliminar el fondo específico de fondo_actual
    conn.local.user.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$pull": {"fondo_actual": {"idFondo": fondo_data.idFondo}},"$set": {"saldo": saldo}}
    )

    # Agregar el fondo modificado al array de histórico
    conn.local.user.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"historico": fondo_a_cancelar}}
    )

    return {"mensaje": "Fondo cancelado y movido a histórico exitosamente"}



def enviar_correo(destinatario: str, asunto: str, mensaje: str):    
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"  # Cambia esto si usas otro proveedor
    smtp_port = 465  # El puerto para TLS
    remitente = os.getenv('EMAIL_ADMIN')  # Cambia esto a tu correo
    contrasena = os.getenv('PASSWORD_ADMIN')  # Cambia esto a tu contraseña

    # Crear el objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Adjuntar el mensaje
    msg.attach(MIMEText(mensaje, 'plain'))
    try:
        # Conectar al servidor SMTP
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # server.starttls()  # Iniciar la conexión TLS
            server.login(remitente, contrasena)  # Iniciar sesión
            data = server.send_message(msg)  # Enviar el correo
        print(f"Correo enviado a {destinatario} con éxito.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")