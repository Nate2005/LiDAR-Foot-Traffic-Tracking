import os
import sqlite3
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'src'))

from database import CampusDB


@pytest.fixture
def db():
    with CampusDB.in_memory() as db:
        yield db


@pytest.fixture
def campus(db):
    """Three intersections: A-B joined by a ramp, B-C joined by stairs."""
    a = db.create('Intersection', intersection_name='A')
    b = db.create('Intersection', intersection_name='B')
    c = db.create('Intersection', intersection_name='C')
    ramp = db.create('PathwaySegment', pathway_name='ramp', ada_accessible=True)
    stairs = db.create('PathwaySegment', pathway_name='stairs', ada_accessible=False)
    for pathway, ends in ((ramp, (a, b)), (stairs, (b, c))):
        for intersection in ends:
            db.link_pathway_intersection(pathway, intersection)
    return {'A': a, 'B': b, 'C': c, 'ramp': ramp, 'stairs': stairs}


def test_ada_accessible_defaults_to_false(db):
    pathway = db.create('PathwaySegment', pathway_name='unverified')
    assert db.get_by_id('PathwaySegment', pathway)['ada_accessible'] == 0


def test_ada_accessible_rejects_non_boolean(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.create('PathwaySegment', pathway_name='bad', ada_accessible=2)


def test_ada_accessible_rejects_null(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.create('PathwaySegment', pathway_name='bad', ada_accessible=None)


def test_find_filters_on_ada_accessible(db, campus):
    names = [row['pathway_name'] for row in db.find('PathwaySegment', ada_accessible=True)]
    assert names == ['ramp']


def test_pathway_edges_includes_all_segments_with_endpoints(db, campus):
    edges = {e['pathway_name']: e for e in db.pathway_edges()}
    assert edges['ramp']['intersection_ids'] == [campus['A'], campus['B']]
    assert edges['stairs']['intersection_ids'] == [campus['B'], campus['C']]
    assert edges['stairs']['ada_accessible'] == 0


def test_pathway_edges_ada_only_excludes_stairs(db, campus):
    edges = db.pathway_edges(ada_only=True)
    assert [e['pathway_name'] for e in edges] == ['ramp']


def test_pathway_edges_keeps_unlinked_pathway(db):
    db.create('PathwaySegment', pathway_name='orphan', ada_accessible=True)
    assert db.pathway_edges()[0]['intersection_ids'] == []
