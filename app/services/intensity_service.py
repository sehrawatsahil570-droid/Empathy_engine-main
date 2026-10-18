import re


class IntensityService:

    def calculate_intensity(self, text: str, confidence: float) -> float:
        """
        Combines model confidence with textual signals
        """
        bonus = 0.0

        # 🔥 Exclamation boost
        exclamations = text.count("!")
        bonus += min(0.15, exclamations * 0.05)

        # 🔥 ALL CAPS boost
        if text.isupper():
            bonus += 0.2

        # 🔥 Repeated characters (e.g., sooo, veryyyy)
        if re.search(r"(.)\1{2,}", text):
            bonus += 0.1

        # 🔥 Strong words boost
        strong_words = ["very", "extremely", "really", "so", "too"]
        if any(word in text.lower() for word in strong_words):
            bonus += 0.1

        # Final intensity (clamped)
        intensity = min(1.0, confidence + bonus)

        return round(intensity, 3)