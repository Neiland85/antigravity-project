from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json, os
from dotenv import load_dotenv
import google.generativeai as genai

CACHE_FILE = "oracle_cache.json"
CACHE = {}

def load_cache():
    global CACHE
    try:
        with open(CACHE_FILE, "r") as f:
            CACHE = json.load(f)
    except:
        CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f, indent=2)

load_dotenv()
api_key = os.getenv("ANTIGRAVITY_API_KEY")
genai.configure(api_key=api_key)

load_cache()

app = FastAPI(); import app.middleware.ratelimit as rl; app.middleware('http')(rl.rate_limit)
templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "messages": []})

@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    key = question.lower().strip()

    if key in CACHE:
        answer = CACHE[key]
        source = "⚡ Caché"
    else:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(f"Responde con ciencia real y sarcasmo: {question}")
        answer = response.text
        CACHE[key] = answer
        save_cache()
        source = "🧠 IA"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": [{"question": question, "answer": answer, "source": source}],
        }
    )

from storage import SessionLocal, Question

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

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
