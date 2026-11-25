import os
import json
import anthropic

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


SYSTEM_PROMPT = """You are a business call analysis assistant. Given a call transcript, return a JSON object with:
- summary: 2-3 sentence overview of the call
- key_points: list of 3-6 important points discussed
- action_items: list of concrete next steps or commitments made (empty list if none)
- sentiment: one of "positive", "neutral", "negative", or "mixed"

Respond ONLY with valid JSON, no extra text."""


def analyze(transcript: str) -> dict:
    client = _get_client()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Transcript:\n\n{transcript}",
            }
        ],
    )

    raw = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)
