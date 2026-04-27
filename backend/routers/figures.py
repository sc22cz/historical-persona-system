import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection
from services.extractor import extract_profile

router = APIRouter(prefix="/figures", tags=["figures"])

class FigureCreate(BaseModel):
    name: str
    era: int
    period: str
    source: str
    raw_text: str
    api_key: str

@router.post("/")
def create_figure(data: FigureCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO figures (name, era, period, source, raw_text)
        VALUES (?, ?, ?, ?, ?)
    """, (data.name, data.era, data.period, data.source, data.raw_text))
    
    figure_id = cursor.lastrowid

    profile = extract_profile(data.name, data.raw_text, data.api_key)

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

    return {"id": figure_id, "name": data.name, "profile": profile}

@router.get("/")
def list_figures():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, era, period FROM figures")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]