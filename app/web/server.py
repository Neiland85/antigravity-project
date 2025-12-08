from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.api.v1.antigravity import router as antigravity_router
import os

app = FastAPI(title="Antigravity API")

STATIC_DIR = "app/web/static"
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory="app/web/templates")

app.include_router(antigravity_router, prefix="/api/v1/antigravity")
