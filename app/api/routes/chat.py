from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from app.rag.embedding import generate_query_embedding
from app.rag.vector_store import search_documents
from app.services.llm_service import generate_ans

from app.auth.dependencies import get_current_user
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.db.models import ChatHistory

router=APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    question:str

@router.post("/chat")
async def chat(request: ChatRequest, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        query_embedding = generate_query_embedding(request.question)
        result = search_documents(query_embedding)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    retrieved_chunks = result["documents"][0]
    # Pass chunks list directly to generate_ans
    generate_answer = generate_ans(request.question, retrieved_chunks)

    chat_entry = ChatHistory(
        question=request.question,
        answer=generate_answer,
        username=current_user
    )

    db.add(chat_entry)
    db.commit()

    return {
        "question": request.question,
        "retrieved_chunks": retrieved_chunks,
        "generated_answer": generate_answer
    }

@router.get("/history")
async def get_history(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = db.query(ChatHistory).filter(
        ChatHistory.username == current_user
    ).all()

    history = []
    for chat in chats:
        history.append({
            "question": chat.question,
            "answer": chat.answer
        })

    return {
        "history": history
    }
