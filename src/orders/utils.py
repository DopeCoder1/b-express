from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session, get_db
from src.directions.models import Directions
from src.directions.schemas import DirectionOut
from src.exceptions import PermissionDenied
from src.geography.models import City
from src.geography.schemas import CityOut
from src.orders.models import OrderItems, Orders, Payment
from src.orders.schemas import OrderItemsOut, OrderViewSchemas, PaymentOut
from src.users.schemas import UserViewSchemas
from src.warehouse.models import Warehouse
from src.warehouse.schemas import WarehouseOutShort


class OrderViewSerialized:

    async def serialize_by_id(self, id: int, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> OrderViewSchemas:
        order = await db.execute(select(Orders).where(Orders.id == id))
        order = order.scalar_one_or_none()
        if not order or order.creator != user.id:
            raise PermissionDenied()

        warehouse = await db.execute(select(Warehouse).where(Warehouse.id == order.warehouse_id))
        warehouse = warehouse.scalars().first()
        warehouse_model = None
        if warehouse:
            warehouse_model = WarehouseOutShort(**warehouse.__dict__)

        direction = await db.execute(select(Directions).where(Directions.id == order.direction_id))
        direction = direction.scalars().first()

        arival_city = await db.execute(select(City).where(City.id == direction.arrival_city_id))
        arival_city = arival_city.scalars().first()

        departure_city = await db.execute(select(City).where(City.id == direction.departure_city_id))
        departure_city = departure_city.scalars().first()

        arrival_city_out = CityOut(**arival_city.__dict__)
        departure_city_out = CityOut(**departure_city.__dict__)

        direction_out = DirectionOut(**direction.__dict__,
                                     arrival_city=arrival_city_out,
                                     departure_city=departure_city_out)

        payment = await db.execute(select(Payment).where(Payment.order_id == order.id))
        payment = payment.scalars().first()

        order_items = await db.execute(select(OrderItems).where(OrderItems.order_id == order.id))
        order_items = order_items.scalars().all()

        order_items_out = []
        for order_item in order_items:
            order_items_out.append(OrderItemsOut(**order_item.__dict__))
        return OrderViewSchemas(
            **order.__dict__,
            warehouse=warehouse_model,
            direction=direction_out,
            payment=PaymentOut(**payment.__dict__),
            diection=direction_out,
            order_items=order_items_out
        )


nested_serializer = OrderViewSerialized()
