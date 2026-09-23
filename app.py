import os
import hmac
import streamlit as st

from config import ADMIN_PASSWORD

from graph import medical_graph


from database import (
    save_chat,
    get_chat_history
)

from feedback import save_feedback

from ingest import ensure_vector_database

ensure_vector_database()



# PAGE CONFIGURATION
st.set_page_config(
    page_title="Diabetes Medical RAG Assistant",
    page_icon="🩺",
    layout="centered"
)



# TITLE
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



# ADMIN

with st.sidebar:

    st.header("🔐 Admin")

    admin_password = ADMIN_PASSWORD

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


    
    # ADMIN CHAT HISTORY
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



# SESSION CHAT HISTORY
if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# USER QUESTION
question = st.chat_input(
    "Ask your Diabetes medical question in Arabic or English..."
)


if question:

    
    # SHOW USER QUESTION
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):

        st.markdown(question)


    
    # ASSISTANT
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching Diabetes medical knowledge..."
        ):

            try:

            
                # RUN MEDICAL RAG DIRECTLY
                result = medical_graph.invoke(
                    {
                        "question": question
                    }
                )

                answer = result.get(
                    "answer",
                    "No answer generated."
                )

                sources = result.get(
                    "sources",
                    []
                )


            
                # SAVE CHAT TO MONGODB
                try:

                    save_chat(
                        question,
                        answer,
                        sources
                    )

                except Exception as error:

                    print(
                        f"Database error: "
                        f"{type(error).__name__}"
                    )


        
            # APPLICATION ERROR

            except Exception as error:

                print(
                    f"Application error: "
                    f"{type(error).__name__}"
                )

                answer = (
                    "An error occurred while processing "
                    "your request. Please try again later."
                )

                sources = []


        
        # DISPLAY ANSWER
        st.markdown(
            answer
        )


        
        # DISPLAY SOURCES
        if sources:

            st.divider()

            st.subheader(
                "📚 Sources"
            )

            for source in sources:

                st.write(
                    f"- {source}"
                )


    
        # FEEDBACK
        st.divider()

        st.write(
            "Was this answer helpful?"
        )

        col1, col2 = st.columns(2)


        
        # POSITIVE FEEDBACK
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



        # NEGATIVE FEEDBACK
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



    # SAVE ASSISTANT MESSAGE
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


