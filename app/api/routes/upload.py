from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.core.config import UPLOAD_DIR
from app.services.pdf_service import extract_text_from_pdf
from app.rag.chunker import (
    chunk_text,
    normalize_text
)
from app.rag.vector_store import store_documents

from app.auth.dependencies import get_current_user
from fastapi import Depends


router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...),current_user: str = Depends(get_current_user)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        pages = extract_text_from_pdf(file_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}") from exc

    all_chunks = []

    total_characters = 0

    for page in pages:

        normalized_page = normalize_text(page)

        total_characters += len(normalized_page)

        page_chunks = chunk_text(normalized_page)

        all_chunks.extend(page_chunks)

    if not all_chunks:
        raise HTTPException(status_code=400, detail="No usable text chunks found in PDF")

    try:
        store_documents(all_chunks)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not store document chunks: {exc}") from exc

    return {
        "filename": file.filename,
        "characters": total_characters,
        "chunks": len(all_chunks),
        "message": "Embeddings stored successfully"
    }
