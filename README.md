# LiDAR Foot Traffic Tracking

## Course Information

| | |
|---|---|
| **College** | University of Nevada, Reno |
| **Course** | Computer Science and Engineering Capstone |
| **Term** | Fall 2026 to Spring 2027 |
| **Instructor(s)** | Erin Keith, Zach Estreito |
| **Advisor** | TBD |

## Authors

- Andre Jimenez
- Nathan Biggs
- Matthew Amorelli
- Samuel Landaverde

## Backend

Linux only. From the `backend/` folder:

| Task | Command |
|---|---|
| Run the API (sets up `.venv` and the database on first run) | `scripts/run_backend.sh` |
| Add test rows to the database | `.venv/bin/python scripts/seed_db.py` |
| Archive the current database | `bash scripts/archive_db.sh` |
| Run the tests | `.venv/bin/python -m pytest` |

The API runs at <http://127.0.0.1:8000>, with interactive docs at <http://127.0.0.1:8000/docs>.

## Documentation

| Doc | Contents |
|---|---|
| [`docs/api.md`](docs/api.md) | Backend API endpoints, formats and examples |
| [`docs/STRUCTURE.md`](docs/STRUCTURE.md) | Repository layout, conventions and ownership |
| [`docs/frontend.md`](docs/frontend.md) | Building the map site, map tiles and deploying |

## Repository map

| Path | Contents |
|---|---|
| `firmware/` | ESP32 LiDAR scanner code |
| `frontend/` | Vue + Vite map site |
| `backend/` | Python services (API, database, ingest, monitoring), scripts and tests |
| `map/` | Map tile pipeline |
| `deploy/` | nginx config and frontend build/deploy scripts |
| `prototypes/` | Old throwaway code |
| `docs/` | All documentation |
