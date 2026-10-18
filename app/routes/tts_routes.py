from fastapi import APIRouter
from app.services.emotion_service import get_emotion_service
from app.services.intensity_service import IntensityService
from app.services.mapping_service import MappingService
from app.services.tts_service import TTSService
from app.models.schemas import TextRequest

# 🔥 REQUIRED: define router
router = APIRouter()

# Initialize services
intensity_service = IntensityService()
mapping_service = MappingService()
tts_service = TTSService()


@router.post("/generate-audio")
def generate_audio(request: TextRequest):
    text = request.text

    emotion_service = get_emotion_service()
    top_emotions = emotion_service.get_top_emotions(text)

    enriched = []
    for emo in top_emotions:
        intensity = intensity_service.calculate_intensity(text, emo["score"])

        enriched.append({
            "emotion": emo["label"],
            "confidence": round(emo["score"], 3),
            "intensity": intensity
        })

    voice_params = mapping_service.map_emotions(enriched)

    # 🔥 Generate audio
    audio_path = tts_service.generate_audio(text, voice_params)

    return {
        "text": text,
        "analysis": enriched,
        "voice_parameters": voice_params,
        "audio_file": audio_path
    }