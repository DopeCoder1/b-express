from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session, get_db
from src.directions.models import Directions
from src.directions.schemas import DirectionOut, DirectionViewSchemas
from src.exceptions import PermissionDenied
from src.geography.models import City
from src.geography.schemas import CityOut, GeographyViewSchemas
from src.orders.models import OrderItems, Orders, Payment
from src.orders.schemas import OrderItemsOut, OrderViewSchemas, PaymentOut
from src.users.models import Users
from src.users.schemas import UserViewSchemas
from src.warehouse.models import Warehouse
from src.warehouse.schemas import WarehouseViewSchemas


class DirectionViewSerialized:

    async def serialize_by_id(self, id: int, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> DirectionViewSchemas:

        direction_query = await db.execute(select(Directions).where(Directions.id == id))
        direction = direction_query.scalar_one_or_none()

        arrival_city_query = await db.execute(select(City).where(City.id == direction.arrival_city_id))
        arrival_city = arrival_city_query.scalar_one_or_none()
        arrival_city_model = GeographyViewSchemas(**arrival_city.__dict__)

        departure_city_query = await db.execute(select(City).where(City.id == direction.departure_city_id))
        departure_city = departure_city_query.scalar_one_or_none()
        departure_city_model = GeographyViewSchemas(**departure_city.__dict__)

        direction_model = DirectionViewSchemas(
            id=direction.id,
            transportation_type=direction.transportation_type,
            is_active=direction.is_active,
            arrival_city=arrival_city_model,
            departure_city=departure_city_model
        )
        return direction_model


nested_serializer = DirectionViewSerialized()
