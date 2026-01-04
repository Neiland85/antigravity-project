from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json, os, logging, random
from sqlalchemy import func

from app.infrastructure.storage import SessionLocal, Question
from app.core.settings import settings
import google.generativeai as genai

# Setup genai from settings
genai.configure(api_key=settings.GOOGLE_API_KEY)

CACHE_FILE = "oracle_cache.json"
CACHE = {}

def load_cache():
    global CACHE
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                CACHE = json.load(f)
    except Exception as e:
        logging.error(f"Error loading cache: {e}")
        CACHE = {}

def save_cache():
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(CACHE, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving cache: {e}")

from app.infrastructure.storage import SessionLocal, Question, init_db
load_cache()
try:
    init_db()
except Exception as e:
    logging.error(f"Error initializing DB: {e}")

app = FastAPI()
import app.middleware.ratelimit as rl
app.middleware('http')(rl.rate_limit)

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "messages": []})

@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    # --- SENTINEL SECURITY CHECK ---
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{settings.SENTINEL_URL}/validate", json={"question": question}, timeout=2.0)
            if resp.status_code == 403:
                return templates.TemplateResponse("index.html", {
                    "request": request,
                    "messages": [{"question": question, "answer": "🛡️ SEGURIDAD: Petición bloqueada por Sentinel (Patrón no autorizado).", "source": "👮 Sentinel"}]
                })
    except Exception as e:
        logging.warning(f"Sentinel connection skipped: {e}")
    # -------------------------------

    key = question.lower().strip()

    if key in CACHE:
        answer = CACHE[key]
        source = "⚡ Caché"
    else:

        if settings.MOCK_AI:
            mock_responses = [
                "Según mis cálculos de la constante cosmológica, sí, pero solo los martes.",
                "La interferencia cuántica sugiere que el resultado es indeterminado hasta que lo observes.",
                "Correlación no implica causalidad, pero en este universo de juguete, todo es posible.",
                "He simulado este escenario 14 millones de veces y en solo una ganamos... ah, espera, pregunta equivocada.",
                "La entropía del sistema ha aumentado solo con leer esa pregunta."
            ]
            answer = f"{random.choice(mock_responses)} (Simulación completada con éxito r={random.random():.2f})"
            CACHE[key] = answer
            save_cache()
            source = "🧪 Modo Laboratorio (Mock)"
            
            # Guardar en DB (también en Mock para persistencia)
            try:
                db = SessionLocal()
                db.add(Question(question=question, answer=answer))
                db.commit()
                db.close()
            except Exception as e:
                logging.error(f"Error saving to DB (Mock): {e}")
        else:
            history_context = ""
            try:
                # 1. Recuperar contexto (Historia reciente)
                try:
                    db = SessionLocal()
                    last_interactions = db.query(Question).order_by(Question.id.desc()).limit(5).all()
                    db.close()
                    # Revertir para orden cronológico
                    for interaction in reversed(last_interactions):
                        history_context += f"User: {interaction.question}\nAI: {interaction.answer}\n"
                except Exception as ex:
                    logging.error(f"Error recuperando historial: {ex}")
                
                # 2. Detectar Modo Arquitecto
                architect_keywords = ["/plan", "plan:", "idea:", "arquitecto"]
                is_architect = any(k in question.lower() for k in architect_keywords)
                
                if is_architect:
                    system_prompt = (
                        "Eres un Arquitecto Matemático. Tu objetivo es formalizar la idea del usuario en un plan técnico.\n"
                        "NO generes el plan de inmediato. PRIMERO debes entrevistar al usuario.\n"
                        "Haz preguntas cortas y precisas para aclarar requisitos faltantes.\n"
                        "Solo cuando tengas toda la información, genera el plan matemático final.\n"
                        "Contexto de la conversación:\n"
                    )
                    full_prompt = f"{system_prompt}\n{history_context}\nUser: {question}\nAI (Architect):"
                else:
                # Modo Oráculo Sarcástico (Default)
                    full_prompt = (
                        "Responde como un científico loco y sarcástico.\n"
                        f"Contexto:\n{history_context}\n"
                        f"Pregunta: {question}"
                    )

                from app.core.reasoning import IntuitionEngine
                engine = IntuitionEngine()
                raw_answer = engine.generate_with_reasoning(full_prompt)
                
                # Formatear el pensamiento para HTML
                answer = raw_answer.replace("<thought>", "<details><summary>👁️ Ver Proceso de Intuición</summary><pre class='reasoning'>").replace("</thought>", "</pre></details>")
                
                CACHE[key] = answer
                save_cache()
                if is_architect:
                    source = "📐 Arquitecto (+Intuición)"
                else:
                    source = "🧠 IA (+Intuición)"
            
                # Guardar en DB History
                try:
                    db = SessionLocal()
                    db.add(Question(question=question, answer=answer))
                    db.commit()
                    db.close()
                except Exception as e:
                    logging.error(f"Error saving to DB: {e}")

            except Exception as e:
                logging.error(f"Error en Gemini API: {e}")
                
                try:
                    from app.core.local_reasoning import reason_locally
                    answer = reason_locally(question, context=history_context)
                    source = "🎛️ Local Transformers Node"
                except Exception as le:
                    logging.error(f"Error en Local Reasoning: {le}")
                    fallbacks = [
                        "La entropía local es demasiado alta para procesar tu pregunta. Intenta reducir el desorden de tu habitación primero.",
                        "El gato de Schrödinger se negó a cooperar. Está vivo y muerto a la vez, igual que este servidor.",
                        "Error 42: La respuesta es 42, pero olvidé cuál era la pregunta.",
                        "Mis transistores cuánticos están en huelga. Vuelve cuando la función de onda colapse.",
                        "He detectado una paradoja temporal en tu pregunta. Bloqueada por seguridad del continuo espacio-tiempo."
                    ]
                    answer = random.choice(fallbacks)
                    source = "🔮 Backup de Emergencia"

    # Análisis Retroactivo (Random Forest)
    try:
        from app.core.retroactive_node import intuition_node
        analysis = intuition_node.analyze(answer)
        analysis_text = f"\n\n[Retro-Análisis: {analysis['category']} (Confiabilidad: {int(analysis['confidence'] * 100)}%)]"
        answer += analysis_text
    except Exception as re:
        logging.error(f"Error en Retro-Analisis: {re}")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": [{"question": question, "answer": answer, "source": source}],
        }
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    db = SessionLocal()
    records = db.query(Question).order_by(Question.id.desc()).limit(50).all()
    db.close()
    return templates.TemplateResponse(
        "history.html",
        {"request": request, "records": records}
    )

@app.get("/random", response_class=HTMLResponse)
async def random_answer(request: Request):
    db = SessionLocal()
    record = db.query(Question).order_by(func.random()).first()
    db.close()
    return templates.TemplateResponse(
        "history.html",
        {"request": request, "records": [record] if record else []}
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
