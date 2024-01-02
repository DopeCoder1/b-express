from datetime import datetime
from enum import Enum

from sqlalchemy import (JSON, Column, DateTime, Float, ForeignKey, Integer,
                        String)


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    