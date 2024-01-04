from pydantic import BaseModel


class WarehouseCreateSchemas(BaseModel):
    address: str
    name: str
    city: int
    street: str
    number: str


class WarehouseViewSchemas(BaseModel):
    id: int
    address: str
    name: str
    city: int
    street: str
    number: str
    creator: int

    class Config:
        from_attributes = True
