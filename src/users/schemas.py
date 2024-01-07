from pydantic import BaseModel, EmailStr

from src.geography.schemas import CityOut


class UserSchemas(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example":
            {
                "email": "zshanabek@gmail.com",
                "password": "132312qQ"
            }
        }
    }


class UserCreateSchemas(BaseModel):
    email: EmailStr
    group_id: int
    city_id: int
    salary: float
    phone: str
    first_name: str
    last_name: str

    model_config = {
        "json_schema_extra": {
            "example":
            {
                "email": "zshanabek@gmail.com",
                "group_id": 1,
                "city_id": 1,
                "salary": 350000,
                "phone": "+77785547554",
                "first_name": "John",
                "last_name": "Doe"
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
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    city: CityOut | None = None
    salary: float | None = None
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


PERMISSIONS_MAP = [
    {
        "group_name": "SUPER_ADMIN",
        "permissions": [
            {
                "name": "CREATE_ROLE",
                "codename": "CREATE_ROLE"
            },
            {
                "name": "VIEW_EMPLOYEES",
                "codename": "VIEW_EMPLOYEES"
            },
            {
                "name": "CREATE_REMOVE_USER",
                "codename": "CREATE_REMOVE_USER"
            }
        ]
    },
    {
        "group_name": "ADMIN",
        "permissions": [
            {
                "name": "CREATE_REMOVE_ORDER",
                "codename": "CREATE_REMOVE_ORDER"
            },
            {
                "name": "LIST_ORDERS",
                "codename": "LIST_ORDERS"
            },
            {
                "name": "VIEW_EMPLOYEES",
                "codename": "VIEW_EMPLOYEES"
            },
            {
                "name": "CREATE_REMOVE_USER",
                "codename": "CREATE_REMOVE_USER"
            },
            {
                "name": "CANCEL_ORDERS",
                "codename": "CANCEL_ORDERS"
            },
            {
                "name": "GENERATE_REPORTS",
                "codename": "GENERATE_REPORTS"
            },
        ]
    },
    {
        "group_name": "SUPERVISOR",
        "permissions": [
            {
                "name": "CREATE_REMOVE_ORDER",
                "codename": "CREATE_REMOVE_ORDER"
            },
            {
                "name": "LIST_ORDERS",
                "codename": "LIST_ORDERS"
            },
            {
                "name": "VIEW_EMPLOYEES",
                "codename": "VIEW_EMPLOYEES"
            },
            {
                "name": "CREATE_REMOVE_USER",
                "codename": "CREATE_REMOVE_USER"
            },
            {
                "name": "CANCEL_ORDERS",
                "codename": "CANCEL_ORDERS"
            },
        ]
    },
    {
        "group_name": "MANAGER",
        "permissions": [
            {
                "name": "CREATE_REMOVE_ORDER",
                "codename": "CREATE_REMOVE_ORDER"
            },
            {
                "name": "LIST_ORDERS",
                "codename": "LIST_ORDERS"
            },
            {
                "name": "CANCEL_ORDERS",
                "codename": "CANCEL_ORDERS"
            },
            {
                "name": "SIGN_ORDERS",
                "codename": "SIGN_ORDERS"
            },
        ]
    },
    {
        "group_name": "USER",
        "permissions": [
            {
                "name": "LIST_ORDERS",
                "codename": "LIST_ORDERS"
            },
            {
                "name": "CANCEL_ORDERS",
                "codename": "CANCEL_ORDERS"
            },
            {
                "name": "PAY_ORDERS",
                "codename": "PAY_ORDERS"
            },
        ]
    }
]
