from datetime import date

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models import SortOrder
from src.dao.base import BaseDao
from src.database import get_db
from src.directions.models import Directions, TransportationType
from src.exceptions import PermissionDenied
from src.orders.models import (STATUS_GROUPS, OrderItems, Orders, OrderStatus,
                               Payment, PaymentStatus)
from src.orders.schemas import (OrderPaginated, OrdersCreateSchemas,
                                OrderViewSchemas)
from src.orders.utils import nested_serializer
from src.users.schemas import UserViewSchemas


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

    async def get_orders_paginated(self, user: UserViewSchemas, db: AsyncSession = Depends(get_db), status: list[OrderStatus] = None, warehouse_id: list[int] = None, direction_id: list[int] = None, transportation_type: list[TransportationType] = None, start_date: date = None, end_date: date = None, page: int = 1, limit: int = 10, sort_by: str = None, sort_order: SortOrder = None, today: bool = None, all_time: bool = None) -> OrderPaginated:
        orders = select(Orders).where(Orders.creator == user.id)
        if status is not None:
            orders = orders.where(Orders.order_status == status.value)
        if warehouse_id is not None:
            orders = orders.where(Orders.warehouse_id == warehouse_id)
        if direction_id is not None:
            orders = orders.where(Orders.direction_id == direction_id)
        if start_date is not None:
            orders = orders.where(Orders.created_at >= start_date)
        if end_date is not None:
            orders = orders.where(Orders.created_at <= end_date)
        if transportation_type is not None:
            orders = orders.join(Directions).where(
                Directions.transportation_type == transportation_type.value)
        if today is not None:
            orders = orders.where(Orders.created_at == date.today())
        if all_time is not None:
            orders = orders.where(Orders.created_at >= date(2021, 1, 1))
        if sort_by is not None:
            if sort_order == "desc":
                orders = orders.order_by(getattr(Orders, sort_by).desc())
            else:
                orders = orders.order_by(getattr(Orders, sort_by).asc())
        else:
            if sort_order == "desc":
                orders = orders.order_by(Orders.created_at.desc())
            else:
                orders = orders.order_by(Orders.created_at.asc())

        offset = (page - 1) * limit
        orders = orders.offset(offset).limit(limit)

        result = await db.execute(orders)
        orders = result.scalars().all()

        response = []
        for order in orders:
            response.append(await nested_serializer.serialize_by_id(order.id, user, db))
        all_orders = await db.execute(select(Orders))
        all_orders = all_orders.scalars().all()
        total = len(all_orders)
        return OrderPaginated(page=page, limit=limit, total=total, data=response)

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
