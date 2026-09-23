from langchain_chroma import Chroma

from embeddings import get_embeddings

from config import (
    CHROMA_DIR,
    CHROMA_COLLECTION,
    TOP_K,
    FINAL_TOP_K,
    RELEVANCE_THRESHOLD
)


# =========================
# VECTORSTORE
# =========================

def get_vectorstore():

    embeddings = get_embeddings()

    return Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )


# =========================
# RETRIEVE DOCUMENTS
# =========================

def retrieve_documents(question: str):

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=TOP_K
    )

    relevant_documents = []

    for document, score in results:

        if score >= RELEVANCE_THRESHOLD:

            document.metadata["relevance_score"] = float(score)

            relevant_documents.append(document)


    # =========================
    # SORT BY RELEVANCE
    # =========================

    relevant_documents.sort(
        key=lambda doc: doc.metadata.get(
            "relevance_score",
            0
        ),
        reverse=True
    )

    return relevant_documents[:FINAL_TOP_K]


# =========================
# BUILD CONTEXT
# =========================

def build_context(documents):

    if not documents:

        return ""

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        source = document.metadata.get(
            "source_file",
            "Unknown"
        )

        page = document.metadata.get(
            "page"
        )

        score = document.metadata.get(
            "relevance_score",
            0
        )

        location = source

        if page is not None:

            location += f", page {page + 1}"

        context_parts.append(
            f"""
[Document {index}]

Source: {location}

Relevance Score: {score:.3f}

{document.page_content}
"""
        )

    return "\n".join(context_parts)


# =========================
# GET SOURCES
# =========================

def get_sources(documents):

    unique_sources = []

    for document in documents:

        source = document.metadata.get(
            "source_file",
            "Unknown"
        )

        if source not in unique_sources:

            unique_sources.append(source)

    return unique_sources


#################
# from langchain_chroma import Chroma

# from embeddings import get_embeddings

# from config import (
#     CHROMA_DIR,
#     CHROMA_COLLECTION,
#     TOP_K,
#     FINAL_TOP_K,
#     RELEVANCE_THRESHOLD
# )


# def get_vectorstore():

#     embeddings = get_embeddings()

#     return Chroma(
#         collection_name=CHROMA_COLLECTION,
#         persist_directory=CHROMA_DIR,
#         embedding_function=embeddings
#     )


# def retrieve_documents(question: str):

#     vectorstore = get_vectorstore()

#     results = vectorstore.similarity_search_with_relevance_scores(
#         question,
#         k=TOP_K
#     )

#     relevant_documents = []

#     for document, score in results:

#         if score >= RELEVANCE_THRESHOLD:

#             document.metadata["relevance_score"] = float(score)

#             relevant_documents.append(document)

#     relevant_documents.sort(
#         key=lambda doc: doc.metadata.get(
#             "relevance_score",
#             0
#         ),
#         reverse=True
#     )

#     return relevant_documents[:FINAL_TOP_K]


# def build_context(documents):

#     if not documents:
#         return ""

#     context_parts = []

#     for index, document in enumerate(
#         documents,
#         start=1
#     ):

#         source = document.metadata.get(
#             "source_file",
#             "Unknown"
#         )

#         page = document.metadata.get(
#             "page"
#         )

#         score = document.metadata.get(
#             "relevance_score",
#             0
#         )

#         location = source

#         if page is not None:
#             location += f", page {page + 1}"

#         context_parts.append(
#             f"""
# [Document {index}]

# Source: {location}

# Relevance Score: {score:.3f}

# {document.page_content}
# """
#         )

#     return "\n".join(context_parts)


# def get_sources(documents):

#     unique_sources = []

#     for document in documents:

#         source = document.metadata.get(
#             "source_file",
#             "Unknown"
#         )

#         if source not in unique_sources:
#             unique_sources.append(source)

#     return unique_sources

