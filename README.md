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

Linux only. From the repo root:

| Task | Command |
|---|---|
| Run the API (sets up `.venv` and the database on first run) | `scripts/run_backend.sh` |
| Add test rows to the database | `.venv/bin/python scripts/database/seed_db.py` |
| Archive the current database | `bash scripts/database/archive_db.sh` |
| Run the tests | `.venv/bin/python -m pytest` |

The API runs at <http://127.0.0.1:8000>, with interactive docs at <http://127.0.0.1:8000/docs>.

## Documentation

| Doc | Contents |
|---|---|
| [`docs/api.md`](docs/api.md) | Backend API endpoints, formats and examples |
| [`docs/STRUCTURE.md`](docs/STRUCTURE.md) | Repository layout, conventions and ownership |

## Repository map

| Path | Contents |
|---|---|
| `src/api/` | FastAPI backend |
| `src/database/` | Database code and schema |
| `scripts/` | Run and database management scripts |
| `tests/` | pytest tests |
| `data/`, `archive/` | Runtime and archived databases |
| `docs/` | All documentation |
