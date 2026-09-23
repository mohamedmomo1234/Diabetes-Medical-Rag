from datetime import datetime, timezone

from database import get_collection


def save_feedback(
    question: str,
    answer: str,
    feedback: str
):

    collection = get_collection()

    collection.insert_one({
        "type": "feedback",
        "question": question,
        "answer": answer,
        "feedback": feedback,
        "created_at": datetime.now(
            timezone.utc
        )
    })
