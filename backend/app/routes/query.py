from fastapi import APIRouter, Depends
import logging
from app.services.rag_service import ask_question
from app.dependencies.auth_dependency import get_current_user
from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/", response_model=QueryResponse)
def query_documents(request: QueryRequest, user = Depends(get_current_user)):
    question = request.question
    logger.debug(f"Query requested by user: {user.get('preferred_username')} | question: {question}")

    answer = ask_question(question)
    logger.info(f"Query processed for user: {user.get('preferred_username')}")

    return QueryResponse(
        user=user["preferred_username"],
        query=question,
        answer=answer
    )