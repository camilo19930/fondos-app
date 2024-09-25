from fastapi import FastAPI
from config.db import conn
from routes.transaction import transaction
from routes.user import user

app = FastAPI(
    title="REST API with FastAPI and MongoDB",
    description="This is a simple REST API using fastAPI and MongoDB",
    version="0.0.1"
)

app.include_router(transaction)
app.include_router(user)