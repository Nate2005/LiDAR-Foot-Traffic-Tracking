"""FastAPI backend for the campus map frontend.

nginx forwards /api/* to this app with the /api prefix stripped, so the
frontend calls e.g. `fetch("/api/buildings")` and this app sees /buildings.

Run (from the backend/ folder; sets up .venv and the database first, see README):

    scripts/run_backend.sh
"""
import json
import os
import sqlite3
from typing import Annotated, Literal, NamedTuple, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field, field_validator

from database import CampusDB, DEFAULT_DB_PATH, TABLES


# --- GeoJSON geometry models (RFC 7946, positions are [longitude, latitude]) ---

Position = Annotated[list[float], Field(min_length=2, max_length=3)]
LinearRing = Annotated[list[Position], Field(min_length=4)]
LineCoordinates = Annotated[list[Position], Field(min_length=2)]


def _check_rings_closed(polygons):
    for rings in polygons:
        for ring in rings:
            if ring[0] != ring[-1]:
                raise ValueError("each linear ring must start and end at the same position")


class Point(BaseModel):
    type: Literal['Point']
    coordinates: Position


class LineString(BaseModel):
    type: Literal['LineString']
    coordinates: LineCoordinates


class MultiLineString(BaseModel):
    type: Literal['MultiLineString']
    coordinates: Annotated[list[LineCoordinates], Field(min_length=1)]


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
PathwayShape = Annotated[Union[LineString, MultiLineString, Polygon, MultiPolygon],
                         Field(discriminator='type')]
IntersectionShape = Annotated[Union[Point, Polygon, MultiPolygon],
                              Field(discriminator='type')]


# --- Buildings ---

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


# --- Pathway segments ---

PATHWAY_NAME_DOC = "Unique pathway segment name, e.g. 'Quad north walk'"
BOUNDARY_DOC = "GeoJSON LineString, MultiLineString, Polygon or MultiPolygon geometry"
RIDERS_DOC = "Bikes, scooters and skateboards may use this segment"
VEHICLES_DOC = "Vehicles may use this segment"
ADA_DOC = "No stairs or other non-ADA-compliant features (unverified segments: false)"


class PathwayIn(BaseModel):
    pathway_name: str = Field(min_length=1, description=PATHWAY_NAME_DOC)
    boundary: Optional[PathwayShape] = Field(default=None, description=BOUNDARY_DOC)
    allow_riders: bool = Field(default=False, description=RIDERS_DOC)
    allow_vehicles: bool = Field(default=False, description=VEHICLES_DOC)
    ada_accessible: bool = Field(default=False, description=ADA_DOC)


class PathwayPatch(BaseModel):
    pathway_name: Optional[str] = Field(default=None, min_length=1, description=PATHWAY_NAME_DOC)
    boundary: Optional[PathwayShape] = Field(default=None, description=BOUNDARY_DOC)
    allow_riders: Optional[bool] = Field(default=None, description=RIDERS_DOC)
    allow_vehicles: Optional[bool] = Field(default=None, description=VEHICLES_DOC)
    ada_accessible: Optional[bool] = Field(default=None, description=ADA_DOC)


class PathwayOut(BaseModel):
    pathway_id: int
    pathway_name: str = Field(description=PATHWAY_NAME_DOC)
    boundary: Optional[PathwayShape] = Field(default=None, description=BOUNDARY_DOC)
    allow_riders: Optional[bool] = Field(default=None, description=RIDERS_DOC)
    allow_vehicles: Optional[bool] = Field(default=None, description=VEHICLES_DOC)
    ada_accessible: bool = Field(description=ADA_DOC)


# --- Intersections ---

INTERSECTION_NAME_DOC = "Unique intersection key, e.g. 'quad-north'"
DISPLAY_NAME_DOC = "Optional display name, e.g. 'North end of the Quad'"
AREA_DOC = "GeoJSON Point, Polygon or MultiPolygon geometry"


class IntersectionIn(BaseModel):
    intersection_name: str = Field(min_length=1, description=INTERSECTION_NAME_DOC)
    name: Optional[str] = Field(default=None, description=DISPLAY_NAME_DOC)
    boundary: Optional[IntersectionShape] = Field(default=None, description=AREA_DOC)


class IntersectionPatch(BaseModel):
    intersection_name: Optional[str] = Field(default=None, min_length=1,
                                             description=INTERSECTION_NAME_DOC)
    name: Optional[str] = Field(default=None, description=DISPLAY_NAME_DOC)
    boundary: Optional[IntersectionShape] = Field(default=None, description=AREA_DOC)


class IntersectionOut(BaseModel):
    intersection_id: int
    intersection_name: str = Field(description=INTERSECTION_NAME_DOC)
    name: Optional[str] = Field(default=None, description=DISPLAY_NAME_DOC)
    boundary: Optional[IntersectionShape] = Field(default=None, description=AREA_DOC)


