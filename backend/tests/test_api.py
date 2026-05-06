"""
Integration-style tests using FastAPI TestClient.
All external dependencies (DB, Claude) are mocked.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

from main import app

client = TestClient(app, raise_server_exceptions=False)

SAMPLE_FIGURE = {
    "id": 1, "name": "Julius Caesar", "era": -44, "period": "Ancient",
    "vector": [0.9, 0.5, 0.8, 0.6, 0.7, 0.3, 0.8, 0.9, 0.7, 0.9],
    "confidence": [0.9] * 10,
    "evidence": [f"Evidence {i}" for i in range(10)],
}

SAMPLE_PROFILE = {
    "name": "Julius Caesar",
    "vector": SAMPLE_FIGURE["vector"],
    "confidence": SAMPLE_FIGURE["confidence"],
    "evidence": SAMPLE_FIGURE["evidence"],
}


# ── GET /figures/ ──────────────────────────────────────────────────────────────

@patch("routers.figures.get_connection")
def test_list_figures_returns_list(mock_gc):
    cursor = MagicMock()
    cursor.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_gc.return_value = conn

    r = client.get("/figures/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@patch("routers.figures.get_connection")
def test_list_figures_returns_correct_shape(mock_gc):
    row = MagicMock()
    row.__getitem__ = lambda self, k: {
        "id": 1, "name": "Caesar", "era": -44, "period": "Ancient",
        "vector": json.dumps([0.5]*10),
        "confidence": json.dumps([0.8]*10),
        "evidence": json.dumps(["e"]*10),
    }[k]
    cursor = MagicMock()
    cursor.fetchall.return_value = [row]
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_gc.return_value = conn

    r = client.get("/figures/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == "Caesar"
    assert len(data[0]["vector"]) == 10


# ── POST /match/ ───────────────────────────────────────────────────────────────

@patch("routers.match.find_matches")
@patch("routers.match.extract_profile")
def test_match_returns_results(mock_extract, mock_find):
    mock_extract.return_value = SAMPLE_PROFILE
    mock_find.return_value = [
        {"id": 1, "name": "Caesar", "era": -44, "period": "Ancient", "score": 0.95}
    ]
    payload = {"description": "I am a determined leader who takes bold action.", "top_k": 3}
    r = client.post("/match/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "matches" in data
    assert len(data["matches"]) == 1


def test_match_missing_description_fails():
    payload = {"top_k": 3}  # description is required
    r = client.post("/match/", json=payload)
    assert r.status_code == 422


# ── POST /predict/ ─────────────────────────────────────────────────────────────

@patch("routers.predict.get_historical_responses")
def test_predict_returns_figures(mock_ghr):
    mock_ghr.return_value = {
        "question": "test question",
        "figures": [
            {"name": "Caesar", "era": -44, "period": "Ancient",
             "score": 0.9, "type": "ancient", "response": "I fought."}
        ],
    }
    payload = {"question": "What to do?", "user_vector": [0.5] * 10}
    r = client.post("/predict/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "figures" in data
    assert data["figures"][0]["name"] == "Caesar"


@patch("routers.predict.get_historical_responses")
def test_predict_missing_question_fails(mock_ghr):
    payload = {"user_vector": [0.5] * 10}
    r = client.post("/predict/", json=payload)
    assert r.status_code == 422


# ── POST /reconstruct/ ────────────────────────────────────────────────────────

@patch("routers.reconstruct.reconstruct_history")
def test_reconstruct_returns_narratives(mock_rh):
    mock_rh.return_value = {
        "action": "left career",
        "figures": [
            {"name": "Caesar", "era": -44, "period": "Ancient",
             "score": 0.88, "narrative": "He crossed the Rubicon..."}
        ],
    }
    payload = {"action": "I left my job", "source_vector": [0.5] * 10}
    r = client.post("/reconstruct/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "figures" in data
    assert "narrative" in data["figures"][0]


# ── GET / (health check) ───────────────────────────────────────────────────────

def test_root_returns_200():
    r = client.get("/")
    assert r.status_code == 200
