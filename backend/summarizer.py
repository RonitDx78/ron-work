import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = """You are a business call analysis assistant. Given a call transcript, return a JSON object with:
- summary: 2-3 sentence overview of the call
- key_points: list of 3-6 important points discussed
- action_items: list of concrete next steps or commitments made (empty list if none)
- sentiment: one of "positive", "neutral", "negative", or "mixed"

Respond ONLY with valid JSON, no extra text."""


def analyze(transcript: str) -> dict:
    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Transcript:\n\n{transcript}"},
        ],
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    raw = response.json()["message"]["content"].strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)
