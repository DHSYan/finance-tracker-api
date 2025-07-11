from pydantic import BaseModel
import datetime as dt
from typing import Optional

class FinancialRecordBase(BaseModel):
    amount: float
    description: str
    class Config:
        from_attributes = True  # Enables ORM mode for DB mapping

class FinancialRecordCreate(FinancialRecordBase):
    transaction_date: Optional[dt.datetime] = None

class FinancialRecord(FinancialRecordBase):
    id: int
    transaction_date: dt.datetime
