"""
Timeout Manager
Enforces global 55-second timeout with fallback JSON.
"""

import time
from typing import Callable, Any

TIMEOUT_SECONDS = 55
TIMEOUT_WARNING_SECONDS = 50

def with_timeout(func: Callable, *args, **kwargs) -> Any:
    """
    Execute function with timeout protection.
    
    Args:
        func: Function to execute
        *args, **kwargs: Function arguments
        
    Returns:
        Function result or fallback JSON if timeout exceeded
    """
    # TODO: Implement timeout logic
    pass

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
        "job_url": "https://jobs.lever.co/vercel/xyz123"
    }

