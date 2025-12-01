"""
Tests for Schema Validator
"""

import pytest
from core.schema_validator import (
    validate_resume_schema,
    validate_job_schema,
    validate_final_output_schema,
    strip_debug,
    SchemaValidationError
)


def test_validate_resume_schema_valid():
    """Test resume schema validation with valid data."""
    valid_resume = {
        "name": "John Doe",
        "years_of_experience": 5,
        "current_title": "Software Engineer",
        "skills": ["python", "react"],
        "education": ["Bachelor's in CS"],
        "work_history": [
            {
                "company": "Tech Corp",
                "role": "Software Engineer",
                "start": "2020-01",
                "end": "2024-01",
                "points": ["Built API", "Led team"]
            }
        ]
    }
    assert validate_resume_schema(valid_resume) is True


def test_validate_resume_schema_extra_keys():
    """Test resume schema rejects extra keys."""
    invalid_resume = {
        "name": "John Doe",
        "years_of_experience": 5,
        "current_title": "Software Engineer",
        "skills": [],
        "education": [],
        "work_history": [],
        "extra_key": "should fail"
    }
    with pytest.raises(SchemaValidationError, match="Extra keys"):
        validate_resume_schema(invalid_resume)


def test_validate_resume_schema_missing_keys():
    """Test resume schema rejects missing keys."""
    invalid_resume = {
        "name": "John Doe",
        "years_of_experience": 5,
        # Missing current_title, skills, education, work_history
    }
    with pytest.raises(SchemaValidationError, match="Missing"):
        validate_resume_schema(invalid_resume)


def test_validate_job_schema_valid():
    """Test job schema validation with valid data."""
    valid_job = {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "skills": ["python", "react"],
        "responsibilities": ["Build APIs", "Write tests"],
        "experience_level": "Mid Level",
        "job_url": "https://jobs.lever.co/techcorp/123"
    }
    assert validate_job_schema(valid_job) is True


def test_validate_job_schema_extra_keys():
    """Test job schema rejects extra keys."""
    invalid_job = {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "skills": [],
        "responsibilities": [],
        "experience_level": "",
        "job_url": "",
        "extra_key": "should fail"
    }
    with pytest.raises(SchemaValidationError, match="Extra keys"):
        validate_job_schema(invalid_job)


def test_validate_final_output_schema_valid():
    """Test final output schema validation with valid data."""
    valid_output = {
        "match_score": 85,
        "score_breakdown": "Skills 80% · Experience 9/10 · Education Match",
        "missing_skills": ["kubernetes"],
        "strengths": ["Strong Python skills"],
        "how_to_improve": ["Learn Kubernetes"],
        "optimized_summary": "Experienced engineer with strong Python skills.",
        "cover_letter": "Dear Hiring Manager...",
        "recruiter_message": "Interested in this position.",
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "job_url": "https://jobs.lever.co/techcorp/123",
        "_debug": {"parser_attempts": 1}
    }
    assert validate_final_output_schema(valid_output) is True


def test_validate_final_output_schema_null_score():
    """Test final output schema accepts null match_score."""
    valid_output = {
        "match_score": None,
        "score_breakdown": "",
        "missing_skills": [],
        "strengths": [],
        "how_to_improve": [],
        "optimized_summary": "",
        "cover_letter": "",
        "recruiter_message": "",
        "job_title": "",
        "company": "",
        "job_url": "",
        "_debug": {}
    }
    assert validate_final_output_schema(valid_output) is True


def test_strip_debug():
    """Test _debug field is stripped correctly."""
    data_with_debug = {
        "match_score": 85,
        "job_title": "Engineer",
        "_debug": {"parser_attempts": 1, "total_time_ms": 5000}
    }
    result = strip_debug(data_with_debug)
    assert "_debug" not in result
    assert "match_score" in result
    assert "job_title" in result


def test_strip_debug_no_debug_field():
    """Test strip_debug handles data without _debug field."""
    data_without_debug = {
        "match_score": 85,
        "job_title": "Engineer"
    }
    result = strip_debug(data_without_debug)
    assert "_debug" not in result
    assert result == data_without_debug

