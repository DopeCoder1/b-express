from src.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from datetime import datetime

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    address = Column(String, nullable=False)