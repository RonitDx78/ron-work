import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from models import CallSummary
from transcriber import transcribe_bytes
from summarizer import analyze

app = FastAPI(
    title="AI Call Summarizer",
    description="Upload a business call recording and get a transcript, summary, key points, and action items.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"}

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
def root():
    index = frontend_path / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "AI Call Summarizer API — POST /summarize with an audio file"}


@app.post("/summarize", response_model=CallSummary)
async def summarize_call(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower() if file.filename else ".wav"

    if suffix not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{suffix}'. Use one of: {', '.join(SUPPORTED_FORMATS)}",
        )

    audio_bytes = await file.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    transcript, segments, duration = transcribe_bytes(audio_bytes, suffix=suffix)

    if not transcript:
        raise HTTPException(status_code=422, detail="Could not extract speech from the audio.")

    analysis = analyze(transcript)

    return CallSummary(
        transcript=transcript,
        segments=segments,
        summary=analysis.get("summary", ""),
        key_points=analysis.get("key_points", []),
        action_items=analysis.get("action_items", []),
        sentiment=analysis.get("sentiment", "neutral"),
        duration_seconds=duration,
    )


@app.get("/health")
def health():
    return {"status": "ok"}
