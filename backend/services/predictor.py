import json
import anthropic
from database import get_connection

PREDICT_PROMPT = """You are a behavioural analyst who uses historical patterns to provide life guidance.

A user has described themselves and been matched to historical figures. Based on their behavioural profile and their closest historical matches, provide life guidance.

User's behavioural profile:
- Reaction to oppression: {d0} (0=endures silently, 1=actively resists)
- Group dependency: {d1} (0=lone wolf, 1=relies on collective)
- Principle vs interest: {d2} (0=principle above all, 1=interest above all)
- Interpersonal trust: {d3} (0=highly open, 1=deeply suspicious)
- Change orientation: {d4} (0=preserve status quo, 1=radical change)
- Emotional stability: {d5} (0=calm and controlled, 1=emotional and impulsive)
- Core motivation: {d6} (0=idealism, 1=survival/power)
- Historical mission: {d7} (0=lives in present, 1=mission-driven)
- Response to injustice: {d8} (0=accepts and adapts, 1=anger and resistance)
- Expression style: {d9} (0=silent and reserved, 1=vocal and assertive)

Closest historical matches:
{matches}

User's self description:
{description}

Based on this profile and historical parallels, provide:
1. Their likely life trajectory and peak period
2. Their greatest strength and their blind spot
3. The type of crisis they are most likely to face
4. One concrete piece of advice drawn from how their historical matches navigated similar challenges

Be specific, honest, and grounded in the behavioural data. Avoid generic life advice.
"""

def predict_future(description: str, vector: list, matches: list, api_key: str) -> dict:
    matches_text = "\n".join([
        f"- {m['name']} ({m['era']} {'BC' if m['era'] < 0 else 'AD'}): similarity {m['score']}"
        for m in matches
    ])

    prompt = PREDICT_PROMPT.format(
        d0=vector[0], d1=vector[1], d2=vector[2],
        d3=vector[3], d4=vector[4], d5=vector[5],
        d6=vector[6], d7=vector[7], d8=vector[8], d9=vector[9],
        matches=matches_text,
        description=description
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "vector": vector,
        "matches": matches,
        "prediction": response.content[0].text
    }