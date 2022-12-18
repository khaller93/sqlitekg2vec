import pytest as pytest
from pyrdf2vec.graphs import Vertex

import sqlitekg2vec

GRAPH = [
    ["Alice", "knows", "Bob"],
    ["Alice", "knows", "Dean"],
    ["Bob", "knows", "Casper"],
]


@pytest.fixture
def local_kg():
    with sqlitekg2vec.open(GRAPH) as local_kg:
        yield local_kg


def test_get_id_of_unknown_entity_name_must_return_none(local_kg):
    entity_id = local_kg.id('Robert')
    assert entity_id is None


def test_get_id_of_alice_must_return_1(local_kg):
    entity_id = local_kg.id('Alice')
    assert entity_id == 1


def test_from_id_3_as_str_must_return_bob(local_kg):
    entity_name = local_kg.from_id('3')
    assert entity_name == 'Bob'


def test_from_id_3_as_int_must_return_bob(local_kg):
    entity_name = local_kg.from_id(3)
    assert entity_name == 'Bob'


def test_from_unknown_id_as_int_must_return_none(local_kg):
    entity_name = local_kg.from_id(-1)
    assert entity_name is None


def test_get_hops(local_kg):
        neighbors = local_kg.get_hops(Vertex('Alice'))
        predicates = [neighbor[0] for neighbor in neighbors]
        objects = [neighbor[1] for neighbor in neighbors]

        assert len(neighbors) == 2
        assert len(predicates) == 2
        assert len(objects) == 2

        assert {predicate.name for predicate in predicates} == {'knows'}
        assert Vertex('Bob') in objects
        assert Vertex('Dean') in objects

        neighbors = local_kg.get_hops(Vertex('Bob'), is_reverse=True)
        predicates = [neighbor[0] for neighbor in neighbors]
        objects = [neighbor[1] for neighbor in neighbors]

        assert len(neighbors) == 1
        assert len(predicates) == 1
        assert len(objects) == 1
        assert Vertex('Alice') in objects
