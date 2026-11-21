import json
import os
import sqlite3
import sys

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'src'))

from api import create_app
from database import CampusDB, SCHEMA_PATH

SEM_NAME = 'Scrugham Engineering and Mines'
DMSC_NAME = 'Davidson Mathematics and Science Center'

RING = [[-119.812960, 39.539794], [-119.813061, 39.540125], [-119.813923, 39.539963],
        [-119.813861, 39.539768], [-119.814197, 39.539707], [-119.814086, 39.539355],
        [-119.813905, 39.539389], [-119.813972, 39.539603], [-119.812960, 39.539794]]
POLYGON = {'type': 'Polygon', 'coordinates': [RING]}
MULTIPOLYGON = {'type': 'MultiPolygon', 'coordinates': [[RING], [RING]]}


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / 'campus.db'
    with open(SCHEMA_PATH) as f, sqlite3.connect(path) as conn:
        conn.executescript(f.read())
    return str(path)


@pytest.fixture
def client(db_path):
    with TestClient(create_app(db_path=db_path)) as c:
        yield c


def make(client, building_name=SEM_NAME, building_code='SEM', outline=POLYGON):
    response = client.post('/buildings', json={
        'building_name': building_name, 'building_code': building_code, 'outline': outline,
    })
    assert response.status_code == 201, response.text
    return response.json()


def test_list_empty(client):
    response = client.get('/buildings')
    assert response.status_code == 200
    assert response.json() == []


def test_create_returns_row_with_id(client):
    assert make(client) == {
        'building_id': 1, 'building_name': SEM_NAME,
        'building_code': 'SEM', 'outline': POLYGON,
    }


def test_create_without_outline(client):
    response = client.post('/buildings', json={'building_name': DMSC_NAME,
                                                'building_code': 'DMSC'})
    assert response.status_code == 201
    assert response.json()['outline'] is None


def test_create_persists_and_lists_in_id_order(client):
    make(client, SEM_NAME, 'SEM')
    make(client, DMSC_NAME, 'DMSC')
    codes = [b['building_code'] for b in client.get('/buildings').json()]
    assert codes == ['SEM', 'DMSC']


def test_search_by_code_or_name(client):
    make(client, SEM_NAME, 'SEM')
    make(client, DMSC_NAME, 'DMSC')

    def codes(q):
        response = client.get('/buildings', params={'q': q})
        assert response.status_code == 200
        return [b['building_code'] for b in response.json()]

    assert codes('sem') == ['SEM']
    assert codes('Davidson') == ['DMSC']
    assert codes('center') == ['DMSC']
    assert codes('zzz') == []


def test_blank_search_lists_all(client):
    make(client, SEM_NAME, 'SEM')
    make(client, DMSC_NAME, 'DMSC')
    assert len(client.get('/buildings', params={'q': '  '}).json()) == 2


def test_search_returns_parsed_outline(client):
    make(client)
    assert client.get('/buildings', params={'q': 'sem'}).json()[0]['outline'] == POLYGON


