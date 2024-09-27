
from fastapi import APIRouter, Response, status, HTTPException
from schemas.fund import fundEntity, fundsEntity
from config.db import conn
from models.fund import Fund
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

fund = APIRouter()

@fund.get('/funds', tags=["funds"])
def find_all_funds():
    try:
        return fundsEntity(conn.local.fund.find())
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.post('/funds', tags=["funds"])
def create_fund(fund: Fund):
    try:
        new_fund =  dict(fund)
        del new_fund["id"]
        id = conn.local.fund.insert_one(new_fund).inserted_id
        fund = conn.local.fund.find_one({"_id":id})
        return fundEntity(fund)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.get('/funds/{id}', tags=["funds"])
def find_user(id:str):
    try:
        return fundEntity(conn.local.fund.find_one({"_id": ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.put('/funds/{id}', tags=["fund"])
def update_user(id:str, fund: Fund):
    try:
        conn.local.fund.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(fund)})
        return fundEntity(conn.local.fund.find_one({"_id":ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.delete('/funds/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["funds"])
def delete_user(id: str):
    try:
        fundEntity(conn.local.fund.find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})