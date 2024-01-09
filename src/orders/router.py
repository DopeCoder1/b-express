from fastapi import APIRouter, Depends, status
from src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.schemas import OrdersCreateSchemas, OrderViewSchemas
from src.orders.service import order_service
from src.users.auth import JWTBearer

router = APIRouter(
    tags=["Orders"]
)


@router.post("/orders", status_code=status.HTTP_201_CREATED, response_model=OrderViewSchemas)
async def create_order(payload: OrdersCreateSchemas, user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    return await order_service.create_order(payload, user, db)


@router.get("/orders", dependencies=[Depends(JWTBearer())], response_model=list[OrderViewSchemas], status_code=status.HTTP_200_OK)
async def get_orders(user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    return await order_service.get_orders(user, db)


@router.get("/orders/{id}", dependencies=[Depends(JWTBearer())], response_model=OrderViewSchemas, status_code=status.HTTP_200_OK)
async def get_order(id: int, user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)   ):
    return await order_service.get_order(id, user, db)


@router.delete("/orders/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int, user: str = Depends(JWTBearer())):
    return await order_service.delete_orders(id, user)


@router.put("/orders/{id}", dependencies=[Depends(JWTBearer())], response_model=OrderViewSchemas, status_code=status.HTTP_200_OK)
async def update_order(id: int, payload: OrdersCreateSchemas, user: str = Depends(JWTBearer())):
    return await order_service.update_order(id, payload, user)
