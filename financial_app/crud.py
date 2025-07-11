from sqlalchemy.orm import Session
from .models import FinancialRecord
from .schemas import FinancialRecordCreate

def create_record(db: Session, record: FinancialRecordCreate):
    db_record = FinancialRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: Session):
    return db.query(FinancialRecord).all()

def get_record(db: Session, id: int):
    return db.query(FinancialRecord).filter(FinancialRecord.id == id).first()

def update_record(db: Session, id: int, record: FinancialRecordCreate):
    db_record = get_record(db, id)
    if db_record:
        for key, value in record.dict().items(exclude_unset=True):
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, id: int):
    db_record = get_record(db, id)
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record
