import os
import json
import anthropic
from database import get_connection
from imputer import impute_profile

RECONSTRUCT_PROMPT = """You are a historian and behavioural analyst.

You have been given:
1. Known historical facts about {name} (era: {era})
2. Their behavioural profile (10 dimensions, 0.0-1.0)
3. The most similar reference figure: {similar_figure}

Known facts:
{raw_text}

Historical context:
This person lived in {era_context}. Consider the specific social structures, power dynamics, religious beliefs, and daily life constraints of that civilisation when making inferences. Do not apply modern psychological frameworks anachronistically.

Behavioural profile (some dimensions were imputed from {similar_figure}):
- Reaction to oppression: {d0}
- Group dependency: {d1}
- Principle vs interest: {d2}
- Interpersonal trust: {d3}
- Change orientation: {d4}
- Emotional stability: {d5}
- Core motivation: {d6}
- Historical mission: {d7}
- Response to injustice: {d8}
- Expression style: {d9}

Based on this profile and the known facts, reconstruct the following missing aspects of {name}'s life:
1. How did they likely behave in private relationships?
2. How did they likely respond to personal failure or setbacks?
3. What were their likely personal fears and motivations beyond public record?
4. What decisions might they have made that were never recorded?

Write 4 short paragraphs, one for each question. Be specific and grounded in the behavioural profile. Label each paragraph clearly. Do not fabricate specific events - only infer patterns of behaviour.
"""

def reconstruct_history(figure_id: int, user_vector: list = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.name, f.era, f.raw_text, p.vector, p.confidence
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
        WHERE f.id = ?
    """, (figure_id,))

    figure = cursor.fetchone()
    conn.close()

    if not figure:
        return {"error": "Figure not found"}

    imputed = impute_profile(figure_id, user_vector=user_vector)
    vector = imputed["imputed_vector"]
    imputed_from = imputed.get("imputed_from", {})

    similar_figure = "unknown"
    if imputed_from:
        first_key = list(imputed_from.keys())[0]
        donor = imputed_from[first_key]["borrowed_from"]
        similar_figure = "you (the user)" if donor == "user" else donor

    if figure["era"] < -500:
        era_context = f"ancient {abs(figure['era'])} BC, in a world of city-states, oral tradition, and divine kingship"
    elif figure["era"] < 500:
        era_context = f"the classical period around {abs(figure['era'])} BC/AD, with emerging empires and philosophical traditions"
    elif figure["era"] < 1500:
        era_context = f"the medieval period around {figure['era']} AD, shaped by religious authority and feudal structures"
    else:
        era_context = f"the modern period around {figure['era']}, with print culture, nation-states, and industrial change"

    safe_raw_text = figure["raw_text"].replace("{", "{{").replace("}", "}}")
    prompt = RECONSTRUCT_PROMPT.format(
        name=figure["name"],
        era=figure["era"],
        raw_text=safe_raw_text,
        era_context=era_context,
        similar_figure=similar_figure,
        d0=vector[0], d1=vector[1], d2=vector[2],
        d3=vector[3], d4=vector[4], d5=vector[5],
        d6=vector[6], d7=vector[7], d8=vector[8], d9=vector[9]
    )

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "figure_id": figure_id,
        "name": figure["name"],
        "era": figure["era"],
        "imputed_vector": vector,
        "similar_figure": similar_figure,
        "user_vector_used": user_vector is not None,
        "reconstruction": response.content[0].text
    }
