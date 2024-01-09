from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDao
from src.database import get_db
from src.directions.models import Directions
from src.directions.schemas import (DirectionCreateSchemas, DirectionOut,
                                    DirectionViewSchemas)
from src.directions.utils import nested_serializer
from src.users.schemas import UserViewSchemas


class DirectionService(BaseDao):
    class_name = Directions

    async def create_direction(self, payload: DirectionCreateSchemas, user: UserViewSchemas,  db: AsyncSession = Depends(get_db)):
        direction = await DirectionService.add({
            "arrival_city_id": payload.arrival_city_id,
            "departure_city_id": payload.departure_city_id,
            "is_active": payload.is_active,
            "transportation_type": payload.transportation_type
        })
        return await nested_serializer.serialize_by_id(direction.id, user, db)

    async def get_directions(self, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> List[DirectionViewSchemas]:
        directions = await DirectionService.find_all({})
        resp = []
        for direction in directions:
            resp.append(await nested_serializer.serialize_by_id(direction.id, user, db))
        return resp

    async def get_direction(self, id: int, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> DirectionViewSchemas:
        return await nested_serializer.serialize_by_id(id, user, db)


direction_service = DirectionService()
