from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from app.core.settings import settings
from app.core.ai import ask_google

router = APIRouter()

class AskPayload(BaseModel):
    question: str

@router.post("/ask")
async def ask_endpoint(payload: AskPayload, authorization: str = Header(None)):
    if authorization != f"Bearer {settings.GOOGLE_API_KEY}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    answer = await ask_google(payload.question)
    return {"answer": answer}
