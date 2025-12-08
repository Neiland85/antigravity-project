from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.core.fallback import fallback_answer
from app.core.oracle import ask

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_api(payload: QuestionRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")

    try:
        answer = ask(payload.question)
        return {"answer": answer}
    except Exception:
        return {"answer": fallback_answer(payload.question)}
