from fastapi import Request, HTTPException
from time import time

# 5 peticiones por 10 segundos
MAX_REQ = 5
WINDOW = 10
requests_per_user = {}

async def rate_limit(request: Request, call_next):
    token = request.headers.get("Authorization", "")
    now = time()

    if token not in requests_per_user:
        requests_per_user[token] = []

    # limpiar la ventana
    requests_per_user[token] = [t for t in requests_per_user[token] if now - t < WINDOW]

    if len(requests_per_user[token]) >= MAX_REQ:
        raise HTTPException(status_code=429, detail="Demasiada curiosidad cósmica")

    requests_per_user[token].append(now)
    return await call_next(request)
