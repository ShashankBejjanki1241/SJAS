"""
Job Extractor Agent
Extracts job information from ATS pages using browse_page tool.
"""

def extract_job(job_url: str, backup_url: str = None) -> dict:
    """
    Extract job information from ATS page.
    
    Args:
        job_url: Primary job URL (Lever/Greenhouse/AshbyHQ/Workable only)
        backup_url: Backup job URL if primary fails
        
    Returns:
        Structured job JSON following strict schema:
        {
            "job_title": "",
            "company": "",
            "skills": [],
            "responsibilities": [],
            "experience_level": "",
            "job_url": ""
        }
        
    Fallback:
        - Primary → backup → default Vercel job
    """
    # TODO: Implement job extraction logic
    pass

