from pydantic import BaseModel

from src.directions.schemas import DirectionOut
from src.orders.models import OrderStatus
from src.warehouse.schemas import WarehouseOutShort


class OrderItemsCreateSchemas(BaseModel):
    photo: str
    description: str


class OrderItemsOut(OrderItemsCreateSchemas):
    id: int
    status: OrderStatus


class PaymentCreateSchemas(BaseModel):
    amount: float
    currency: str
    payment_type: str
    payer_type: str
    bin: str


class PaymentOut(PaymentCreateSchemas):
    payment_status: str


class OrdersCreateSchemas(BaseModel):
    address: str
    courier: int | None = None
    sender_fio: str
    sender_phone: str
    reciever_fio: str
    reciever_phone: str
    total_weight: float
    total_volume: float
    insurance: float
    warehouse_id: int
    direction_id: int
    payment: PaymentCreateSchemas
    order_items: list[OrderItemsCreateSchemas]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example":
            {
                "address": "Almaty",
                "courier": 1,
                "sender_fio": "John Doe",
                "sender_phone": "+77785547554",
                "reciever_fio": "John Doe",
                "reciever_phone": "+77785547554",
                "total_weight": 10.0,
                "total_volume": 10.0,
                "insurance": 10.0,
                "warehouse_id": 1,
                "direction_id": 1,
                "payment": {
                    "amount": 100.0,
                    "currency": "KZT",
                    "payment_type": "cash",
                    "payer_type": "sender",
                    "bin": "123456789012"
                },
                "order_items": [
                    {
                        "photo": "https://b-express.kz/img/logo.png",
                        "description": "Parcel"
                    }
                ]
            }
        }


class OrderViewSchemas(BaseModel):
    address: str
    courier: int | None = None
    sender_fio: str
    sender_phone: str
    reciever_fio: str
    reciever_phone: str
    total_weight: float
    total_volume: float
    insurance: float
    direction: DirectionOut | None = None
    payment: PaymentOut | None = None
    warehouse: WarehouseOutShort | None = None
    order_items: list[OrderItemsOut] | None = None
    direction: DirectionOut | None = None

    class Config:
        from_attributes = True
