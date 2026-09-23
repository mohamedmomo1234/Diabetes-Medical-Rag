# 🩺 Diabetes RAG Chatbot

An AI-powered medical question-answering system focused on
diabetes-related information using Retrieval-Augmented Generation (RAG).

## 📌 Project Overview

This project is a medical RAG chatbot designed to answer
diabetes-related questions using trusted medical documents.

Instead of relying only on the language model's internal knowledge,
the system retrieves relevant information from a medical knowledge base
and provides the retrieved context to the LLM before generating an answer.

The system is designed to reduce hallucinations and provide
source-aware medical information.

## 🏗️ System Architecture

Medical Documents
        ↓
Document Loading
        ↓
Document Cleaning
        ↓
Chunking
        ↓
Sentence Transformer
        ↓
Embeddings
        ↓
ChromaDB
        ↓
User Question
        ↓
Security Guard
        ↓
Diabetes Topic Guard
        ↓
Semantic Retrieval
        ↓
Relevance Filtering
        ↓
Context Building
        ↓
Medical Prompt
        ↓
Groq LLM
        ↓
Grounded Answer
        ↓
Source Documents
        ↓
MongoDB
        ↓
Feedback & Evaluation


## 🛠️ Technologies Used

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### LLM / Generative AI
- Groq
- Large Language Model

### RAG
- LangChain
- LangGraph
- ChromaDB

### Embeddings
- Sentence Transformers
- HuggingFace Embeddings

### Database
- ChromaDB for vector search
- MongoDB for chat history and feedback

### Monitoring
- LangSmith

### Document Processing
- PyPDF
- python-docx
- Recursive Character Text Splitter

### Programming Language
- Python 3.11

## 📂 Project Structure

```text
Rag_Medical/
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
├── data/
│   └── medical_docs/
│       └── diabetes.pdf
│
├── chroma_db/
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md

ثم:

```markdown
## 📄 File Responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Streamlit user interface |
| `api.py` | FastAPI backend |
| `graph.py` | LangGraph workflow |
| `generator.py` | Groq LLM generation |
| `retriever.py` | ChromaDB retrieval |
| `embeddings.py` | Sentence Transformer embeddings |
| `ingest.py` | Document ingestion and chunking |
| `security.py` | Input security and prompt-injection protection |
| `output_guard.py` | Output security |
| `prompts.py` | Medical system prompt |
| `config.py` | Environment configuration |
| `database.py` | MongoDB operations |
| `feedback.py` | User feedback |
| `health.py` | System health checks |
| `evaluation.py` | Retrieval evaluation |

## 🔎 How RAG Works

The chatbot follows a Retrieval-Augmented Generation architecture.

### 1. Document Ingestion

Medical documents are loaded from:

`data/medical_docs/`

Supported formats include:

- PDF
- TXT
- DOCX

### 2. Chunking

Large documents are divided into smaller chunks using
RecursiveCharacterTextSplitter.

### 3. Embeddings

Each chunk is converted into a numerical vector using
a pretrained multilingual Sentence Transformer.

### 4. Vector Database

The embeddings are stored in ChromaDB.

### 5. User Question

The user asks a diabetes-related question in Arabic or English.

### 6. Retrieval

The question is converted into an embedding and compared
with the medical document embeddings.

### 7. Relevance Filtering

The system retrieves the most relevant chunks and filters
out results below the configured relevance threshold.

### 8. Generation

The retrieved context is passed to the Groq LLM.

The LLM generates an answer based primarily on the retrieved
medical context.

### 9. Sources

The system returns the source document names used to generate
the answer.


## 🔐 Security

The project includes multiple security layers.

### Input Security

The system detects requests attempting to reveal:

- API keys
- passwords
- system prompts
- developer prompts
- environment variables
- private application data

### Prompt Injection Protection

User instructions cannot override the medical system instructions.

### Output Protection

Generated responses are checked before being returned to the user.

### Secrets Management

Sensitive credentials are stored in environment variables.

The `.env` file is excluded from Git using `.gitignore`.

API keys and database credentials are never hard-coded
into the source code.


## ⚕️ Medical Safety

This chatbot provides educational medical information.

