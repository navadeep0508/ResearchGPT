from fastapi import APIRouter, UploadFile, File
import os

from app.services.pdf_service import extract_text_from_pdf
from app.rag.chunker import (
    chunk_text,
    normalize_text
)
from app.rag.embedding import generate_embeddings
from app.rag.vector_store import store_embeddings

from app.auth.dependencies import get_current_user
from fastapi import Depends


router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...),current_user: str = Depends(get_current_user)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    pages = extract_text_from_pdf(file_path)

    all_chunks = []

    total_characters = 0

    for page in pages:

        normalized_page = normalize_text(page)

        total_characters += len(normalized_page)

        page_chunks = chunk_text(normalized_page)

        all_chunks.extend(page_chunks)

    embeddings = generate_embeddings(all_chunks)

    store_embeddings(all_chunks, embeddings)

    return {
        "filename": file.filename,
        "characters": total_characters,
        "chunks": len(all_chunks),
        "message": "Embeddings stored successfully"
    }