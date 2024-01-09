from sqlalchemy import select

from src.dao.base import BaseDao
from src.database import async_session
from src.directions.models import Directions
from src.directions.schemas import DirectionOut
from src.exceptions import PermissionDenied
from src.geography.models import City
from src.geography.schemas import CityOut
from src.orders.models import (OrderItems, Orders, OrderStatus, Payment,
                               PaymentStatus)
from src.orders.schemas import (OrderItemsCreateSchemas, OrderItemsOut,
                                OrdersCreateSchemas, OrderViewSchemas,
                                PaymentOut)
from src.orders.utils import nested_serializer
from src.users.schemas import UserViewSchemas
from src.warehouse.models import Warehouse
from src.warehouse.schemas import WarehouseOutShort
from src.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

class OrderService(BaseDao):
    class_name = Orders

    async def create_order(self, payload: OrdersCreateSchemas, user: UserViewSchemas, db: AsyncSession = Depends(get_db)):
        order = await OrderService.add({
            "creator": user.id,
            "warehouse_id": payload.warehouse_id,
            "direction_id": payload.direction_id,
            "address": payload.address,
            "courier": payload.courier,
            "order_status": OrderStatus.CREATED.value,
            "total_weight": payload.total_weight,
            "total_volume": payload.total_volume,
            "sender_fio": payload.sender_fio,
            "sender_phone": payload.sender_phone,
            "reciever_fio": payload.reciever_fio,
            "reciever_phone": payload.reciever_phone,
            "insurance": payload.insurance,
        })
        payment = Payment(**payload.payment.model_dump(),
                          order_id=order.id, payment_status=PaymentStatus.NOT_PAID.value)
        db.add(payment)
        order.payment = payment
        order.order_items = payload.order_items
        for order_item in payload.order_items:
            order_item = OrderItems(
                **order_item.model_dump(), order_id=order.id, status=OrderStatus.CREATED.value)
            db.add(order_item)
        await db.commit()
        return await nested_serializer.serialize_by_id(order.id, user, db)

    async def get_orders(self, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> list[OrderViewSchemas]:
        orders = await OrderService.find_all({"creator": user.id})
        response = []
        for order in orders:
            response.append(await nested_serializer.serialize_by_id(order.id, user, db))
        return response

    async def get_order(self, id: int, user: UserViewSchemas, db: AsyncSession = Depends(get_db)) -> OrderViewSchemas:
        return await nested_serializer.serialize_by_id(id, user, db)

    async def delete_orders(self, id: int, user: UserViewSchemas):
        order = await OrderService.find_one_or_none({"id": id})
        if order and order.creator == user.id:
            await OrderService.delete({"id": id})
        raise PermissionDenied()

    async def update_order(self, id: int, payload: OrdersCreateSchemas, user: UserViewSchemas):
        order = await OrderService.find_one_or_none({"id": id})
        order = await OrderService.update({"id": id}, payload)
        return order


order_service = OrderService()
