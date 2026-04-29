import json
import anthropic
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

def get_figure_locations(figure_id: int, api_key: str) -> dict:
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

    prompt = LOCATIONS_PROMPT.format(
        name=figure["name"],
        era=figure["era"],
        raw_text=figure["raw_text"]
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    import json
    result = json.loads(raw.strip())

    return {
        "figure": figure["name"],
        "era": figure["era"],
        "locations": result["locations"]
    }