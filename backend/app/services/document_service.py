import os
from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from langchain_core.documents import Document
from app.services.rag_service import vector_store

# 🔹 Save file
UPLOAD_DIR = "uploads"

def save_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


# 🔹 Read PDF
def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# 🔹 Read TXT
def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# 🔹 Split text
def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    return splitter.split_text(text)


# 🔹 Main processing function
def process_document(file_path: str):
    if file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_path.endswith(".txt"):
        text = read_txt(file_path)
    else:
        raise ValueError("Unsupported file type")


    chunks = split_text(text)

    documents = [Document(page_content=chunk) for chunk in chunks]

    vector_store.add_documents(documents)

    return {"message": "Document processed and stored successfully", "num_chunks": len(chunks)}