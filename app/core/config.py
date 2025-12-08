import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("ANTIGRAVITY_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ Falta ANTIGRAVITY_API_KEY en .env")

genai.configure(api_key=API_KEY)
