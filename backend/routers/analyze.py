import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.wiki_fetcher import fetch_wikipedia_text
from services.extractor import extract_profile
from services.matcher import find_matches
from database import get_connection
import json

router = APIRouter(prefix="/analyze", tags=["analyze"])

class AnalyzeRequest(BaseModel):
    name: str
    api_key: str

@router.post("/")
def analyze_person(data: AnalyzeRequest):
    text = fetch_wikipedia_text(data.name)
    
    if not text:
        raise HTTPException(status_code=404, detail=f"No Wikipedia page found for '{data.name}'")
    
    profile = extract_profile(data.name, text, data.api_key)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO figures (name, era, period, source, raw_text)
        VALUES (?, ?, ?, ?, ?)
    """, (data.name, 0, "analyzed", "Wikipedia", text))
    
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
    conn.close()
    
    matches = find_matches(profile["vector"], top_k=5)
    matches = [m for m in matches if m["name"] != data.name]
    
    return {
        "name": data.name,
        "profile": profile,
        "matches": matches[:5]
    }