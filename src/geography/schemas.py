from pydantic import BaseModel


class GeographyCreateSchemas(BaseModel):
    name: str


class GeographyViewSchemas(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CityOut(BaseModel):
    id: int
    name: str
