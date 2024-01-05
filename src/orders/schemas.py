from pydantic import BaseModel


class OrderItemsCreateSchemas(BaseModel):
    photo: str
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
    courier: int | None = None
    sender_fio: str
    sender_phone: str
    reciever_fio: str
    reciever_phone: str
    total_weight: float
    total_volume: float
    insurance: float
    warehouse_id: int
    payment: PaymentCreateSchemas
    order_items: OrderItemsCreateSchemas


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
    warehouse_id: int

    class Config:
        from_attributes = True
