"""
Tests for Job Extractor Agent
"""

import pytest
from unittest.mock import patch, MagicMock
from agents.extractor_agent import extract_job, _is_allowed_domain, DEFAULT_JOB_URL


def test_is_allowed_domain_lever():
    """Test domain validation for Lever."""
    assert _is_allowed_domain("https://jobs.lever.co/company/123") is True


def test_is_allowed_domain_greenhouse():
    """Test domain validation for Greenhouse."""
    assert _is_allowed_domain("https://boards.greenhouse.io/company/jobs/123") is True


def test_is_allowed_domain_ashby():
    """Test domain validation for AshbyHQ."""
    assert _is_allowed_domain("https://jobs.ashbyhq.com/company/123") is True


def test_is_allowed_domain_workable():
    """Test domain validation for Workable."""
    assert _is_allowed_domain("https://apply.workable.com/company/j/123") is True


def test_is_allowed_domain_blocked():
    """Test domain validation blocks non-ATS domains."""
    assert _is_allowed_domain("https://linkedin.com/jobs/123") is False
    assert _is_allowed_domain("https://indeed.com/jobs/123") is False


def test_extractor_primary_success():
    """Test extractor with successful primary URL."""
    mock_job_data = {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "skills": ["python", "react"],
        "responsibilities": ["Build APIs"],
        "experience_level": "Mid Level",
        "job_url": "https://jobs.lever.co/techcorp/123"
    }
    
    with patch('agents.extractor_agent._extract_from_url', return_value=mock_job_data):
        result = extract_job("https://jobs.lever.co/techcorp/123", "https://jobs.lever.co/techcorp/456")
        assert result["job_title"] == "Software Engineer"
        assert result["job_url"] == "https://jobs.lever.co/techcorp/123"


def test_extractor_backup_success():
    """Test extractor fallback to backup URL when primary fails."""
    mock_job_data = {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "skills": [],
        "responsibilities": [],
        "experience_level": "",
        "job_url": "https://jobs.lever.co/techcorp/456"
    }
    
    def mock_extract(url):
        if "123" in url:
            raise Exception("Primary fails")
        return mock_job_data
    
    with patch('agents.extractor_agent._extract_from_url', side_effect=mock_extract):
        result = extract_job("https://jobs.lever.co/techcorp/123", "https://jobs.lever.co/techcorp/456")
        assert result["job_url"] == "https://jobs.lever.co/techcorp/456"


def test_extractor_default_fallback():
    """Test extractor fallback to default job when both fail."""
    mock_default_job = {
        "job_title": "Software Engineer",
        "company": "Vercel",
        "skills": [],
        "responsibilities": [],
        "experience_level": "",
        "job_url": DEFAULT_JOB_URL
    }
    
    def mock_extract(url):
        if url != DEFAULT_JOB_URL:
            raise Exception("Both primary and backup fail")
        return mock_default_job
    
    with patch('agents.extractor_agent._extract_from_url', side_effect=mock_extract):
        result = extract_job("https://jobs.lever.co/fail/123", "https://jobs.lever.co/fail/456")
        assert result["job_url"] == DEFAULT_JOB_URL
        assert result["company"] == "Vercel"
