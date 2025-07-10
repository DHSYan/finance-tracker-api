# Finance Tracker

A personal finance tracking REST API built with FastAPI, PostgreSQL, and Python.

## Features

- Add, retrieve, and manage transactions
- PostgreSQL for reliable data storage
- FastAPI backend with automatic OpenAPI documentation

## Tech Stack

- Python 3.x
- FastAPI
- PostgreSQL
- psycopg (PostgreSQL client)
- Uvicorn (ASGI server)

# Setup

```bash
git clone https://github.com/your-username/finance-tracker.git
cd finance-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
## Address
- Application is to be hosted on `http://127.0.0.1:8000`


# Database Configuration
edit this in `main.py`
`psycopg.connect("postgresql://<user>:<password>@<host>:<port>/<db>")`


# Licence 
MIT

