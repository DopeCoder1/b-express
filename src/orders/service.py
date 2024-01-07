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
from src.users.schemas import UserViewSchemas
from src.warehouse.models import Warehouse
from src.warehouse.schemas import WarehouseOutShort


class OrderService(BaseDao):
    class_name = Orders

    async def create_order(self, payload: OrdersCreateSchemas, user: UserViewSchemas):
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
        payment = Payment(**payload.payment.dict(),
                          order_id=order.id, payment_status=PaymentStatus.NOT_PAID.value)
        session = async_session()
        session.add(payment)
        order.payment = payment
        order.order_items = payload.order_items
        for order_item in payload.order_items:
            order_item = OrderItems(
                **order_item.dict(), order_id=order.id, status=OrderStatus.CREATED.value)
            session.add(order_item)
        await session.commit()
        return order

    async def get_orders(self, user: UserViewSchemas) -> list[OrderViewSchemas]:
        session = async_session()
        orders = await session.execute(select(Orders))
        orders = orders.scalars().all()
        orders_out = []
        for order in orders:
            warehouse = await session.execute(select(Warehouse).where(Warehouse.id == order.warehouse_id))
            warehouse = warehouse.scalars().first()

            direction = await session.execute(select(Directions).where(Directions.id == order.direction_id))
            direction = direction.scalars().first()

            arival_city = await session.execute(select(City).where(City.id == direction.arrival_city_id))
            arival_city = arival_city.scalars().first()

            departure_city = await session.execute(select(City).where(City.id == direction.departure_city_id))
            departure_city = departure_city.scalars().first()

            arrival_city_out = CityOut(**arival_city.__dict__)
            departure_city_out = CityOut(**departure_city.__dict__)

            direction_out = DirectionOut(**direction.__dict__,
                                         arrival_city=arrival_city_out,
                                         departure_city=departure_city_out)

            payment = await session.execute(select(Payment).where(Payment.order_id == order.id))
            payment = payment.scalars().first()

            order_items = await session.execute(select(OrderItems).where(OrderItems.order_id == order.id))
            order_items = order_items.scalars().all()

            order_items_out = []
            for order_item in order_items:
                order_items_out.append(OrderItemsOut(**order_item.__dict__))

            orders_out.append(OrderViewSchemas(
                **order.__dict__,
                warehouse=WarehouseOutShort(**warehouse.__dict__),
                direction=direction_out,
                payment=PaymentOut(**payment.__dict__),
                diection=direction_out,
                order_items=order_items_out
            ))
        return orders_out

    async def get_order(self, id: int, user: UserViewSchemas) -> OrderViewSchemas:
        order = await OrderService.find_one_or_none({"id": id})
        if order and order.creator == user.id:
            return order
        raise PermissionDenied()

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
