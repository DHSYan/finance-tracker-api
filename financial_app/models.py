from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    transaction_date = Column(DateTime, default=datetime.now, nullable=False)
