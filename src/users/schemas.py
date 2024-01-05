from pydantic import BaseModel, EmailStr


class UserSchemas(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchemas(BaseModel):
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example":
            {
                "email": "zshanabek@gmail.com"
            }
        }
    }


class UserConfirmationEmailSchemas(BaseModel):
    code: str
    user_id: int
    password: str
    confirm_password: str


class GroupViewSchemas(BaseModel):
    id: int
    name: str


class UserViewSchemas(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool
    is_active: bool
    is_delete: bool
    group: GroupViewSchemas | None = None
    confirmation_link: str | None = None
    creator: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    city: int | None = None
    salary: float | None = None
    group_id: int | None = None
    creator: int | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: str | None = None


class PermissionCreateSchemas(BaseModel):
    name: str
    codename: str


class PermissionViewSchemas(BaseModel):
    name: str
    codename: str

    class Config:
        from_attributes = True


class GroupCreateSchemas(BaseModel):
    name: str


class GroupViewSchemas(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AuthGroupPermissionCreateSchemas(BaseModel):
    group_id: int
    codename: str


class AuthGroupPermissionViewSchemas(BaseModel):
    id: int
    group_id: int
    codename: str

    class Config:
        from_attributes = True
