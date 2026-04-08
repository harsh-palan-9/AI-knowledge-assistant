from fastapi import APIRouter, Depends
from app.services.rag_service import ask_question
from app.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/query", tags=["Query"])

@router.get("/")
def query_documents(q: str, user = Depends(get_current_user)):

    answer = ask_question(q)

    return {
        "user": user["preferred_username"],
        "query": q,
        "answer": answer
    }