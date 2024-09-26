from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    id: Optional[str] = None
    name:str
    category:str
    minimum_amount:float
    
class FondoCancelacion(BaseModel):
    idFondo: str