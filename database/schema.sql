CREATE TABLE readings (
id INTEGER PRIMARY KEY,
sensor TEXT NOT NULL,
value REAL NOT NULL,
time TEXT NOT NULL DEFAULT (datetime('now'))
);
