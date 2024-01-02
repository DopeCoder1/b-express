from typing import Optional
from pydantic import BaseModel, EmailStr

class UserSchemas(BaseModel):
    email: EmailStr
    password: str

class UserViewSchemas(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool
    is_active: bool
    is_delete: bool
    group_id:  int | None = None

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: str | None = None