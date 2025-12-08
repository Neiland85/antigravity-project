from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

from app.api.v1.routes import router as api_router

app = FastAPI(title="Oráculo Antigravitacional")

# Detect testing mode (GitHub Actions)
TESTING = os.getenv("TESTING", "false").lower() == "true"
IN_DOCKER = os.getenv("IN_DOCKER", "false").lower() == "true"

if IN_DOCKER:
    STATIC_DIR = "/app/web/static"
    TEMPLATE_DIR = "/app/web/templates"
elif TESTING:
    STATIC_DIR = "web/static"
    TEMPLATE_DIR = "web/templates"
else:
    STATIC_DIR = "web/static"
    TEMPLATE_DIR = "web/templates"

# Only mount if paths exist
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

app.include_router(api_router, prefix="/api/v1", tags=["antigravity"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
