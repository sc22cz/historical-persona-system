import json
import pytest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


VALID_PROFILE = {
    "name": "Test Figure",
    "vector": [0.8, 0.5, 0.6, 0.7, 0.7, 0.4, 0.7, 0.9, 0.7, 0.6],
    "confidence": [0.9, 0.8, 0.7, 0.8, 0.9, 0.7, 0.8, 0.9, 0.8, 0.7],
    "evidence": [f"Evidence {i}" for i in range(10)],
}


def _mock_claude_response(text: str):
    content = MagicMock()
    content.text = text
    response = MagicMock()
    response.content = [content]
    return response


@patch("services.extractor.anthropic.Anthropic")
def test_extract_profile_returns_valid_structure(mock_anthropic):
    client = MagicMock()
    client.messages.create.return_value = _mock_claude_response(json.dumps(VALID_PROFILE))
    mock_anthropic.return_value = client

    from services.extractor import extract_profile
    result = extract_profile("Test Figure", "Some text about Test Figure.")

    assert "vector" in result
    assert "confidence" in result
    assert "evidence" in result
    assert len(result["vector"]) == 10
    assert len(result["confidence"]) == 10
    assert len(result["evidence"]) == 10


@patch("services.extractor.anthropic.Anthropic")
def test_extract_profile_name_overrides_claude_name(mock_anthropic):
    profile = {**VALID_PROFILE, "name": "Wrong Name From Claude"}
    client = MagicMock()
    client.messages.create.return_value = _mock_claude_response(json.dumps(profile))
    mock_anthropic.return_value = client

    from services.extractor import extract_profile
    result = extract_profile("Correct Name", "Some text.")
    assert result["name"] == "Correct Name"


@patch("services.extractor.anthropic.Anthropic")
def test_extract_profile_strips_markdown_fences(mock_anthropic):
    raw = f"```json\n{json.dumps(VALID_PROFILE)}\n```"
    client = MagicMock()
    client.messages.create.return_value = _mock_claude_response(raw)
    mock_anthropic.return_value = client

    from services.extractor import extract_profile
    result = extract_profile("Test Figure", "Some text.")
    assert result["vector"] == VALID_PROFILE["vector"]


@patch("services.extractor.anthropic.Anthropic")
def test_extract_profile_raises_on_invalid_json(mock_anthropic):
    from fastapi import HTTPException
    client = MagicMock()
    client.messages.create.return_value = _mock_claude_response("not valid json at all")
    mock_anthropic.return_value = client

    from services.extractor import extract_profile
    with pytest.raises(HTTPException) as exc_info:
        extract_profile("Test Figure", "Some text.")
    assert exc_info.value.status_code == 500


@patch("services.extractor.anthropic.Anthropic")
def test_extract_profile_vector_values_in_range(mock_anthropic):
    client = MagicMock()
    client.messages.create.return_value = _mock_claude_response(json.dumps(VALID_PROFILE))
    mock_anthropic.return_value = client

    from services.extractor import extract_profile
    result = extract_profile("Test Figure", "Some text.")
    for v in result["vector"]:
        assert 0.0 <= v <= 1.0
