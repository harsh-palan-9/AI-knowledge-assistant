from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import logging
from app.services.document_service import save_file, process_document
from app.dependencies.auth_dependency import get_current_user, require_role

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/document", tags=["Document"])

@router.post("/upload/")
async def upload_document(
    file: UploadFile = File(...), 
    user = Depends(get_current_user)
):
    logger.debug(f"Upload endpoint accessed - File: {file.filename}")
    logger.debug(f"User info: {user}")

    if not file.filename.endswith((".pdf", ".txt")):
        logger.warning(f"Unsupported file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file type")

    logger.info(f"Processing file upload: {file.filename}")
    file_path = save_file(file)

    chunks, embeddings = process_document(file_path)

    logger.info(f"File processed successfully - Chunks: {len(chunks)}")
    return {
        "message": "File uploaded successfully",
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0])
    }