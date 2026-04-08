from fastapi import APIRouter
from app.services.rag_service import ask_question

router = APIRouter(prefix="/query", tags=["Query"])

@router.get("/")
def query_documents(q: str):
    answer = ask_question(q)

    return {
        "query": q,
        "answer": answer
    }