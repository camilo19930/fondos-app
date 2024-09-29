
from fastapi import APIRouter, Response, status, HTTPException, Depends
from schemas.user import userEntity, usersEntity
from config.db import conn
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

def get_users_db():
    return conn.bd_btg.user

@user.get('/users', tags=["users"])
def find_all_users(user_db=Depends(get_users_db)):
    try:
        return usersEntity(user_db.find())
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.post('/users',  tags=["users"])
def create_user(user: User, user_db=Depends(get_users_db)):
    try:
        new_user =  dict(user)
        # new_user["password"] = sha256_crypt.encrypt(new_user["password"] )
        del new_user["id"]
        id = user_db.insert_one(new_user).inserted_id
        user = user_db.find_one({"_id":id})
        return userEntity(user)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.get('/users/{id}', tags=["users"])
def find_user(id:str, user_db=Depends(get_users_db)):
    try:
        return userEntity(user_db.find_one({"_id": ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.put('/users/{id}', tags=["users"])
def update_user(id:str, user: User, user_db=Depends(get_users_db)):
    try:
        user_db.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(user)})
        return userEntity(user_db.find_one({"_id":ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str, user_db=Depends(get_users_db)):
    try:
        userEntity(user_db.find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})


