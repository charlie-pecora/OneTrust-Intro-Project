from re import I
import pytest
import pytest_asyncio

from api.database import InMemoryDB, FirestoreDB

collection_name = "test_collection"

initial_collection_data = {"red": {"total_count": 1}, "blue": {"total_count": 5}}


@pytest_asyncio.fixture
async def db(request):
    if request.param == "test":
        db = InMemoryDB()
        await db.set_tag_data(initial_collection_data)
    else:
        db = FirestoreDB()
        await db.set_tag_data(initial_collection_data)
    return db


@pytest.mark.database
@pytest.mark.asyncio
@pytest.mark.parametrize("db", [("test"), ("cloud")], indirect=True)
async def test_get_all_tags(db):
    tag_names = []
    async for tag in db.get_all_tags():
        tag_names.append(tag.name)
        assert isinstance(tag.total_count, int)
    assert sorted(tag_names) == sorted(list(initial_collection_data.keys()))


@pytest.mark.database
@pytest.mark.asyncio
@pytest.mark.parametrize("db", [("test"), ("cloud")], indirect=True)
@pytest.mark.parametrize(
    "tag,count,expected_total_count",
    [
        ("green", 1, 1),
        ("red", 9, 10),
        ("red", 0, 1),
    ],
)
async def test_increment_tag_count(db, tag, count, expected_total_count):
    await db.increment_tag_total_count(tag, count)
    async for each_tag in db.get_all_tags():
        if each_tag.name == tag:
            assert each_tag.total_count == expected_total_count
