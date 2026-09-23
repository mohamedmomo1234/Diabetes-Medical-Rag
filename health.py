from config import (
    GROQ_API_KEY,
    MONGODB_URI
)

from retriever import get_vectorstore


def check_chroma():

    try:

        vectorstore = get_vectorstore()

        vectorstore._collection.count()

        return True

    except Exception:

        return False


def check_environment():

    return {
        "GROQ_API_KEY": bool(
            GROQ_API_KEY
        ),
        "MONGODB_URI": bool(
            MONGODB_URI
        ),
        "CHROMA": check_chroma()
    }


if __name__ == "__main__":

    health = check_environment()

    for name, status in health.items():

        symbol = "OK" if status else "FAIL"

        print(
            f"{name}: {symbol}"
        )
