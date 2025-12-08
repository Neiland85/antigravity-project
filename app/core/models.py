from pydantic import BaseModel

class AntigravityResponse(BaseModel):
    thought: str
    effect: str
    risk_level: str
    sources: list[str]
