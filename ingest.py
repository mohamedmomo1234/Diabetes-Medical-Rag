from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embeddings import get_embeddings

from config import (
    CHROMA_DIR,
    CHROMA_COLLECTION,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


DOCS_DIR = Path("data/medical_docs")


def load_documents():

    documents = []

    for file in DOCS_DIR.rglob("*"):

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension == ".pdf":

            docs = PyPDFLoader(
                str(file)
            ).load()

        elif extension == ".txt":

            docs = TextLoader(
                str(file),
                encoding="utf-8"
            ).load()

        elif extension == ".docx":

            docs = Docx2txtLoader(
                str(file)
            ).load()

        else:
            continue

        for doc in docs:

            doc.metadata["source_file"] = file.name
            doc.metadata["file_type"] = extension
            doc.metadata["document_type"] = "medical_reference"

        documents.extend(docs)

    return documents


def add_topic_metadata(documents):

    for doc in documents:

        filename = doc.metadata.get(
            "source_file",
            ""
        ).lower()

        if "diabetes" in filename:
            topic = "diabetes"

        elif "heart" in filename:
            topic = "heart"

        elif "skin" in filename:
            topic = "dermatology"

        elif "eye" in filename:
            topic = "eye"

        elif "neuro" in filename:
            topic = "neurology"

        elif (
            "anxiety" in filename
            or "stress" in filename
        ):
            topic = "anxiety_stress"

        else:
            topic = "general_medical"

        doc.metadata["topic"] = topic

    return documents


def create_vector_database():

    documents = load_documents()

    if not documents:

        raise ValueError(
            "No medical documents found "
            "inside data/medical_docs/"
        )

    print(
        f"Loaded documents: {len(documents)}"
    )

    documents = add_topic_metadata(
        documents
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(
        documents
    )

    for index, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = index

    print(
        f"Created chunks: {len(chunks)}"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=CHROMA_DIR,
        collection_name=CHROMA_COLLECTION
    )

    print(
        "Medical knowledge base created successfully."
    )


if __name__ == "__main__":
    create_vector_database()

