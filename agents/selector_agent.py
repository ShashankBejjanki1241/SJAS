"""
Deterministic Job Selector Agent
Selects job URL from pre-vetted job_map.json based on query.
"""

def select_job(job_query: str, job_map: dict) -> tuple[str, str]:
    """
    Select primary and backup job URLs based on query.
    
    Args:
        job_query: User job query (1-6 words, supports "DEMO:" prefix)
        job_map: Loaded job_map.json dictionary
        
    Returns:
        Tuple of (primary_url, backup_url)
        
    Logic:
        - If query starts with "DEMO:" → use "default" job
        - Else exact match category in job_map.json
        - Else fuzzy match via tags
        - Else fallback to "default"
    """
    # TODO: Implement job selection logic
    pass

