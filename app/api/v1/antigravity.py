from fastapi import APIRouter, Header, HTTPException
from app.core.settings import settings
from app.core.ai import ask_google

router = APIRouter()

@router.post("/antigravity")
async def antigravity(question: str, authorization: str = Header(None)):
    if authorization != f"Bearer {settings.GOOGLE_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    answer = await ask_google(question)
    return {"answer": answer, "lift": "upward", "gravity": "ignored"}
