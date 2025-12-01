"""
Tests for Job Selector Agent
"""

import pytest
from agents.selector_agent import select_job


def test_selector_demo_mode():
    """Test selector with DEMO: prefix returns default."""
    job_map = {
        "python": {
            "tags": ["python"],
            "urls": ["https://jobs.lever.co/python/1", "https://jobs.lever.co/python/2"]
        },
        "default": {
            "tags": ["*"],
            "urls": ["https://jobs.lever.co/default/1"]
        }
    }
    
    primary, backup = select_job("DEMO: Python Developer", job_map)
    # Should return default URLs, not python URLs
    assert "default" in primary or primary == job_map["default"]["urls"][0]


def test_selector_exact_match():
    """Test selector with exact category match."""
    job_map = {
        "python": {
            "tags": ["python"],
            "urls": ["https://jobs.lever.co/python/1", "https://jobs.lever.co/python/2"]
        },
        "default": {
            "tags": ["*"],
            "urls": ["https://jobs.lever.co/default/1"]
        }
    }
    
    primary, backup = select_job("python", job_map)
    assert primary == job_map["python"]["urls"][0]
    assert backup == job_map["python"]["urls"][1]


def test_selector_fuzzy_match():
    """Test selector with fuzzy tag matching."""
    job_map = {
        "backend": {
            "tags": ["backend", "api"],
            "urls": ["https://jobs.lever.co/backend/1", "https://jobs.lever.co/backend/2"]
        },
        "default": {
            "tags": ["*"],
            "urls": ["https://jobs.lever.co/default/1"]
        }
    }
    
    primary, backup = select_job("api developer", job_map)
    # Should match "backend" via "api" tag
    assert "backend" in primary or primary == job_map["backend"]["urls"][0]


def test_selector_fallback_to_default():
    """Test selector falls back to default when no match."""
    job_map = {
        "python": {
            "tags": ["python"],
            "urls": ["https://jobs.lever.co/python/1"]
        },
        "default": {
            "tags": ["*"],
            "urls": ["https://jobs.lever.co/default/1"]
        }
    }
    
    primary, backup = select_job("unknown query", job_map)
    assert primary == job_map["default"]["urls"][0]


def test_selector_always_returns_tuple():
    """Test selector always returns (primary, backup) tuple."""
    job_map = {
        "default": {
            "tags": ["*"],
            "urls": ["https://jobs.lever.co/default/1"]
        }
    }
    
    result = select_job("any query", job_map)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0]  # Primary URL exists
    assert result[1]  # Backup URL exists
