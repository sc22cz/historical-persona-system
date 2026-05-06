import os
import re
import json
import anthropic
from fastapi import HTTPException
from database import get_connection

LOCATIONS_PROMPT = """You are a historical geographer. Based on the following information about {name} (era: {era}), list the key locations associated with their life.

Known facts:
{raw_text}

Return ONLY valid JSON, no other text:
{{
  "locations": [
    {{
      "name": "location name",
      "lat": latitude as float,
      "lng": longitude as float,
      "description": "why this place matters to {name}",
      "type": "birthplace/battlefield/capital/exile/death"
    }}
  ]
}}

Include 3-6 locations maximum. Only include locations with high historical confidence.
"""

def get_figure_locations(figure_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.name, f.era, f.raw_text
        FROM figures f
        WHERE f.id = ?
    """, (figure_id,))

    figure = cursor.fetchone()
    conn.close()

    if not figure:
        return {"error": "Figure not found"}

    safe_raw_text = (figure["raw_text"] or "").replace("{", "{{").replace("}", "}}")
    prompt = LOCATIONS_PROMPT.format(
        name=figure["name"],
        era=figure["era"],
        raw_text=safe_raw_text
    )

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r'^```json?\n?', '', raw)
    raw = re.sub(r'\n?```$', '', raw)

    try:
        result = json.loads(raw.strip())
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse locations from Claude: {e}")

    return {
        "figure": figure["name"],
        "era": figure["era"],
        "locations": result["locations"]
    }
