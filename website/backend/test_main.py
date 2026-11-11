import sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

import main

SCHEMA = Path(__file__).parents[2] / 'database' / 'schema.sql'

@pytest.fixture
def db(tmp_path):                              # integrated
    conn = sqlite3.connect(tmp_path / 'app.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text())
    yield conn
    conn.close()

@pytest.fixture
def client(db):                                 # integrated
    main.app.dependency_overrides[main.getdb] = lambda: db
    with TestClient(main.app) as clnt:
        yield clnt
    main.app.dependency_overrides.clear()

def test_readings_returns_rows_newest_first(client, db):        # developed
    db.executemany(
        'INSERT INTO readings (sensor, value, time) VALUES (?, ?, ?)',
        [('a', 1.5, '2026-01-01 00:00:00'), ('b', 2.5, '2026-01-02 00:00:00')]
    )
    db.commit()

    response = client.get('/readings')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 2, 'sensor': 'b', 'value': 2.5, 'time': '2026-01-02 00:00:00'},
        {'id': 1, 'sensor': 'a', 'value': 1.5, 'time': '2026-01-01 00:00:00'},
    ]
