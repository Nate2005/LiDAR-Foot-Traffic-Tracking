import sqlite3

import pytest


from database import CampusDB

SEM_NAME = 'Scrugham Engineering and Mines'
DMSC_NAME = 'Davidson Mathematics and Science Center'


@pytest.fixture
def db():
    with CampusDB.in_memory() as database:
        yield database


# --- open / close ---

def test_open_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        CampusDB.open(str(tmp_path / 'no_such_campus.db'))


def test_context_manager_closes_connection():
    with CampusDB.in_memory() as database:
        conn = database.conn
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute('SELECT 1')


# --- CRUD ---

def test_create_assigns_sequential_ids_and_get_returns_row(db):
    first = db.create('Building', building_name=SEM_NAME, building_code='SEM')
    second = db.create('Building', building_name=DMSC_NAME, building_code='DMSC')
    assert (first, second) == (1, 2)
    assert db.get_by_id('Building', first)['building_code'] == 'SEM'
    assert db.get_by_id('Building', 99) is None


def test_get_by_name(db):
    db.create('Building', building_name=SEM_NAME, building_code='SEM')
    assert db.get_by_name('Building', SEM_NAME)['building_code'] == 'SEM'
    assert db.get_by_name('Building', 'nope') is None


def test_find_filters_and_lists_all(db):
    db.create('Building', building_name=SEM_NAME, building_code='SEM')
    db.create('Building', building_name=DMSC_NAME, building_code='DMSC')
    assert len(db.find('Building')) == 2
    found = db.find('Building', building_code='DMSC')
    assert [row['building_name'] for row in found] == [DMSC_NAME]


def test_update(db):
    row_id = db.create('Building', building_name='Scrugham', building_code='SEM')
    assert db.update('Building', row_id, building_name=SEM_NAME)
    assert db.get_by_id('Building', row_id)['building_name'] == SEM_NAME
    assert not db.update('Building', 99, building_code='x')
    assert not db.update('Building', row_id)


def test_delete(db):
    row_id = db.create('Building', building_name=SEM_NAME, building_code='SEM')
    assert db.delete('Building', row_id)
    assert not db.delete('Building', row_id)


def test_building_name_and_code_are_each_unique(db):
    db.create('Building', building_name=SEM_NAME, building_code='SEM')
    with pytest.raises(sqlite3.IntegrityError):
        db.create('Building', building_name=SEM_NAME, building_code='OTHER')
    with pytest.raises(sqlite3.IntegrityError):
        db.create('Building', building_name='Other Building', building_code='SEM')


def test_building_code_is_required(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.create('Building', building_name=SEM_NAME)


def test_unknown_table_or_column_rejected(db):
    with pytest.raises(ValueError):
        db.get_by_id('Nope', 1)
    with pytest.raises(ValueError):
        db.find('Building', bogus=1)
    with pytest.raises(ValueError):
        db.create('Building', bogus=1)


# --- search_buildings ---

@pytest.fixture
def search_db(db):
    for name, code in [(SEM_NAME, 'SEM'), (DMSC_NAME, 'DMSC'),
                       ('Mathewson-IGT Knowledge Center', 'MIKC'),
                       ('100% Fake_Hall', 'FAKE')]:
        db.create('Building', building_name=name, building_code=code)
    return db


def codes(database, text):
    return [row['building_code'] for row in database.search_buildings(text)]


def test_search_matches_code_ignoring_case(search_db):
    assert codes(search_db, 'dmsc') == ['DMSC']


def test_search_matches_part_of_name_ignoring_case(search_db):
    assert codes(search_db, 'davidson') == ['DMSC']
    assert codes(search_db, 'engineering') == ['SEM']


def test_search_exact_code_then_prefix_then_substring(search_db):
    # 'mi' prefixes code MIKC and appears mid-name in SEM ("...and Mines")
    assert codes(search_db, 'mi') == ['MIKC', 'SEM']
    search_db.create('Building', building_name='Mi Hall', building_code='MI')
    assert codes(search_db, 'mi') == ['MI', 'MIKC', 'SEM']


def test_search_no_match(search_db):
    assert codes(search_db, 'zzz') == []


def test_search_wildcards_are_literal(search_db):
    assert codes(search_db, '%') == ['FAKE']
    assert codes(search_db, 'g_n') == []   # '_' as a wildcard would hit "Engineering"
    assert codes(search_db, 'e_h') == ['FAKE']


# --- get_or_create ---

def test_get_or_create_creates_once_then_returns_existing_row(db):
    values = {'building_name': SEM_NAME, 'building_code': 'SEM'}

    first_id, first_created = db.get_or_create('Building', **values)
    second_id, second_created = db.get_or_create('Building', **values)

    assert first_created
    assert not second_created
    assert first_id == second_id
    assert len(db.find('Building')) == 1


# --- transactions ---

def test_transaction_rolls_back_on_error(db):
    with pytest.raises(RuntimeError):
        with db.transaction():
            db.create('Building', building_name=SEM_NAME, building_code='SEM')
            raise RuntimeError
    assert db.find('Building') == []


def test_transaction_commits_on_success(db):
    with db.transaction():
        db.create('Building', building_name=SEM_NAME, building_code='SEM')
    assert len(db.find('Building')) == 1


# --- pathway / intersection links ---

def test_pathway_intersection_link_lookup_and_unlink(db):
    pathway = db.create('PathwaySegment', pathway_name='W1')
    intersection = db.create('Intersection', intersection_name='I1')

    assert db.link_pathway_intersection(pathway, intersection)
    assert not db.link_pathway_intersection(pathway, intersection)

    assert [r['intersection_id'] for r in db.intersections_for_pathway(pathway)] == [intersection]
    assert [r['pathway_id'] for r in db.pathways_for_intersection(intersection)] == [pathway]

    assert db.unlink_pathway_intersection(pathway, intersection)
    assert not db.unlink_pathway_intersection(pathway, intersection)
    assert db.intersections_for_pathway(pathway) == []
