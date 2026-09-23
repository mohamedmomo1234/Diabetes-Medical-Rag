import os
import hmac
import requests

import streamlit as st

from config import (
    API_URL,
    API_SECRET_KEY
)

from database import (
    save_chat,
    get_chat_history
)

from feedback import save_feedback


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Diabetes Medical RAG Assistant",
    page_icon="🩺",
    layout="centered"
)


# =========================
# TITLE
# =========================

st.title(
    "🩺 Diabetes Medical RAG Assistant"
)

st.info(
    "You can ask about diabetes symptoms, causes, "
    "risk factors, type 1 and type 2 diabetes, MODY, "
    "prevention, diagnosis, management, low blood glucose, "
    "insulin, medicines, A1C tests, diabetes and food, "
    "pregnancy, gum disease, sexual and urological problems, "
    "eye disease, kidney disease, and heart disease."
)

st.caption(
    "Diabetes medical information assistant powered by "
    "RAG + Groq + ChromaDB + Sentence Transformers"
)

st.warning(
    "This chatbot provides educational diabetes medical "
    "information and is not a substitute for professional "
    "medical care."
)


# =========================
# ADMIN
# =========================

with st.sidebar:

    st.header("🔐 Admin")

    admin_password = os.getenv(
        "ADMIN_PASSWORD"
    )

    password_input = st.text_input(
        "Admin password",
        type="password"
    )

    if st.button("Login"):

        if (
            admin_password
            and password_input
            and hmac.compare_digest(
                password_input,
                admin_password
            )
        ):

            st.session_state[
                "admin_authenticated"
            ] = True

        else:

            st.session_state[
                "admin_authenticated"
            ] = False

            st.error(
                "Incorrect password"
            )


    # =========================
    # ADMIN CHAT HISTORY
    # =========================

    if st.session_state.get(
        "admin_authenticated",
        False
    ):

        st.success(
            "Admin authenticated"
        )

        if st.button("Logout"):

            st.session_state[
                "admin_authenticated"
            ] = False

            st.rerun()


        st.divider()

        st.subheader(
            "📊 Chat History"
        )

        try:

            history = get_chat_history()

            if not history:

                st.info(
                    "No conversations saved yet."
                )

            else:

                st.write(
                    f"Total conversations: "
                    f"{len(history)}"
                )

                for chat in history:

                    created_at = chat.get(
                        "created_at"
                    )

                    if created_at:

                        created_at = (
                            created_at.strftime(
                                "%Y-%m-%d %H:%M:%S UTC"
                            )
                        )

                    st.write(
                        f"📅 {created_at}"
                    )

                    st.write(
                        "Question:",
                        chat.get(
                            "question",
                            ""
                        )
                    )

                    st.write(
                        "Answer:",
                        chat.get(
                            "answer",
                            ""
                        )
                    )

                    sources = chat.get(
                        "sources",
                        []
                    )

                    if sources:

                        st.write(
                            "Sources:"
                        )

                        for source in sources:

                            st.write(
                                f"- {source}"
                            )

                    st.divider()

        except Exception:

            st.error(
                "Could not load chat history."
            )


# =========================
# SESSION CHAT HISTORY
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================
# USER QUESTION
# =========================

question = st.chat_input(
    "Ask your Diabetes medical question in Arabic or English..."
)


