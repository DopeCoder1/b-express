from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDao
from src.database import get_db
from src.users.models import Users
from src.warehouse.models import Warehouse
from src.warehouse.schemas import (WarehouseCreateSchemas,
                                   WarehouseViewSchemas,
                                   )
from src.warehouse.utils import nested_serializer

class WarehouseService(BaseDao):
    class_name = Warehouse

    async def create(self, payload: WarehouseCreateSchemas, user: Users) -> dict:
        return await WarehouseService.add({"address": payload.address, "name": payload.name, "city": payload.city, "street": payload.street, "number": payload.number, "creator": user.id})

    async def get(self, user: Users, db: AsyncSession = Depends(get_db)) -> list[dict]:
        warehouses = await WarehouseService.find_all({"creator": user.id})
        response = []
        for warehouse in warehouses:
            response.append(await nested_serializer.serialize_by_id(warehouse.id, user, db))
        return response

    async def get_one(self, id: int, user: Users, db: AsyncSession = Depends(get_db)) -> dict:
        return await nested_serializer.serialize_by_id(id, user, db)

    async def update(self, id: int, payload: WarehouseCreateSchemas, user: Users) -> dict:
        return await WarehouseService.update({"id": id, "creator": user.id}, payload)


warehouse_service = WarehouseService()
