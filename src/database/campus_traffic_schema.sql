-- Schema Definition for LiDAR Foot Traffic Monitoring
-- This Schema is not to be used in the actual system, it is simply the source of 
-- truth for the database design and will be used to generate the actual database schema.

CREATE TABLE Building (
    building_name VARCHAR(255) PRIMARY KEY,
    building_id SERIAL UNIQUE,
    name VARCHAR(255) NOT NULL,
    outline GEOMETRY
);

CREATE TABLE WalkwaySegment (
    walkway_name VARCHAR(255) PRIMARY KEY,
    walkway_id SERIAL UNIQUE,
    boundary GEOMETRY,
    allow_riders BOOLEAN,
    allow_vehicles BOOLEAN
);

CREATE TABLE Intersection (
    intersection_name VARCHAR(255) PRIMARY KEY,
    intersection_id SERIAL UNIQUE,
    name VARCHAR(255),
    boundary GEOMETRY
);

CREATE TABLE Walkway_Intersection (
    walkway_id INTEGER NOT NULL,
    intersection_id INTEGER NOT NULL,
    PRIMARY KEY (walkway_id, intersection_id),
    FOREIGN KEY (walkway_id) REFERENCES WalkwaySegment(walkway_id) ON DELETE CASCADE,
    FOREIGN KEY (intersection_id) REFERENCES Intersection(intersection_id) ON DELETE CASCADE
);

CREATE TABLE SensorNode (
    sensor_name VARCHAR(255) PRIMARY KEY,
    sensor_id SERIAL UNIQUE,
    status VARCHAR(50),
    walkway_id INTEGER,
    intersection_id INTEGER,
    FOREIGN KEY (walkway_id) REFERENCES WalkwaySegment(walkway_id) ON DELETE SET NULL,
    FOREIGN KEY (intersection_id) REFERENCES Intersection(intersection_id) ON DELETE SET NULL,
    CONSTRAINT chk_sensor_location CHECK (
        (walkway_id IS NOT NULL AND intersection_id IS NULL) OR 
        (walkway_id IS NULL AND intersection_id IS NOT NULL)
    )
);

CREATE TABLE SpatialGridScan (
    scan_name VARCHAR(255) PRIMARY KEY,
    scan_id SERIAL UNIQUE,
    sensor_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    grid_data BYTEA,
    FOREIGN KEY (sensor_id) REFERENCES SensorNode(sensor_id) ON DELETE CASCADE
);

CREATE TABLE TrafficEvent (
    event_name VARCHAR(255) PRIMARY KEY,
    event_id SERIAL UNIQUE,
    intersection_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    average_density NUMERIC,
    peak_density NUMERIC,
    peak_event_duration INTEGER,
    FOREIGN KEY (intersection_id) REFERENCES Intersection(intersection_id) ON DELETE CASCADE
);
