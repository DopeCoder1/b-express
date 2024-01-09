from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models import SortOrder
from src.database import get_db
from src.directions.models import TransportationType
from src.orders.schemas import (OrderPaginated, OrdersCreateSchemas,
                                OrderStatus, OrderViewSchemas)
from src.orders.service import order_service
from src.users.auth import JWTBearer

router = APIRouter(
    tags=["Orders"]
)


@router.post("/orders", status_code=status.HTTP_201_CREATED, response_model=OrderViewSchemas)
async def create_order(payload: OrdersCreateSchemas, user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    return await order_service.create_order(payload, user, db)


@router.get("/orders/paginated", dependencies=[Depends(JWTBearer())], response_model=OrderPaginated, status_code=status.HTTP_200_OK)
async def get_orders_paginated(user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db), status: list[OrderStatus] = Query(None), warehouse_id: list[int] = Query(None), direction_id: list[int] = Query(None), transportation_type: list[TransportationType] = Query(None), start_date: date = Query(None), end_date: date = Query(None), page: int = 1, limit: int = 10, sort_by: str = Query(None), sort_order: SortOrder = Query(None), today: bool = Query(None), all_time: bool = Query(None)) -> OrderPaginated:
    return await order_service.get_orders_paginated(user, db, status, warehouse_id, direction_id, transportation_type, start_date, end_date, page, limit, sort_by, sort_order, today, all_time)


@router.get("/orders", dependencies=[Depends(JWTBearer())], response_model=list[OrderViewSchemas], status_code=status.HTTP_200_OK)
async def get_orders(user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    return await order_service.get_orders(user, db)


@router.get("/orders/{id}", dependencies=[Depends(JWTBearer())], response_model=OrderViewSchemas, status_code=status.HTTP_200_OK)
async def get_order(id: int, user: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    return await order_service.get_order(id, user, db)


@router.delete("/orders/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int, user: str = Depends(JWTBearer())):
    return await order_service.delete_orders(id, user)


@router.put("/orders/{id}", dependencies=[Depends(JWTBearer())], response_model=OrderViewSchemas, status_code=status.HTTP_200_OK)
async def update_order(id: int, payload: OrdersCreateSchemas, user: str = Depends(JWTBearer())):
    return await order_service.update_order(id, payload, user)
