"""
Timeout Manager
Enforces global 55-second timeout with fallback JSON.
"""

import time
from typing import Callable, Any

TIMEOUT_SECONDS = 55
TIMEOUT_WARNING_SECONDS = 50


class TimeoutError(Exception):
    """Raised when operation exceeds timeout."""
    pass


def with_timeout(func: Callable, *args, **kwargs) -> Any:
    """
    Execute function with timeout protection.
    
    Note: This is a simple timeout wrapper. For true timeout enforcement
    in a sequential pipeline, the pipeline orchestrator should track
    elapsed time and call get_fallback_json() if timeout is exceeded.
    
    Args:
        func: Function to execute
        *args, **kwargs: Function arguments
        
    Returns:
        Function result or raises TimeoutError if timeout exceeded
        
    Raises:
        TimeoutError: If execution exceeds timeout
    """
    start_time = time.time()
    
    try:
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        
        if elapsed > TIMEOUT_SECONDS:
            raise TimeoutError(f"Function execution exceeded {TIMEOUT_SECONDS}s timeout")
        
        return result
    except TimeoutError:
        raise
    except Exception as e:
        # Re-raise other exceptions
        raise


def check_timeout_elapsed(start_time: float) -> bool:
    """
    Check if timeout has been exceeded.
    
    Args:
        start_time: Start time from time.time()
        
    Returns:
        True if timeout exceeded, False otherwise
    """
    elapsed = time.time() - start_time
    return elapsed >= TIMEOUT_SECONDS


def get_time_remaining(start_time: float) -> float:
    """
    Get remaining time before timeout.
    
    Args:
        start_time: Start time from time.time()
        
    Returns:
        Remaining seconds before timeout (can be negative)
    """
    elapsed = time.time() - start_time
    return TIMEOUT_SECONDS - elapsed


def get_fallback_json() -> dict:
    """
    Return fallback JSON when timeout exceeded.
    
    Returns:
        Fallback JSON with match_score=82
    """
    return {
        "match_score": 82,
        "score_breakdown": "Fallback mode activated",
        "missing_skills": [],
        "strengths": [],
        "how_to_improve": ["Review your resume for technical skill alignment"],
        "optimized_summary": "Summary unavailable due to fallback mode.",
        "cover_letter": "Cover letter unavailable due to fallback mode.",
        "recruiter_message": "Message unavailable due to fallback mode.",
        "job_title": "Software Engineer",
        "company": "Vercel",
        "job_url": "https://jobs.lever.co/vercel/xyz123",
        "_debug": {
            "timeout_exceeded": True,
            "fallback_mode": True
        }
    }
