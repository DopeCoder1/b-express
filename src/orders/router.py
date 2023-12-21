from fastapi import APIRouter,status, Depends
from src.users.auth import JWTBearer

from src.orders.schemas import OrderViewSchemas, OrdersCreateSchemas
from src.orders.service import order_service

router = APIRouter(
    tags=["Orders"]
)


@router.post("/orders",status_code=status.HTTP_201_CREATED, response_model=OrderViewSchemas)
async def create_order(payload: OrdersCreateSchemas, user: str = Depends(JWTBearer())):
    return await order_service.create_order(payload, user)

@router.get("/orders",dependencies=[Depends(JWTBearer())], response_model=list[OrderViewSchemas], status_code=status.HTTP_200_OK)
async def get_orders(user: str = Depends(JWTBearer())):
    return await order_service.get_orders(user=user)

@router.delete("/orders/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int, user: str = Depends(JWTBearer())):
    return await order_service.delete_orders(id, user)

