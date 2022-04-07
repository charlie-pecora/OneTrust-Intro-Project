import abc
from collections import namedtuple
from copy import deepcopy
from typing import Generator
import logging

from .config import app_settings

import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import transforms

Tag = namedtuple("Tag", ["name", "total_count"])


class AbstractDB(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_all_tags(self):
        pass

    @abc.abstractmethod
    def increment_tag_total_count(self, name: str, count: int):
        pass


class InMemoryDB(AbstractDB):
    """
    The TestDB is a simplified in-memory mock interface to the Firebase Document DB.
    """

    def __init__(self):
        self.tags: dict = {}

    async def get_all_tags(self) -> Generator[Tag, None, None]:
        for name, data in self.tags.items():
            yield Tag(name, data["total_count"])

    async def set_tag_data(self, tag_data: dict):
        self.tags = deepcopy(tag_data)

    async def increment_tag_total_count(self, name: str, count: int):
        if name not in self.tags:
            self.tags[name] = {"total_count": count}
        else:
            self.tags[name]["total_count"] += count


class FirestoreDB(AbstractDB):
    def __init__(self, project_id: str = None):
        try:
            firebase_admin.initialize_app(
                credentials.ApplicationDefault(), {"projectId": project_id}
            )
        except ValueError:
            logging.debug("Firebase already initialized... skipping")
        self._db = firestore.AsyncClient()
        self.db_collection = app_settings.db_collection

    async def get_all_tags(self):
        collection = self._db.collection(self.db_collection)
        async for document in collection.stream():
            yield Tag(document.id, document.get("total_count"))

    async def increment_tag_total_count(self, name: str, count: int):
        transaction = self._db.transaction()
        collection = self._db.collection(self.db_collection)
        document = collection.document(name)
        snapshot = await document.get()
        if snapshot.exists:
            transaction.update(document, {"total_count": transforms.Increment(count)})
        else:
            transaction.create(document, document_data={"total_count": count})
        await transaction.commit()

    async def set_tag_data(self, tag_data: dict):
        collection = self._db.collection(self.db_collection)
        async for document in collection.list_documents():
            await document.delete()
        for k, v in tag_data.items():
            await collection.add(document_data=v, document_id=k)


def get_db() -> AbstractDB:
    """
    Uses the app settings to determine which database interface to use.
    """
    if app_settings.db_type == "test":
        return InMemoryDB()
    else:
        return FirestoreDB(project_id=app_settings.google_project_id)


db = get_db()
