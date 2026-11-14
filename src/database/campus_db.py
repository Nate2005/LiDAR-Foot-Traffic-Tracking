import os
import sqlite3
from collections import namedtuple
from contextlib import contextmanager

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEFAULT_DB_PATH = os.path.join(REPO_ROOT, 'data', 'campus_traffic.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'campus_traffic_schema.sql')

Table = namedtuple('Table', ['name_column', 'id_column', 'columns'])

# Table and column names are interpolated into SQL, so only these are accepted
TABLES = {
    'Building': Table('building_name', 'building_id',
                      ('building_name', 'name', 'outline')),
    'WalkwaySegment': Table('walkway_name', 'walkway_id',
                            ('walkway_name', 'boundary', 'allow_riders', 'allow_vehicles')),
    'Intersection': Table('intersection_name', 'intersection_id',
                          ('intersection_name', 'name', 'boundary')),
    'SensorNode': Table('sensor_name', 'sensor_id',
                        ('sensor_name', 'status', 'walkway_id', 'intersection_id')),
    'SpatialGridScan': Table('scan_name', 'scan_id',
                             ('scan_name', 'sensor_id', 'timestamp', 'grid_data')),
    'TrafficEvent': Table('event_name', 'event_id',
                          ('event_name', 'intersection_id', 'start_time', 'end_time',
                           'average_density', 'peak_density', 'peak_event_duration')),
}


def _table(table):
    if table not in TABLES:
        raise ValueError(f"Unknown table '{table}'")
    return TABLES[table]


def _check_columns(table, columns):
    unknown = set(columns) - set(_table(table).columns)
    if unknown:
        raise ValueError(f"Unknown column(s) for {table}: {', '.join(sorted(unknown))}")


class CampusDB:
    """Wrapper around the campus traffic SQLite database.

    Build one with CampusDB.open() for an existing database, or 
    CampusDB.in_memory() for an in memory database.

    This object does not close itself when it goes out of scope. Use inside 
    a `with` block:

        with CampusDB.open() as db:
            db.find('Intersection')

    If you can't use `with`, call db.close() yourself, e.g. in try/finally.
    """

    def __init__(self, conn):
        """Wrap an open sqlite3 connection.

        Args:
            conn: An open sqlite3.Connection. CampusDB takes ownership of it.
        """
        conn.isolation_level = None
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        self.conn = conn

    @classmethod
    def open(cls, path=DEFAULT_DB_PATH):
        """Open an existing database; raises FileNotFoundError if it is missing.

        Args:
            path: Path to the SQLite file (default DB path if omitted).
        """
        if path != ':memory:' and not os.path.exists(path):
            raise FileNotFoundError(
                f"No database found at {path}. Run scripts/database/create_db.py first."
            )
        return cls(sqlite3.connect(path))

    @classmethod
    def in_memory(cls, schema_path=SCHEMA_PATH):
        """Build a new in-memory database (intended for tests).

        Args:
            schema_path: SQL file to run on the new database (default project schema).
        """
        conn = sqlite3.connect(':memory:')
        with open(schema_path) as f:
            conn.executescript(f.read())
        return cls(conn)

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def __enter__(self) -> "CampusDB":
        return self

    def __exit__(self, *exc):
        self.close()

    @contextmanager
    def transaction(self):
        """Context manager running its block atomically. Rolls back on error."""
        if self.conn.in_transaction:
            yield
            return
        # IMMEDIATE takes the write lock up front so ID assignment can't race
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.conn.rollback()
            raise
        self.conn.commit()

    def get_by_id(self, table, row_id):
        """Return one row as a dict, or None if not found.

        Args:
            table: Table name to query.
            row_id: Serial ID value of the row.
        """
        spec = _table(table)
        row = self.conn.execute(
            f"SELECT * FROM {table} WHERE {spec.id_column} = ?", (row_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_by_name(self, table, name):
        """Return the row with the given name as a dict, or None if not found.

        Args:
            table: Table name to query.
            name: Value to match against the table's name column.
        """
        spec = _table(table)
        row = self.conn.execute(
            f"SELECT * FROM {table} WHERE {spec.name_column} = ?", (name,)
        ).fetchone()
        return dict(row) if row else None

    def find(self, table, **filters):
        """Return a list of row dicts matching all filters (every row if none given).

        Args:
            table: Table name to query.
            **filters: column=value pairs that rows must match.
        """
        spec = _table(table)
        _check_columns(table, filters)
        where = ' AND '.join(f"{column} = ?" for column in filters) or '1'
        rows = self.conn.execute(
            f"SELECT * FROM {table} WHERE {where} ORDER BY {spec.id_column}",
            tuple(filters.values()),
        )
        return [dict(row) for row in rows]

    def create(self, table, **values):
        """Insert a row and return its newly assigned ID.

        Args:
            table: Table to insert into.
            **values: column=value pairs for the new row (ID is assigned automatically).
        """
        spec = _table(table)
        _check_columns(table, values)
        with self.transaction():
            row = {spec.id_column: self._next_id(table), **values}
            columns = ', '.join(row)
            placeholders = ', '.join('?' for _ in row)
            self.conn.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                tuple(row.values()),
            )
        return row[spec.id_column]

    def get_or_create(self, table, **values):
        """Return (id, created) for the row with the given name, creating it if absent.

        Args:
            table: Table to search and insert into.
            **values: column=value pairs; must include the name column, used for lookup.
        """
        spec = _table(table)
        with self.transaction():
            existing = self.get_by_name(table, values[spec.name_column])
            if existing:
                return existing[spec.id_column], False
            return self.create(table, **values), True

    def update(self, table, row_id, **values):
        """Update columns on one row. Return True if a row was changed.

        Args:
            table: Table containing the row.
            row_id: Primary key value of the row to update.
            **values: column=value pairs to set.
        """
        spec = _table(table)
        _check_columns(table, values)
        if not values:
            return False
        assignments = ', '.join(f"{column} = ?" for column in values)
        with self.transaction():
            cursor = self.conn.execute(
                f"UPDATE {table} SET {assignments} WHERE {spec.id_column} = ?",
                (*values.values(), row_id),
            )
        return cursor.rowcount > 0

    def delete(self, table, row_id):
        """Delete one row. Return True if a row was removed.

        Args:
            table: Table containing the row.
            row_id: Primary key value of the row to delete.
        """
        spec = _table(table)
        with self.transaction():
            cursor = self.conn.execute(
                f"DELETE FROM {table} WHERE {spec.id_column} = ?", (row_id,)
            )
        return cursor.rowcount > 0

    def link_walkway_intersection(self, walkway_id, intersection_id):
        """Link a walkway to an intersection. Return True if newly linked.

        Args:
            walkway_id: ID of the walkway segment.
            intersection_id: ID of the intersection.
        """
        with self.transaction():
            cursor = self.conn.execute(
                "INSERT OR IGNORE INTO Walkway_Intersection (walkway_id, intersection_id) "
                "VALUES (?, ?)",
                (walkway_id, intersection_id),
            )
        return cursor.rowcount > 0

    def unlink_walkway_intersection(self, walkway_id, intersection_id):
        """Remove a walkway-intersection link. Return True if one existed.

        Args:
            walkway_id: ID of the walkway segment.
            intersection_id: ID of the intersection.
        """
        with self.transaction():
            cursor = self.conn.execute(
                "DELETE FROM Walkway_Intersection "
                "WHERE walkway_id = ? AND intersection_id = ?",
                (walkway_id, intersection_id),
            )
        return cursor.rowcount > 0

    def intersections_for_walkway(self, walkway_id):
        """Return all intersections (as dicts) linked to a walkway.

        Args:
            walkway_id: ID of the walkway segment.
        """
        rows = self.conn.execute(
            "SELECT i.* FROM Intersection i "
            "JOIN Walkway_Intersection wi ON wi.intersection_id = i.intersection_id "
            "WHERE wi.walkway_id = ? ORDER BY i.intersection_id",
            (walkway_id,),
        )
        return [dict(row) for row in rows]

    def walkways_for_intersection(self, intersection_id):
        """Return all walkway segments (as dicts) linked to an intersection.

        Args:
            intersection_id: ID of the intersection.
        """
        rows = self.conn.execute(
            "SELECT w.* FROM WalkwaySegment w "
            "JOIN Walkway_Intersection wi ON wi.walkway_id = w.walkway_id "
            "WHERE wi.intersection_id = ? ORDER BY w.walkway_id",
            (intersection_id,),
        )
        return [dict(row) for row in rows]

    def _next_id(self, table):
        # SQLite does not auto-increment SERIAL columns, so IDs are assigned here.
        id_column = _table(table).id_column
        query = f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM {table}"
        return self.conn.execute(query).fetchone()[0]
