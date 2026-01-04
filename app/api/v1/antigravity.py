from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.core.settings import settings
from app.core.ai import ask_google

router = APIRouter()

from typing import Optional

class QuestionRequest(BaseModel):
    question: Optional[str] = None

@router.post("/antigravity")
async def antigravity(request: QuestionRequest, authorization: str = Header(None)):
    if authorization != f"Bearer {settings.GOOGLE_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not request.question:
        raise HTTPException(status_code=400, detail="Missing question")

    answer = await ask_google(request.question)
    return {"answer": answer, "lift": "upward", "gravity": "ignored"}
