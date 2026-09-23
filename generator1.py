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







##############################
# from langchain_groq import ChatGroq

# from config import GROQ_API_KEY, GROQ_MODEL
# from prompts import MEDICAL_SYSTEM_PROMPT


# llm = ChatGroq(
#     api_key=GROQ_API_KEY,
#     model=GROQ_MODEL,
#     temperature=0
# )


# def call_model(
#     question,
#     context
#  ):


# #def generate_answer(question, context):

#     prompt = f"""
# {MEDICAL_SYSTEM_PROMPT}

# Retrieved medical context:

# {context}

# User question:

# {question}
# """

#     response = llm.invoke(prompt)

#     return response.content




#########################

# #from openai import OpenAI
# from langchain_groq import ChatGroq

# from groq import Groq

# from config import (
#     GROQ_API_KEY,
#     GROQ_MODEL

# )

# from prompts import (
#     MEDICAL_SYSTEM_PROMPT
# )


# client = ChatGroq(
#     api_key=GROQ_API_KEY,
#     model=GROQ_MODEL,
#     temperature=0.3  # درجة حرارة منخفضة للحصول على إجابات طبية دقيقة وثابتة
# )


# def call_model(
#     question,
#     context
# ):

#     prompt = MEDICAL_SYSTEM_PROMPT.format(
#         context=context
#     )

#     response = client.chat.completions.create(

#         model=GROQ_MODEL,

#        #response = client.chat.completions.create(
#         #model=GROQ_MODEL,
#         messages=[
#             {"role": "system", "content": prompt},
#             {"role": "user", "content": question}
#         ],
#         temperature=0.3  # درجة حرارة منخفضة للحصول على إجابات طبية دقيقة وثابتة
#     )
    
#     # إرجاع النص الناتج من رد الموديل
#     return response.choices[0].message.content


#         #instructions=prompt,
#         #input=question
    
# # 