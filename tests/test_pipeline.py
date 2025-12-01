"""
Integration Tests for Pipeline
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from core.pipeline import run_pipeline
from core.timeout_manager import TIMEOUT_SECONDS


def test_pipeline_happy_path():
    """Test pipeline end-to-end happy path."""
    resume_text = "John Doe\nSoftware Engineer\n5 years experience\nSkills: Python, React"
    job_query = "python developer"
    
    # Mock all ADK calls
    mock_resume_json = {
        "name": "John Doe",
        "years_of_experience": 5,
        "current_title": "Software Engineer",
        "skills": ["python", "react"],
        "education": ["Bachelor's"],
        "work_history": []
    }
    
    mock_job_json = {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "skills": ["python", "react"],
        "responsibilities": ["Build APIs"],
        "experience_level": "Mid Level",
        "job_url": "https://jobs.lever.co/techcorp/123"
    }
    
    with patch('agents.parser_agent._call_llm_parse_resume', return_value=mock_resume_json):
        with patch('agents.extractor_agent._extract_from_url', return_value=mock_job_json):
            with patch('agents.analyzer_writer_agent._get_experience_score', return_value=8):
                with patch('agents.analyzer_writer_agent._generate_summary', return_value="Summary."):
                    with patch('agents.analyzer_writer_agent._generate_cover_letter', return_value="Cover " * 100):
                        with patch('agents.analyzer_writer_agent._generate_recruiter_message', return_value="Message."):
                            result = run_pipeline(resume_text, job_query)
                            
                            assert "match_score" in result
                            assert "_debug" not in result  # Should be stripped
                            assert result["job_title"] == "Software Engineer"


def test_pipeline_parser_failure():
    """Test pipeline handles parser failure."""
    resume_text = "invalid resume"
    job_query = "python"
    
    with patch('agents.parser_agent._call_llm_parse_resume', side_effect=Exception("Parse failed")):
        result = run_pipeline(resume_text, job_query)
        assert "error" in result
        assert result["match_score"] is None


def test_pipeline_demo_mode():
    """Test pipeline with DEMO mode."""
    resume_text = "John Doe\nEngineer"
    job_query = "DEMO: Python Developer"
    
    mock_resume_json = {
        "name": "John Doe",
        "years_of_experience": 5,
        "current_title": "Engineer",
        "skills": ["python"],
        "education": [],
        "work_history": []
    }
    
    mock_job_json = {
        "job_title": "Software Engineer",
        "company": "Vercel",
        "skills": ["python"],
        "responsibilities": [],
        "experience_level": "",
        "job_url": "https://jobs.lever.co/vercel/xyz123"
    }
    
    with patch('agents.parser_agent._call_llm_parse_resume', return_value=mock_resume_json):
        with patch('agents.extractor_agent._extract_from_url', return_value=mock_job_json):
            with patch('agents.analyzer_writer_agent._get_experience_score', return_value=8):
                with patch('agents.analyzer_writer_agent._generate_summary', return_value="Summary."):
                    with patch('agents.analyzer_writer_agent._generate_cover_letter', return_value="Cover " * 100):
                        with patch('agents.analyzer_writer_agent._generate_recruiter_message', return_value="Message."):
                            result = run_pipeline(resume_text, job_query)
                            # Should use default job
                            assert result["job_url"] == "https://jobs.lever.co/vercel/xyz123"


def test_pipeline_timeout_fallback():
    """Test pipeline timeout fallback."""
    resume_text = "John Doe\nEngineer"
    job_query = "python"
    
    # Mock timeout check to return True (timeout exceeded) at the first check
    # This simulates timeout being detected at the start of the pipeline
    with patch('core.pipeline.check_timeout_elapsed', return_value=True):
        start = time.time()
        result = run_pipeline(resume_text, job_query)
        elapsed = time.time() - start
        
        # Should return fallback immediately (not wait)
        assert elapsed < 1
        assert result["match_score"] == 82
        assert "Fallback mode activated" in result["score_breakdown"]


def test_pipeline_extractor_fallback():
    """Test pipeline handles extractor failure with fallback."""
    resume_text = "John Doe\nEngineer"
    job_query = "python"
    
    mock_resume_json = {
        "name": "John Doe",
        "years_of_experience": 5,
        "current_title": "Engineer",
        "skills": ["python"],
        "education": [],
        "work_history": []
    }
    
    mock_default_job = {
        "job_title": "Software Engineer",
        "company": "Vercel",
        "skills": [],
        "responsibilities": [],
        "experience_level": "",
        "job_url": "https://jobs.lever.co/vercel/xyz123"
    }
    
    with patch('agents.parser_agent._call_llm_parse_resume', return_value=mock_resume_json):
        # Primary and backup fail, should use default
        with patch('agents.extractor_agent._extract_from_url', side_effect=[Exception("Fail"), Exception("Fail"), mock_default_job]):
            with patch('agents.analyzer_writer_agent._get_experience_score', return_value=8):
                with patch('agents.analyzer_writer_agent._generate_summary', return_value="Summary."):
                    with patch('agents.analyzer_writer_agent._generate_cover_letter', return_value="Cover " * 100):
                        with patch('agents.analyzer_writer_agent._generate_recruiter_message', return_value="Message."):
                            result = run_pipeline(resume_text, job_query)
                            assert result["job_url"] == "https://jobs.lever.co/vercel/xyz123"

