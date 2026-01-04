from fastapi import Request
from fastapi.responses import JSONResponse
from time import time

# 5 peticiones por 10 segundos
MAX_REQ = 50
WINDOW = 10
requests_per_user = {}

async def rate_limit(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time()

    if client_ip not in requests_per_user:
        requests_per_user[client_ip] = []

    # limpiar la ventana
    requests_per_user[client_ip] = [t for t in requests_per_user[client_ip] if now - t < WINDOW]

    if len(requests_per_user[client_ip]) >= MAX_REQ:
        return JSONResponse(status_code=429, content={"detail": "Demasiada curiosidad cósmica"})

    requests_per_user[client_ip].append(now)
    return await call_next(request)
