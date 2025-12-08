def fallback_answer(question: str) -> str:
    return (
        "⚠️ El Oráculo está meditando.\n"
        "Intenta de nuevo en unos segundos o pídele algo menos absurdo:\n"
        f"→ '{question}' requiere un sacrificio computacional considerable."
    )
