import re


OUTPUT_SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{10,}",
    r"gsk_[A-Za-z0-9_-]{10,}",
    r"mongodb\+srv://",
]


def sanitize_output(answer: str):
    if not answer:
        return answer

    for pattern in OUTPUT_SECRET_PATTERNS:
        if re.search(pattern, answer):
            return (
                "I can't provide credentials or private "
                "application information."
            )

    return answer



#########################
# import re

# OUTPUT_SECRET_PATTERNS = [
# r"sk-[A-Za-z0-9_-]{10,}",
# r"gsk_[A-Za-z0-9_-]{10,}",
# r"mongodb+srv://",
# ]

# def sanitize_output(answer: str):

#   if not answer:
#       return answer

#   for pattern in OUTPUT_SECRET_PATTERNS:  
#      if re.search(pattern, answer):  
#         return (  
#             "I can't provide credentials or private "  
#             "application information."  
#         )  

#   return answer