"""
Resume Parser Agent
Parses raw resume text into structured JSON following strict schema.
"""

import json
from typing import Optional
from core.utils import preprocess_resume_text, normalize_skills
from core.schema_validator import validate_resume_schema, SchemaValidationError
from core.adk_integration import llm_call_json


def parse_resume(resume_text: str, retry_count: int = 0) -> dict:
    """
    Parse resume text into structured JSON.
    
    Args:
        resume_text: Raw resume text (plain text only, max 8000 chars)
        retry_count: Current retry attempt (0 = first attempt, 1 = retry)
        
    Returns:
        Structured resume JSON following strict schema
        
    Raises:
        SchemaValidationError: If parsing fails after retry
    """
    # Preprocess resume text
    processed_text = preprocess_resume_text(resume_text)
    
    # Call LLM to parse resume (ADK integration point)
    try:
        parsed_data = _call_llm_parse_resume(processed_text)
    except Exception as e:
        # If first attempt fails, retry once
        if retry_count < 1:
            return parse_resume(resume_text, retry_count + 1)
        else:
            # After retry, return structured error JSON
            return _get_error_json(str(e))
    
    # Normalize skills
    if "skills" in parsed_data and isinstance(parsed_data["skills"], list):
        parsed_data["skills"] = normalize_skills(parsed_data["skills"])
    
    # Limit work history points to max 4 per job
    if "work_history" in parsed_data and isinstance(parsed_data["work_history"], list):
        for job in parsed_data["work_history"]:
            if "points" in job and isinstance(job["points"], list):
                job["points"] = job["points"][:4]
    
    # Ensure all required fields exist with defaults
    result = {
        "name": parsed_data.get("name", ""),
        "years_of_experience": parsed_data.get("years_of_experience", 0),
        "current_title": parsed_data.get("current_title", ""),
        "skills": parsed_data.get("skills", []),
        "education": parsed_data.get("education", []),
        "work_history": parsed_data.get("work_history", [])
    }
    
    # Validate schema
    try:
        validate_resume_schema(result)
    except SchemaValidationError as e:
        # If validation fails, retry once
        if retry_count < 1:
            return parse_resume(resume_text, retry_count + 1)
        else:
            return _get_error_json(f"Schema validation failed: {str(e)}")
    
    return result


def _call_llm_parse_resume(resume_text: str) -> dict:
    """
    Call LLM to parse resume text into structured JSON.
    
    Uses ADK integration for LLM calls.
    
    Args:
        resume_text: Preprocessed resume text
        
    Returns:
        Parsed resume data as dictionary
        
    Raises:
        Exception: If LLM call fails or returns invalid JSON
    """
    prompt = (
        "Parse the following resume text into a JSON object with this exact structure:\n"
        "{\n"
        '  "name": "Full name",\n'
        '  "years_of_experience": <integer>,\n'
        '  "current_title": "Current job title",\n'
        '  "skills": ["skill1", "skill2", ...],\n'
        '  "education": ["education1", "education2", ...],\n'
        '  "work_history": [\n'
        "    {\n"
        '      "company": "Company name",\n'
        '      "role": "Job title",\n'
        '      "start": "Start date",\n'
        '      "end": "End date or Present",\n'
        '      "points": ["achievement1", "achievement2", ...]\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Resume text:\n"
        f"{resume_text}\n\n"
        "Return only valid JSON, no additional text."
    )
    
    # Call ADK LLM and parse JSON response
    parsed_data = llm_call_json(prompt)
    
    return parsed_data


def _get_error_json(error_message: str = "") -> dict:
    """
    Return structured error JSON when parsing fails.
    
    Args:
        error_message: Error message to include
        
    Returns:
        Structured error JSON matching final output schema shape
    """
    return {
        "error": f"Resume parsing failed — please paste plain text only (no PDF formatting, tables, headers/footers). {error_message}".strip(),
        "match_score": None,
        "missing_skills": [],
        "strengths": [],
        "how_to_improve": [],
        "optimized_summary": "",
        "cover_letter": "",
        "recruiter_message": "",
        "job_title": "",
        "company": "",
        "job_url": ""
    }
