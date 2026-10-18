import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()


class TTSService:

    def __init__(self):
        api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=api_key)

    def generate_audio(self, text: str, voice_params: dict, output_path: str = "static/audio/output.mp3"):
        """
        Generate speech using ElevenLabs (new SDK)
        """

        # Map parameters
        style = min(1.0, voice_params["style"])
        stability = max(0.2, 1 - style)

        audio = self.client.text_to_speech.convert(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # Rachel voice
            model_id="eleven_multilingual_v2",
            text=text,
            voice_settings={
                "stability": stability,
                "similarity_boost": 0.7,
                "style": style
            }
        )

        # Save audio
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return output_path