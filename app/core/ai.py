from google import generativeai as gen_ai
from app.core.settings import settings
from app.core.models import AntigravityResponse

gen_ai.configure(api_key=settings.GOOGLE_API_KEY)

async def ask_google_structured(question: str) -> AntigravityResponse:
    model = gen_ai.GenerativeModel("gemini-pro")

    prompt = f"""
    Eres el motor oficial de Antigravity.
    Pregunta del usuario: "{question}"

    Devuelve JSON en este formato exacto:
    {{
      "thought": "breve análisis técnico",
      "effect": "impacto físico o científico",
      "risk_level": "bajo/medio/alto",
      "sources": ["url1", "url2"]
    }}
    """

    response = await model.generate_content_async(prompt)
    text = response.text

    return AntigravityResponse.model_validate_json(text)