if question:

    # =========================
    # SHOW USER QUESTION
    # =========================

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):

        st.markdown(question)


    # =========================
    # ASSISTANT
    # =========================

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching Diabetes medical knowledge..."
        ):

            try:

                # =========================
                # API REQUEST
                # =========================

                response = requests.post(

                    f"{API_URL}/chat",

                    json={
                        "question": question
                    },

                    headers={
                        "X-API-Key":
                        API_SECRET_KEY
                    },

                    timeout=120
                )


                # =========================
                # SUCCESS
                # =========================

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer generated."
                    )

                    sources = data.get(
                        "sources",
                        []
                    )


                    # =========================
                    # SAVE CHAT TO MONGODB
                    # =========================

                    try:

                        save_chat(
                            question,
                            answer,
                            sources
                        )

                    except Exception:

                        # Do not expose
                        # database errors
                        # to the user.

                        pass


                # =========================
                # UNAUTHORIZED
                # =========================

                elif response.status_code == 401:

                    answer = (
                        "Authentication failed. "
                        "Please contact the administrator."
                    )

                    sources = []


                # =========================
                # RATE LIMIT
                # =========================

                elif response.status_code == 429:

                    answer = (
                        "Too many requests. "
                        "Please wait a moment and try again."
                    )

                    sources = []


                # =========================
                # BAD REQUEST
                # =========================

                elif response.status_code == 400:

                    answer = (
                        "The question could not be processed. "
                        "Please check your question and try again."
                    )

                    sources = []


                # =========================
                # SERVER ERROR
                # =========================

                elif response.status_code == 500:

                    answer = (
                        "The backend service is temporarily "
                        "unavailable. Please try again later."
                    )

                    sources = []


                # =========================
                # OTHER RESPONSE
                # =========================

                else:

                    answer = (
                        "An unexpected error occurred. "
                        "Please try again later."
                    )

                    sources = []


            # =========================
            # CONNECTION ERROR
            # =========================

            except requests.exceptions.ConnectionError:

                answer = (
                    "Unable to connect to the backend service. "
                    "Please try again later."
                )

                sources = []


            # =========================
            # TIMEOUT
            # =========================

            except requests.exceptions.Timeout:

                answer = (
                    "The request took too long to process. "
                    "Please try again."
                )

                sources = []


            # =========================
            # OTHER ERROR
            # =========================

            except Exception as error:

                print(
                    f"Application error: "
                    f"{type(error).__name__}"
                )

                answer = (
                    "An error occurred while processing "
                    "your request. Please try again."
                )

                sources = []


        # =========================
        # DISPLAY ANSWER
        # =========================

        st.markdown(
            answer
        )


        # =========================
        # DISPLAY SOURCES
        # =========================

        if sources:

            st.divider()

            st.subheader(
                "📚 Sources"
            )

            for source in sources:

                st.write(
                    f"- {source}"
                )


        # =========================
        # FEEDBACK
        # =========================

        st.divider()

        st.write(
            "Was this answer helpful?"
        )


        col1, col2 = st.columns(2)


        # =========================
        # POSITIVE FEEDBACK
        # =========================

        with col1:

            if st.button(
                "👍 Helpful",
                key=f"up_{len(st.session_state.messages)}"
            ):

                try:

                    save_feedback(
                        question,
                        answer,
                        "positive"
                    )

                    st.success(
                        "Thanks for your feedback."
                    )

                except Exception:

                    st.error(
                        "Could not save feedback."
                    )


        # =========================
        # NEGATIVE FEEDBACK
        # =========================

        with col2:

            if st.button(
                "👎 Not helpful",
                key=f"down_{len(st.session_state.messages)}"
            ):

                try:

                    save_feedback(
                        question,
                        answer,
                        "negative"
                    )

                    st.success(
                        "Thanks for your feedback."
                    )

                except Exception:

                    st.error(
                        "Could not save feedback."
                    )


    # =========================
    # SAVE ASSISTANT MESSAGE
    # =========================

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })










###############################
# import os
# import hmac
# import requests

# import streamlit as st

# from database import (
#     save_chat,
#     get_chat_history
# )

# from feedback import save_feedback


# API_URL = "http://127.0.0.1:8000"


# st.set_page_config(
#     page_title="Diabetes Medical RAG Assistant",
#     page_icon="🩺",
#     layout="centered"
# )


# st.title("🩺 Diabetes Medical RAG Assistant")

# st.info(
#     "You can ask about diabetes symptoms, causes, risk factors type 2 diabetes, MODY, prevention type 2 diabetes,"
#     "diagnosis, management, Low Blood Glucose, type 1 and type 2 diabetes, Insulin,medicines ,A1C Test,"
#     "diabetes with food, pregnancy, Gum disease, Sexual, Urological, Eye, Kidney, heart disease"
# )

# st.caption(
#     "Diabetes Medical information assistant powered by "
#     "RAG + Groq + ChromaDB + Sentence Transformers"
# )

# st.warning(
#     "This chatbot provides educational Diabetes medical "
#     "information and is not a substitute for "
#     "professional medical care."
# )


# # =========================
# # ADMIN
# # =========================

# with st.sidebar:

#     st.header("🔐 Admin")

#     admin_password = os.getenv(
#         "ADMIN_PASSWORD"
#     )

