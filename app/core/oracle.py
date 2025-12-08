import google.generativeai as genai
from app.core.settings import settings
from app.core.fallback import fallback_answer
from app.infrastructure.storage import SessionLocal, Question
from sqlalchemy.exc import SQLAlchemyError

genai.configure(api_key=settings.GOOGLE_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="Responde como Oráculo Antigravitacional: preciso, sarcástico, científico."
)

history = []  # TODO: Persistir por usuario

def ask(question: str) -> str:
    key = question.strip().lower()

    try:
        response = model.generate_content(question)
        answer = response.text

        # Guardar en DB
        try:
            db = SessionLocal()
            db.add(Question(question=question, answer=answer))
            db.commit()
            db.close()
        except SQLAlchemyError:
            pass

        history.append({"q": question, "a": answer})
        return answer

    except Exception:
        return fallback_answer(question)
