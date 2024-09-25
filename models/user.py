from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    name:str
    email:str
    password:str
    telefono:str
    fondo_actual:Optional[List[object]] = None
    historico:Optional[List[object]] = None
    saldo:int