#     password_input = st.text_input(
#         "Admin password",
#         type="password"
#     )

#     if st.button("Login"):

#         if (
#             admin_password
#             and password_input
#             and hmac.compare_digest(
#                 password_input,
#                 admin_password
#             )
#         ):

#             st.session_state[
#                 "admin_authenticated"
#             ] = True

#         else:

#             st.session_state[
#                 "admin_authenticated"
#             ] = False

#             st.error(
#                 "Incorrect password"
#             )

#     if st.session_state.get(
#         "admin_authenticated",
#         False
#     ):

#         st.success(
#             "Admin authenticated"
#         )

#         if st.button("Logout"):

#             st.session_state[
#                 "admin_authenticated"
#             ] = False

#             st.rerun()

#         st.divider()

#         st.subheader(
#             "📊 Chat History"
#         )

#         try:

#             history = get_chat_history()

#             if not history:

#                 st.info(
#                     "No conversations saved yet."
#                 )

#             else:

#                 st.write(
#                     f"Total conversations: "
#                     f"{len(history)}"
#                 )

#                 for chat in history:

#                     created_at = chat.get(
#                         "created_at"
#                     )

#                     if created_at:

#                         created_at = (
#                             created_at.strftime(
#                                 "%Y-%m-%d %H:%M:%S UTC"
#                             )
#                         )

#                     st.write(
#                         f"📅 {created_at}"
#                     )

#                     st.write(
#                         "Question:",
#                         chat.get(
#                             "question",
#                             ""
#                         )
#                     )

#                     st.write(
#                         "Answer:",
#                         chat.get(
#                             "answer",
#                             ""
#                         )
#                     )

#                     sources = chat.get(
#                         "sources",
#                         []
#                     )

#                     if sources:

#                         st.write(
#                             "Sources:"
#                         )

#                         for source in sources:

#                             st.write(
#                                 f"- {source}"
#                             )

#                     st.divider()

#         except Exception:

#             st.error(
#                 "Could not load chat history."
#             )


# # =========================
# # CHAT HISTORY
# # =========================

# if "messages" not in st.session_state:

#     st.session_state.messages = []


# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )


# # =========================
# # USER QUESTION
# # =========================

# question = st.chat_input(
#     "Ask your Diabetes medical question in Arabic or English..."
# )


# if question:

#     st.session_state.messages.append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):

#         st.markdown(question)


#     # =========================
#     # ASSISTANT
#     # =========================

#     with st.chat_message("assistant"):

#         with st.spinner(
#             "Searching Diabetes medical knowledge..."
#         ):

#             try:

#                 # Send question to FastAPI
#                 response = requests.post(
#                     f"{API_URL}/chat",
#                     json={
#                         "question": question
#                     },
#                     timeout=120
#                 )


#                 # =========================
#                 # FASTAPI RESPONSE
#                 # =========================

#                 if response.status_code == 200:

#                     data = response.json()

#                     answer = data.get(
#                         "answer",
#                         "No answer generated."
#                     )

#                     sources = data.get(
#                         "sources",
#                         []
#                     )

#                 else:

#                     answer = (
#                         "An error occurred while connecting"
#                         "to the backend service." 
#                     )

#                     sources = []


#             except requests.exceptions.ConnectionError:

#                 answer = (
#                     "Unable to connect to the FastAPI Backend."
#                     "Please ensure that the FastAPI service is running at"
#                     "http://127.0.0.1:8000"
#                 )

#                 sources = []


#             except requests.exceptions.Timeout:

#                 answer = (
#                     "The order took too long to process."
#                     "Please try again."
#                 )

#                 sources = []


#             except Exception as error:

#                 print(
#                     f"Application error: "
#                     f"{type(error).__name__}"
#                 )

#                 answer = (
#                     "An error occurred while processing your request. "
#                     "Please try again."
#                 )

#                 sources = []


#         # =========================
#         # DISPLAY ANSWER
#         # =========================

#         st.markdown(answer)


#         # =========================
#         # SOURCES
#         # =========================

#         if sources:

#             st.divider()

#             st.subheader(
#                 "📚 Sources"
#             )

#             for source in sources:

#                 st.write(
#                     f"- {source}"
#                 )


#         # =========================
#         # FEEDBACK
#         # =========================

