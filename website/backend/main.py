import sqlite3
from fastapi import FastAPI

app = FastAPI(root_path="/api")

@app.get("/hello")
def hello():
	return {"message": "Hello from FastAPI on the Pi"}
