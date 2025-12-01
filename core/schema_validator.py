"""
Schema Validator
Enforces strict JSON schemas for all agent outputs.
"""


class SchemaValidationError(Exception):
    """Raised when JSON schema validation fails."""
    pass


def validate_resume_schema(data: dict) -> bool:
    """
    Validate resume JSON schema.
    
    Args:
        data: Resume JSON to validate
        
    Returns:
        True if valid
        
    Raises:
        SchemaValidationError: If schema is invalid
        
    Expected schema:
    {
        "name": "",
        "years_of_experience": 0,
        "current_title": "",
        "skills": [],
        "education": [],
        "work_history": [
            {
                "company": "",
                "role": "",
                "start": "",
                "end": "",
                "points": []
            }
        ]
    }
    """
    if not isinstance(data, dict):
        raise SchemaValidationError("Resume data must be a dictionary")
    
    # Define required keys (exact schema - no extra keys allowed)
    required_keys = {
        "name", "years_of_experience", "current_title", 
        "skills", "education", "work_history"
    }
    
    # Check for extra keys
    data_keys = set(data.keys())
    if data_keys != required_keys:
        extra_keys = data_keys - required_keys
        missing_keys = required_keys - data_keys
        if extra_keys:
            raise SchemaValidationError(f"Extra keys found in resume schema: {extra_keys}")
        if missing_keys:
            raise SchemaValidationError(f"Missing required keys in resume schema: {missing_keys}")
    
    # Validate types
    if not isinstance(data["name"], str):
        raise SchemaValidationError("'name' must be a string")
    
    if not isinstance(data["years_of_experience"], int):
        raise SchemaValidationError("'years_of_experience' must be an integer")
    
    if not isinstance(data["current_title"], str):
        raise SchemaValidationError("'current_title' must be a string")
    
    if not isinstance(data["skills"], list):
        raise SchemaValidationError("'skills' must be a list")
    
    if not isinstance(data["education"], list):
        raise SchemaValidationError("'education' must be a list")
    
    if not isinstance(data["work_history"], list):
        raise SchemaValidationError("'work_history' must be a list")
    
    # Validate work_history items
    for idx, job in enumerate(data["work_history"]):
        if not isinstance(job, dict):
            raise SchemaValidationError(f"work_history[{idx}] must be a dictionary")
        
        job_required_keys = {"company", "role", "start", "end", "points"}
        job_keys = set(job.keys())
        
        if job_keys != job_required_keys:
            extra_keys = job_keys - job_required_keys
            missing_keys = job_required_keys - job_keys
            if extra_keys:
                raise SchemaValidationError(f"Extra keys in work_history[{idx}]: {extra_keys}")
            if missing_keys:
                raise SchemaValidationError(f"Missing keys in work_history[{idx}]: {missing_keys}")
        
        if not isinstance(job["company"], str):
            raise SchemaValidationError(f"work_history[{idx}]['company'] must be a string")
        if not isinstance(job["role"], str):
            raise SchemaValidationError(f"work_history[{idx}]['role'] must be a string")
        if not isinstance(job["start"], str):
            raise SchemaValidationError(f"work_history[{idx}]['start'] must be a string")
        if not isinstance(job["end"], str):
            raise SchemaValidationError(f"work_history[{idx}]['end'] must be a string")
        if not isinstance(job["points"], list):
            raise SchemaValidationError(f"work_history[{idx}]['points'] must be a list")
    
    return True


