import pytest
import mongomock
from freezegun import freeze_time
from news_catalog.mongoDB_handler import MongoDBHandler


class MockMongoDBHandler(MongoDBHandler):
    def __init__(self, settings):
        self.client = mongomock.MongoClient(
            settings["server"], settings["port"]
        )
        self.db = self.client[settings["db"]]
        self.collection = self.db[settings["collection"]]


@pytest.fixture
def mock_mongo_db():
    settings = {
        "server": "localhost",
        "port": 27017,
        "db": "news-catalog",
        "collection": "newses",
    }

    return MockMongoDBHandler(settings)


def test_insert_many(mock_mongo_db):
    objects = [{"a": 1, "b": "xyz"}, {"a": 2, "b": "abc"}]

    mock_mongo_db.insert(objects)
    found_items = list(mock_mongo_db.collection.find())

    assert len(found_items) == 2


def test_insert_one(mock_mongo_db):
    object = {"a": 1, "b": "xyz"}

    mock_mongo_db.insert(object)
    found_items = list(mock_mongo_db.collection.find())

    assert len(found_items) == 1


def test_drop_duplicates_one_key(mock_mongo_db):
    objects = [
        {"a": 1, "b": "xyz"},
        {"a": 1, "b": "abc"},
        {"a": 1, "b": "gax"},
    ]
    mock_mongo_db.collection.insert_many(objects)

    mock_mongo_db.drop_duplicates(unique_keys=["a"])
    found_items = list(mock_mongo_db.collection.find())

    assert len(found_items) == 1


def test_drop_duplicates_multiple_keys(mock_mongo_db):
    objects = [
        {"a": 1, "b": "xyz"},
        {"a": 2, "b": "abc"},
        {"a": 1, "b": "xyz"},
    ]
    mock_mongo_db.collection.insert_many(objects)

    mock_mongo_db.drop_duplicates(unique_keys=["a", "b"])
    found_items = list(mock_mongo_db.collection.find())

    assert len(found_items) == 2


def test_get_data(mock_mongo_db):
    objects = [
        {"a": 1, "b": "xyz"},
        {"a": 2, "b": "abc"},
        {"a": 1, "b": "xyz"},
    ]
    mock_mongo_db.collection.insert_many(objects)

    items = mock_mongo_db.get_data()

    assert items == objects


def test_get_max_date(mock_mongo_db):
    objects = [
        {"date": "2024-01-01", "b": "xyz"},
        {"date": "2024-03-01", "b": "abc"},
        {"date": "2024-02-01", "b": "xyz"},
    ]
    mock_mongo_db.collection.insert_many(objects)

    actual_output = mock_mongo_db.get_max_date()
    expected_output = "2024-03-01"

    assert actual_output == expected_output


@freeze_time("2024-01-01")
def test_get_max_date_default(mock_mongo_db):
    actual_output = mock_mongo_db.get_max_date()
    expected_output = "2023-12-30"

    assert actual_output == expected_output


def test_update_item(mock_mongo_db):
    objects = [
        {"_id": "1", "a": "xyz"},
        {"_id": "2", "a": "abc"},
    ]
    mock_mongo_db.collection.insert_many(objects)

    mock_mongo_db.update_item("1", "a", "xyz-modified")

    found_items = list(mock_mongo_db.collection.find())
    expected_ouptut = [
        {"_id": "1", "a": "xyz-modified"},
        {"_id": "2", "a": "abc"},
    ]

    assert len(found_items) == 2
    assert found_items == expected_ouptut


def test_update_item_new_field(mock_mongo_db):
    objects = [
        {"_id": "1", "a": "xyz"},
        {"_id": "2", "a": "abc"},
    ]
    mock_mongo_db.collection.insert_many(objects)

    mock_mongo_db.update_item("2", "tags", ["tag1", "tag2"])

    found_items = list(mock_mongo_db.collection.find())
    expected_ouptut = [
        {"_id": "1", "a": "xyz"},
        {"_id": "2", "a": "abc", "tags": ["tag1", "tag2"]},
    ]

    assert len(found_items) == 2
    assert found_items == expected_ouptut
