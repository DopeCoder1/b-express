from sqlalchemy import Column, Integer, String

from src.common.models import TimestampMixin
from src.database import Base


class City(Base, TimestampMixin):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    