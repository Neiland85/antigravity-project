from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.api.v1.antigravity import router as antigravity_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
app.include_router(antigravity_router, prefix="/api/v1")

# Mount static only if exists
import os
static_path = os.path.join(os.getcwd(), "app/web/static")
if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend API is running", "docs": "/docs"}
