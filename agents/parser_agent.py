"""
Resume Parser Agent
Parses raw resume text into structured JSON following strict schema.
"""

def parse_resume(resume_text: str) -> dict:
    """
    Parse resume text into structured JSON.
    
    Args:
        resume_text: Raw resume text (plain text only, max 8000 chars)
        
    Returns:
        Structured resume JSON following strict schema:
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
    # TODO: Implement resume parsing logic
    pass

