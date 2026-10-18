# Empathy Engine

Empathy Engine is a small web application that analyzes the emotion expressed in a piece of text and uses the result to guide text-to-speech generation. The goal is to make generated speech sound more expressive by adjusting voice settings based on the text's detected emotion and estimated intensity.

## How it works

1. A user enters text in the web interface and clicks **Generate Voice**.
2. The frontend sends the text to the FastAPI backend at `POST /generate-audio`.
3. A Hugging Face Transformers model (`j-hartmann/emotion-english-distilroberta-base`) scores the emotions in the text. The service selects the two highest-scoring labels.
4. The intensity service adjusts the scores using simple text cues such as exclamation marks, all-uppercase text, repeated characters, and intensity words.
5. The mapping service combines supported emotion profiles into voice parameters.
6. The ElevenLabs API generates speech. The backend saves the MP3 under `static/audio/output.mp3` and returns the emotion analysis, voice parameters, and audio path.
7. The frontend displays the emotion scores and loads the generated audio into its audio player.

> **Note:** This is a prototype. Emotion detection is a model prediction, not a definitive reading of someone's feelings. The current implementation uses a fixed ElevenLabs voice and output filename, so each new generation overwrites the previous audio file.

## Features

- Text-based emotion classification
- Selection of the top two detected emotions
- Rule-based intensity adjustment using textual signals
- Mapping from supported emotions to speech-style parameters
- Speech generation through ElevenLabs
- Browser UI with a loading indicator, emotion results, and an audio player
- FastAPI backend with interactive API documentation

## Technology stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI, Uvicorn
- **Emotion model:** Hugging Face Transformers and `j-hartmann/emotion-english-distilroberta-base`
- **Text-to-speech:** ElevenLabs API (`eleven_multilingual_v2`)
- **Configuration:** environment variables loaded with `python-dotenv`

## Project structure

```text
Empathy_engine-main/
├── app/
│   ├── main.py                 # FastAPI application and static-file mounting
│   ├── models/
│   │   └── schemas.py          # Request schema
│   ├── routes/
│   │   └── tts_routes.py       # POST /generate-audio endpoint
│   ├── services/
│   │   ├── emotion_service.py  # Emotion classification
│   │   ├── intensity_service.py# Text-based intensity adjustment
│   │   ├── mapping_service.py  # Emotion-to-voice mapping
│   │   ├── stt_service.py      # Placeholder for speech-to-text functionality
│   │   └── tts_service.py      # ElevenLabs speech generation
│   └── utils/
│       ├── audio_utils.py      # Placeholder utility module
│       └── ssml_builder.py     # Placeholder utility module
├── frontend/
│   ├── index.html              # User interface
│   ├── script.js               # API calls and audio playback
│   └── style.css               # Page styling
├── hf_login.py                 # Optional Hugging Face CLI-style login helper
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10 or newer is recommended.
- An internet connection for downloading the emotion model and calling ElevenLabs.
- An ElevenLabs API key. Create/manage one in your [ElevenLabs account](https://elevenlabs.io/).
- Git is optional and only needed if you want to clone or contribute to the repository.

## Setup and run

The commands below are for macOS/Linux and should be run from the project root (`Empathy_engine-main/`). On Windows, activate the virtual environment with `.venv\Scripts\activate` instead of the `source` command.

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the ElevenLabs API key

Create a file named `.env` in the project root and add your key:

```dotenv
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

Do not commit `.env` or share your API key. The included `.gitignore` already excludes `.env`.

### 4. Create the audio output directory

The current code expects the `static` directory to exist when the backend starts and writes generated audio to `static/audio/output.mp3`. Create it before launching the server:

```bash
mkdir -p static/audio
```

### 5. Start the backend

From the project root, with the virtual environment active, run:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

- Application health check: <http://127.0.0.1:8000/>
- Interactive API docs: <http://127.0.0.1:8000/docs>

The first request may take longer while Transformers downloads and loads the emotion model.

### 6. Start the frontend

Open a **second terminal** in the project root, activate the same virtual environment if needed, and run:

```bash
python -m http.server 5500 --directory frontend
```

Then open <http://127.0.0.1:5500> in your browser. Enter a sentence and click **Generate Voice**. The browser sends requests to the backend at `http://127.0.0.1:8000`.

Keep both terminal processes running while using the application. Stop a server with `Ctrl+C`.

## API usage

### `GET /`

Returns a basic health message:

```json
{"message":"Empathy Engine is running 🚀"}
```

### `POST /generate-audio`

Request body:

```json
{
  "text": "I am so excited about this opportunity!"
}
```

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/generate-audio \
  -H 'Content-Type: application/json' \
  -d '{"text":"I am so excited about this opportunity!"}'
```

The response includes the original text, emotion labels and confidence scores, calculated intensity values, the mapped voice parameters, and the relative path of the generated audio file. You can also try the endpoint interactively at <http://127.0.0.1:8000/docs>.

## Troubleshooting

- **`ELEVENLABS_API_KEY` is missing or authentication fails:** Confirm that `.env` is in the project root, the variable name is exactly `ELEVENLABS_API_KEY`, and the key is valid. Restart the backend after changing `.env`.
- **Error that the `static` directory does not exist:** Run `mkdir -p static/audio` from the project root, then restart Uvicorn.
- **The page opens but generation fails:** Check that the backend is running on port `8000`; inspect the backend terminal for the error and the browser developer console for frontend errors.
- **Model download is slow or fails:** Check your internet connection and ensure the environment has enough disk space and memory. The model is loaded when the service is first initialized.
- **The audio player cannot load the result:** Confirm that `static/audio/output.mp3` was created and that the backend is serving the `/static` path.
- **Port already in use:** Start Uvicorn on another port, but update `frontend/script.js` to use that same backend port because the current URL is hard-coded to `http://127.0.0.1:8000`.

## Current limitations

- The frontend currently targets a local backend URL (`127.0.0.1:8000`); it is not configured for deployment.
- Generated audio uses a single fixed filename, so concurrent requests can overwrite each other's output.
- The mapping service only has explicit profiles for a subset of possible emotion labels; labels without a matching profile do not contribute to the mapped voice parameters.
- `stt_service.py`, `audio_utils.py`, and `ssml_builder.py` are currently empty placeholders; speech-to-text is not implemented in this version.
- CORS is configured to allow all origins. Review this before deploying the project publicly.

## Security

Never commit API keys, access tokens, or personal secrets. Use environment variables for credentials and restrict CORS and network access before any production deployment.
