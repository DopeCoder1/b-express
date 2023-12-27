from datetime import datetime
from enum import Enum

from sqlalchemy import (JSON, Column, DateTime, Float, ForeignKey, Integer,
                        String)

from common.models import TimestampMixin
from src.database import Base


class City(Base, TimestampMixin):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

