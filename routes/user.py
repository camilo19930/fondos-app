
from fastapi import APIRouter, Response, status
from schemas.user import userEntity, usersEntity
from config.db import conn
from models.user import User
user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
def find_all_users():
    return usersEntity(conn.local.user.find())