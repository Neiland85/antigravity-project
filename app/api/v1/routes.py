from fastapi import APIRouter, Header
from app.core.oracle import ask

router = APIRouter()

@router.post("/ask")
async def ask_api(payload: dict, authorization: str = Header(None)):
    if authorization != "ArchitectSupreme":
        return {"error": "401 Unauthorized"}
    question = payload.get("question", "")
    return {"answer": ask(question)}
