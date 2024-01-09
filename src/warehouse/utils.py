from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session, get_db
from src.directions.models import Directions
from src.directions.schemas import DirectionOut
from src.exceptions import PermissionDenied
from src.geography.models import City
from src.geography.schemas import CityOut, GeographyViewSchemas
from src.orders.models import OrderItems, Orders, Payment
from src.orders.schemas import OrderItemsOut, OrderViewSchemas, PaymentOut
from src.users.models import Users
from src.users.schemas import UserViewSchemas
from src.warehouse.models import Warehouse
from src.warehouse.schemas import WarehouseViewSchemas


class WarehouseViewSerialized:

    async def serialize_by_id(self, id: int, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> WarehouseViewSchemas:
        warehouse_query = await db.execute(select(Warehouse).where(Warehouse.id == id))
        warehouse = warehouse_query.scalar_one_or_none()
        user_query = await db.execute(select(Users).where(Users.id == warehouse.creator))
        user = user_query.scalar_one_or_none()
        user_model = UserViewSchemas(**user.__dict__)

        city_query = await db.execute(select(City).where(City.id == warehouse.city))
        city = city_query.scalar_one_or_none()
        city_model = GeographyViewSchemas(**city.__dict__)

        warehouse_model = WarehouseViewSchemas(
            id=warehouse.id,
            address=warehouse.address,
            name=warehouse.name,
            street=warehouse.street,
            number=warehouse.number,
            city=city_model,
            creator=user_model
        )
        return warehouse_model


nested_serializer = WarehouseViewSerialized()
