from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.common.models import TimestampMixin
from src.database import Base


class TransportationType(Enum):
    AIR = "AIR"
    SEA = "SEA"
    RAIL = "RAIL"
    ROAD = "ROAD"


class Directions(Base, TimestampMixin):
    __tablename__ = "directions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    arrival_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    departure_city_id = Column(
        Integer, ForeignKey("cities.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    transportation_type = Column(PgEnum(TransportationType), nullable=False)
