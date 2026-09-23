import os

from dotenv import load_dotenv

load_dotenv()


# =========================
# GROQ
# =========================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing."
    )


# =========================
# LANGSMITH
# =========================

LANGSMITH_API_KEY = os.getenv(
    "LANGSMITH_API_KEY"
)

LANGSMITH_TRACING = os.getenv(
    "LANGSMITH_TRACING",
    "false"
)

LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "medical-rag-chatbot"
)


# =========================
# MONGODB
# =========================

MONGODB_URI = os.getenv(
    "MONGODB_URI"
)

MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "medical_rag"
)

MONGODB_COLLECTION = os.getenv(
    "MONGODB_COLLECTION",
    "chat_history"
)


# =========================
# ADMIN
# =========================

ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD"
)


# =========================
# CHROMA
# =========================

CHROMA_DIR = "chroma_db"

CHROMA_COLLECTION = (
    "medical_knowledge"
)


# =========================
# RETRIEVAL
# =========================

TOP_K = 20

FINAL_TOP_K = 8

RELEVANCE_THRESHOLD = 0.1


# =========================
# CHUNKING
# =========================

CHUNK_SIZE = 600

CHUNK_OVERLAP = 120


######################

# import os

# from dotenv import load_dotenv


# load_dotenv()



# # GROQ
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# GROQ_MODEL = os.getenv(
#     "GROQ_MODEL",
#     "openai/gpt-oss-120b"
# )


# if not GROQ_API_KEY:
#     raise ValueError(
#         "GROQ_API_KEY is missing. "
#         "Add it to your .env file."
#     )


# # API SECURITY
# # API_SECRET_KEY = os.getenv(
# #     "API_SECRET_KEY"
# # )

# # if not API_SECRET_KEY:
# #     raise ValueError(
# #         "API_SECRET_KEY is missing. "
# #         "Add it to your .env file."
# #     )



# # LANGSMITH
# LANGSMITH_API_KEY = os.getenv(
#     "LANGSMITH_API_KEY"
# )

# LANGSMITH_TRACING = os.getenv(
#     "LANGSMITH_TRACING",
#     "false"
# )

# LANGSMITH_PROJECT = os.getenv(
#     "LANGSMITH_PROJECT",
#     "medical-rag-chatbot"
# )



# # MONGODB
# MONGODB_URI = os.getenv(
#     "MONGODB_URI"
# )

# MONGODB_DATABASE = os.getenv(
#     "MONGODB_DATABASE",
#     "medical_rag"
# )

# MONGODB_COLLECTION = os.getenv(
#     "MONGODB_COLLECTION",
#     "chat_history"
# )



# # ADMIN
# ADMIN_PASSWORD = os.getenv(
#     "ADMIN_PASSWORD"
# )



# # CHROMA
# CHROMA_DIR = "chroma_db"

# CHROMA_COLLECTION = (
#     "medical_knowledge"
# )



# # RETRIEVAL
# TOP_K = 12
# FINAL_TOP_K = 4
# RELEVANCE_THRESHOLD = 0.20



# # CHUNKING
# CHUNK_SIZE = 350
# CHUNK_OVERLAP = 80



# # FRONTEND / API
# # API_URL = os.getenv(
# #     "API_URL",
# #     "http://127.0.0.1:8000"
# # )