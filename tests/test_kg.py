import pytest as pytest

import sqlitekg2vec
from sqlitekg2vec.kg import SQLiteKG

GRAPH = [
    ["Alice", "knows", "Bob"],
    ["Alice", "knows", "Dean"],
    ["Bob", "knows", "Casper"],
]


@pytest.fixture
def local_kg() -> SQLiteKG:
    with sqlitekg2vec.open_from(GRAPH) as local_kg:
        yield local_kg


def test_entity_count_must_return_4(local_kg: SQLiteKG):
    cnt = local_kg.entity_count
    assert cnt == 4


def test_predicate_count_must_return_1(local_kg: SQLiteKG):
    cnt = local_kg.predicate_count
    assert cnt == 1


def test_statement_count_must_return_3(local_kg: SQLiteKG):
    cnt = local_kg.statement_count
    assert cnt == 3


def test_get_id_of_unknown_entity_name_must_return_none(local_kg: SQLiteKG):
    entity_id = local_kg.id('Robert')
    assert entity_id is None


def test_get_id_of_alice_must_return_1(local_kg: SQLiteKG):
    entity_id = local_kg.id('Alice')
    assert int(entity_id) == 1


def test_from_id_3_as_str_must_return_bob(local_kg: SQLiteKG):
    entity_name = local_kg.from_id(str(local_kg.id('Bob')))
    assert entity_name == 'Bob'


def test_from_id_3_as_int_must_return_bob(local_kg: SQLiteKG):
    entity_name = local_kg.from_id(int(local_kg.id('Bob')))
    assert entity_name == 'Bob'


def test_from_unknown_id_as_int_must_return_none(local_kg: SQLiteKG):
    entity_name = local_kg.from_id(-1)
    assert entity_name is None


def test_entities_empty_restrict_must_return_empty_list(local_kg: SQLiteKG):
    ent = local_kg.entities(restricted_to=[])
    assert len(ent) == 0


def test_entities_stream_proper_list(local_kg: SQLiteKG):
    ent = local_kg.entities(restricted_to=['Alice', 'Bob', 'Robert', 'Dean'])
    assert all([a == b for a, b in zip(ent, [str(local_kg.id(x)) for x in
                                             ['Alice', 'Bob', 'Dean']])])


def test_is_exist_all_existing_entities_must_return_true(local_kg: SQLiteKG):
    assert local_kg.is_exist([local_kg.id(x) for x in ['Alice', 'Bob', 'Dean']])


def test_is_exist_all_existing_entities_must_return_false(local_kg: SQLiteKG):
    assert not local_kg.is_exist(['1', '3', '4', '8'])
