# AI Call Summarizer

Upload a business call recording and instantly get a transcript, summary, key points, action items, and sentiment — powered by OpenAI Whisper and Claude.

Built as a portfolio project targeting [HaorGrix](https://haorgrix.com), specifically as an extension to their **Reiva** AI receptionist product.

## Features

- Audio transcription via **OpenAI Whisper** (runs locally, no API cost)
- Intelligent summarization via **Claude** (Haiku — fast + cheap)
- Extracts key points, action items, and sentiment
- Drag-and-drop web UI
- REST API for easy CRM integration
- Docker-ready for deployment

## Supported Formats

MP3, WAV, M4A, OGG, FLAC, WEBM

## Quick Start

**1. Clone & install**
```bash
git clone https://github.com/RonitDx78/ron-work.git
cd ron-work
pip install -r requirements.txt
```

**2. Set your API key**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

**3. Run**
```bash
cd backend
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## API

```
POST /summarize
Content-Type: multipart/form-data
Body: file=<audio file>
```

**Response:**
```json
{
  "transcript": "...",
  "segments": [{"start": 0.0, "end": 2.4, "text": "..."}],
  "summary": "...",
  "key_points": ["...", "..."],
  "action_items": ["...", "..."],
  "sentiment": "positive",
  "duration_seconds": 142.5
}
```

## Docker

```bash
docker build -t call-summarizer .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_key call-summarizer
```

## Stack

| Layer | Technology |
|---|---|
| Transcription | OpenAI Whisper (base model) |
| Summarization | Anthropic Claude Haiku |
| Backend | FastAPI + Python |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Docker |