# --- Shared row handling ---

class Resource(NamedTuple):
    """How one table is exposed over the API."""
    table: str
    label: str              # used in error messages, e.g. 'Building'
    geometry: str           # column holding GeoJSON text
    not_null: tuple         # PATCH fields where null means "leave as is"


BUILDING = Resource('Building', 'Building', 'outline', ('building_name', 'building_code'))
PATHWAY = Resource('PathwaySegment', 'Pathway', 'boundary',
                   ('pathway_name', 'allow_riders', 'allow_vehicles', 'ada_accessible'))
INTERSECTION = Resource('Intersection', 'Intersection', 'boundary', ('intersection_name',))


def _to_db(resource, values):
    """Serialize the GeoJSON geometry to text for storage."""
    if values.get(resource.geometry) is not None:
        values[resource.geometry] = json.dumps(values[resource.geometry])
    return values


def _from_db(resource, row):
    """Parse the stored GeoJSON geometry text back into an object."""
    if row is not None and row.get(resource.geometry) is not None:
        row[resource.geometry] = json.loads(row[resource.geometry])
    return row


def _conflict(resource, error):
    """Turn an IntegrityError into a 409, naming the clashing field when it is UNIQUE."""
    message = str(error)
    for column in TABLES[resource.table].columns:
        if f"{resource.table}.{column}" in message:
            return HTTPException(status_code=409, detail=f"{column} already exists")
    if 'chk_sensor_location' in message:
        return HTTPException(status_code=409, detail=(
            f"{resource.label} has a sensor attached; move or delete the sensor first"))
    return HTTPException(status_code=409,
                         detail=f"{resource.label} conflicts with an existing row")


def _get_or_404(db, resource, row_id):
    row = _from_db(resource, db.get_by_id(resource.table, row_id))
    if row is None:
        raise HTTPException(status_code=404, detail=f"{resource.label} not found")
    return row


def _create(db, resource, body):
    try:
        row_id = db.create(resource.table, **_to_db(resource, body.model_dump()))
    except sqlite3.IntegrityError as error:
        raise _conflict(resource, error)
    return _get_or_404(db, resource, row_id)


def _patch(db, resource, row_id, changes):
    _get_or_404(db, resource, row_id)
    values = changes.model_dump(exclude_unset=True)
    for field in resource.not_null:
        if values.get(field) is None:
            values.pop(field, None)
    try:
        db.update(resource.table, row_id, **_to_db(resource, values))
    except sqlite3.IntegrityError as error:
        raise _conflict(resource, error)
    return _get_or_404(db, resource, row_id)


def _delete(db, resource, row_id):
    try:
        deleted = db.delete(resource.table, row_id)
    except sqlite3.IntegrityError as error:
        raise _conflict(resource, error)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"{resource.label} not found")
    return Response(status_code=204)


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


