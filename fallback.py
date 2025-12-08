import random

SARCASTIC_FALLBACKS = [
    "La cuota se ha ido de vacaciones. DevOps llora. Entropía aumenta.",
    "Si no hay IA, solo queda el caos… y StackOverflow.",
    "La API dice que tus preguntas son demasiado profundas para el plan gratuito.",
    "Error 429: Inteligencia artificial tomándose un café.",
    "Vuelve mañana. La verdad absoluta también necesita descanso."
]

def fallback_answer():
    return random.choice(SARCASTIC_FALLBACKS)
