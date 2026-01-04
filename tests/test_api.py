from fastapi.testclient import TestClient

from app.web.server import app

client = TestClient(app)


def test_home():
    res = client.get("/")
    assert res.status_code == 200
    assert "Backend API" in res.text


def test_api_unauthorized():
    res = client.post("/api/v1/ask", json={"question": "¿Hola?"})
    assert res.status_code == 401
