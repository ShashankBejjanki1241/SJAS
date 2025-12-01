"""
Analyzer & Writer Agent
Analyzes resume-job match and generates writing outputs.
"""

import re
from core.utils import normalize_skills, count_words, validate_word_count
from core.schema_validator import validate_final_output_schema, SchemaValidationError
from core.adk_integration import llm_call, llm_call_integer


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
    # Calculate hard skill overlap
    skill_overlap_ratio = _calculate_skill_overlap(resume_json, job_json)
    
    # Get experience score (integer-only, 0-10)
    experience_score = _get_experience_score(resume_json, job_json)
    
    # Calculate education match
    edu_match = _check_education_match(resume_json)
    
    # Calculate final score
    final_score = _calculate_final_score(skill_overlap_ratio, experience_score, edu_match)
    
    # Identify missing skills
    missing_skills = _identify_missing_skills(resume_json, job_json)
    
    # Generate strengths
    strengths = _generate_strengths(resume_json, job_json, skill_overlap_ratio)
    
    # Generate how to improve
    how_to_improve = _generate_how_to_improve(missing_skills, skill_overlap_ratio)
    
    # Generate writing outputs
    optimized_summary = _generate_summary(resume_json, job_json, final_score)
    cover_letter = _generate_cover_letter(resume_json, job_json, final_score)
    recruiter_message = _generate_recruiter_message(resume_json, job_json, final_score)
    
    # Post-validate word counts
    cover_letter = _validate_cover_letter_word_count(cover_letter)
    recruiter_message = _validate_recruiter_message(recruiter_message)
    optimized_summary = _validate_summary(optimized_summary)
    
    # Build result
    result = {
        "match_score": final_score,
        "score_breakdown": _generate_score_breakdown(skill_overlap_ratio, experience_score, edu_match),
        "missing_skills": missing_skills,
        "strengths": strengths,
        "how_to_improve": how_to_improve,
        "optimized_summary": optimized_summary,
        "cover_letter": cover_letter,
        "recruiter_message": recruiter_message,
        "job_title": job_json.get("job_title", ""),
        "company": job_json.get("company", ""),
        "job_url": job_json.get("job_url", ""),
        "_debug": {
            "skill_overlap_ratio": skill_overlap_ratio,
            "experience_score": experience_score,
            "edu_match": edu_match
        }
    }
    
    # Validate schema
    try:
        validate_final_output_schema(result)
    except SchemaValidationError:
        # Return minimal valid structure if validation fails
        return {
            "match_score": final_score,
            "score_breakdown": "",
            "missing_skills": [],
            "strengths": [],
            "how_to_improve": [],
            "optimized_summary": "",
            "cover_letter": "",
            "recruiter_message": "",
            "job_title": job_json.get("job_title", ""),
            "company": job_json.get("company", ""),
            "job_url": job_json.get("job_url", ""),
            "_debug": {}
        }
    
    return result


def _calculate_skill_overlap(resume_json: dict, job_json: dict) -> float:
    """
    Calculate hard skill overlap ratio.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        
    Returns:
        Skill overlap ratio (0.0 to 1.0)
    """
    resume_skills = set(normalize_skills(resume_json.get("skills", [])))
    job_skills = set(normalize_skills(job_json.get("skills", [])))
    
    if not job_skills:
        return 0.0
    
    overlap = len(resume_skills.intersection(job_skills))
    return overlap / len(job_skills)


def _get_experience_score(resume_json: dict, job_json: dict) -> int:
    """
    Get experience score using bulletproof prompt (integer-only, 0-10).
    
    This is an ADK integration point. Replace with actual LLM call.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        
    Returns:
        Integer score from 0 to 10
    """
    # Build prompt
    responsibilities = "\n".join(job_json.get("responsibilities", []))
    exp_points = []
    for job in resume_json.get("work_history", []):
        exp_points.extend(job.get("points", []))
    candidate_experience = "\n".join(exp_points)
    
    prompt = (
        "On a scale from 0 to 10, where 0 means no relevant experience and 10 means perfect match, "
        "how well does the candidate's experience match the job responsibilities below? "
        "Answer with a single number only, no explanation.\n\n"
        f"Responsibilities: {responsibilities}\n\n"
        f"Candidate experience: {candidate_experience}"
    )
    
    # Call ADK LLM and extract integer score
    score = llm_call_integer(prompt, min_value=0, max_value=10)
    return score


