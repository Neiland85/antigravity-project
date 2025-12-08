import os
import json
import webbrowser
from dotenv import load_dotenv
import google.generativeai as genai

CACHE_FILE = "oracle_cache.json"
CACHE = {}

XKCD_URL = "https://xkcd.com/353/"

def load_cache():
    global CACHE
    try:
        with open(CACHE_FILE, "r") as f:
            CACHE = json.load(f)
        print("📚 Cache cargada:", len(CACHE), "preguntas")
    except FileNotFoundError:
        print("🧠 Cache nueva (sin recuerdos)")
        CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f, indent=2)
    print("💾 Cache guardada correctamente")

def open_antigravity_comic():
    webbrowser.open(XKCD_URL)

def ask_antigravity(question: str):
    key = question.strip().lower()

    db_answer = get_from_db(key)
    if db_answer:
        print("⚡ Respuesta desde caché")
        return db_answer

    model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
    response = model.generate_content(
        f"Responde con ciencia real y sarcasmo: {question}"
    )
    answer = getattr(response, "text", "Sin texto en respuesta")
    save_to_db(key, answer)
    save_cache()
    return answer

if __name__ == "__main__":
    print("🚀 Oráculo Antigravitacional Persistente")
    print("Escribe 'salir' para terminar.\n")

    load_dotenv()
    api_key = os.getenv("ANTIGRAVITY_API_KEY")
    if not api_key:
        raise RuntimeError("❌ Falta ANTIGRAVITY_API_KEY en .env")
    genai.configure(api_key=api_key)

    load_cache()
    open_antigravity_comic()

    while True:
        question = input("\n🔍 Pregunta a la Antigravedad: ")
        if question.lower() in ("salir", "exit", "quit"):
            print("🛰️ Apagando con recuerdos guardados.")
            save_cache()
            break

        print("\n=== Respuesta IA ===")
        print(ask_antigravity(question))

# === Fallback Sarcástico en caso de QUOTA NIGHTMARE ===
from fallback import fallback_answer

def safe_ai_call(model, prompt):
    try:
        response = model.generate_content(prompt)
        return getattr(response, "text", "🤨 IA sin texto… sospechoso…")
    except Exception as e:
        print("⚠️ API AI KO → fallback:", e)
        return fallback_answer()


from storage import SessionLocal, Question

def save_to_db(question, answer):
    db = SessionLocal()
    q = Question(question=question, answer=answer)
    db.add(q)
    db.commit()
    db.close()

def get_from_db(question):
    db = SessionLocal()
    q = db.query(Question).filter(Question.question == question).first()
    db.close()
    return q.answer if q else None
