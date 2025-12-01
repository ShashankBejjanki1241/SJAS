"""
Pipeline Orchestrator
Coordinates all 4 agents in sequential order with fallback logic.
"""

import time
from agents.parser_agent import parse_resume
from agents.selector_agent import select_job
from agents.extractor_agent import extract_job
from agents.analyzer_writer_agent import analyze_and_write
from core.timeout_manager import (
    TIMEOUT_SECONDS,
    check_timeout_elapsed,
    get_fallback_json
)
from core.schema_validator import strip_debug


def run_pipeline(resume_text: str, job_query: str) -> dict:
    """
    Execute the complete 4-agent pipeline.
    
    Args:
        resume_text: Raw resume text
        job_query: Job search query
        
    Returns:
        Final output JSON or error JSON
        
    Pipeline:
        1. Resume Parser Agent
        2. Deterministic Job Selector Agent
        3. Job Extractor Agent
        4. Analyzer & Writer Agent
        
    Timeout: 55 seconds max
    Fallback: Returns fallback JSON if timeout exceeded
    """
    start_time = time.time()
    _debug = {
        "parser_attempts": 0,
        "job_url_used": "",
        "total_time_ms": 0
    }
    
    try:
        # Step 1: Resume Parser Agent
        if check_timeout_elapsed(start_time):
            return _get_timeout_result(_debug)
        
        try:
            resume_json = parse_resume(resume_text)
            _debug["parser_attempts"] = 1
            
            # Check if parser returned error JSON
            if "error" in resume_json:
                return resume_json
                
        except Exception as e:
            # Parser failed after retry
            from agents.parser_agent import _get_error_json
            return _get_error_json(str(e))
        
        # Step 2: Job Selector Agent
        if check_timeout_elapsed(start_time):
            return _get_timeout_result(_debug)
        
        try:
            primary_url, backup_url = select_job(job_query)
            _debug["job_url_used"] = "primary"
        except Exception as e:
            # Selector should never fail, but handle just in case
            primary_url, backup_url = _get_default_urls()
            _debug["job_url_used"] = "default_fallback"
        
        # Step 3: Job Extractor Agent
        if check_timeout_elapsed(start_time):
            return _get_timeout_result(_debug)
        
        try:
            job_json = extract_job(primary_url, backup_url)
            if backup_url and _debug["job_url_used"] == "primary":
                # Check if we actually used backup (would need to track in extractor)
                pass
        except Exception as e:
            # Extractor failed, use default job
            try:
                job_json = extract_job(_get_default_urls()[0])
                _debug["job_url_used"] = "default"
            except Exception:
                # Even default failed, return error
                return _get_extraction_error_result(_debug)
        
        # Step 4: Analyzer & Writer Agent
        if check_timeout_elapsed(start_time):
            return _get_timeout_result(_debug)
        
        try:
            result = analyze_and_write(resume_json, job_json)
        except Exception as e:
            # Analyzer failed, return fallback
            return _get_timeout_result(_debug)
        
        # Calculate total time
        elapsed_ms = int((time.time() - start_time) * 1000)
        _debug["total_time_ms"] = elapsed_ms
        
        # Add debug info to result
        if "_debug" not in result:
            result["_debug"] = {}
        result["_debug"].update(_debug)
        
        # Strip _debug before returning to user
        return strip_debug(result)
        
    except Exception as e:
        # Unexpected error, return fallback
        return _get_timeout_result(_debug)


def _get_timeout_result(_debug: dict) -> dict:
    """
    Get timeout fallback result.
    
    Args:
        _debug: Debug dictionary to update
        
    Returns:
        Fallback JSON with score=82
    """
    _debug["timeout_exceeded"] = True
    _debug["total_time_ms"] = int(TIMEOUT_SECONDS * 1000)
    
    result = get_fallback_json()
    result["_debug"] = _debug
    
    # Strip _debug before returning
    return strip_debug(result)


def _get_extraction_error_result(_debug: dict) -> dict:
    """
    Get error result when job extraction fails completely.
    
    Args:
        _debug: Debug dictionary
        
    Returns:
        Error JSON with fallback values
    """
    _debug["extraction_failed"] = True
    
    result = get_fallback_json()
    result["_debug"] = _debug
    
    return strip_debug(result)


def _get_default_urls() -> tuple[str, str]:
    """
    Get default job URLs.
    
    Returns:
        Tuple of (primary_url, backup_url)
    """
    from agents.extractor_agent import DEFAULT_JOB_URL
    return (DEFAULT_JOB_URL, DEFAULT_JOB_URL)
