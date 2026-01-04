import google.generativeai as genai
import logging

class IntuitionEngine:
    def __init__(self, model_name="models/gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
    
    def generate_with_reasoning(self, prompt: str) -> str:
        """
        Generates a response that includes an internal monologue (Chain of Thought).
        It forces the model to 'think' inside <thought> tags before answering.
        """
        augmented_prompt = (
            f"{prompt}\n\n"
            "INSTRUCCIÓN DE RAZONAMIENTO PROFUNDO:\n"
            "Antes de dar tu respuesta final, debes generar un proceso de 'pensamiento interno' para validar tu intuición.\n"
            "1. Analiza la intención oculta del usuario.\n"
            "2. Critica tu primera impresión (¿estoy asumiendo algo incorrecto?).\n"
            "3. Refina tu enfoque.\n\n"
            "Formato de salida requerido:\n"
            "<thought>\n"
            "[Aquí escribe tu razonamiento interno, tus dudas y tu análisis lógico]\n"
            "</thought>\n\n"
            "[Aquí tu respuesta final al usuario, pulida y directa]"
        )
        
        try:
            response = self.model.generate_content(augmented_prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error in IntuitionEngine: {e}")
            raise e
