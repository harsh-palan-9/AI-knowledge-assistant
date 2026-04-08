from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.document_service import save_file, process_document
from app.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/document", tags=["Document"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), user = Depends(get_current_user)):

    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = save_file(file)

    chunks, embeddings = process_document(file_path)

    return {
        "message": "File uploaded successfully",
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0])
    }