
import time
from collections import defaultdict

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Request
)

from pydantic import BaseModel

from config import API_SECRET_KEY

from graph import medical_graph


app = FastAPI(
    title="Diabetes Medical RAG API",
    description="Diabetes Medical RAG Chatbot Backend",
    version="1.0.0"
)



# RATE LIMITING

RATE_LIMIT = 10

RATE_WINDOW = 60

request_history = defaultdict(list)


def check_rate_limit(
    client_ip: str
):
    current_time = time.time()

    history = request_history[
        client_ip
    ]

    history[:] = [
        timestamp
        for timestamp in history
        if current_time - timestamp
        < RATE_WINDOW
    ]

    if len(history) >= RATE_LIMIT:
        return False

    history.append(current_time)

    return True



# API KEY CHECK

def verify_api_key(
    api_key: str | None
):
    if not api_key:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if not hmac.compare_digest(
        api_key,
        API_SECRET_KEY
    ):

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )



# REQUEST / RESPONSE

class ChatRequest(BaseModel):

    question: str


class ChatResponse(BaseModel):

    answer: str

    sources: list[str]



# ROOT

@app.get("/")
def root():

    return {
        "message":
        "Diabetes Medical RAG API is running"
    }



# HEALTH

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



# CHAT

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    http_request: Request,
    x_api_key: str | None = Header(
        default=None
    )
):

    
    # API KEY

    verify_api_key(
        x_api_key
    )


    
    # RATE LIMIT

    client_ip = (
        http_request.client.host
        if http_request.client
        else "unknown"
    )

    if not check_rate_limit(
        client_ip
    ):

        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )


    
    # QUESTION VALIDATION

    question = (
        request.question.strip()
    )


    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    if len(question) > 2000:

        raise HTTPException(
            status_code=400,
            detail="Question is too long."
        )



    # RUN RAG

    try:

        result = medical_graph.invoke(
            {
                "question": question
            }
        )


        return {
            "answer": result.get(
                "answer",
                "No answer generated."
            ),
            "sources": result.get(
                "sources",
                []
            )
        }


    except Exception as error:

        print(
            f"API error: "
            f"{type(error).__name__}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )
