from fastapi import APIRouter, Depends, status

from src.users.auth import JWTBearer
from src.users.models import Users
from src.warehouse.schemas import WarehouseCreateSchemas, WarehouseViewSchemas
from src.warehouse.service import warehouse_service

router = APIRouter(
    tags=["Warehouse"]
)


@router.post("/warehouse", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, response_model=WarehouseViewSchemas)
async def create_warehouse(payload: WarehouseCreateSchemas, user: Users = Depends(JWTBearer())):
    return await warehouse_service.create(payload, user)


@router.get("/warehouse", status_code=status.HTTP_200_OK, response_model=list[WarehouseViewSchemas])
async def get_warehouse(user: Users = Depends(JWTBearer())):
    return await warehouse_service.get(user)
