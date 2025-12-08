import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=".env")
genai.configure(api_key=os.getenv("ANTIGRAVITY_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-lite-latest")
response = model.generate_content("¿Cuál es la gravedad en la Luna?")
print("Respuesta:", response.text)
