import hmac
import os
import sqlite3
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

DB_PATH = '/data/app.db'
INGEST_KEY = os.environ.get('INGEST_KEY')

def getdb():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

class Reading(BaseModel):
    sensor: str
    value: float

@app.post('/', status_code=201)
def ingest(reading: Reading, api_key: str = Header(default=''), db: sqlite3.Connection = Depends(getdb)):
    if not INGEST_KEY or not hmac.compare_digest(api_key.encode(), INGEST_KEY.encode()):
        raise HTTPException(status_code=401, detail='Invalid API Key')

    db.execute(
        'INSERT INTO readings (sensor, value) VALUES (?, ?)',
        (reading.sensor, reading.value)
    )
    db.commit()
    return {"ok": True}
