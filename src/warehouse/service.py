from src.dao.base import BaseDao
from src.users.models import Users
from src.warehouse.models import Warehouse
from src.warehouse.schemas import WarehouseCreateSchemas, WarehouseViewSchemas


class WarehouseService(BaseDao):
    class_name = Warehouse

    async def create(self, payload: WarehouseCreateSchemas, user: Users) -> dict:
        return await WarehouseService.add({"address": payload.address, "name": payload.name, "city": payload.city, "street": payload.street, "number": payload.number, "creator": user.id})

    async def get(self, user: Users) -> list[dict]:
        return await WarehouseService.find_all({"creator": user.id})


warehouse_service = WarehouseService()
