from datetime import datetime
from pydantic import BaseModel

from src.users.schemas import UserViewSchemas

class OrderItemsCreateSchemas(BaseModel):
    photo:str
    status: str
    description: str 

class PaymentCreateSchemas(BaseModel):
    amount: float
    currency: str
    payment_status: str
    payment_type: str
    payer_type: str
    bin: str

class OrdersCreateSchemas(BaseModel):
    address: str
    courier: int
    sender_fio: str
    sender_phone: str
    reciever_fio: str
    reciever_phone: str
    total_weight:float
    total_volume:float
    insurance: float
    warehouse_id:int
    payment: PaymentCreateSchemas
    order_items: OrderItemsCreateSchemas

class OrderViewSchemas(BaseModel):
    id: int
    creator: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    address: str

    class Config:
        from_attributes = True
