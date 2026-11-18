"""FastAPI backend for the campus map frontend.

nginx forwards /api/* to this app with the /api prefix stripped, so the
frontend calls e.g. `fetch("/api/buildings")` and this app sees /buildings.

Run (from the repo root; sets up .venv and the database first, see README):

    scripts/run_backend.sh
"""
import json
import os
import sqlite3
from typing import Annotated, Literal, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field, field_validator

from database import CampusDB, DEFAULT_DB_PATH


Position = Annotated[list[float], Field(min_length=2, max_length=3)]
LinearRing = Annotated[list[Position], Field(min_length=4)]


def _check_rings_closed(polygons):
    for rings in polygons:
        for ring in rings:
            if ring[0] != ring[-1]:
                raise ValueError("each linear ring must start and end at the same position")


class Polygon(BaseModel):
    type: Literal['Polygon']
    coordinates: Annotated[list[LinearRing], Field(min_length=1)]

    @field_validator('coordinates')
    @classmethod
    def rings_closed(cls, coordinates):
        _check_rings_closed([coordinates])
        return coordinates


class MultiPolygon(BaseModel):
    type: Literal['MultiPolygon']
    coordinates: Annotated[list[Annotated[list[LinearRing], Field(min_length=1)]],
                           Field(min_length=1)]

    @field_validator('coordinates')
    @classmethod
    def rings_closed(cls, coordinates):
        _check_rings_closed(coordinates)
        return coordinates


Footprint = Annotated[Union[Polygon, MultiPolygon], Field(discriminator='type')]


NAME_DOC = "Full building name (unique), e.g. 'Scrugham Engineering and Mines'"
CODE_DOC = "Building code (unique), e.g. 'SEM'"
OUTLINE_DOC = "Footprint as a GeoJSON Polygon or MultiPolygon geometry"


class BuildingIn(BaseModel):
    building_name: str = Field(min_length=1, description=NAME_DOC)
    building_code: str = Field(min_length=1, description=CODE_DOC)
    outline: Optional[Footprint] = Field(default=None, description=OUTLINE_DOC)


class BuildingPatch(BaseModel):
    building_name: Optional[str] = Field(default=None, min_length=1, description=NAME_DOC)
    building_code: Optional[str] = Field(default=None, min_length=1, description=CODE_DOC)
    outline: Optional[Footprint] = Field(default=None, description=OUTLINE_DOC)


class BuildingOut(BaseModel):
    building_id: int
    building_name: str = Field(description=NAME_DOC)
    building_code: str = Field(description=CODE_DOC)
    outline: Optional[Footprint] = Field(default=None, description=OUTLINE_DOC)


def _to_db(values):
    """Serialize the GeoJSON outline to text for storage."""
    if values.get('outline') is not None:
        values['outline'] = json.dumps(values['outline'])
    return values


def _from_db(row):
    """Parse the stored GeoJSON outline text back into an object."""
    if row is not None and row.get('outline') is not None:
        row['outline'] = json.loads(row['outline'])
    return row


def get_db(request: Request):
    """Open one CampusDB connection per request."""
    path = request.app.state.db_path
    if not os.path.exists(path):
        raise HTTPException(status_code=503, detail="Database is not available")
    # fastapi may run dependency and endpoint on different threads
    db = CampusDB(sqlite3.connect(path, check_same_thread=False))
    try:
        yield db
    finally:
        db.close()


def _conflict(error):
    """Turn a UNIQUE constraint IntegrityError into a 409 naming the clashing field."""
    if f"Building.building_code" in str(error):
        return HTTPException(status_code=409, detail="building_code already exists")
    if f"Building.building_name" in str(error):
        return HTTPException(status_code=409, detail="building_name already exists")
    return HTTPException(status_code=409, detail="Building conflicts with an existing row")


def _building_or_404(db, building_id):
    row = _from_db(db.get_by_id('Building', building_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return row


def create_app(db_path=DEFAULT_DB_PATH):
    """Build the FastAPI app.

    Args:
        db_path: SQLite file to serve. Inject a temp database in tests.
    """
    app = FastAPI(title="UNR Walking Map API")
    app.state.db_path = db_path

    @app.get('/buildings', response_model=list[BuildingOut])
    def list_buildings(
        q: Optional[str] = Query(
            default=None,
            description="Search text matched against full name and building code, "
                        "ignoring case, e.g. 'sem' or 'davidson'. Omit to list all."),
        db: CampusDB = Depends(get_db),
    ):
        text = (q or '').strip()
        rows = db.search_buildings(text) if text else db.find('Building')
        return [_from_db(row) for row in rows]

    @app.get('/buildings/{building_id}', response_model=BuildingOut)
    def get_building(building_id: int, db: CampusDB = Depends(get_db)):
        return _building_or_404(db, building_id)

    @app.post('/buildings', response_model=BuildingOut, status_code=201)
    def create_building(building: BuildingIn, db: CampusDB = Depends(get_db)):
        try:
            building_id = db.create('Building', **_to_db(building.model_dump()))
        except sqlite3.IntegrityError as error:
            raise _conflict(error)
        return _building_or_404(db, building_id)

    @app.patch('/buildings/{building_id}', response_model=BuildingOut)
    def update_building(building_id: int, changes: BuildingPatch,
                        db: CampusDB = Depends(get_db)):
        _building_or_404(db, building_id)
        values = changes.model_dump(exclude_unset=True)
        # building_name and building_code are required; a null means "leave as is"
        for field in ('building_name', 'building_code'):
            if values.get(field) is None:
                values.pop(field, None)
        try:
            db.update('Building', building_id, **_to_db(values))
        except sqlite3.IntegrityError as error:
            raise _conflict(error)
        return _building_or_404(db, building_id)

    @app.delete('/buildings/{building_id}', status_code=204)
    def delete_building(building_id: int, db: CampusDB = Depends(get_db)):
        if not db.delete('Building', building_id):
            raise HTTPException(status_code=404, detail="Building not found")
        return Response(status_code=204)

    return app


app = create_app()