def _check_education_match(resume_json: dict) -> bool:
    """
    Check if resume contains education keywords.
    
    Args:
        resume_json: Parsed resume JSON
        
    Returns:
        True if resume contains bachelor/master/b.s./m.s., False otherwise
    """
    education_text = " ".join(resume_json.get("education", [])).lower()
    keywords = ["bachelor", "master", "b.s.", "m.s.", "bs", "ms", "ba", "ma"]
    
    return any(keyword in education_text for keyword in keywords)


def _calculate_final_score(skill_overlap_ratio: float, experience_score: int, edu_match: bool) -> int:
    """
    Calculate final match score.
    
    Formula:
        final_score = round(
            40 * (skill_overlap_ratio) +
            40 * (experience_score / 10) +
            20 * (edu_match ? 1 : 0.6)
        )
    
    Args:
        skill_overlap_ratio: Skill overlap ratio (0.0 to 1.0)
        experience_score: Experience score (0 to 10)
        edu_match: Education match boolean
        
    Returns:
        Final score (0 to 100)
    """
    skill_component = 40 * skill_overlap_ratio
    experience_component = 40 * (experience_score / 10)
    education_component = 20 * (1.0 if edu_match else 0.6)
    
    final_score = round(skill_component + experience_component + education_component)
    return max(0, min(100, final_score))  # Clamp to 0-100


def _identify_missing_skills(resume_json: dict, job_json: dict) -> list[str]:
    """
    Identify missing hard skills.
    
    Only includes hard skills that appear >=2 times OR contain "required/must have/experience with".
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        
    Returns:
        List of missing hard skills
    """
    resume_skills = set(normalize_skills(resume_json.get("skills", [])))
    job_skills_text = " ".join(job_json.get("skills", [])).lower()
    job_responsibilities = " ".join(job_json.get("responsibilities", [])).lower()
    full_job_text = (job_skills_text + " " + job_responsibilities).lower()
    
    missing = []
    
    # Get all job skills
    job_skills = set(normalize_skills(job_json.get("skills", [])))
    
    for skill in job_skills:
        if skill in resume_skills:
            continue  # Skill is present
        
        # Count occurrences in job description
        count = full_job_text.count(skill.lower())
        
        # Check if in required/must have context
        pattern = rf'(?:required|must have|experience with|need).*?{re.escape(skill)}'
        is_required = bool(re.search(pattern, full_job_text, re.IGNORECASE))
        
        if count >= 2 or is_required:
            missing.append(skill)
    
    return missing


def _generate_strengths(resume_json: dict, job_json: dict, skill_overlap: float) -> list[str]:
    """Generate strengths list."""
    strengths = []
    
    # Skill match strength
    if skill_overlap >= 0.7:
        strengths.append("Strong technical skill alignment with job requirements")
    elif skill_overlap >= 0.4:
        strengths.append("Good technical skill foundation")
    
    # Experience strength
    years_exp = resume_json.get("years_of_experience", 0)
    if years_exp >= 5:
        strengths.append("Extensive professional experience")
    elif years_exp >= 2:
        strengths.append("Relevant work experience")
    
    # Education strength
    if _check_education_match(resume_json):
        strengths.append("Relevant educational background")
    
    return strengths if strengths else ["Strong foundation for growth"]


def _generate_how_to_improve(missing_skills: list[str], skill_overlap: float) -> list[str]:
    """Generate how to improve suggestions."""
    suggestions = []
    
    if missing_skills:
        top_missing = missing_skills[:3]
        suggestions.append(f"Consider learning or highlighting: {', '.join(top_missing)}")
    
    if skill_overlap < 0.5:
        suggestions.append("Focus on developing skills mentioned in the job description")
    
    return suggestions if suggestions else ["Continue building relevant experience"]


def _generate_summary(resume_json: dict, job_json: dict, score: int) -> str:
    """
    Generate optimized summary (2-3 sentences).
    
    Uses ADK integration for LLM calls.
    """
    name = resume_json.get("name", "Candidate")
    years_exp = resume_json.get("years_of_experience", 0)
    current_title = resume_json.get("current_title", "")
    job_title = job_json.get("job_title", "this position")
    company = job_json.get("company", "the company")
    
    prompt = (
        f"Write a 2-3 sentence professional summary for a job application. "
        f"Candidate: {name}, {years_exp} years of experience as {current_title}. "
        f"Applying for: {job_title} at {company}. "
        f"Match score: {score}%. "
        f"Keep it concise, professional, and exactly 2-3 sentences. "
        f"Highlight relevant experience and alignment with the role."
    )
    
    summary = llm_call(prompt)
    return summary


