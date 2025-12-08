from app.core.fallback import fallback_answer


def test_fallback():
    text = fallback_answer("probando")
    assert "⚠" in text or "El Oráculo" in text
