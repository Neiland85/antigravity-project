from fastapi import APIRouter, HTTPException, Header
from app.core.ai import ask_google_structured
from app.core.settings import settings

router = APIRouter()

@router.post("")
async def antigravity_api(payload: dict, authorization: str = Header(None)):
    if authorization != f"Bearer {settings.GOOGLE_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question'")

    response = await ask_google_structured(question)
    return response.model_dump()
