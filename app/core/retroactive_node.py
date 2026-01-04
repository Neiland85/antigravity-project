
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

class RetroactiveIntuition:
    _instance = None
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_initial_intuition()

    def _train_initial_intuition(self):
        # Synthetic data: [Text, Intuition Category]
        # 0: Low complexity, 1: Logical Paradox, 2: Scientific Sarcasm
        data = [
            ('La entropia del sistema aumenta', 2),
            ('2+2 es 4 en base 10', 0),
            ('Esta frase es falsa', 1),
            ('Godel demostro que no podemos saberlo todo', 1),
            ('Hola, como estas?', 0),
            ('La singularidad esta cerca pero no llegas al final', 2),
            ('Un conjunto que contiene a todos los conjuntos', 1),
            ('Tu ignorancia es proporcional a tu masa', 2)
        ]
        df = pd.DataFrame(data, columns=['text', 'label'])
        X = self.vectorizer.fit_transform(df['text'])
        self.model.fit(X, df['label'])
        logger.info('Retroactive Random Forest node initialized.')

    def analyze(self, text):
        try:
            X = self.vectorizer.transform([text])
            prediction = self.model.predict(X)[0]
            probs = self.model.predict_proba(X)[0]
            confidence = np.max(probs)
            
            categories = {0: 'Simplista', 1: 'Paradoja Logica', 2: 'Intuicion Cientifica'}
            return {
                'category': categories.get(prediction, 'Desconocido'),
                'confidence': round(float(confidence), 2)
            }
        except Exception as e:
            logger.error(f'Error in Retroactive analysis: {e}')
            return {'category': 'Analisis Fallido', 'confidence': 0.0}

intuition_node = RetroactiveIntuition()
