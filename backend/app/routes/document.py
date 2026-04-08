from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import save_file, process_document

router = APIRouter(prefix="/document", tags=["Document"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = save_file(file)

    chunks, embeddings = process_document(file_path)

    return {
        "message": "File uploaded successfully",
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0])
    }