def _generate_cover_letter(resume_json: dict, job_json: dict, score: int) -> str:
    """
    Generate cover letter (280-320 words, last sentence = CTA, never >340).
    
    Uses ADK integration for LLM calls.
    """
    name = resume_json.get("name", "Candidate")
    years_exp = resume_json.get("years_of_experience", 0)
    current_title = resume_json.get("current_title", "")
    skills = ", ".join(resume_json.get("skills", [])[:5])
    job_title = job_json.get("job_title", "this position")
    company = job_json.get("company", "the company")
    responsibilities = "\n".join(job_json.get("responsibilities", [])[:3])
    
    prompt = (
        f"Write a professional cover letter (280-320 words, never exceed 340 words) for a job application. "
        f"Candidate: {name}, {years_exp} years of experience as {current_title}. "
        f"Key skills: {skills}. "
        f"Applying for: {job_title} at {company}. "
        f"Job responsibilities include: {responsibilities}. "
        f"Match score: {score}%. "
        f"Requirements: "
        f"- Exactly 280-320 words (strictly enforce, never exceed 340 words). "
        f"- Professional tone. "
        f"- Highlight relevant experience and skills. "
        f"- Last sentence must be a clear call to action (CTA). "
        f"- Do not include markdown formatting or HTML tags."
    )
    
    cover_letter = llm_call(prompt)
    # Post-validate word count
    return _validate_cover_letter_word_count(cover_letter)


def _generate_recruiter_message(resume_json: dict, job_json: dict, score: int) -> str:
    """
    Generate recruiter message (1-2 sentences).
    
    Uses ADK integration for LLM calls.
    """
    name = resume_json.get("name", "Candidate")
    current_title = resume_json.get("current_title", "")
    job_title = job_json.get("job_title", "this position")
    company = job_json.get("company", "the company")
    
    prompt = (
        f"Write a brief, professional recruiter message (exactly 1-2 sentences) for a LinkedIn message or email. "
        f"Candidate: {name}, currently {current_title}. "
        f"Interested in: {job_title} at {company}. "
        f"Keep it concise, professional, and engaging. "
        f"Maximum 2 sentences."
    )
    
    message = llm_call(prompt)
    return message


def _validate_cover_letter_word_count(cover_letter: str) -> str:
    """
    Validate and adjust cover letter word count (280-320 words, never >340).
    
    Args:
        cover_letter: Cover letter text
        
    Returns:
        Validated cover letter within word limits
    """
    word_count = count_words(cover_letter)
    
    if word_count > 340:
        # Truncate to 320 words
        words = cover_letter.split()
        words = words[:320]
        cover_letter = " ".join(words)
        # Ensure it ends with a sentence
        if not cover_letter.rstrip().endswith(('.', '!', '?')):
            cover_letter += "."
    elif word_count < 280:
        # Note: In production, would regenerate or expand
        # For now, return as-is (LLM should generate proper length)
        pass
    
    return cover_letter


def _validate_recruiter_message(message: str) -> str:
    """
    Validate recruiter message (1-2 sentences).
    
    Args:
        message: Recruiter message text
        
    Returns:
        Validated message (max 2 sentences)
    """
    sentences = re.split(r'[.!?]+', message)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) > 2:
        return ". ".join(sentences[:2]) + "."
    
    return message


def _validate_summary(summary: str) -> str:
    """
    Validate summary (2-3 sentences).
    
    Args:
        summary: Summary text
        
    Returns:
        Validated summary (max 3 sentences)
    """
    sentences = re.split(r'[.!?]+', summary)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) > 3:
        return ". ".join(sentences[:3]) + "."
    
    return summary


def _generate_score_breakdown(skill_overlap: float, experience_score: int, edu_match: bool) -> str:
    """Generate human-readable score breakdown."""
    skill_pct = int(skill_overlap * 100)
    edu_status = "Match" if edu_match else "Partial"
    
    return f"Skills {skill_pct}% · Experience {experience_score}/10 · Education {edu_status}"
