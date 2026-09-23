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






##########################
# import os

# from datetime import datetime, timezone

# from dotenv import load_dotenv

# from pymongo import MongoClient
# from pymongo.errors import PyMongoError


# load_dotenv()


# MONGODB_URI = os.getenv("MONGODB_URI")

# MONGODB_DATABASE = os.getenv(
#     "MONGODB_DATABASE",
#     "medical_rag"
# )

# MONGODB_COLLECTION = os.getenv(
#     "MONGODB_COLLECTION",
#     "chat_history"
# )


# if not MONGODB_URI:

#     raise ValueError(
#         "MONGODB_URI is missing"
#     )


# client = MongoClient(
#     MONGODB_URI,
#     serverSelectionTimeoutMS=5000
# )


# db = client[MONGODB_DATABASE]

# chat_collection = db[
#     MONGODB_COLLECTION
# ]


# def save_chat(
#     question,
#     answer,
#     sources=None
# ):

#     document = {

#         "question": question,

#         "answer": answer,

#         "sources": sources or [],

#         "created_at":
#             datetime.now(timezone.utc)
#     }


#     try:

#         chat_collection.insert_one(
#             document
#         )

#         return True


#     except PyMongoError:

#         return False


# def get_chat_history(limit=50):

#     try:

#         chats = chat_collection.find(
#             {},
#             {
#                 "_id": 0,
#                 "question": 1,
#                 "answer": 1,
#                 "sources": 1,
#                 "created_at": 1
#             }
#         ).sort(
#             "created_at",
#             -1
#         ).limit(limit)

#         return list(chats)

#     except PyMongoError:

#         return []



# # import os
# # from datetime import datetime, timezone

# # from pymongo import MongoClient
# # from pymongo.errors import PyMongoError
# # from dotenv import load_dotenv


# # load_dotenv()


# # MONGODB_URI = os.getenv("MONGODB_URI")
# # MONGODB_DATABASE = os.getenv(
# #     "MONGODB_DATABASE",
# #     "medical_rag"
# # )
# # MONGODB_COLLECTION = os.getenv(
# #     "MONGODB_COLLECTION",
# #     "chat_history"
# # )


# # if not MONGODB_URI:
# #     raise ValueError("MONGODB_URI is missing")


# # client = MongoClient(
# #     MONGODB_URI,
# #     serverSelectionTimeoutMS=5000
# # )

# # db = client[MONGODB_DATABASE]
# # chat_collection = db[MONGODB_COLLECTION]


# # def save_chat(question, answer, sources=None):

# #     document = {
# #         "question": question,
# #         "answer": answer,
# #         "sources": sources or [],
# #         "created_at": datetime.now(timezone.utc)
# #     }

# #     try:
# #         chat_collection.insert_one(document)
# #         return True

# #     except PyMongoError:
# #         return False