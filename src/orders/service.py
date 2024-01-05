from src.dao.base import BaseDao
from src.orders.models import Orders
from src.orders.schemas import OrderViewSchemas, OrdersCreateSchemas
from src.users.schemas import UserViewSchemas
from src.exceptions import PermissionDenied


class OrderService(BaseDao):
    class_name = Orders
    
    async def create_order(self, payload: OrdersCreateSchemas, user: UserViewSchemas)-> dict:
        # data = {
        #     "address": payload.address,
        #     "creator": user.id
        # }
        # return await OrderService.add(data)
        order = await OrderService.add({""})
        
        
    async def get_orders(self, user:UserViewSchemas)-> list[OrderViewSchemas]:
        return await OrderService.find_all({"creator": user.id})
    
    async def delete_orders(self, id: int, user:UserViewSchemas):
        order = await OrderService.find_one_or_none({"id":id})
        if order and order.creator == user.id:
            await OrderService.delete({"id": id})
        raise PermissionDenied()

order_service = OrderService()