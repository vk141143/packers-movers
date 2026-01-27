from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime, timezone
from app.database.db import Base

class ServiceType(Base):
    __tablename__ = "service_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
