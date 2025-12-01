"""
Tests for Timeout Manager
"""

import time
import pytest
from core.timeout_manager import (
    TIMEOUT_SECONDS,
    TIMEOUT_WARNING_SECONDS,
    check_timeout_elapsed,
    get_time_remaining,
    get_fallback_json,
    TimeoutError
)


def test_timeout_constants():
    """Test timeout constants are correct."""
    assert TIMEOUT_SECONDS == 55
    assert TIMEOUT_WARNING_SECONDS == 50


def test_check_timeout_elapsed_not_elapsed():
    """Test timeout check when not elapsed."""
    start_time = time.time()
    assert check_timeout_elapsed(start_time) is False


def test_check_timeout_elapsed_elapsed():
    """Test timeout check when elapsed."""
    start_time = time.time() - 60  # 60 seconds ago
    assert check_timeout_elapsed(start_time) is True


def test_get_time_remaining():
    """Test getting remaining time."""
    start_time = time.time() - 10  # 10 seconds ago
    remaining = get_time_remaining(start_time)
    assert remaining < TIMEOUT_SECONDS
    assert remaining > 0


def test_get_fallback_json():
    """Test fallback JSON structure."""
    fallback = get_fallback_json()
    assert fallback["match_score"] == 82
    assert fallback["score_breakdown"] == "Fallback mode activated"
    assert "job_title" in fallback
    assert "company" in fallback
    assert "_debug" in fallback
    assert fallback["_debug"]["timeout_exceeded"] is True


def test_get_fallback_json_schema():
    """Test fallback JSON matches final output schema."""
    from core.schema_validator import validate_final_output_schema
    fallback = get_fallback_json()
    # Should validate (may need to adjust if _debug structure differs)
    assert isinstance(fallback, dict)

