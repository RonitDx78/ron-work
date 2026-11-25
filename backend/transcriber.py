import whisper
import tempfile
import os
from pathlib import Path
from models import TranscriptSegment


_model = None


def _load_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def transcribe(audio_path: str) -> tuple[str, list[TranscriptSegment], float]:
    model = _load_model()
    result = model.transcribe(audio_path, verbose=False)

    full_text = result["text"].strip()
    duration = result.get("duration", 0.0)

    segments = [
        TranscriptSegment(
            start=seg["start"],
            end=seg["end"],
            text=seg["text"].strip(),
        )
        for seg in result.get("segments", [])
    ]

    return full_text, segments, duration


def transcribe_bytes(audio_bytes: bytes, suffix: str = ".wav") -> tuple[str, list[TranscriptSegment], float]:
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        return transcribe(tmp_path)
    finally:
        os.unlink(tmp_path)