It does not:

- Diagnose diseases
- Replace a doctor
- Provide personalized prescriptions
- Guarantee medical conclusions

For urgent or potentially dangerous symptoms,
users should seek appropriate professional medical care.


## 🗄️ MongoDB

MongoDB is used to store application data such as:

- Chat questions
- Generated answers
- Source documents
- Timestamps
- User feedback

MongoDB is not used as the medical knowledge base.

The medical knowledge base is stored in ChromaDB.


## 🔌 Frontend and Backend

The application separates the frontend from the backend.

### Streamlit

Provides the user interface.

### FastAPI

Provides the REST API used by the frontend.

Communication:

Streamlit
    ↓ HTTP POST
FastAPI `/chat`
    ↓
LangGraph
    ↓
RAG Pipeline
    ↓
Groq
    ↓
FastAPI
    ↓
Streamlit



---

# 14. تشغيل المشروع

```markdown
## 🚀 Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Rag_Medical

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


### 3. Environment Variables
Create a `.env` file in the root directory and add the following configuration:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-70b-8192

LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=medical-rag-chatbot

MONGODB_URI=your_mongodb_connection_string_here
MONGODB_DATABASE=medical_rag
MONGODB_COLLECTION=chat_history

ADMIN_PASSWORD=your_secure_admin_password_here


---

# 15. بناء ChromaDB

```markdown
## 📚 Build the Medical Knowledge Base

Place medical documents inside:

```text
data/medical_docs/

python ingest.py

## ▶️ Run Backend

```bash
uvicorn api:app --reload
http://127.0.0.1:8000
http://127.0.0.1:8000/docs

---

# 17. تشغيل Streamlit

```markdown
## 🖥️ Run Frontend

Open another terminal:

```bash
streamlit run app.py

---

## الشكل النهائي للمشروع

بعد التعديلات يبقى عندك:

```text
                         ┌──────────────┐
                         │   Streamlit  │
                         │  Diabetes UI │
                         └──────┬───────┘
                                │
                              HTTP
                                │
                         ┌──────▼───────┐
                         │   FastAPI    │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │  LangGraph   │
                         └──────┬───────┘
                                │
                    ┌───────────▼───────────┐
                    │ Security + Topic Guard│
                    └───────────┬───────────┘
                                │
                         ┌──────▼───────┐
                         │   ChromaDB   │
                         │   Retrieval  │
                         └──────┬───────┘
                                │
                         Relevant Context
                                │
                         ┌──────▼───────┐
                         │   Groq LLM   │
                         └──────┬───────┘
                                │
                           Grounded Answer
                                │
                     ┌──────────▼──────────┐
                     │ Sources + MongoDB   │
                     └─────────────────────┘











###########################
<!-- # 🩺 Medical RAG Chatbot

A medical information chatbot built with:

- GroqAPI(openai/gpt-oss-120b)
- LangChain
- LangGraph
- ChromaDB
- Sentence Transformers
- LangSmith
- Streamlit

## ⚠️ Medical Disclaimer

This project is for educational and informational purposes.

It is not a medical diagnosis system and should not replace
professional medical evaluation.

Do not use this project for emergency medical decisions.

---

# Architecture

User
  ↓
Streamlit
  ↓
LangGraph
  ↓
Security Check
  ↓
Sentence Transformer
  ↓
ChromaDB
  ↓
Retrieved Medical Context
  ↓
OpenAI GPT
  ↓
Answer + Sources

LangSmith is used for tracing and evaluation.

---

# Features

- Arabic questions
- English questions
- Mixed Arabic/English questions
- Medical terminology explanation
- Retrieval Augmented Generation
- Local multilingual embeddings
- ChromaDB vector database
- LangGraph workflow
- OpenAI GPT generation
- LangSmith tracing
- API key protection
- Prompt injection protection
- Medical source display
- Streamlit interface

---

# Project Structure

```text
medical-rag-chatbot/

├── app.py
├── graph.py
├── generator.py
├── retriever.py
├── embeddings.py
├── ingest.py
├── security.py
├── prompts.py
├── config.py
│
├── data/
│   └── medical_docs/
│
├── chroma_db/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md -->