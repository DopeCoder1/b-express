from fastapi import APIRouter, Depends, status

from src.users.auth import JWTBearer
from src.users.models import Users
from src.warehouse.schemas import WarehouseCreateSchemas, WarehouseViewSchemas
from src.warehouse.service import warehouse_service

router = APIRouter(
    tags=["Warehouse"]
)


@router.post("/warehouses", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, response_model=WarehouseViewSchemas)
async def create_warehouse(payload: WarehouseCreateSchemas, user: Users = Depends(JWTBearer())):
    return await warehouse_service.create(payload, user)


@router.get("/warehouses", status_code=status.HTTP_200_OK, response_model=list[WarehouseViewSchemas])
async def list_warehouse(user: Users = Depends(JWTBearer())):
    return await warehouse_service.get(user)


@router.get("/warehouses/{id}", status_code=status.HTTP_200_OK, response_model=WarehouseViewSchemas)
async def get_warehouse(id: int, user: Users = Depends(JWTBearer())):
    return await warehouse_service.get_one(id, user)


@router.patch("/warehouses/{id}", status_code=status.HTTP_200_OK, response_model=WarehouseViewSchemas)
async def update_warehouse(id: int, payload: WarehouseCreateSchemas, user: Users = Depends(JWTBearer())):
    return await warehouse_service.update(id, payload, user)
