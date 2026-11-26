# Repository Structure

This is the file layout everyone uses. Each part of the system gets one top-level folder, so people can work in parallel without touching each other's files.

## Layout

```
LiDAR-Foot-Traffic-Tracking/
├── README.md  LICENSE  .gitignore  .gitattributes  .editorconfig
├── THIRD_PARTY_LICENSES.txt
├── docs/                         all documentation: STRUCTURE.md, api.md, frontend.md, design docs
│
├── firmware/                     ESP32 code
│   └── lidar_scanner/lidar_scanner.ino
│
├── frontend/                     Vue + Vite map site
│   ├── package.json  package-lock.json  index.html  env.d.ts
│   ├── vite.config.ts  vitest.config.ts  tsconfig*.json
│   ├── eslint.config.ts  .oxlintrc.json  .prettierrc.json  .gitignore
│   ├── public/
│   └── src/
│       ├── App.vue  main.ts
│       └── {components,views,services,stores,types,data,styles,router,__tests__}
│
├── backend/                      every Python service that runs on the Pi
│   ├── pyproject.toml            dependencies + pytest config (pythonpath = ["src"])
│   ├── src/
│   │   ├── database/             __init__.py, campus_db.py, schema.sql (the only schema)
│   │   ├── api/                  __init__.py, main.py: FastAPI app, port 8000, served at /api/
│   │   ├── ingest/               listener.py: sensor listener, port 8001, served at /data/
│   │   ├── processing/           LiDAR scan -> counts/density grids
│   │   └── monitoring/           monitor.py: Pi health checks and alerts
│   ├── scripts/                  create_db.py, seed_db.py, archive_db.sh, run_backend.sh
│   ├── tests/
│   │   ├── unit/                 test_api_buildings.py, test_campus_db.py, test_pathway_ada.py,
│   │   │                         test_listener.py
│   │   └── integration/
│   ├── data/                     runtime campus_traffic.db (gitignored; README placeholder)
│   └── archive/                  archived databases (gitignored; README placeholder)
│
├── map/                          map tile pipeline
│   ├── config/                   config-unr.json, process.lua
│   ├── scripts/create_map_tiles.py
│   └── out/                      generated tiles (gitignored, except .gitkeep)
│
├── deploy/                       anything that configures the Pi
│   ├── nginx/unrwalkingmap.conf
│   ├── systemd/                  api.service, ingest.service, monitor.service
│   ├── cloudflared/
│   └── scripts/                  build_frontend.py, deploy_frontend.py
│
└── prototypes/                   old throwaway code (optional; may be deleted)
    └── test_website/             backend/{main.py, test_main.py}, frontend/{index.html, script.js}
```

## Rules

- **Folder and file names are lowercase snake_case.** Never have two names that differ only by case (for example `Scripts/` and `scripts/`). macOS and Windows treat them as the same folder.

- **There is one database schema:** `backend/src/database/schema.sql`. All Python code reads and writes the database through `CampusDB`. No other module runs raw SQL against the database file.

- **`api`, `ingest`, `processing` and `monitoring` are separate packages.** They may import `database` but must not import each other.

- **Python tests use pytest** and live in `backend/tests/`. Use the `pythonpath` setting in `pyproject.toml` instead of `sys.path` hacks. Pass dependencies such as database connections and paths in as arguments, so the code can be tested.

- **Documentation lives in `docs/`.** The only README outside it is the root `README.md`, which GitHub shows on the repo page. A short placeholder README is fine in a folder that would otherwise be empty, such as `backend/data/`, so Git keeps tracking that folder.

- **Generated files are never committed:** `dist/`, `map/out/`, `*.db`, `.venv/`, `node_modules/`, `.DS_Store`.

- **Scripts find paths relative to their own location** (`Path(__file__).resolve().parent`), never relative to the current working directory.