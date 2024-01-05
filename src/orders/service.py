from src.dao.base import BaseDao
from src.exceptions import PermissionDenied
from src.orders.models import Orders
from src.orders.schemas import OrdersCreateSchemas, OrderViewSchemas
from src.users.schemas import UserViewSchemas


class OrderService(BaseDao):
    class_name = Orders

    async def create_order(self, payload: OrdersCreateSchemas, user: UserViewSchemas):
        return await OrderService.add({"creator": user.id, "status": payload.status, "warehouse": payload.warehouse, "driver": payload.driver, "description": payload.description})
    

    async def get_orders(self, user: UserViewSchemas) -> list[OrderViewSchemas]:
        return await OrderService.find_all({"creator": user.id})

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
