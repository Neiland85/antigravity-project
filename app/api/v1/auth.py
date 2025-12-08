from fastapi import Header, HTTPException

VALID_TOKENS = {"neiland": "ArchitectSupreme"}

def require_token(authorization: str = Header(None)):
    if authorization not in VALID_TOKENS.values():
        raise HTTPException(status_code=401, detail="Acceso denegado al Oráculo")
    return True
