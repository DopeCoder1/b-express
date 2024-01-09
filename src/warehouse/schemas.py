from pydantic import BaseModel

from src.geography.schemas import GeographyViewSchemas
from src.users.schemas import UserViewSchemas

class WarehouseCreateSchemas(BaseModel):
    address: str
    name: str
    city: int
    street: str
    number: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "address": "Almaty",
                "name": "Almaty",
                "city": 1,
                "street": "Almaty",
                "number": "1",
            }
        },
    }


class WarehouseViewSchemas(BaseModel):
    id: int
    address: str
    name: str
    city: GeographyViewSchemas
    street: str
    number: str
    creator: UserViewSchemas

    class Config:
        from_attributes = True


class WarehouseOutShort(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        from_attributes = True
