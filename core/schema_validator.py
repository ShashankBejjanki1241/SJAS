"""
Schema Validator
Enforces strict JSON schemas for all agent outputs.
"""

def validate_resume_schema(data: dict) -> bool:
    """
    Validate resume JSON schema.
    
    Args:
        data: Resume JSON to validate
        
    Returns:
        True if valid, raises exception if invalid
    """
    # TODO: Implement schema validation
    pass

def validate_job_schema(data: dict) -> bool:
    """
    Validate job JSON schema.
    
    Args:
        data: Job JSON to validate
        
    Returns:
        True if valid, raises exception if invalid
    """
    # TODO: Implement schema validation
    pass

def validate_final_output_schema(data: dict) -> bool:
    """
    Validate final output JSON schema.
    
    Args:
        data: Final output JSON to validate
        
    Returns:
        True if valid, raises exception if invalid
    """
    # TODO: Implement schema validation
    pass

def strip_debug(data: dict) -> dict:
    """
    Remove _debug field from output before returning to user.
    
    Args:
        data: Output JSON with _debug field
        
    Returns:
        Output JSON without _debug field
    """
    if "_debug" in data:
        data = data.copy()
        del data["_debug"]
    return data

