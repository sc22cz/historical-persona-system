import os
import anthropic

PREDICT_PROMPT = """You are channeling the lived wisdom of historical figures — not as an analyst, but as their voice.

A person has described themselves:
{description}

They share deep behavioural patterns with these historical figures:
{matches_detail}

Their behavioural profile:
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

Now respond as if these historical figures are speaking directly to this person. Do NOT give abstract analysis. Do NOT give therapist-style advice. Do NOT be rational or balanced.

Instead:
- Speak in the raw, direct voice of someone who has lived through real consequences
- Reference how these specific figures actually handled adversity — their real decisions, their real failures, their real instincts
- Be honest about the dangers of this person's nature, based on how similar figures were destroyed or succeeded
- Ground every word in character and lived experience, not theory

Tell this person what they need to hear — not what they want to hear.
What would {match_names} say to someone exactly like them?
"""

def predict_future(description: str, vector: list, matches: list) -> dict:
    matches_detail = "\n".join([
        f"- {m['name']} ({abs(m['era'])} {'BC' if m['era'] < 0 else 'AD'}): {round(m['score']*100,1)}% behavioural similarity"
        for m in matches
    ])
    match_names = ", ".join([m["name"] for m in matches])

    prompt = PREDICT_PROMPT.format(
        description=description,
        matches_detail=matches_detail,
        match_names=match_names,
        d0=vector[0], d1=vector[1], d2=vector[2],
        d3=vector[3], d4=vector[4], d5=vector[5],
        d6=vector[6], d7=vector[7], d8=vector[8], d9=vector[9]
    )

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "vector": vector,
        "matches": matches,
        "prediction": response.content[0].text
    }
