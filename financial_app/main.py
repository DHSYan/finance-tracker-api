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

def handler(event, context):
    # Parse API Gateway v2 event
    if 'version' in event and event['version'] == '2.0':
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
        headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
        body = base64.b64decode(event['body']) if event.get('body') else b''
        query_string = event.get('rawQueryString', '')
    else:
        # Fallback for v1 if needed
        method = event['httpMethod']
        path = event['path']
        headers = {k.lower(): v for k, v in event['headers'].items()}
        body = base64.b64decode(event['body']) if event.get('isBase64Encoded') else event['body'].encode('utf-8') if event['body'] else b''
        query_string = event.get('queryStringParameters', '')

    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'HTTP_HOST': headers.get('host', 'lambda'),
        'wsgi.input': body,
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    for k, v in headers.items():
        environ[f'HTTP_{k.upper().replace("-", "_")}'] = v

    # Create Flask request and get response
    req = WRequest(environ)
    with app.request_context(req):
        response = app.full_dispatch_request()

    # Return v2-compatible Lambda response
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True),
        'isBase64Encoded': False
    }
