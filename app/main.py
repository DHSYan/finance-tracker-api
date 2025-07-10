from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import psycopg

import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

postgresql_url = os.getenv("DATABASE_URL")

print(postgresql_url)

try:
    conn = psycopg.connect(postgresql_url)
    cursor = conn.cursor()
    cur.execute("SELECT * FROM record")
    rows = cur.fetchall()
    print(row)
except Exception as e:
    print(f"Error: {e}")


# BaseModel is a class from Pydantic
class Record(BaseModel):
    id: int
    description: str
    amount: float

# @app.get("/transactions", response_model=List[Transaction])
# def get_transactions():
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, description, amount FROM transactions;")
#         rows = cur.fetchall()
#         return [{"id": r[0], "description": r[1], "amount": r[2]} for r in rows]


