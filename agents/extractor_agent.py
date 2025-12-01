"""
Job Extractor Agent
Extracts job information from ATS pages using browse_page tool.
"""

import re
from typing import Optional
from urllib.parse import urlparse
from core.schema_validator import validate_job_schema, SchemaValidationError

# ADK load_web_page tool - will be imported when ADK is available
try:
    from google.adk.tools.load_web_page import load_web_page as adk_load_web_page
    ADK_BROWSE_AVAILABLE = True
except ImportError:
    ADK_BROWSE_AVAILABLE = False


# Allowed ATS domains
ALLOWED_DOMAINS = {
    "lever.co",
    "greenhouse.io",
    "ashbyhq.com",
    "workable.com"
}

# Default job URL (fallback) - Verified working URL
DEFAULT_JOB_URL = "https://jobs.lever.co/nava/7a315e81-41eb-40cc-bb0e-b065b7f88712"


def extract_job(job_url: str, backup_url: Optional[str] = None) -> dict:
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
        
    Fallback logic:
        - Primary URL → if fails → Backup URL → if fails → Default Vercel job
    """
    # Try primary URL
    if job_url and _is_allowed_domain(job_url):
        try:
            result = _extract_from_url(job_url)
            if result:
                return result
        except Exception:
            pass  # Fall through to backup
    
    # Try backup URL
    if backup_url and _is_allowed_domain(backup_url):
        try:
            result = _extract_from_url(backup_url)
            if result:
                return result
        except Exception:
            pass  # Fall through to default
    
    # Fallback to default Vercel job
    return _extract_from_url(DEFAULT_JOB_URL)


def _is_allowed_domain(url: str) -> bool:
    """
    Check if URL is from an allowed ATS domain.
    
    Args:
        url: URL to check
        
    Returns:
        True if domain is allowed, False otherwise
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Check if domain matches any allowed domain
        for allowed in ALLOWED_DOMAINS:
            if allowed in domain:
                return True
        return False
    except Exception:
        return False


def _extract_from_url(url: str) -> dict:
    """
    Extract job information from a single URL using ADK's load_web_page tool.
    
    Uses ADK integration for page browsing.
    
    Args:
        url: Job URL to extract from
        
    Returns:
        Extracted job data as dictionary
        
    Raises:
        Exception: If extraction fails
    """
    if not ADK_BROWSE_AVAILABLE:
        raise NotImplementedError(
            "ADK load_web_page tool not available. Please install google-adk."
        )
    
    # Call ADK load_web_page tool to get page content
    page_content = adk_load_web_page(url)
    
    # Parse the page content into structured job data
    return _parse_job_content(page_content, url)


def _parse_job_content(page_content: str, job_url: str) -> dict:
    """
    Parse job content from page HTML/text into structured JSON.
    
    Args:
        page_content: Raw page content from browse_page
        job_url: Original job URL
        
    Returns:
        Structured job JSON
    """
    # Strip HTML/markdown
    text_content = _strip_html_markdown(page_content)
    
    # Extract job information using regex/parsing
    # This is a simplified parser - in production, use LLM or more sophisticated parsing
    
    job_title = _extract_job_title(text_content)
    company = _extract_company(text_content, job_url)
    skills = _extract_hard_skills(text_content)
    responsibilities = _extract_responsibilities(text_content)
    experience_level = _extract_experience_level(text_content)
    
    result = {
        "job_title": job_title,
        "company": company,
        "skills": skills[:10],  # Limit to max 10
        "responsibilities": responsibilities[:6],  # Limit to max 6
        "experience_level": experience_level,
        "job_url": job_url
    }
    
    # Validate schema
    try:
        validate_job_schema(result)
    except SchemaValidationError:
        # If validation fails, return minimal valid structure
        return {
            "job_title": job_title or "Software Engineer",
            "company": company or "Company",
            "skills": [],
            "responsibilities": [],
            "experience_level": "",
            "job_url": job_url
        }
    
    return result


def _strip_html_markdown(content: str) -> str:
    """
    Strip HTML and markdown from content.
    
    Args:
        content: Raw content with HTML/markdown
        
    Returns:
        Plain text content
    """
    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Remove markdown formatting
    content = re.sub(r'#{1,6}\s+', '', content)  # Headers
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*([^*]+)\*', r'\1', content)  # Italic
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Links
    content = re.sub(r'`([^`]+)`', r'\1', content)  # Code
    
    # Clean up whitespace
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    return content


def _extract_job_title(text: str) -> str:
    """Extract job title from text."""
    # Simple extraction - in production, use LLM or more sophisticated parsing
    patterns = [
        r'(?:job title|position|role):\s*([^\n]+)',
        r'(?:hiring|looking for|seeking)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "Software Engineer"  # Default


def _extract_company(text: str, url: str) -> str:
    """Extract company name from text or URL."""
    # Try to extract from URL first
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Extract company from domain (e.g., jobs.lever.co/vercel -> vercel)
        if 'lever.co' in domain:
            path_parts = [p for p in parsed.path.split('/') if p]
            if path_parts:
                return path_parts[0].title()
    except Exception:
        pass
    
    # Try to extract from text
    patterns = [
        r'(?:company|at|working at):\s*([^\n]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "Company"  # Default


def _extract_hard_skills(text: str) -> list[str]:
    """
    Extract hard/technical skills from job description.
    
    Only extracts technical terms, not soft skills.
    """
    # Common hard skills patterns
    hard_skills = [
        # Languages
        r'\b(python|java|javascript|typescript|go|rust|c\+\+|c#|ruby|php|swift|kotlin)\b',
        # Frameworks
        r'\b(react|vue|angular|django|flask|spring|express|node\.?js|rails)\b',
        # Tools/Platforms
        r'\b(kubernetes|docker|aws|gcp|azure|terraform|ansible|jenkins|git)\b',
        # Databases
        r'\b(postgresql|mysql|mongodb|redis|cassandra|elasticsearch)\b',
        # Other technical terms
        r'\b(api|rest|graphql|microservices|ci/cd|devops|ml|ai|data science)\b',
    ]
    
    found_skills = set()
    text_lower = text.lower()
    
    for pattern in hard_skills:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            # Normalize skill name
            skill = match.lower().strip()
            skill = re.sub(r'\.', '', skill)  # Remove dots
            skill = re.sub(r'\s+', '', skill)  # Remove spaces
            if skill and len(skill) > 2:  # Filter out very short matches
                found_skills.add(skill)
    
    return list(found_skills)[:10]  # Limit to max 10


def _extract_responsibilities(text: str) -> list[str]:
    """Extract responsibilities from job description."""
    # Look for bullet points or numbered lists
    patterns = [
        r'(?:^|\n)[\s]*[-•*]\s*([^\n]+)',
        r'(?:^|\n)[\s]*\d+\.\s*([^\n]+)',
    ]
    
    responsibilities = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        for match in matches:
            resp = match.strip()
            if resp and len(resp) > 10:  # Filter out very short items
                responsibilities.append(resp)
    
    return responsibilities[:6]  # Limit to max 6


def _extract_experience_level(text: str) -> str:
    """Extract experience level from job description."""
    text_lower = text.lower()
    
    if re.search(r'\b(junior|entry|intern|0-2|1-2)\s*(?:years?|yrs?)?', text_lower):
        return "Entry Level"
    elif re.search(r'\b(senior|lead|principal|staff|5\+|7\+|10\+)\s*(?:years?|yrs?)?', text_lower):
        return "Senior"
    elif re.search(r'\b(mid|middle|3-5|2-5|4-6)\s*(?:years?|yrs?)?', text_lower):
        return "Mid Level"
    else:
        return ""
