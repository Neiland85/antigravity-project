
import logging
import random
import hashlib

logger = logging.getLogger(__name__)
_model_cache = {}

def get_local_model():
    if 'generator' not in _model_cache:
        logger.info('Loading local reasoning model...')
        try:
            from transformers import pipeline
            import torch
            _model_cache['generator'] = pipeline(
                'text-generation',
                model='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7,
            )
            logger.info('Model loaded successfully')
        except Exception as e:
            logger.error(f'Failed to load local model: {e}')
            _model_cache['generator'] = None
    return _model_cache.get('generator')

def reason_locally(question, context=''):
    generator = get_local_model()
    if generator is None:
        return generate_dynamic_fallback(question)
    
    prompt = f'Responde en espanol con sarcasmo cientifico: {question}'
    result = generator(prompt)
    return result[0]['generated_text'].replace(prompt, '').strip()

def generate_dynamic_fallback(question):
    seed = int(hashlib.md5(question.encode()).hexdigest(), 16)
    random.seed(seed)
    
    templates = [
        'Segun el teorema de {concept}, tu pregunta sobre "{topic}" implica que {conclusion}.',
        'Interesante. Si aplicamos {concept} a "{topic}", obtenemos que {conclusion}.',
        'La {concept} sugiere que "{topic}" es {conclusion}.',
        'Analizando "{topic}" con {concept}: {conclusion}.',
    ]
    
    concepts = ['incompletitud de Godel', 'entropia termodinamica', 'recursividad de Turing',
                'paradoja de Russell', 'principio de incertidumbre', 'teoria de categorias']
    
    conclusions = [
        'la consistencia es indecidible', 'el sistema no puede autoverificarse',
        'la respuesta existe pero es incognoscible', 'necesitamos un metasistema',
        'la complejidad crece exponencialmente', 'hay una paradoja oculta'
    ]
    
    topic = question[:50] if len(question) > 50 else question
    template = random.choice(templates)
    
    return template.format(
        concept=random.choice(concepts),
        topic=topic,
        conclusion=random.choice(conclusions)
    ) + f' (Hash: {seed % 10000})'
