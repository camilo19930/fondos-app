
from fastapi import APIRouter, Response, status, HTTPException
from schemas.user import userEntity, usersEntity
from config.db import conn
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', tags=["users"])
def find_all_users():
    try:
        return usersEntity(conn.bd_btg.user.find())
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.post('/users',  tags=["users"])
def create_user(user: User):
    try:
        new_user =  dict(user)
        # new_user["password"] = sha256_crypt.encrypt(new_user["password"] )
        del new_user["id"]
        id = conn.bd_btg.user.insert_one(new_user).inserted_id
        user = conn.bd_btg.user.find_one({"_id":id})
        return userEntity(user)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.get('/users/{id}', tags=["users"])
def find_user(id:str):
    try:
        return userEntity(conn.bd_btg.user.find_one({"_id": ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.put('/users/{id}', tags=["users"])
def update_user(id:str, user: User):
    try:
        conn.bd_btg.user.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(user)})
        return userEntity(conn.bd_btg.user.find_one({"_id":ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    try:
        userEntity(conn.bd_btg.user.find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})
