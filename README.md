🩺 Diabetes Medical RAG Assistant
A medical Retrieval-Augmented Generation (RAG) chatbot focused on Diabetes medical information.

**Author: Mohamed Said Abdalaziz // 
https://github.com/mohamedmomo1234/Diabetes-Medical-Rag**

##Live Demo
https://diabetes-medical-rag-huebamm32s5n2h6odvkmjnsdk.streamlit.app/

##Project Overview

This project is a medical RAG chatbot designed to provide educational information about Diabetes using a medical knowledge base. The application combines document retrieval, semantic embeddings, ChromaDB, LangGraph, Groq, security controls, MongoDB, and Streamlit.

##RAG

Retrieval-Augmented Generation (RAG) retrieves relevant information from the medical knowledge base before sending the retrieved context to the language model.


##System Architecture

Internet
   ↓
Streamlit Cloud
   ↓
app.py
   ↓
LangGraph
   ↓
Security → Retrieval → Context → Groq → Output Guard
   ↓
ChromaDB
   ↓
MongoDB


##RAG Workflow

User Question
   ↓
Security Check
   ↓
Retrieve Relevant Documents
   ↓
Build Medical Context
   ↓
Generate Answer with Groq
   ↓
Output Guard
   ↓
Answer + Sources
   ↓
MongoDB Chat History


##Document Loading

Medical documents are stored inside data/medical_docs/. The ingestion pipeline loads supported medical documents and prepares them for retrieval.

##Chunking

Documents are divided into smaller text chunks using RecursiveCharacterTextSplitter. Chunk size and overlap are controlled through the project configuration.

##Embeddings

Sentence Transformers convert document chunks and user questions into numerical vector representations. A multilingual embedding model supports Arabic and English questions.

##ChromaDB

ChromaDB stores document embeddings and enables semantic similarity search over the medical knowledge base.

##Retrieval Configuration

TOP_K controls the initial number of retrieved candidates. FINAL_TOP_K controls the maximum number of relevant documents passed to the final context.

##Relevance Filtering

Retrieved documents are filtered using a configurable relevance threshold before being included in the final context.

##Context Building

Retrieved chunks are combined into structured medical context containing source information, page information when available, relevance information, and document content.

##LangGraph

LangGraph manages the workflow for security checking, retrieval, context validation, answer generation, and output protection.

##Security

The application protects against prompt injection and requests for sensitive information such as API keys, passwords, system prompts, developer prompts, environment variables, and private application data.

##Prompt Injection Protection
User input is checked before retrieval and generation. Requests attempting to override application instructions or reveal protected information are blocked.

##Output Protection

Generated output is checked for patterns that may indicate credentials or private application information before the response is displayed.

##Medical Safety

The chatbot provides educational medical information. It does not claim to diagnose users or provide personalized medical treatment. Potentially urgent symptoms should be evaluated by an appropriate healthcare professional.

##Groq

Groq is used as the language-model provider through LangChain. The configured model is controlled through the GROQ_MODEL environment variable.

##MongoDB

MongoDB stores chat history and feedback separately from the medical vector knowledge base.

##Feedback

Users can provide positive or negative feedback about generated answers. Feedback is stored in MongoDB.

##Admin Dashboard

The Streamlit sidebar provides an administrator area protected by an administrator password. Authenticated administrators can review stored chat history.



##Project Files

File
Responsibility
app.py
Streamlit interface and direct RAG execution
graph.py
LangGraph workflow
generator.py
Groq LLM generation
retriever.py
ChromaDB retrieval and context building
embeddings.py
Sentence Transformer embeddings
ingest.py
Medical document loading, chunking and indexing
security.py
Prompt-injection and secret-request protection
output_guard.py
Generated-output protection


##Project Structure

E:\Rag_Medical
│
├── app.py
├── api.py
├── graph.py
├── generator.py
├── retriever.py
├── embeddings.py
├── ingest.py
├── security.py
├── output_guard.py
├── prompts.py
├── config.py
├── database.py
├── feedback.py
├── health.py
├── evaluation.py
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── medical_docs/
│       └── diabetes.pdf
│
└── chroma_db/


##Backend Integration

The current architecture integrates the RAG workflow directly into Streamlit. app.py invokes the LangGraph workflow directly and does not require a separate backend server for normal application execution.

##Installation

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


##Environment Variables
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=false
LANGSMITH_PROJECT=medical-rag-chatbot
MONGODB_URI=your_mongodb_uri
MONGODB_DATABASE=medical_rag
MONGODB_COLLECTION=chat_history
ADMIN_PASSWORD=your_admin_password

##Git Ignore

.env
.venv/
venv/
__pycache__/
*.pyc
chroma_db/
.ipynb_checkpoints/


##Building the Knowledge Base

python ingest.py


##Streamlit Cloud Deployment

The application can be deployed directly to Streamlit Cloud. Sensitive environment variables are configured through Streamlit Cloud Secrets.

##RAG Evaluation

RAG evaluation should measure retrieval quality and answer quality separately. Retrieval can be evaluated using relevant documents, relevance scores, and coverage of supported medical questions.

##RAG vs Model Training

This project uses RAG rather than training the language model on the medical documents. Documents are indexed into a vector database and retrieved at query time.

##Technologies

Python, Streamlit, LangChain, LangGraph, LangSmith, ChromaDB, Sentence Transformers, Hugging Face embeddings, Groq, MongoDB, PyPDF, python-docx, Git, and GitHub.

##Security Architecture

Security is implemented through input validation, prompt-injection protection, protected system instructions, output protection, environment-based secret management, and administrator authentication.

##Limitations

The chatbot is limited by the content and quality of the medical documents available in its knowledge base. It is not a replacement for a qualified healthcare professional.

##Future Improvements

Possible improvements include expanding the trusted medical knowledge base, improving retrieval evaluation, adding reranking, improving Arabic medical terminology retrieval, and expanding automated RAG evaluation.

##Medical Knowledge Sources

The medical knowledge base should use reliable and authoritative medical references such as recognized medical organizations and official health information sources.

##Current Deployment

The current application is deployed as a Streamlit application and uses the integrated architecture described in this README.

##Project Status

The project is currently focused on Diabetes medical information and uses ChromaDB retrieval, Sentence Transformer embeddings, LangGraph orchestration, Groq generation, MongoDB storage, security controls, and Streamlit.

##Disclaimer

This project is for educational and software-development purposes. It does not provide medical diagnosis or personalized medical treatment. Users should consult qualified healthcare professionals for medical decisions.

**Author: Mohamed Said Abdalaziz // 
https://github.com/mohamedmomo1234/Diabetes-Medical-Rag**






