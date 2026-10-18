from transformers import pipeline
from functools import lru_cache
from typing import List, Dict


class EmotionService:
    def __init__(self):
        # Load model once
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None
        )

    def analyze(self, text: str) -> List[Dict]:
        """
        Returns sorted emotion probabilities
        """
        results = self.classifier(text)[0]

        # Sort by score descending
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)

        return sorted_results

    def get_top_emotions(self, text: str, top_n: int = 2) -> List[Dict]:
        """
        Returns top N emotions
        """
        results = self.analyze(text)
        return results[:top_n]


# Singleton instance (IMPORTANT for performance)
@lru_cache()
def get_emotion_service():
    return EmotionService()