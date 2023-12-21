from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from src.users.schemas import UserViewSchemas

class OrdersCreateSchemas(BaseModel):
    address: str

class OrderViewSchemas(BaseModel):
    id:int 
    creator: int
    created_at: datetime|None = None
    updated_at: datetime|None = None
    address: str

    class Config:
        orm_mode = True
    




