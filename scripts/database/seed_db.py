#!/usr/bin/env python3
import os
import sqlite3
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, os.path.join(WORKING_DIR, 'src'))

from database import CampusDB, DEFAULT_DB_PATH

TEST_PREFIX = 'TEST_'
TEST_TIME = '2000-01-01 00:00:00'
TEST_END_TIME = '2000-01-01 00:05:00'
TEST_POLYGON = 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'


def seed(db):
    results = []

    def seed_row(table, **values):
        row_id, created = db.get_or_create(table, **values)
        results.append((table, next(iter(values.values())), created))
        return row_id

    seed_row('Building',
             building_name=f'{TEST_PREFIX}building',
             name='TEST Building (fake seed data)',
             outline=TEST_POLYGON)

    walkway_id = seed_row('WalkwaySegment',
                          walkway_name=f'{TEST_PREFIX}walkway',
                          boundary=TEST_POLYGON,
                          allow_riders=True,
                          allow_vehicles=False)

    intersection_id = seed_row('Intersection',
                               intersection_name=f'{TEST_PREFIX}intersection',
                               name='TEST Intersection (fake seed data)',
                               boundary=TEST_POLYGON)

    linked = db.link_walkway_intersection(walkway_id, intersection_id)
    results.append(('Walkway_Intersection', 'test link', linked))

    sensor_id = seed_row('SensorNode',
                         sensor_name=f'{TEST_PREFIX}sensor',
                         status='TEST',
                         walkway_id=walkway_id,
                         intersection_id=None)

    seed_row('SpatialGridScan',
             scan_name=f'{TEST_PREFIX}scan',
             sensor_id=sensor_id,
             timestamp=TEST_TIME,
             grid_data=b'TEST_GRID_DATA')

    seed_row('TrafficEvent',
             event_name=f'{TEST_PREFIX}event',
             intersection_id=intersection_id,
             start_time=TEST_TIME,
             end_time=TEST_END_TIME,
             average_density=0.5,
             peak_density=1.0,
             peak_event_duration=60)

    return results


def main():
    try:
        with CampusDB.open(DEFAULT_DB_PATH) as db, db.transaction():
            results = seed(db)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except sqlite3.Error as e:
        print(f"An error occurred, no test rows were saved: {e}")
        sys.exit(1)

    for table, name, created in results:
        print(f"{table}: inserted '{name}'." if created else f"{table}: '{name}' already exists, skipping.")
    print("Seeding complete.")


if __name__ == "__main__":
    main()
