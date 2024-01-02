from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchemas(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchemas(BaseModel):
    email: EmailStr


class UserConfirmationEmailSchemas(BaseModel):
    code: str
    user_id: int
    password: str
    confirm_password: str


class UserViewSchemas(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool
    is_active: bool
    is_delete: bool
    group_id:  int | None = None
    confirmation_link: str | None = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: str | None = None
