#!/usr/bin/env bash

# Define paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
WORKING_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DATA_DIR="$WORKING_DIR/data"
ARCHIVE_DIR="$WORKING_DIR/archive"
DB_PATH="$DATA_DIR/campus_traffic.db"

mkdir -p "$ARCHIVE_DIR"

if [ ! -f "$DB_PATH" ]; then
    echo "No active database found at $DB_PATH to archive."
    exit 0
fi

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_PATH="$ARCHIVE_DIR/campus_traffic_$TIMESTAMP.db"

echo "Archiving current database to $ARCHIVE_PATH..."
mv "$DB_PATH" "$ARCHIVE_PATH"

if [ $? -eq 0 ]; then
    echo "Database successfully archived."
else
    echo "Error occurred while archiving the database."
    exit 1
fi
