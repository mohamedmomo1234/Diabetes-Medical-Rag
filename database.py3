from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import (
    MONGODB_URI,
    MONGODB_DATABASE,
    MONGODB_COLLECTION
)


_client = None
_collection = None


def get_collection():

    global _client
    global _collection

    if _collection is not None:
        return _collection

    if not MONGODB_URI:
        raise RuntimeError(
            "MONGODB_URI is not configured."
        )

    _client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )

    _client.admin.command("ping")

    database = _client[
        MONGODB_DATABASE
    ]

    _collection = database[
        MONGODB_COLLECTION
    ]

    return _collection


def save_chat(
    question: str,
    answer: str,
    sources: list
):

    try:

        collection = get_collection()

        collection.insert_one({
            "question": question,
            "answer": answer,
            "sources": sources,
            "created_at": datetime.now(
                timezone.utc
            )
        })

        return True

    except PyMongoError as error:

        print(
            f"MongoDB save failed: "
            f"{type(error).__name__}"
        )

        return False


def get_chat_history(limit: int = 100):

    collection = get_collection()

    return list(
        collection.find(
            {},
            {"_id": 0}
        )
        .sort(
            "created_at",
            -1
        )
        .limit(limit)
    )
