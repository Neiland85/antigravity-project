from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.core.oracle import ask

router = APIRouter()

async def require_key(x_api_key: str | None = Header(default=None)):
    expected = "fake"  # CI uses fake, override in prod with real env var
    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

@router.post("/ask")
async def ask_route(data: dict, _auth=Depends(require_key)):
    question = data.get("question", "")
    return {"answer": await ask(question)}
