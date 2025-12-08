from fastapi import APIRouter
from app.core.oracle import ask

router = APIRouter()

@router.get("/ask")
def api_ask(question: str):
    return {"question": question, "answer": ask(question)}
