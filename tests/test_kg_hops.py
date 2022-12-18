import pytest as pytest
from pyrdf2vec.graphs import Vertex

import sqlitekg2vec
from sqlitekg2vec.kg import SQLiteKG

GRAPH = [
    ["Alice", "knows", "Bob"],
    ["Alice", "knows", "Dean"],
    ["Bob", "knows", "Casper"],
]


@pytest.fixture
def local_kg() -> SQLiteKG:
    with sqlitekg2vec.open(GRAPH) as local_kg:
        yield local_kg


def test_get_forward_hops(local_kg):
    neighbors = local_kg.get_hops(Vertex(local_kg.id('Alice')))
    predicates = [neighbor[0] for neighbor in neighbors]
    objects = [neighbor[1] for neighbor in neighbors]

    assert len(neighbors) == 2
    assert len(predicates) == 2
    assert len(objects) == 2

    assert {predicate.name for predicate in predicates} == {
        local_kg.id('knows')}
    assert Vertex(local_kg.id('Bob')) in objects
    assert Vertex(local_kg.id('Dean')) in objects


def test_get_backward_hops(local_kg):
    neighbors = local_kg.get_hops(Vertex(local_kg.id('Bob')), is_reverse=True)
    predicates = [neighbor[0] for neighbor in neighbors]
    objects = [neighbor[1] for neighbor in neighbors]

    assert len(neighbors) == 1
    assert len(predicates) == 1
    assert len(objects) == 1

    assert Vertex(local_kg.id('Alice')) in objects
