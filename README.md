# AI-knowledge-assistant


## 🚀 Overview
A production-ready multi-user Retrieval-Augmented Generation (RAG) platform where users can upload documents and ask questions.

The system retrieves relevant content using vector search and generates accurate responses using an LLM.

---

## 🧠 Features

- Document Upload
- Semantic Search (RAG)
- Multi-user support
- Secure Authentication (Keycloak)
- Structured responses

---

## 🛠 Tech Stack

- FastAPI (Backend)
- Streamlit (Frontend)
- LangChain (Processing)
- Pinecone (Vector DB)
- LLaMA (via Groq)
- Keycloak (Auth)

---

## 📁 Project Structure
backend/
frontend/
vector_store/

---

## ⚙️ Setup Instructions

1. Create virtual environment
2. Install dependencies
3. Run FastAPI:
   uvicorn app.main:app --reload

4. Run Streamlit:
   streamlit run app.py

---

## 🔐 Authentication

Uses Keycloak for:
- Login
- Token validation
- Role-based access

---

## 👨‍💻 Author
Harsh Palan