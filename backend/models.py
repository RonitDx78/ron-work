from pydantic import BaseModel
from typing import List


class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str


class CallSummary(BaseModel):
    transcript: str
    segments: List[TranscriptSegment]
    summary: str
    key_points: List[str]
    action_items: List[str]
    sentiment: str
    duration_seconds: float
