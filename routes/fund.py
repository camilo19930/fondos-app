
from fastapi import APIRouter, Response, status, HTTPException, Depends
from schemas.fund import fundEntity, fundsEntity
from config.db import conn
from models.fund import Fund
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

fund = APIRouter()

def get_finds_db():
    return conn.bd_btg.fund


@fund.get('/funds', tags=["funds"])
def find_all_funds(funds_bd=Depends(get_finds_db)):
    try:
        return fundsEntity(funds_bd.find())
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.post('/funds', tags=["funds"])
def create_fund(fund: Fund, funds_bd=Depends(get_finds_db)):
    try:
        new_fund =  dict(fund)
        del new_fund["id"]
        id = funds_bd.insert_one(new_fund).inserted_id
        fund = funds_bd.find_one({"_id":id})
        return fundEntity(fund)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.get('/funds/{id}', tags=["funds"])
def find_user(id:str, funds_bd=Depends(get_finds_db)):
    try:
        return fundEntity(funds_bd.find_one({"_id": ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.put('/funds/{id}', tags=["fund"])
def update_fund(id:str, fund: Fund, funds_bd=Depends(get_finds_db)):
    try:
        funds_bd.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(fund)})
        return fundEntity(funds_bd.find_one({"_id":ObjectId(id)}))
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})

@fund.delete('/funds/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["funds"])
def delete_user(id: str, funds_bd=Depends(get_finds_db)):
    try:
        fundEntity(funds_bd.find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as error:
        return HTTPException(status_code=500, detail={'error':str(error)})