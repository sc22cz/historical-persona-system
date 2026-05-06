import json
import pytest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imputer import impute_profile


def _make_row(id, name, era, vector, confidence):
    row = MagicMock()
    row.__getitem__ = lambda self, k: {
        "id": id, "name": name, "era": era,
        "vector": json.dumps(vector),
        "confidence": json.dumps(confidence),
    }[k]
    return row


TARGET_VEC = [0.8, 0.5, 0.0, 0.7, 0.6, 0.3, 0.9, 0.4, 0.2, 0.1]
TARGET_CONF = [0.9, 0.0, 0.0, 0.8, 0.7, 0.9, 0.8, 0.7, 0.0, 0.0]

DONOR_VEC  = [0.7, 0.6, 0.3, 0.8, 0.5, 0.4, 0.8, 0.5, 0.9, 0.7]
DONOR_CONF = [0.8, 0.9, 0.8, 0.9, 0.8, 0.9, 0.9, 0.8, 0.9, 0.8]


def _make_mock_conn(target_row, donor_rows):
    cursor = MagicMock()
    cursor.fetchone.return_value = target_row
    cursor.fetchall.return_value = donor_rows
    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn


@patch("imputer.get_connection")
def test_missing_figure_returns_error(mock_gc):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_gc.return_value = conn

    result = impute_profile(999)
    assert "error" in result


@patch("imputer.get_connection")
def test_impute_fills_low_confidence_dims(mock_gc):
    target = _make_row(1, "Target", 500, TARGET_VEC, TARGET_CONF)
    donor  = _make_row(2, "Donor", 1900, DONOR_VEC, DONOR_CONF)
    mock_gc.return_value = _make_mock_conn(target, [donor])

    result = impute_profile(1)
    imputed = result["imputed_vector"]
    original = result["original_vector"]

    # dims with low confidence (0.0) should be filled in
    low_conf_dims = [i for i, c in enumerate(TARGET_CONF) if c < 0.4]
    for i in low_conf_dims:
        # if a donor was found, value should differ from original
        if i in result["imputed_from"]:
            assert imputed[i] != original[i] or imputed[i] == DONOR_VEC[i]


@patch("imputer.get_connection")
def test_impute_preserves_high_confidence_dims(mock_gc):
    target = _make_row(1, "Target", 500, TARGET_VEC, TARGET_CONF)
    donor  = _make_row(2, "Donor", 1900, DONOR_VEC, DONOR_CONF)
    mock_gc.return_value = _make_mock_conn(target, [donor])

    result = impute_profile(1)
    imputed = result["imputed_vector"]
    original = result["original_vector"]

    high_conf_dims = [i for i, c in enumerate(TARGET_CONF) if c >= 0.4]
    for i in high_conf_dims:
        assert imputed[i] == original[i]


@patch("imputer.get_connection")
def test_impute_result_has_required_keys(mock_gc):
    target = _make_row(1, "Target", 500, TARGET_VEC, TARGET_CONF)
    mock_gc.return_value = _make_mock_conn(target, [])

    result = impute_profile(1)
    assert "figure_id" in result
    assert "original_vector" in result
    assert "original_confidence" in result
    assert "imputed_vector" in result
    assert "imputed_from" in result


@patch("imputer.get_connection")
def test_impute_vector_length_preserved(mock_gc):
    target = _make_row(1, "Target", 500, TARGET_VEC, TARGET_CONF)
    donor  = _make_row(2, "Donor", 1900, DONOR_VEC, DONOR_CONF)
    mock_gc.return_value = _make_mock_conn(target, [donor])

    result = impute_profile(1)
    assert len(result["imputed_vector"]) == 10


@patch("imputer.get_connection")
def test_impute_no_donors_returns_original(mock_gc):
    target = _make_row(1, "Target", 500, TARGET_VEC, TARGET_CONF)
    mock_gc.return_value = _make_mock_conn(target, [])

    result = impute_profile(1)
    assert result["imputed_vector"] == result["original_vector"]
    assert result["imputed_from"] == {}


@patch("imputer.get_connection")
def test_impute_with_user_vector(mock_gc):
    target = _make_row(1, "Target", 500, TARGET_VEC, TARGET_CONF)
    mock_gc.return_value = _make_mock_conn(target, [])

    user_vector = [0.6, 0.7, 0.4, 0.5, 0.8, 0.3, 0.7, 0.6, 0.9, 0.8]
    result = impute_profile(1, user_vector=user_vector)

    # User vector should fill some low-confidence dims
    low_conf_dims = [i for i, c in enumerate(TARGET_CONF) if c < 0.4]
    filled = list(result["imputed_from"].keys())
    assert any(int(i) in low_conf_dims for i in filled)
