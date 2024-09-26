from fastapi import FastAPI
from config.db import conn
from routes.transaction import transaction
from routes.user import user
from routes.fund import fund
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="REST API with FastAPI and MongoDB",
    description="This is a simple REST API using fastAPI and MongoDB",
    version="0.0.1"
)

app.include_router(transaction)
app.include_router(user)
app.include_router(fund)

origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)