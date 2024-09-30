from fastapi import FastAPI
from config.db import conn
from routes.transaction import transaction
from routes.user import user
from routes.fund import fund
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI(
    title="REST API with FastAPI and MongoDB",
    description="This is a simple REST API using fastAPI and MongoDB",
    version="0.0.1"
)

app.include_router(transaction)
app.include_router(user)
app.include_router(fund)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aceptar solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Aceptar todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Aceptar todos los encabezados
)

handler = Mangum(app)  # Crea el handler de Mangum