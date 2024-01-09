from datetime import datetime
from enum import Enum

from sqlalchemy import (DECIMAL, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from src.common.models import TimestampMixin
from src.database import Base


class OrderStatus(Enum):
    CREATED = "CREATED"
    ASSIGNED_TO_COURIER = "ASSIGNED_TO_COURIER"
    COURIER_DELIVERING_TO_WAREHOUSE = "COURIER_DELIVERING_TO_WAREHOUSE"
    ACCEPTED_TO_WAREHOUSE = "ACCEPTED_TO_WAREHOUSE"
    CLIENT_DELIVERING_TO_WAREHOUSE = "CLIENT_DELIVERING_TO_WAREHOUSE"
    IN_TRANSIT = "IN_TRANSIT"
    ARRIVED_TO_DESTINATION = "ARRIVED_TO_DESTINATION"
    DELIVERING_TO_RECIPIENT = "DELIVERING_TO_RECIPIENT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


STATUS_GROUPS = {
    "PENDING": [OrderStatus.ASSIGNED_TO_COURIER, OrderStatus.COURIER_DELIVERING_TO_WAREHOUSE, OrderStatus.ACCEPTED_TO_WAREHOUSE, OrderStatus.CLIENT_DELIVERING_TO_WAREHOUSE],
    "IN_TRANSIT": [OrderStatus.IN_TRANSIT, OrderStatus.ARRIVED_TO_DESTINATION, OrderStatus.DELIVERING_TO_RECIPIENT],
    "DELIVERED": [OrderStatus.DELIVERED],
    "CANCELLED": [OrderStatus.CANCELLED]
}


class PaymentStatus(Enum):
    NOT_PAID = "NOT_PAID"
    PAID = "PAID"


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    payment_status = Column(String, nullable=False)
    payment_type = Column(String, nullable=False)
    payer_type = Column(String, nullable=False)
    bin = Column(String, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Orders", back_populates="payment")


class Orders(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    address = Column(String, nullable=False)
    courier = Column(Integer, ForeignKey("users.id"), nullable=True)
    sender_fio = Column(String, nullable=False)
    sender_phone = Column(String, nullable=False)
    reciever_fio = Column(String, nullable=False)
    reciever_phone = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
    payment = relationship("Payment", uselist=False, back_populates="order")
    insurance = Column(DECIMAL(10, 2), nullable=False)
    total_weight = Column(Float, nullable=False)
    total_volume = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    direction_id = Column(Integer, ForeignKey("directions.id"))


class OrderItems(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    photo = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=False)
