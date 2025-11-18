"""
Analyzer & Writer Agent
Analyzes resume-job match and generates writing outputs.
"""

def analyze_and_write(resume_json: dict, job_json: dict) -> dict:
    """
    Analyze resume-job match and generate outputs.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        
    Returns:
        Final output JSON following strict schema:
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
        
    Scoring:
        - Hard skill overlap ratio
        - Integer-only experience score (0-10)
        - Education match boolean
        - Final score formula: 40% skills + 40% experience + 20% education
    """
    # TODO: Implement analysis and writing logic
    pass

