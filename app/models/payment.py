from sqlalchemy import Column, String, Float, DateTime, Boolean
from datetime import datetime
from app.database.db import Base
import uuid

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    payment_type = Column(String, nullable=False)  # deposit, final
    amount = Column(Float, nullable=False)
    payment_status = Column(String, default="pending")  # pending, completed, failed, refunded
    payment_method = Column(String, nullable=True)  # card, bank_transfer, etc
    transaction_id = Column(String, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    refunded_at = Column(DateTime, nullable=True)
    refund_amount = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