def create_app(db_path=DEFAULT_DB_PATH):
    """Build the FastAPI app.

    Args:
        db_path: SQLite file to serve. Inject a temp database in tests.
    """
    app = FastAPI(title="UNR Walking Map API")
    app.state.db_path = db_path

    # --- Buildings ---

    @app.get('/buildings', response_model=list[BuildingOut], tags=['buildings'])
    def list_buildings(
        q: Optional[str] = Query(
            default=None,
            description="Search text matched against full name and building code, "
                        "ignoring case, e.g. 'sem' or 'davidson'. Omit to list all."),
        db: CampusDB = Depends(get_db),
    ):
        text = (q or '').strip()
        rows = db.search_buildings(text) if text else db.find('Building')
        return [_from_db(BUILDING, row) for row in rows]

    @app.get('/buildings/{building_id}', response_model=BuildingOut, tags=['buildings'])
    def get_building(building_id: int, db: CampusDB = Depends(get_db)):
        return _get_or_404(db, BUILDING, building_id)

    @app.post('/buildings', response_model=BuildingOut, status_code=201, tags=['buildings'])
    def create_building(building: BuildingIn, db: CampusDB = Depends(get_db)):
        return _create(db, BUILDING, building)

    @app.patch('/buildings/{building_id}', response_model=BuildingOut, tags=['buildings'])
    def update_building(building_id: int, changes: BuildingPatch,
                        db: CampusDB = Depends(get_db)):
        return _patch(db, BUILDING, building_id, changes)

    @app.delete('/buildings/{building_id}', status_code=204, tags=['buildings'])
    def delete_building(building_id: int, db: CampusDB = Depends(get_db)):
        return _delete(db, BUILDING, building_id)

    # --- Pathways ---

    @app.get('/pathways', response_model=list[PathwayOut], tags=['pathways'])
    def list_pathways(
        ada_accessible: Optional[bool] = Query(default=None, description=ADA_DOC),
        allow_riders: Optional[bool] = Query(default=None, description=RIDERS_DOC),
        allow_vehicles: Optional[bool] = Query(default=None, description=VEHICLES_DOC),
        db: CampusDB = Depends(get_db),
    ):
        filters = {column: value for column, value in (
            ('ada_accessible', ada_accessible),
            ('allow_riders', allow_riders),
            ('allow_vehicles', allow_vehicles),
        ) if value is not None}
        return [_from_db(PATHWAY, row) for row in db.find('PathwaySegment', **filters)]

    @app.get('/pathways/{pathway_id}', response_model=PathwayOut, tags=['pathways'])
    def get_pathway(pathway_id: int, db: CampusDB = Depends(get_db)):
        return _get_or_404(db, PATHWAY, pathway_id)

    @app.post('/pathways', response_model=PathwayOut, status_code=201, tags=['pathways'])
    def create_pathway(pathway: PathwayIn, db: CampusDB = Depends(get_db)):
        return _create(db, PATHWAY, pathway)

    @app.patch('/pathways/{pathway_id}', response_model=PathwayOut, tags=['pathways'])
    def update_pathway(pathway_id: int, changes: PathwayPatch,
                       db: CampusDB = Depends(get_db)):
        return _patch(db, PATHWAY, pathway_id, changes)

    @app.delete('/pathways/{pathway_id}', status_code=204, tags=['pathways'])
    def delete_pathway(pathway_id: int, db: CampusDB = Depends(get_db)):
        return _delete(db, PATHWAY, pathway_id)

    # --- Intersections ---

    @app.get('/intersections', response_model=list[IntersectionOut], tags=['intersections'])
    def list_intersections(db: CampusDB = Depends(get_db)):
        return [_from_db(INTERSECTION, row) for row in db.find('Intersection')]

    @app.get('/intersections/{intersection_id}', response_model=IntersectionOut,
             tags=['intersections'])
    def get_intersection(intersection_id: int, db: CampusDB = Depends(get_db)):
        return _get_or_404(db, INTERSECTION, intersection_id)

    @app.post('/intersections', response_model=IntersectionOut, status_code=201,
              tags=['intersections'])
    def create_intersection(intersection: IntersectionIn, db: CampusDB = Depends(get_db)):
        return _create(db, INTERSECTION, intersection)

    @app.patch('/intersections/{intersection_id}', response_model=IntersectionOut,
               tags=['intersections'])
    def update_intersection(intersection_id: int, changes: IntersectionPatch,
                            db: CampusDB = Depends(get_db)):
        return _patch(db, INTERSECTION, intersection_id, changes)

    @app.delete('/intersections/{intersection_id}', status_code=204, tags=['intersections'])
    def delete_intersection(intersection_id: int, db: CampusDB = Depends(get_db)):
        return _delete(db, INTERSECTION, intersection_id)

    # --- Pathway <-> intersection links (the routing graph) ---

    @app.get('/pathways/{pathway_id}/intersections', response_model=list[IntersectionOut],
             tags=['links'])
    def intersections_for_pathway(pathway_id: int, db: CampusDB = Depends(get_db)):
        _get_or_404(db, PATHWAY, pathway_id)
        return [_from_db(INTERSECTION, row) for row in db.intersections_for_pathway(pathway_id)]

    @app.get('/intersections/{intersection_id}/pathways', response_model=list[PathwayOut],
             tags=['links'])
    def pathways_for_intersection(intersection_id: int, db: CampusDB = Depends(get_db)):
        _get_or_404(db, INTERSECTION, intersection_id)
        return [_from_db(PATHWAY, row) for row in db.pathways_for_intersection(intersection_id)]

    @app.put('/pathways/{pathway_id}/intersections/{intersection_id}', status_code=204,
             tags=['links'])
    def link(pathway_id: int, intersection_id: int, db: CampusDB = Depends(get_db)):
        """Connect a pathway to an intersection. Linking twice is not an error."""
        _get_or_404(db, PATHWAY, pathway_id)
        _get_or_404(db, INTERSECTION, intersection_id)
        db.link_pathway_intersection(pathway_id, intersection_id)
        return Response(status_code=204)

    @app.delete('/pathways/{pathway_id}/intersections/{intersection_id}', status_code=204,
                tags=['links'])
    def unlink(pathway_id: int, intersection_id: int, db: CampusDB = Depends(get_db)):
        if not db.unlink_pathway_intersection(pathway_id, intersection_id):
            raise HTTPException(status_code=404, detail="Link not found")
        return Response(status_code=204)

    return app


app = create_app()
