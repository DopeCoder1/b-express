from sqlalchemy import (Boolean, Column, ForeignKey,
                        Integer, String)

from src.common.models import TimestampMixin
from src.database import Base


class Warehouse(Base, TimestampMixin):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    city = Column(Integer, ForeignKey("cities.id"), nullable=False)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Boolean, server_default="false")
    warehouse_user = Column(Integer, ForeignKey("users.id"), nullable=False)
