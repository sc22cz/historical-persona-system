import os
import re
import json
import anthropic
from fastapi import HTTPException
from database import get_connection
from services.matcher import cosine_similarity

RELICS_PROMPT = """You are a museum curator and behavioural analyst.

A relic has been found with the following description:
Material: {material}
Description: {description}

Based on this relic, extract behavioural signals about its likely owner or creator:
- Would they be a lone wolf or group-oriented?
- Would they be change-oriented or tradition-preserving?
- Would they be mission-driven or present-focused?
- Would they be assertive or reserved in expression?

Return ONLY valid JSON:
{{
  "inferred_vector": [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9],
  "confidence": [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9],
  "reasoning": "brief explanation"
}}

Scores are 0.0 to 1.0. Set confidence to 0 if no evidence.
"""

def match_relic(description: str, material: str) -> dict:
    prompt = RELICS_PROMPT.format(description=description, material=material)

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r'^```json?\n?', '', raw)
    raw = re.sub(r'\n?```$', '', raw)

    try:
        relic_profile = json.loads(raw.strip())
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse relic profile from Claude: {e}")

    relic_vector = relic_profile["inferred_vector"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, f.name, f.era, f.period, p.vector
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
    """)
    figures = cursor.fetchall()
    conn.close()

    results = []
    for fig in figures:
        vector = json.loads(fig["vector"])
        score = cosine_similarity(relic_vector, vector)
        results.append({
            "id": fig["id"],
            "name": fig["name"],
            "era": fig["era"],
            "score": round(score, 4)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "relic_profile": relic_profile,
        "matches": results[:5]
    }
