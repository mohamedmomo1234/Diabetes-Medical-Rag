from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from security import security_check
from retriever import (
    retrieve_documents,
    build_context,
    get_sources
)
from generator import call_model
from output_guard import sanitize_output


class MedicalState(TypedDict, total=False):
    question: str
    allowed: bool
    context: str
    answer: str
    sources: list
    documents: list


def security_node(state):
    allowed, message = security_check(
        state["question"]
    )

    if not allowed:
        return {
            "allowed": False,
            "answer": message
        }

    return {
        "allowed": True
    }


def security_router(state):

    if state.get("allowed") is False:
        return "blocked"

    return "continue"


def retrieve_node(state):

    documents = retrieve_documents(
        state["question"]
    )

    context = build_context(documents)

    sources = get_sources(documents)

    return {
        "documents": documents,
        "context": context,
        "sources": sources
    }


def relevance_router(state):

    context = state.get(
        "context",
        ""
    )

    if not context.strip():
        return "no_context"

    return "has_context"


def no_context_node(state):

    return {
        "answer": (
            "لا توجد معلومات طبية كافية وموثوقة "
            "في قاعدة المعرفة الحالية للإجابة عن هذا السؤال."
        )
    }


def generate_node(state):

    answer = call_model(
        state["question"],
        state["context"]
    )

    answer = sanitize_output(answer)

    return {
        "answer": answer
    }


def add_sources_node(state):

    answer = state.get(
        "answer",
        ""
    )

    sources = state.get(
        "sources",
        []
    )

    if sources:

        answer += "\n\n### Sources\n"

        for source in sources:
            answer += f"- {source}\n"

    return {
        "answer": answer
    }


builder = StateGraph(MedicalState)


builder.add_node(
    "security",
    security_node
)

builder.add_node(
    "retrieve",
    retrieve_node
)

builder.add_node(
    "no_context",
    no_context_node
)

builder.add_node(
    "generate",
    generate_node
)

builder.add_node(
    "add_sources",
    add_sources_node
)


builder.add_edge(
    START,
    "security"
)


builder.add_conditional_edges(
    "security",
    security_router,
    {
        "continue": "retrieve",
        "blocked": END
    }
)


builder.add_conditional_edges(
    "retrieve",
    relevance_router,
    {
        "has_context": "generate",
        "no_context": "no_context"
    }
)


builder.add_edge(
    "no_context",
    END
)


builder.add_edge(
    "generate",
    "add_sources"
)


builder.add_edge(
    "add_sources",
    END
)


medical_graph = builder.compile()