def validate_job_schema(data: dict) -> bool:
    """
    Validate job JSON schema.
    
    Args:
        data: Job JSON to validate
        
    Returns:
        True if valid
        
    Raises:
        SchemaValidationError: If schema is invalid
        
    Expected schema:
    {
        "job_title": "",
        "company": "",
        "skills": [],
        "responsibilities": [],
        "experience_level": "",
        "job_url": ""
    }
    """
    if not isinstance(data, dict):
        raise SchemaValidationError("Job data must be a dictionary")
    
    # Define required keys (exact schema - no extra keys allowed)
    required_keys = {
        "job_title", "company", "skills", 
        "responsibilities", "experience_level", "job_url"
    }
    
    # Check for extra keys
    data_keys = set(data.keys())
    if data_keys != required_keys:
        extra_keys = data_keys - required_keys
        missing_keys = required_keys - data_keys
        if extra_keys:
            raise SchemaValidationError(f"Extra keys found in job schema: {extra_keys}")
        if missing_keys:
            raise SchemaValidationError(f"Missing required keys in job schema: {missing_keys}")
    
    # Validate types
    if not isinstance(data["job_title"], str):
        raise SchemaValidationError("'job_title' must be a string")
    
    if not isinstance(data["company"], str):
        raise SchemaValidationError("'company' must be a string")
    
    if not isinstance(data["skills"], list):
        raise SchemaValidationError("'skills' must be a list")
    
    if not isinstance(data["responsibilities"], list):
        raise SchemaValidationError("'responsibilities' must be a list")
    
    if not isinstance(data["experience_level"], str):
        raise SchemaValidationError("'experience_level' must be a string")
    
    if not isinstance(data["job_url"], str):
        raise SchemaValidationError("'job_url' must be a string")
    
    return True


def validate_final_output_schema(data: dict) -> bool:
    """
    Validate final output JSON schema.
    
    Args:
        data: Final output JSON to validate
        
    Returns:
        True if valid
        
    Raises:
        SchemaValidationError: If schema is invalid
        
    Expected schema:
    {
        "match_score": null,
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
    """
    if not isinstance(data, dict):
        raise SchemaValidationError("Final output data must be a dictionary")
    
    # Define required keys (exact schema - no extra keys allowed)
    # Note: _debug is optional (gets stripped before returning to user)
    required_keys = {
        "match_score", "score_breakdown", "missing_skills", "strengths",
        "how_to_improve", "optimized_summary", "cover_letter", 
        "recruiter_message", "job_title", "company", "job_url"
    }
    
    # Allowed optional keys (can be present but not required)
    optional_keys = {"_debug"}
    
    # Check for extra keys
    data_keys = set(data.keys())
    required_in_data = required_keys.intersection(data_keys)
    extra_keys = data_keys - required_keys - optional_keys
    
    if len(required_in_data) != len(required_keys):
        missing_keys = required_keys - data_keys
        raise SchemaValidationError(f"Missing required keys in final output schema: {missing_keys}")
    
    if extra_keys:
        raise SchemaValidationError(f"Extra keys found in final output schema: {extra_keys}")
    
    # Validate types
    if data["match_score"] is not None and not isinstance(data["match_score"], int):
        raise SchemaValidationError("'match_score' must be an integer or null")
    
    if not isinstance(data["score_breakdown"], str):
        raise SchemaValidationError("'score_breakdown' must be a string")
    
    if not isinstance(data["missing_skills"], list):
        raise SchemaValidationError("'missing_skills' must be a list")
    
    if not isinstance(data["strengths"], list):
        raise SchemaValidationError("'strengths' must be a list")
    
    if not isinstance(data["how_to_improve"], list):
        raise SchemaValidationError("'how_to_improve' must be a list")
    
    if not isinstance(data["optimized_summary"], str):
        raise SchemaValidationError("'optimized_summary' must be a string")
    
    if not isinstance(data["cover_letter"], str):
        raise SchemaValidationError("'cover_letter' must be a string")
    
    if not isinstance(data["recruiter_message"], str):
        raise SchemaValidationError("'recruiter_message' must be a string")
    
    if not isinstance(data["job_title"], str):
        raise SchemaValidationError("'job_title' must be a string")
    
    if not isinstance(data["company"], str):
        raise SchemaValidationError("'company' must be a string")
    
    if not isinstance(data["job_url"], str):
        raise SchemaValidationError("'job_url' must be a string")
    
    # Validate _debug if present (optional field - gets stripped before returning to user)
    if "_debug" in data and not isinstance(data["_debug"], dict):
        raise SchemaValidationError("'_debug' must be a dictionary")
    
    return True


def strip_debug(data: dict) -> dict:
    """
    Remove _debug field from output before returning to user.
    
    Args:
        data: Output JSON with _debug field
        
    Returns:
        Output JSON without _debug field (new dict, original unchanged)
    """
    if "_debug" in data:
        data = data.copy()
        del data["_debug"]
    return data
