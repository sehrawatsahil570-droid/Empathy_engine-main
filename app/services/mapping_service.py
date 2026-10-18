from typing import List, Dict


class MappingService:
    """
    Maps emotions + intensity → voice parameters
    """

    def __init__(self):
        # Base emotion profiles
        self.emotion_profiles = {
            "joy": {"pitch": 15, "rate": 18, "volume": 0.8, "style": 0.8},
            "excited": {"pitch": 20, "rate": 25, "volume": 0.9, "style": 1.0},
            "sadness": {"pitch": -15, "rate": -20, "volume": 0.5, "style": 0.4},
            "anger": {"pitch": 5, "rate": 20, "volume": 0.85, "style": 0.9},
            "fear": {"pitch": 8, "rate": 15, "volume": 0.6, "style": 0.7},
            "surprise": {"pitch": 12, "rate": 22, "volume": 0.75, "style": 0.85},
            "neutral": {"pitch": 0, "rate": 0, "volume": 0.7, "style": 0.5}
        }

    def map_emotions(self, analysis: List[Dict]) -> Dict:
        """
        Takes top emotions and returns blended voice parameters
        """

        final = {
            "pitch": 0,
            "rate": 0,
            "volume": 0,
            "style": 0
        }

        total_weight = 0

        for emo in analysis:
            label = emo["emotion"]
            intensity = emo["intensity"]

            if label not in self.emotion_profiles:
                continue

            profile = self.emotion_profiles[label]

            weight = intensity
            total_weight += weight

            final["pitch"] += profile["pitch"] * weight
            final["rate"] += profile["rate"] * weight
            final["volume"] += profile["volume"] * weight
            final["style"] += profile["style"] * weight

        # Normalize (avoid overflow)
        if total_weight > 0:
            for key in final:
                final[key] = round(final[key] / total_weight, 3)

        return final