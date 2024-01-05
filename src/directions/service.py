from src.dao.base import BaseDao
from src.directions.models import Directions
from src.directions.schemas import DirectionCreateSchemas, DirectionViewSchemas
from src.users.schemas import UserViewSchemas


class DirectionService(BaseDao):
    class_name = Directions

    async def create_direction(self, payload: DirectionCreateSchemas, user: UserViewSchemas):
        return await DirectionService.add({
            "arrival_city_id": payload.arrival_city_id,
            "departure_city_id": payload.departure_city_id,
            "is_active": payload.is_active,
            "transportation_type": payload.transportation_type
        })

    async def get_directions(self, user: UserViewSchemas):
        return await DirectionService.find_all({})

    async def get_direction(self, id: int, user: UserViewSchemas):
        return await DirectionService.find_one_or_none({"id": id})


direction_service = DirectionService()
