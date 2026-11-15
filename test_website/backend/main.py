import sqlite3
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse

app = FastAPI()

DB_PATH = '/data/app.db'

# Opens connection to SQLite database.
def getdb():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Listens for request sent by button press. Queries database for all rows, returns them as a dictionary.
@app.get('/readings')
def readings(db: sqlite3.Connection = Depends(getdb)):
    rows = db.execute(
        "SELECT id, sensor, value, time FROM readings ORDER BY id DESC"
	).fetchall()
    return [dict(r) for r in rows]