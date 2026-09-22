import os
from dotenv import load_dotenv

load_dotenv()



# GROQ

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



# LANGSMITH

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



# MONGODB

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



# ADMIN

ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD"
)



# CHROMA

CHROMA_DIR = "chroma_db"

CHROMA_COLLECTION = (
    "medical_knowledge"
)



# RETRIEVAL

TOP_K = 12

FINAL_TOP_K = 4

RELEVANCE_THRESHOLD = 0.20



# CHUNKING

CHUNK_SIZE = 350

CHUNK_OVERLAP = 80
