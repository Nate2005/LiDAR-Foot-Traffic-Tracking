-- Schema Definition for LiDAR Foot Traffic Monitoring
-- This Schema is not to be used in the actual system, it is simply the source of 
-- truth for the database design and will be used to generate the actual database schema.
--
-- GEOMETRY columns store a GeoJSON geometry object as text
--
-- Naming convention:   `<table>_name` primary human chosen key (e.g. 'Scrugham Engineering and Mines') 
--                      `<table>_id` used for foreign keys and API URLs
--                      `building_code` is the short code (e.g. 'SEM')

CREATE TABLE Building (
    building_name VARCHAR(255) PRIMARY KEY,
    building_id SERIAL UNIQUE,
    building_code VARCHAR(255) NOT NULL UNIQUE,
    outline GEOMETRY
);

CREATE TABLE PathwaySegment (
    pathway_name VARCHAR(255) PRIMARY KEY,
    pathway_id SERIAL UNIQUE,
    boundary GEOMETRY,
    allow_riders BOOLEAN,
    allow_vehicles BOOLEAN,
    ada_accessible BOOLEAN NOT NULL DEFAULT FALSE CHECK (ada_accessible IN (0, 1))
);

CREATE TABLE Intersection (
    intersection_name VARCHAR(255) PRIMARY KEY,
    intersection_id SERIAL UNIQUE,
    name VARCHAR(255),
    boundary GEOMETRY
);

CREATE TABLE Pathway_Intersection (
    pathway_id INTEGER NOT NULL,
    intersection_id INTEGER NOT NULL,
    PRIMARY KEY (pathway_id, intersection_id),
    FOREIGN KEY (pathway_id) REFERENCES PathwaySegment(pathway_id) ON DELETE CASCADE,
    FOREIGN KEY (intersection_id) REFERENCES Intersection(intersection_id) ON DELETE CASCADE
);

CREATE TABLE SensorNode (
    sensor_name VARCHAR(255) PRIMARY KEY,
    sensor_id SERIAL UNIQUE,
    status VARCHAR(50),
    pathway_id INTEGER,
    intersection_id INTEGER,
    FOREIGN KEY (pathway_id) REFERENCES PathwaySegment(pathway_id) ON DELETE SET NULL,
    FOREIGN KEY (intersection_id) REFERENCES Intersection(intersection_id) ON DELETE SET NULL,
    CONSTRAINT chk_sensor_location CHECK (
        (pathway_id IS NOT NULL AND intersection_id IS NULL) OR 
        (pathway_id IS NULL AND intersection_id IS NOT NULL)
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
