"""
Tests for Resume Parser Agent
"""

import pytest
from unittest.mock import patch, MagicMock
from agents.parser_agent import parse_resume, _get_error_json
from core.schema_validator import SchemaValidationError


def test_parser_error_json_structure():
    """Test parser returns structured error JSON on failure."""
    # Mock the LLM call to fail
    with patch('agents.parser_agent._call_llm_parse_resume', side_effect=Exception("Parse failed")):
        result = parse_resume("invalid resume text", retry_count=1)
        assert "error" in result
        assert result["match_score"] is None
        assert result["missing_skills"] == []
        assert result["strengths"] == []


def test_parser_retry_logic():
    """Test parser retries once on failure."""
    call_count = [0]
    
    def mock_llm_call(text):
        call_count[0] += 1
        if call_count[0] == 1:
            raise Exception("First attempt fails")
        # Second attempt succeeds
        return {
            "name": "John Doe",
            "years_of_experience": 5,
            "current_title": "Engineer",
            "skills": ["python"],
            "education": [],
            "work_history": []
        }
    
    with patch('agents.parser_agent._call_llm_parse_resume', side_effect=mock_llm_call):
        result = parse_resume("resume text")
        assert call_count[0] == 2  # Should retry once
        assert "name" in result


def test_parser_skill_normalization():
    """Test parser normalizes skills."""
    mock_parsed = {
        "name": "John",
        "years_of_experience": 5,
        "current_title": "Engineer",
        "skills": ["React", "react", "React.js"],
        "education": [],
        "work_history": []
    }
    
    with patch('agents.parser_agent._call_llm_parse_resume', return_value=mock_parsed):
        result = parse_resume("resume")
        # Skills should be normalized (deduplicated)
        assert len(result["skills"]) <= len(mock_parsed["skills"])


def test_parser_work_history_points_limit():
    """Test parser limits work history points to 4."""
    mock_parsed = {
        "name": "John",
        "years_of_experience": 5,
        "current_title": "Engineer",
        "skills": [],
        "education": [],
        "work_history": [
            {
                "company": "Tech",
                "role": "Engineer",
                "start": "2020",
                "end": "2024",
                "points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5", "Point 6"]
            }
        ]
    }
    
    with patch('agents.parser_agent._call_llm_parse_resume', return_value=mock_parsed):
        result = parse_resume("resume")
        assert len(result["work_history"][0]["points"]) <= 4


def test_get_error_json():
    """Test error JSON structure."""
    error_json = _get_error_json("Test error")
    assert "error" in error_json
    assert error_json["match_score"] is None
    assert isinstance(error_json["missing_skills"], list)
    assert isinstance(error_json["strengths"], list)
