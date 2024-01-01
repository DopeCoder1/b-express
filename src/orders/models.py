from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from src.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    address = Column(String, nullable=False)