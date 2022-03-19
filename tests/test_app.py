from fastapi.testclient import TestClient
import pytest

from api.app import app, database


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def populate_db(client):
    database.db.set_collection_data(
        {"tags": {"red": {"total_count": 1}, "blue": {"total_count": 5}}}
    )


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["msg"] == "ok"


def test_get_empty_tag_stats(client):
    response = client.get("/tags")
    assert response.status_code == 200
    assert not response.json()


def test_get_populated_tag_stats(client, populate_db):
    response = client.get("/tags")
    assert response.status_code == 200


@pytest.mark.parametrize("tag,count,expected_total_count,expected_status_code", [
    ("green", 1, 1, 204),
    ("blue_1", 1, 0, 422),
    ("red", 9, 10, 204),
    ("red", 10, 1, 422),
    ("red", 0, 1, 422),
    ])
def test_increment_tag_count(tag: str, count: int, expected_total_count: int, expected_status_code: int, client, populate_db):
    payload = {
        "name": tag,
        "value": count,
    }
    response = client.put("/tags", json=payload)
    assert response.status_code == expected_status_code
    tag_counts = client.get("/tags").json()
    assert tag_counts.get(tag, 0) == expected_total_count
