import os

# Si estamos en CI/testing, no queremos usar disco
TESTING = os.getenv("TESTING") == "true"

DB_URL = (
    "sqlite:///:memory:"
    if TESTING
    else "sqlite:///data/antigravity.db"
)
