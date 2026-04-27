import json
import anthropic

DIMENSIONS = [
    "reaction_to_oppression",
    "group_dependency", 
    "principle_vs_interest",
    "interpersonal_trust",
    "change_orientation",
    "emotional_stability",
    "core_motivation",
    "historical_mission",
    "response_to_injustice",
    "expression_style"
]

PROMPT_TEMPLATE = """You are a behavioural analyst specialising in historical figures.
Analyse the following text and score the person on 10 behavioural dimensions.

Rules:
- Score based ONLY on observable behaviours described in the text
- Ignore personality descriptions and third-party character judgements
- Each score is 0.0 to 1.0
- If evidence is insufficient, set confidence to 0.0

Dimensions:
1. reaction_to_oppression: 0.0 = endures silently, 1.0 = actively resists
2. group_dependency: 0.0 = lone wolf, 1.0 = relies on collective
3. principle_vs_interest: 0.0 = principle above all, 1.0 = interest above all
4. interpersonal_trust: 0.0 = highly open, 1.0 = deeply suspicious
5. change_orientation: 0.0 = preserve status quo, 1.0 = radical change
6. emotional_stability: 0.0 = calm and controlled, 1.0 = emotional and impulsive
7. core_motivation: 0.0 = idealism, 1.0 = survival/power
8. historical_mission: 0.0 = lives in present, 1.0 = mission-driven
9. response_to_injustice: 0.0 = accepts and adapts, 1.0 = anger and resistance
10. expression_style: 0.0 = silent and reserved, 1.0 = vocal and assertive

Output ONLY valid JSON, no other text:
{
  "name": "figure name",
  "vector": [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10],
  "confidence": [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10],
  "evidence": ["reason for d1", ..., "reason for d10"]
}

Text to analyse:
{text}
"""

def extract_profile(name: str, text: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = PROMPT_TEMPLATE.replace("{text}", text)
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    result = json.loads(raw.strip())



    result["name"] = name
    return result