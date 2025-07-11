from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .schemas import FinancialRecord, FinancialRecordCreate
from .crud import create_record, get_records, update_record, delete_record
# get_record_by_id,

app = FastAPI()

# Create DB tables if not exist
Base.metadata.create_all(bind=engine)

@app.post("/records/", response_model=FinancialRecord)
def create_financial_record(record: FinancialRecordCreate, db: Session = Depends(get_db)):
    return create_record(db=db, record=record)

@app.get("/records/", response_model=list[FinancialRecord])
def read_financial_records(db: Session = Depends(get_db)):
    return get_records(db)

@app.get("/records/{id}", response_model=FinancialRecord)
def read_financial_record(id: int, db: Session = Depends(get_db)):
    record = get_record_by_id(db, id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.put("/records/{id}", response_model=FinancialRecord)
def update_financial_record(id: int, record: FinancialRecordCreate, db: Session = Depends(get_db)):
    updated = update_record(db, id, record)
    if updated is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

@app.delete("/records/{id}")
def delete_financial_record(id: int, db: Session = Depends(get_db)):
    deleted = delete_record(db, id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}
