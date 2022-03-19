import abc
from collections import namedtuple

from .config import app_settings

Document = namedtuple("Document", ["id", "document"])

class AbstractDB(abc.ABC):
    pass

    @abc.abstractmethod
    def get_all_documents_in_collection(self, collection: str):
        pass

    @abc.abstractmethod
    def create_collection(self, collection: str):
        pass

    @abc.abstractmethod
    def increment_tag_total_count(self, name: str, count: int):
        pass

class TestDB(AbstractDB):
    """
    The TestDB is a simplified in-memory mock interface to the Firebase Document DB.
    """

    def __init__(self):
        self.collections: dict = {}

    def get_all_documents_in_collection(self, collection: str):
        for id, document in self.collections[collection].items():
            yield Document(id, document)

    def create_collection(self, collection: str):
        self.collections[collection] = {}

    def set_collection_data(self, collection_data: dict):
        self.collections = collection_data
    
    def increment_tag_total_count(self, name: str, count: int):
        if name not in self.collections["tags"]:
            self.collections["tags"][name] = {"total_count": count}
        else:
            self.collections["tags"][name]["total_count"] += count


def get_db() -> AbstractDB:
    """
    Uses the app settings to determine which database interface to use.
    """
    if not app_settings.database_config:
        return TestDB()


db = get_db()
