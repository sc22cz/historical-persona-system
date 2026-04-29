import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_connection
from services.extractor import extract_profile
from services.wiki_fetcher import fetch_wikipedia_text

def resolve_figure(name: str, api_key: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.id, f.name, f.era, f.raw_text, p.vector, p.confidence
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
        WHERE LOWER(f.name) = LOWER(?)
    """, (name,))

    figure = cursor.fetchone()

    if figure:
        conn.close()
        return dict(figure)

    text = fetch_wikipedia_text(name)
    if not text:
        conn.close()
        return None

    profile = extract_profile(name, text, api_key)

    cursor.execute("""
        INSERT INTO figures (name, era, period, source, raw_text)
        VALUES (?, ?, ?, ?, ?)
    """, (name, 0, "analyzed", "Wikipedia", text))

    figure_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO profiles (figure_id, vector, confidence, evidence)
        VALUES (?, ?, ?, ?)
    """, (
        figure_id,
        json.dumps(profile["vector"]),
        json.dumps(profile["confidence"]),
        json.dumps(profile["evidence"])
    ))

    conn.commit()

    cursor.execute("""
        SELECT f.id, f.name, f.era, f.raw_text, p.vector, p.confidence
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
        WHERE f.id = ?
    """, (figure_id,))

    new_figure = cursor.fetchone()
    conn.close()

    return dict(new_figure)