#         st.divider()

#         st.write(
#             "Was this answer helpful?"
#         )


#         col1, col2 = st.columns(2)


#         with col1:

#             if st.button(
#                 "👍 Helpful",
#                 key=f"up_{len(st.session_state.messages)}"
#             ):

#                 try:

#                     save_feedback(
#                         question,
#                         answer,
#                         "positive"
#                     )

#                     st.success(
#                         "Thanks for your feedback."
#                     )

#                 except Exception:

#                     st.error(
#                         "Could not save feedback."
#                     )


#         with col2:

#             if st.button(
#                 "👎 Not helpful",
#                 key=f"down_{len(st.session_state.messages)}"
#             ):

#                 try:

#                     save_feedback(
#                         question,
#                         answer,
#                         "negative"
#                     )

#                     st.success(
#                         "Thanks for your feedback."
#                     )

#                 except Exception:

#                     st.error(
#                         "Could not save feedback."
#                     )


#     # =========================
#     # SAVE CHAT IN SESSION
#     # =========================

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer
#     })





########################################################
# import os
# import hmac
# import requests

# import streamlit as st

# from graph import medical_graph
# from database import (
#     save_chat,
#     get_chat_history
# )
# from feedback import save_feedback


# st.set_page_config(
#     page_title="Medical RAG Assistant",
#     page_icon="🩺",
#     layout="centered"
# )


# st.title("🩺 Medical RAG Assistant")

# st.caption(
#     "Medical information assistant powered by "
#     "RAG + Groq"
# )

# st.warning(
#     "This chatbot provides educational medical "
#     "information and is not a substitute for "
#     "professional medical care."
# )


# # =========================
# # ADMIN
# # =========================

# with st.sidebar:

#     st.header("🔐 Admin")

#     admin_password = os.getenv(
#         "ADMIN_PASSWORD"
#     )

#     password_input = st.text_input(
#         "Admin password",
#         type="password"
#     )

#     if st.button("Login"):

#         if (
#             admin_password
#             and password_input
#             and hmac.compare_digest(
#                 password_input,
#                 admin_password
#             )
#         ):

#             st.session_state[
#                 "admin_authenticated"
#             ] = True

#         else:

#             st.session_state[
#                 "admin_authenticated"
#             ] = False

#             st.error(
#                 "Incorrect password"
#             )

#     if st.session_state.get(
#         "admin_authenticated",
#         False
#     ):

#         st.success(
#             "Admin authenticated"
#         )

#         if st.button("Logout"):

#             st.session_state[
#                 "admin_authenticated"
#             ] = False

#             st.rerun()

#         st.divider()

#         st.subheader(
#             "📊 Chat History"
#         )

#         try:

#             history = get_chat_history()

#             if not history:

#                 st.info(
#                     "No conversations saved yet."
#                 )

#             else:

#                 st.write(
#                     f"Total conversations: "
#                     f"{len(history)}"
#                 )

#                 for chat in history:

#                     created_at = chat.get(
#                         "created_at"
#                     )

#                     if created_at:

#                         created_at = (
#                             created_at.strftime(
#                                 "%Y-%m-%d %H:%M:%S UTC"
#                             )
#                         )

#                     st.write(
#                         f"📅 {created_at}"
#                     )

#                     st.write(
#                         "Question:",
#                         chat.get(
#                             "question",
#                             ""
#                         )
#                     )

#                     st.write(
#                         "Answer:",
#                         chat.get(
#                             "answer",
#                             ""
#                         )
#                     )

#                     sources = chat.get(
#                         "sources",
#                         []
#                     )

#                     if sources:

#                         st.write(
#                             "Sources:"
#                         )

#                         for source in sources:
#                             st.write(
#                                 f"- {source}"
#                             )

#                     st.divider()

#         except Exception:

#             st.error(
#                 "Could not load chat history."
#             )


# # =========================
# # CHAT
# # =========================

# if "messages" not in st.session_state:

#     st.session_state.messages = []


# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )


# question = st.chat_input(
#     "Ask your medical question in Arabic or English..."
# )


# if question:

#     st.session_state.messages.append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):

#         st.markdown(question)

#     with st.chat_message("assistant"):

#         with st.spinner(
#             "Searching medical knowledge..."
#         ):

#             try:

