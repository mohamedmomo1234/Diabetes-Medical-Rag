from retriever import retrieve_documents


TEST_CASES = [
    {
        "question": "What is diabetes?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "What are symptoms of diabetes?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "What causes diabetes?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "How is diabetes diagnosed?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "What are the risk factors for diabetes?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "How can diabetes be managed?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "What are complications of diabetes?",
        "expected_source": "diabetes.pdf"
    },
    {
        "question": "What is type 2 diabetes?",
        "expected_source": "diabetes.pdf"
    }
]


def run_retrieval_evaluation():

    total = len(TEST_CASES)
    correct = 0

    for test in TEST_CASES:

        documents = retrieve_documents(
            test["question"]
        )

        sources = [
            doc.metadata.get(
                "source_file",
                ""
            )
            for doc in documents
        ]

        if test["expected_source"] in sources:

            correct += 1
            status = "PASS"

        else:

            status = "FAIL"

        print(
            f"{status} | {test['question']}"
        )

        print(
            f"Retrieved: {sources}"
        )

        print()

    score = correct / total

    print(
        f"Retrieval accuracy: {score:.2%}"
    )


if __name__ == "__main__":
    run_retrieval_evaluation()





#########################
# from retriever import (
#     retrieve_documents
# )


# TEST_CASES = [
#     {
#         "question": "What is diabetes?",
#         "expected_source": "diabetes.pdf"
#     },
#     {
#         "question": "What are symptoms of diabetes?",
#         "expected_source": "diabetes.pdf"
#     }
# ]


# def run_retrieval_evaluation():

#     total = len(TEST_CASES)
#     correct = 0

#     for test in TEST_CASES:

#         documents = retrieve_documents(
#             test["question"]
#         )

#         sources = [
#             doc.metadata.get(
#                 "source_file",
#                 ""
#             )
#             for doc in documents
#         ]

#         if test["expected_source"] in sources:

#             correct += 1

#             status = "PASS"

#         else:

#             status = "FAIL"

#         print(
#             f"{status} | "
#             f"{test['question']}"
#         )

#         print(
#             f"Retrieved: {sources}"
#         )

#         print()

#     if total:

#         score = correct / total

#         print(
#             f"Retrieval accuracy: "
#             f"{score:.2%}"
#         )


# if __name__ == "__main__":
#     run_retrieval_evaluation()