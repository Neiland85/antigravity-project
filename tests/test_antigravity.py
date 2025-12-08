from fastapi.testclient import TestClient
from app.web.server import app
from app.core.settings import settings

client = TestClient(app)

def test_antigravity_unauthorized():
    res = client.post("/api/v1/antigravity", json={"question": "Hola?"})
    assert res.status_code == 401

def test_antigravity_missing_question():
    res = client.post(
        "/api/v1/antigravity",
        headers={"Authorization": f"Bearer {settings.GOOGLE_API_KEY}"},
        json={}
    )
    assert res.status_code == 400
