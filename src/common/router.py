from fastapi import APIRouter

from src.directions.models import TransportationType
from src.orders.models import OrderStatus
from src.orders.schemas import OrderStatus

router = APIRouter(
    tags=["root"]
)


@router.get("/api/v1/statuses", tags=["root"])
async def get_statuses():
    return [status.value for status in OrderStatus]


@router.get("/api/v1/transportation_types", tags=["root"])
async def get_transportation_types():
    return [transportation_type.value for transportation_type in TransportationType]
