from google import generativeai as gen_ai
from app.core.settings import settings

gen_ai.configure(api_key=settings.GOOGLE_API_KEY)

async def ask_google(question: str) -> str:
    model = gen_ai.GenerativeModel("gemini-pro")
    response = await model.generate_content_async(question)
    return response.text
