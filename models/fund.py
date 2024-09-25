from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Fund(BaseModel):
    id: Optional[str] = None
    name:str
    category:str
    minimun_amount: int

class FondoActual(BaseModel):
    idFondo: Optional[str] = None
    nombreFondo: Optional[str] = None
    fechaVinculación: Optional[datetime] = None
    monto: float = 0