#                 result = medical_graph.invoke({
#                     "question": question
#                 })

#                 answer = result.get(
#                     "answer",
#                     "حدث خطأ غير متوقع."
#                 )

#                 sources = result.get(
#                     "sources",
#                     []
#                 )

#                 save_chat(
#                     question=question,
#                     answer=answer,
#                     sources=sources
#                 )

#             except Exception as error:

#                 print(
#                     f"Application error: "
#                     f"{type(error).__name__}"
#                 )

#                 answer = (
#                     "حدث خطأ مؤقت في الخدمة. "
#                     "حاول مرة أخرى."
#                 )

#         st.markdown(answer)

#         st.divider()

#         st.write(
#             "Was this answer helpful?"
#         )

#         col1, col2 = st.columns(2)

#         with col1:

#             if st.button(
#                 "👍 Helpful",
#                 key=f"up_{len(st.session_state.messages)}"
#             ):

#                 try:

#                     save_feedback(
#                         question,
#                         answer,
#                         "positive"
#                     )

#                     st.success(
#                         "Thanks for your feedback."
#                     )

#                 except Exception:

#                     st.error(
#                         "Could not save feedback."
#                     )

#         with col2:

#             if st.button(
#                 "👎 Not helpful",
#                 key=f"down_{len(st.session_state.messages)}"
#             ):

#                 try:

#                     save_feedback(
#                         question,
#                         answer,
#                         "negative"
#                     )

#                     st.success(
#                         "Thanks for your feedback."
#                     )

#                 except Exception:

#                     st.error(
#                         "Could not save feedback."
#                     )

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer
#     })






###########################################################

# import streamlit as st
# import os
# import hmac

# from graph import medical_graph

# from database import (
#     save_chat,
#     get_chat_history
# )


# st.set_page_config(
#     page_title="Medical RAG Assistant",
#     page_icon="🩺",
#     layout="centered"
# )


# st.title(
#     "🩺 Medical RAG Assistant"
# )


# st.caption(
#     "Medical information assistant powered by RAG + Groq"
# )


# st.warning(
#     "This chatbot provides educational medical information "
#     "and is not a substitute for professional medical care."
# )


# with st.sidebar:

#     st.header("🔐 Admin")

#     admin_password = os.getenv(
#         "ADMIN_PASSWORD"
#     )

#     password_input = st.text_input(
#         "Admin password",
#         type="password"
#     )

#     if st.button("Login"):

#         if (
#             admin_password
#             and password_input
#             and hmac.compare_digest(
#                 password_input,
#                 admin_password
#             )
#         ):

#             st.session_state.admin_authenticated = True

#         else:

#             st.session_state.admin_authenticated = False

#             st.error(
#                 "Incorrect password"
#             )


#     if st.session_state.get(
#         "admin_authenticated",
#         False
#     ):

#         st.success(
#             "Admin authenticated"
#         )

#         st.divider()

#         st.subheader(
#             "📊 Chat History"
#         )

#         history = get_chat_history()

#         if not history:

#             st.info(
#                 "No conversations saved yet."
#             )

#         else:

#             st.write(
#                 f"Total conversations: {len(history)}"
#             )

#             for chat in history:

#                 created_at = chat.get(
#                     "created_at"
#                 )

#                 if created_at:

#                     created_at = created_at.strftime(
#                         "%Y-%m-%d %H:%M:%S UTC"
#                     )

#                 st.markdown(
#                     f"**📅 {created_at}**"
#                 )

#                 st.markdown(
#                     f"**Question:** {chat.get('question', '')}"
#                 )

#                 st.markdown(
#                     f"**Answer:** {chat.get('answer', '')}"
#                 )

#                 sources = chat.get(
#                     "sources",
#                     []
#                 )

#                 if sources:

#                     st.markdown(
#                         "**Sources:**"
#                     )

#                     for source in sources:

#                         st.write(
#                             f"- {source}"
#                         )

#                 st.divider()


# if "messages" not in st.session_state:

#     st.session_state.messages = []


# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )


# question = st.chat_input(
#     "Ask your medical question in Arabic or English..."
# )


# if question:

#     st.session_state.messages.append({

#         "role": "user",

#         "content": question
#     })


#     with st.chat_message("user"):

#         st.markdown(question)


