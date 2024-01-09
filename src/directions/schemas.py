from pydantic import BaseModel

from src.directions.models import TransportationType
from src.geography.schemas import CityOut, GeographyViewSchemas


class DirectionCreateSchemas(BaseModel):
    arrival_city_id: int
    departure_city_id: int
    is_active: bool
    transportation_type: TransportationType

    model_config = {
        "json_schema_extra": {
            "example":
            {
                "arrival_city_id": 1,
                "departure_city_id": 2,
                "is_active": True,
                "transportation_type": "RAIL"
            }
        }
    }


class DirectionViewSchemas(BaseModel):
    id: int
    arrival_city: GeographyViewSchemas
    departure_city: GeographyViewSchemas
    is_active: bool
    transportation_type: TransportationType

    class Config:
        from_attributes = True


class DirectionOut(BaseModel):
    arrival_city: CityOut
    departure_city: CityOut
    transportation_type: TransportationType

    class Config:
        from_attributes = True
