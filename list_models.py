import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=".env")
genai.configure(api_key=os.getenv("ANTIGRAVITY_API_KEY"))

print("Modelos disponibles:")
for m in genai.list_models():
    print("-", m.name)
