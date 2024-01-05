from pydantic import BaseModel

from src.directions.models import TransportationType


class DirectionCreateSchemas(BaseModel):
    arrival_city_id: int
    departure_city_id: int
    is_active: bool
    transportation_type: TransportationType


class DirectionViewSchemas(BaseModel):
    arrival_city_id: int
    departure_city_id: int
    is_active: bool
    transportation_type: TransportationType

    class Config:
        from_attributes = True
