import google.generativeai as genai
from storage import SessionLocal, Question
from sqlalchemy.exc import SQLAlchemyError

def ask(question: str) -> str:
    db = SessionLocal()
    key = question.strip().lower()

    try:
        existing = db.query(Question).filter_by(question=key).first()
        if existing:
            return existing.answer

        model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
        response = model.generate_content(
            f"Responde con ciencia real y sarcasmo: {question}"
        )
        answer = response.text

        q = Question(question=key, answer=answer)
        db.add(q)
        db.commit()
        return answer

    except SQLAlchemyError as e:
        db.rollback()
        return "El universo se ha roto mientras intentábamos persistir tus tonterías."

    except Exception:
        return "La conexión cósmica falló. Paga Premium y hablamos."

    finally:
        db.close()