def test_get_one(client):
    created = make(client)
    response = client.get(f"/buildings/{created['building_id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_is_404(client):
    assert client.get('/buildings/99').status_code == 404


def test_duplicate_building_code_is_409(client):
    make(client)
    response = client.post('/buildings',
                           json={'building_name': 'Another Building', 'building_code': 'SEM'})
    assert response.status_code == 409
    assert response.json()['detail'] == 'building_code already exists'


def test_duplicate_building_name_is_409(client):
    make(client)
    response = client.post('/buildings',
                           json={'building_name': SEM_NAME, 'building_code': 'OTHER'})
    assert response.status_code == 409
    assert response.json()['detail'] == 'building_name already exists'


@pytest.mark.parametrize('body', [
    {'building_code': 'SEM'},                           # missing name
    {'building_name': SEM_NAME},                        # missing code
    {'building_name': '', 'building_code': 'SEM'},      # empty name
    {'building_name': SEM_NAME, 'building_code': ''},   # empty code
])
def test_create_invalid_body_is_422(client, body):
    assert client.post('/buildings', json=body).status_code == 422


def test_patch_updates_only_given_fields(client):
    created = make(client, building_name='Scrugham')
    response = client.patch(f"/buildings/{created['building_id']}",
                            json={'building_name': SEM_NAME})
    assert response.status_code == 200
    assert response.json() == {**created, 'building_name': SEM_NAME}


def test_patch_can_clear_outline(client):
    created = make(client)
    response = client.patch(f"/buildings/{created['building_id']}", json={'outline': None})
    assert response.json()['outline'] is None


def test_patch_ignores_null_required_fields(client):
    created = make(client)
    response = client.patch(f"/buildings/{created['building_id']}",
                            json={'building_name': None, 'building_code': None})
    assert response.status_code == 200
    assert response.json() == created


def test_patch_missing_is_404(client):
    assert client.patch('/buildings/99', json={'building_code': 'x'}).status_code == 404


@pytest.mark.parametrize('field, value', [
    ('building_code', 'SEM'),
    ('building_name', SEM_NAME),
])
def test_patch_to_duplicate_is_409(client, field, value):
    make(client)
    dmsc = make(client, DMSC_NAME, 'DMSC')
    response = client.patch(f"/buildings/{dmsc['building_id']}", json={field: value})
    assert response.status_code == 409
    assert response.json()['detail'] == f'{field} already exists'


def test_delete(client):
    created = make(client)
    assert client.delete(f"/buildings/{created['building_id']}").status_code == 204
    assert client.get(f"/buildings/{created['building_id']}").status_code == 404


def test_delete_missing_is_404(client):
    assert client.delete('/buildings/99').status_code == 404


def test_create_multipolygon(client):
    assert make(client, outline=MULTIPOLYGON)['outline'] == MULTIPOLYGON


def test_outline_stored_as_geojson_text(client, db_path):
    created = make(client)
    with CampusDB.open(db_path) as db:
        stored = db.get_by_id('Building', created['building_id'])['outline']
    assert json.loads(stored) == POLYGON


def test_reads_geojson_text_written_directly_to_db(client, db_path):
    with CampusDB.open(db_path) as db:
        db.create('Building', building_name=SEM_NAME, building_code='SEM',
                  outline=json.dumps(POLYGON))
    assert client.get('/buildings').json()[0]['outline'] == POLYGON


def test_patch_replaces_outline(client):
    created = make(client)
    response = client.patch(f"/buildings/{created['building_id']}",
                            json={'outline': MULTIPOLYGON})
    assert response.status_code == 200
    assert response.json()['outline'] == MULTIPOLYGON


@pytest.mark.parametrize('outline', [
    'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))',                               # WKT, not GeoJSON
    {'type': 'Point', 'coordinates': [0, 0]},                           # not a footprint
    {'type': 'Polygon', 'coordinates': []},                             # no rings
    {'type': 'Polygon', 'coordinates': [[[0, 0], [1, 0], [0, 0]]]},     # ring too short
    {'type': 'Polygon', 'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1]]]},  # not closed
    {'type': 'Polygon', 'coordinates': [[[0], [1, 0], [1, 1], [0]]]},   # bad position
    {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 0], [1, 1], [0, 1]]]]},
])
def test_invalid_outline_is_422(client, outline):
    response = client.post('/buildings',
                           json={'building_name': SEM_NAME, 'building_code': 'SEM',
                                 'outline': outline})
    assert response.status_code == 422
    created = make(client)
    response = client.patch(f"/buildings/{created['building_id']}", json={'outline': outline})
    assert response.status_code == 422


def test_missing_database_is_503(tmp_path):
    app = create_app(db_path=str(tmp_path / 'nope.db'))
    with TestClient(app) as client:
        assert client.get('/buildings').status_code == 503
