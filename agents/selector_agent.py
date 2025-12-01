"""
Deterministic Job Selector Agent
Selects job URL from pre-vetted job_map.json based on query.
"""

import json
import os
from typing import Tuple, Optional


def select_job(job_query: str, job_map: Optional[dict] = None) -> Tuple[str, str]:
    """
    Select primary and backup job URLs based on query.
    
    Args:
        job_query: User job query (1-6 words, supports "DEMO:" prefix)
        job_map: Optional job map dictionary. If None, loads from resources/job_map.json
        
    Returns:
        Tuple of (primary_url, backup_url)
        
    Logic (priority order):
        1. If query starts with "DEMO:" → use "default" job
        2. Exact match category in job_map.json
        3. Fuzzy match via tags field
        4. Fallback to "default"
    """
    # Load job_map if not provided
    if job_map is None:
        job_map = _load_job_map()
    
    # Convert query to lowercase for matching
    query_lower = job_query.lower().strip()
    
    # Priority 1: DEMO mode override
    if query_lower.startswith("demo:"):
        return _get_default_job_urls(job_map)
    
    # Priority 2: Exact match category
    if query_lower in job_map:
        urls = job_map[query_lower].get("urls", [])
        if urls:
            primary = urls[0] if len(urls) > 0 else ""
            backup = urls[1] if len(urls) > 1 else urls[0] if len(urls) > 0 else ""
            return (primary, backup)
    
    # Priority 3: Fuzzy match via tags
    matched_category = _fuzzy_match_tags(query_lower, job_map)
    if matched_category:
        urls = job_map[matched_category].get("urls", [])
        if urls:
            primary = urls[0] if len(urls) > 0 else ""
            backup = urls[1] if len(urls) > 1 else urls[0] if len(urls) > 0 else ""
            return (primary, backup)
    
    # Priority 4: Fallback to default
    return _get_default_job_urls(job_map)


def _load_job_map() -> dict:
    """
    Load job_map.json from resources directory.
    
    Returns:
        Job map dictionary
        
    Raises:
        FileNotFoundError: If job_map.json not found
        json.JSONDecodeError: If JSON is invalid
    """
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then to resources
    project_root = os.path.dirname(current_dir)
    job_map_path = os.path.join(project_root, "resources", "job_map.json")
    
    with open(job_map_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _fuzzy_match_tags(query: str, job_map: dict) -> Optional[str]:
    """
    Fuzzy match query against tags in job_map.
    Enhanced with better matching logic.
    
    Args:
        query: Lowercase query string
        job_map: Job map dictionary
        
    Returns:
        Matched category name or None
    """
    query_words = set(query.split())
    
    best_match = None
    best_score = 0
    
    for category, data in job_map.items():
        if category == "default":
            continue
        
        tags = data.get("tags", [])
        if not tags:
            continue
        
        # Priority 1: Check if category name appears in query (highest priority)
        if category in query_words:
            return category
        
        # Priority 2: Check if any tag matches query words
        tag_words = set()
        for tag in tags:
            tag_words.update(tag.lower().split())
        
        # Calculate match score (number of matching words)
        match_score = len(query_words.intersection(tag_words))
        
        # Enhanced: Check for semantic matches
        # "developer" matches "python", "backend"
        # "engineer" matches "data", "backend"
        semantic_matches = {
            "developer": ["python", "backend"],
            "engineer": ["data", "backend"],
            "analyst": ["data"],
            "programmer": ["python", "backend"]
        }
        
        for semantic_word, categories in semantic_matches.items():
            if semantic_word in query_words and category in categories:
                match_score += 2  # Boost score for semantic match
        
        if match_score > best_score:
            best_score = match_score
            best_match = category
    
    return best_match if best_score > 0 else None


def infer_job_category_from_resume(parsed_resume: dict, job_map: dict) -> Optional[str]:
    """
    Infer job category from parsed resume when query is vague or empty.
    
    Args:
        parsed_resume: Parsed resume JSON with skills, current_title, work_history
        job_map: Job map dictionary
        
    Returns:
        Matched category name or None
    """
    if not parsed_resume:
        return None
    
    # Collect all relevant information
    current_title = parsed_resume.get("current_title", "").lower()
    skills = [s.lower() if isinstance(s, str) else str(s).lower() for s in parsed_resume.get("skills", [])]
    work_history = parsed_resume.get("work_history", [])
    roles = []
    for job in work_history:
        if isinstance(job, dict):
            role = job.get("role", "")
            if isinstance(role, str):
                roles.append(role.lower())
        elif isinstance(job, str):
            roles.append(job.lower())
    
    # Category keywords mapping
    category_keywords = {
        "data": ["data", "etl", "pipeline", "hadoop", "spark", "informatica", 
                 "glue", "warehouse", "analyst", "bi", "sql", "database"],
        "python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
        "backend": ["backend", "api", "server", "rest", "graphql", "microservice",
                   "node", "java", "spring", "go", "rust"]
    }
    
    # Score each category
    category_scores = {}
    for category, keywords in category_keywords.items():
        score = 0
        
        # Check current title
        for keyword in keywords:
            if keyword in current_title:
                score += 3  # High weight for title match
        
        # Check skills
        for skill in skills:
            for keyword in keywords:
                if keyword in skill:
                    score += 2  # Medium weight for skill match
        
        # Check work history roles
        for role in roles:
            for keyword in keywords:
                if keyword in role:
                    score += 2  # Medium weight for role match
        
        if score > 0:
            category_scores[category] = score
    
    # Return category with highest score
    if category_scores:
        best_category = max(category_scores.items(), key=lambda x: x[1])
        if best_category[1] >= 2:  # Minimum threshold
            return best_category[0]
    
    return None


def _get_default_job_urls(job_map: dict) -> Tuple[str, str]:
    """
    Get default job URLs from job_map.
    
    Args:
        job_map: Job map dictionary
        
    Returns:
        Tuple of (primary_url, backup_url)
    """
    default_data = job_map.get("default", {})
    urls = default_data.get("urls", [])
    
    if not urls:
        # Fallback if no URLs in default
        return ("", "")
    
    primary = urls[0] if len(urls) > 0 else ""
    backup = urls[1] if len(urls) > 1 else urls[0] if len(urls) > 0 else ""
    
    return (primary, backup)
