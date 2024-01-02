from sqlalchemy import (JSON, Column, DateTime, Float, ForeignKey, Integer,
                        String)

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


