from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import build_medical_prompt


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured."
    )


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.1
)


def call_model(question: str, context: str):
    prompt = build_medical_prompt(
        question=question,
        context=context
    )

    response = llm.invoke(prompt)

    return response.content
