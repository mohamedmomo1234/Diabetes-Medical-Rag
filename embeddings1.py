from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )







# from langchain_huggingface import HuggingFaceEmbeddings



# def get_embeddings():
#     return HuggingFaceEmbeddings(
#         model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )



#############
# embedding_model = HuggingFaceEmbeddings(
#     model_name=(
#         "sentence-transformers/"
#         "paraphrase-multilingual-MiniLM-L12-v2"
#     ),
#     model_kwargs={
#         "device": "cpu"
#     },
#     encode_kwargs={
#         "normalize_embeddings": True
#     }
# )