#     with st.chat_message("assistant"):

#         with st.spinner(
#             "Searching medical knowledge..."
#         ):

#             result = medical_graph.invoke({

#                 "question": question
#             })


#             answer = result.get(
#                 "answer",
#                 "حدث خطأ غير متوقع."
#             )


#             sources = result.get(
#                 "sources",
#                 []
#             )


#             save_chat(
#                 question=question,
#                 answer=answer,
#                 sources=sources
#             )


#         st.markdown(answer)


#     st.session_state.messages.append({

#         "role": "assistant",

#         "content": answer
#     })












###################################################
# import streamlit as st

# from graph import medical_graph

# #from database import save_chat

# from database import( 
    
#     save_chat ,
#     get_chat_history )


# st.set_page_config(
#     page_title="Medical RAG Assistant",
#     page_icon="🩺",
#     layout="centered"
# )


# st.title(
#     "🩺 Medical RAG Assistant"
# )


# st.caption(
#     "Medical information assistant powered by RAG + Groq"
# )


# st.warning(
#     "This chatbot provides educational medical information "
#     "and is not a substitute for professional medical care."
# )

# with st.sidebar:



#     st.header("🗄️ MongoDB")

#     if st.button("View Chat History"):

#         history = get_chat_history()

#         if not history:

#             st.info(
#                 "No conversations saved yet."
#             )

#         else:

#             for chat in history:

#                 created_at = chat.get(
#                     "created_at"
#                 )

#                 if created_at:

#                     created_at = created_at.strftime(
#                         "%Y-%m-%d %H:%M:%S"
#                     )

#                 st.markdown(
#                     f"**📅 {created_at}**"
#                 )

#                 st.markdown(
#                     f"**Question:** {chat.get('question', '')}"
#                 )

#                 st.markdown(
#                     f"**Answer:** {chat.get('answer', '')}"
#                 )

#                 sources = chat.get(
#                     "sources",
#                     []
#                 )

#                 if sources:

#                     st.markdown(
#                         "**Sources:**"
#                     )

#                     for source in sources:

#                         st.write(
#                             f"- {source}"
#                         )

#                 st.divider()


# if "messages" not in st.session_state:

#     st.session_state.messages = []


# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )


# question = st.chat_input(
#     "Ask your medical question in Arabic or English..."
# )


# if question:

#     st.session_state.messages.append({

#         "role": "user",

#         "content": question
#     })


#     with st.chat_message("user"):

#         st.markdown(question)


#     with st.chat_message(
#         "assistant"
#     ):

#         with st.spinner(
#             "Searching medical knowledge..."
#         ):

#             result = medical_graph.invoke({

#                 "question": question
#             })


#             answer = result.get(

#                 "answer",

#                 "حدث خطأ غير متوقع."
#             )


#             sources = result.get(

#                 "sources",

#                 []
#             )


#             save_chat(

#                 question=question,

#                 answer=answer,

#                 sources=sources
#             )


#         st.markdown(answer)


#     st.session_state.messages.append({

#         "role": "assistant",

#         "content": answer
#     })




#####################################################
# import streamlit as st

# from graph import (
#     medical_graph
# )

# st.set_page_config(

#     page_title="Medical RAG Assistant",

#     page_icon="🩺",

#     layout="centered"
# )


# st.title(
#     "🩺 Medical RAG Assistant"
# )


# st.caption(
#     "Medical information assistant powered by RAG + OpenAI"
# )


# st.warning(
#     "This chatbot provides educational medical information "
#     "and is not a substitute for professional medical care."
# )


# if "messages" not in st.session_state:

#     st.session_state.messages = []


# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )


# question = st.chat_input(
#     "Ask your medical question in Arabic or English..."
# )


# if question:

#     st.session_state.messages.append({

#         "role": "user",

#         "content": question
#     })


#     with st.chat_message("user"):

#         st.markdown(question)


#     with st.chat_message(
#         "assistant"
#     ):

#         with st.spinner(
#             "Searching medical knowledge..."
#         ):

#             result = medical_graph.invoke({

#                 "question": question
#             })


#             answer = result.get(

#                 "answer",

#                 "حدث خطأ غير متوقع."
#             )


#         st.markdown(answer)


#     st.session_state.messages.append({

#         "role": "assistant",

#         "content": answer
#     })