from fastapi import FastAPI
from app.routes import document, query

app = FastAPI(title="AI Knowledge Assistant", description="A platform for RAG (Retrieval-Augmented Generation) applications")

app.include_router(document.router)
app.include_router(query.router)