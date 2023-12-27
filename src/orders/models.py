from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.common.models import TimestampMixin
from src.database import Base


class OrderStatus(Enum):
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
    order = relationship("Order", back_populates="payment")


class Orders(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    address = Column(String, nullable=False)
    courier = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender = Column(Integer, ForeignKey("users.id"), nullable=False)
    reciever = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_status = Column(String, nullable=False)
    payment = relationship("Payment", uselist=False, back_populates="order")

    total_weight = Column(Float, nullable=False)
    total_volume = Column(Float, nullable=False)
    warehouse = Column(Integer, ForeignKey("warehouses.id"), nullable=False)


class OrderItems(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    photo = Column(String, nullable=False)
    status = Column(String, nullable=False)
