#!/usr/bin/env python3
import sqlite3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
SCHEMA_PATH = os.path.join(SCRIPT_DIR, 'campus_traffic_schema.sql')
DATA_DIR = os.path.join(WORKING_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'campus_traffic.db')

def setup_database():
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)

    if os.path.exists(DB_PATH):
        print(  f"Error: Database already exists at {DB_PATH}. " \
                "If you want to create a new database, run the " \
                "archive script at archive/archive_db.sh first."
        )
        sys.exit(1)

    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Creating SQLite database at {DB_PATH}...")
    
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executescript(schema_sql)
            conn.commit()
        print("Database created and schema applied successfully.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
