import sqlite3
import pytest
from fastapi.testclient import TestClient

import listener

TEST_KEY = "test-secret"

@pytest.fixture
def db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE readings (
            id INTEGER PRIMARY KEY,
            sensor TEXT NOT NULL,
            value REAL NOT NULL,
            time TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture
def client(db, monkeypatch):
    monkeypatch.setattr(listener, 'INGEST_KEY', TEST_KEY)
    listener.app.dependency_overrides[listener.getdb] = lambda: db
    yield TestClient(listener.app)
    listener.app.dependency_overrides.clear()

def test_reading_is_written_to_database(client, db):
    assert db.execute('SELECT COUNT(*) FROM readings').fetchone()[0] == 0

    response = client.post(
        '/',
        json={'sensor': 'test', 'value': 42.3},
        headers={'api-key': TEST_KEY}
    )

    assert response.status_code == 201

    row = db.execute(
        'SELECT sensor, value FROM readings WHERE sensor = ?', ('test',)
    ).fetchone()

    assert row is not None
    assert row == ('test', 42.3)