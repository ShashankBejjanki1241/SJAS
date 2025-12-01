"""
ADK Agent Definitions
Defines all 4 agents using ADK's Agent class pattern.
"""

import os
import json
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required if env vars are set directly

# Try to import ADK - graceful fallback if not available
try:
    from google.adk.agents import Agent
    from google.adk.agents.sequential_agent import SequentialAgent
    from google.adk.tools.load_web_page import load_web_page
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    # Placeholder classes for when ADK is not installed
    class Agent:
        def __init__(self, **kwargs):
            pass
    class SequentialAgent:
        def __init__(self, **kwargs):
            pass
    def load_web_page(url: str) -> str:
        raise NotImplementedError("ADK not available")

# Import our utility functions to use as tools
from core.utils import preprocess_resume_text, normalize_skills, count_words, validate_word_count
from core.schema_validator import validate_resume_schema, validate_job_schema, validate_final_output_schema, strip_debug


# ADK Tools - Custom function tools for our agents

def preprocess_resume_tool(resume_text: str) -> str:
    """
    Preprocess resume text: normalize bullets, strip unicode, truncate to 8000 chars.
    
    Args:
        resume_text: Raw resume text
        
    Returns:
        Preprocessed resume text
    """
    return preprocess_resume_text(resume_text)


def normalize_skills_tool(skills: list[str]) -> list[str]:
    """
    Normalize skills: tokenize, lowercase, deduplicate, limit to 10.
    
    Args:
        skills: Raw skill list
        
    Returns:
        Normalized skill list (max 10, deduplicated, lowercased)
    """
    return normalize_skills(skills)


def validate_resume_schema_tool(data: dict) -> bool:
    """
    Validate resume JSON schema.
    
    Args:
        data: Resume JSON to validate
        
    Returns:
        True if valid, raises SchemaValidationError if invalid
    """
    from core.schema_validator import SchemaValidationError
    try:
        return validate_resume_schema(data)
    except Exception as e:
        raise SchemaValidationError(str(e))


def validate_job_schema_tool(data: dict) -> bool:
    """
    Validate job JSON schema.
    
    Args:
        data: Job JSON to validate
        
    Returns:
        True if valid, raises SchemaValidationError if invalid
    """
    from core.schema_validator import SchemaValidationError
    try:
        return validate_job_schema(data)
    except Exception as e:
        raise SchemaValidationError(str(e))


def validate_final_output_schema_tool(data: dict) -> bool:
    """
    Validate final output JSON schema.
    
    Args:
        data: Final output JSON to validate
        
    Returns:
        True if valid, raises SchemaValidationError if invalid
    """
    from core.schema_validator import SchemaValidationError
    try:
        return validate_final_output_schema(data)
    except Exception as e:
        raise SchemaValidationError(str(e))


def strip_debug_tool(data: dict) -> dict:
    """
    Remove _debug field from output before returning to user.
    
    Args:
        data: Output JSON with _debug field
        
    Returns:
        Output JSON without _debug field
    """
    return strip_debug(data)


def fallback_tool(error_type: str, error_message: str = "", context: str = "") -> dict:
    """
    Fallback handler tool - returns structured fallback JSON when errors occur.
    
    This tool can be called by agents when they encounter errors that should
    trigger a graceful fallback response instead of crashing the pipeline.
    
    Args:
        error_type: Type of error (e.g., "parser_error", "extraction_error", "timeout")
        error_message: Optional error message
        context: Optional context about where the error occurred
        
    Returns:
        Fallback JSON with score=82 and appropriate error information
    """
    from core.timeout_manager import get_fallback_json
    
    result = get_fallback_json()
    
    # Add error information to debug
    if "_debug" not in result:
        result["_debug"] = {}
    
    result["_debug"].update({
        "fallback_triggered": True,
        "error_type": error_type,
        "error_message": error_message,
        "error_context": context
    })
    
    # Update score_breakdown to indicate fallback
    result["score_breakdown"] = f"Fallback mode activated: {error_type}"
    if error_message:
        result["score_breakdown"] += f" - {error_message}"
    
    return result


# Get model from environment or use default
MODEL = os.getenv("ADK_MODEL", "gemini-2.5-flash-lite")


# Agent 1: Resume Parser Agent
resume_parser_agent = Agent(
    name="resume_parser",
    model=MODEL,
    description="Parses raw resume text into structured JSON following strict schema.",
    instruction=(
        "You are a resume parser. You MUST follow this exact workflow:\n\n"
        "STEP 1: Preprocess resume text\n"
        "- Use preprocess_resume_tool with the raw resume text\n"
        "- This normalizes bullets, strips unicode, and truncates to 8000 chars\n"
        "- Inform the user: 'Preprocessing resume text...'\n\n"
        "STEP 2: Parse into JSON structure\n"
        "- Inform the user: 'Parsing resume into structured format...'\n"
        "- Parse the preprocessed text into a JSON object with this EXACT structure (DO NOT use a tool for this, just generate the JSON):\n"
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
        '      "points": ["achievement1", "achievement2", ...] (max 4 points per job)\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "STEP 3: Normalize skills\n"
        "- Inform the user: 'Normalizing and deduplicating skills...'\n"
        "- Use normalize_skills_tool with the skills array from parsed JSON\n"
        "- This tokenizes, lowercases, deduplicates, and limits to 10 skills\n"
        "- Update the parsed JSON with normalized skills\n\n"
        "STEP 4: Limit work history points\n"
        "- Ensure each job in work_history has max 4 points\n"
        "- Truncate if necessary\n\n"
        "STEP 5: Validate schema\n"
        "- Use validate_resume_schema_tool with the final parsed JSON\n"
        "- If validation fails, use fallback_tool\n\n"
        "STEP 6: Return validated JSON\n"
        "- Return only valid JSON, no additional text\n\n"
        "CRITICAL: If parsing fails after retry, use fallback_tool to return a graceful error response. "
        "Do NOT return invalid JSON. Always validate before returning."
    ),
    tools=[
        preprocess_resume_tool,
        normalize_skills_tool,
        validate_resume_schema_tool,
        fallback_tool  # Fallback handler available
    ],
    output_key="parsed_resume"  # Store output in state
)


# Agent 2: Job Selector Agent (Deterministic - no LLM needed, but keeping as Agent for consistency)
# Note: This is actually deterministic logic, but we'll keep it as a simple agent
def select_job_tool(job_query: str, job_map_path: str = "resources/job_map.json") -> dict:
    """
    Select primary and backup job URLs based on query.
    
    Args:
        job_query: User job query (supports "DEMO:" prefix)
        job_map_path: Path to job_map.json file
        
    Returns:
        Dictionary with "primary_url" and "backup_url" keys
    """
    from agents.selector_agent import select_job, _load_job_map
    
    job_map = _load_job_map()
    primary_url, backup_url = select_job(job_query, job_map)
    
    return {
        "primary_url": primary_url,
        "backup_url": backup_url
    }


def infer_job_category_from_resume_tool(parsed_resume: dict) -> str:
    """
    Infer job category from parsed resume when query is vague or conversational.
    This makes the system smarter by using resume information.
    
    Args:
        parsed_resume: Parsed resume JSON from previous agent
        
    Returns:
        Inferred job category string (e.g., "data", "python", "backend")
    """
    from agents.selector_agent import infer_job_category_from_resume, _load_job_map
    
    job_map = _load_job_map()
    inferred_category = infer_job_category_from_resume(parsed_resume, job_map)
    
    if inferred_category:
        return inferred_category
    else:
        # Fallback to "default" if no category can be inferred
        return "default"


job_selector_agent = Agent(
    name="job_selector",
    model=MODEL,
    description="Intelligently selects job URL from pre-vetted job_map.json based on query or resume.",
    instruction=(
        "You are a job selector. You MUST follow this exact workflow:\n\n"
        "STEP 1: Extract job query from user input\n"
        "- The user query is provided in the input\n"
        "- Extract the job query string (1-6 words)\n"
        "- Inform the user: 'Analyzing job query...'\n"
        "- If query is empty, vague, or conversational (e.g., 'I need help finding a job'), "
        "inform the user: 'Query is vague, will infer job category from resume' and proceed to STEP 2B\n\n"
        "STEP 2A: Select job URLs from query (if query is specific)\n"
        "- Inform the user: 'Selecting job based on query...'\n"
        "- Use select_job_tool with the job query\n"
        "- This tool handles:\n"
        "  * DEMO mode: If query starts with 'DEMO:', returns default job\n"
        "  * Exact match: Matches exact category in job_map.json\n"
        "  * Fuzzy match: Matches via tags field (enhanced with semantic matching)\n"
        "  * Fallback: If no match, proceed to STEP 2B\n"
        "- The tool returns a dictionary with 'primary_url' and 'backup_url'\n\n"
        "STEP 2B: Infer job category from resume (if query is vague/empty/no match)\n"
        "- Inform the user: 'Inferring job category from your resume (skills, title, experience)...'\n"
        "- Access the parsed_resume from the previous agent's output\n"
        "- Use infer_job_category_from_resume_tool with the parsed_resume\n"
        "- Inform the user of the inferred category: 'Detected [category] category based on your background'\n"
        "- This tool analyzes:\n"
        "  * Current title (e.g., 'Data Engineer' → 'data' category)\n"
        "  * Skills (e.g., 'hadoop', 'spark' → 'data' category)\n"
        "  * Work history roles (e.g., 'Data Engineer' → 'data' category)\n"
        "- The tool returns an inferred category (e.g., 'data', 'python', 'backend')\n"
        "- Then use select_job_tool with the inferred category\n\n"
        "STEP 3: Return selected URLs\n"
        "- Return the dictionary with primary_url and backup_url\n"
        "- Format: {\"primary_url\": \"...\", \"backup_url\": \"...\"}\n\n"
        "CRITICAL: This is intelligent logic - use resume information when query is vague. "
        "If selection fails (tool returns empty URLs), use fallback_tool to return a graceful error response."
    ),
    tools=[select_job_tool, infer_job_category_from_resume_tool, fallback_tool],  # Added inference tool
    output_key="selected_job_urls"
)


# Agent 3: Job Extractor Agent
def extract_job_tool(job_url: str, backup_url: Optional[str] = None) -> dict:
    """
    Extract job information from ATS page using browse_page.
    
    Args:
        job_url: Primary job URL (Lever/Greenhouse/AshbyHQ/Workable only)
        backup_url: Backup job URL if primary fails
        
    Returns:
        Extracted job JSON with job_title, company, skills, responsibilities, experience_level, job_url
    """
    from agents.extractor_agent import extract_job
    return extract_job(job_url, backup_url)


job_extractor_agent = Agent(
    name="job_extractor",
    model=MODEL,
    description="Extracts job information from ATS pages (Lever, Greenhouse, AshbyHQ, Workable).",
    instruction=(
        "You are a job extractor. You MUST follow this exact workflow:\n\n"
        "STEP 1: Get job URLs from previous agent\n"
        "- Access the selected_job_urls from the previous agent's output\n"
        "- Extract primary_url and backup_url\n\n"
        "STEP 2: Extract job information\n"
        "- Inform the user: 'Extracting job details from ATS page...'\n"
        "- Use extract_job_tool with primary_url and backup_url\n"
        "- This tool:\n"
        "  * Tries primary_url first (if allowed domain: lever.co, greenhouse.io, ashbyhq.com, workable.com)\n"
        "  * Falls back to backup_url if primary fails\n"
        "  * Falls back to default Vercel job if both fail\n"
        "  * Uses load_web_page internally to fetch page content\n"
        "  * Extracts: job_title, company, skills (hard skills only, max 10), "
        "responsibilities (max 6), experience_level, job_url\n\n"
        "STEP 3: Validate extracted job\n"
        "- Use validate_job_schema_tool with the extracted job JSON\n"
        "- If validation fails, the tool returns minimal valid structure\n\n"
        "STEP 4: Return extracted job JSON\n"
        "- Return the validated job JSON with all required fields:\n"
        "  - job_title: string\n"
        "  - company: string\n"
        "  - skills: list of strings (max 10, hard skills only)\n"
        "  - responsibilities: list of strings (max 6)\n"
        "  - experience_level: string\n"
        "  - job_url: string\n\n"
        "CRITICAL: The extract_job_tool handles all extraction logic including fallbacks. "
        "If extraction fails completely (tool returns empty/invalid data), use fallback_tool to return a graceful error response."
    ),
    tools=[extract_job_tool, load_web_page, validate_job_schema_tool, fallback_tool],  # Fallback handler available
    output_key="extracted_job"
)


# Agent 4: Analyzer & Writer Agent
def calculate_skill_overlap_tool(resume_skills: list[str], job_skills: list[str]) -> float:
    """
    Calculate hard skill overlap ratio between resume and job.
    
    Args:
        resume_skills: List of skills from resume
        job_skills: List of skills from job
        
    Returns:
        Skill overlap ratio (0.0 to 1.0)
    """
    from agents.analyzer_writer_agent import _calculate_skill_overlap
    
    resume_json = {"skills": resume_skills}
    job_json = {"skills": job_skills}
    return _calculate_skill_overlap(resume_json, job_json)


def check_education_match_tool(education: list[str]) -> bool:
    """
    Check if education contains bachelor/master/b.s./m.s. keywords.
    
    Args:
        education: List of education entries
        
    Returns:
        True if contains degree keywords, False otherwise
    """
    from agents.analyzer_writer_agent import _check_education_match
    resume_json = {"education": education}
    return _check_education_match(resume_json)


def calculate_final_score_tool(skill_overlap: float, experience_score: int, edu_match: bool) -> int:
    """
    Calculate final match score using formula: 40% skills + 40% experience + 20% education.
    
    Args:
        skill_overlap: Skill overlap ratio (0.0 to 1.0)
        experience_score: Experience score (0 to 10)
        edu_match: Education match boolean
        
    Returns:
        Final score (0 to 100)
    """
    from agents.analyzer_writer_agent import _calculate_final_score
    return _calculate_final_score(skill_overlap, experience_score, edu_match)


def validate_word_count_tool(text: str, min_words: int, max_words: int) -> bool:
    """
    Validate word count is within range.
    
    Args:
        text: Text to validate
        min_words: Minimum word count
        max_words: Maximum word count
        
    Returns:
        True if within range, False otherwise
    """
    return validate_word_count(text, min_words, max_words)


def get_experience_score_tool(resume_json: dict, job_json: dict) -> int:
    """
    Get experience score (0-10 integer) by comparing resume work history with job responsibilities.
    
    Uses LLM to score experience match. This is an ADK integration point.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        
    Returns:
        Integer score from 0 to 10
    """
    from agents.analyzer_writer_agent import _get_experience_score
    return _get_experience_score(resume_json, job_json)


def generate_summary_tool(resume_json: dict, job_json: dict, score: int) -> str:
    """
    Generate optimized summary (2-3 sentences).
    
    Uses LLM to generate professional summary. This is an ADK integration point.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        score: Match score (0-100)
        
    Returns:
        Summary text (2-3 sentences)
    """
    from agents.analyzer_writer_agent import _generate_summary
    return _generate_summary(resume_json, job_json, score)


def generate_cover_letter_tool(resume_json: dict, job_json: dict, score: int) -> str:
    """
    Generate cover letter (280-320 words, last sentence = CTA, never >340).
    
    Uses LLM to generate professional cover letter. This is an ADK integration point.
    Post-validates word count to ensure it's within limits.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        score: Match score (0-100)
        
    Returns:
        Cover letter text (280-320 words, validated)
    """
    from agents.analyzer_writer_agent import _generate_cover_letter
    return _generate_cover_letter(resume_json, job_json, score)


def generate_recruiter_message_tool(resume_json: dict, job_json: dict, score: int) -> str:
    """
    Generate recruiter message (1-2 sentences).
    
    Uses LLM to generate concise recruiter message. This is an ADK integration point.
    Post-validates to ensure it's 1-2 sentences.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        score: Match score (0-100)
        
    Returns:
        Recruiter message text (1-2 sentences, validated)
    """
    from agents.analyzer_writer_agent import _generate_recruiter_message
    return _generate_recruiter_message(resume_json, job_json, score)


def identify_missing_skills_tool(resume_json: dict, job_json: dict) -> list[str]:
    """
    Identify missing hard skills (skills appearing >=2 times OR containing 'required/must have/experience with').
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        
    Returns:
        List of missing hard skills
    """
    from agents.analyzer_writer_agent import _identify_missing_skills
    return _identify_missing_skills(resume_json, job_json)


def generate_strengths_tool(resume_json: dict, job_json: dict, skill_overlap: float) -> list[str]:
    """
    Generate strengths list based on resume-job match.
    
    Args:
        resume_json: Parsed resume JSON
        job_json: Extracted job JSON
        skill_overlap: Skill overlap ratio (0.0 to 1.0)
        
    Returns:
        List of strength strings
    """
    from agents.analyzer_writer_agent import _generate_strengths
    return _generate_strengths(resume_json, job_json, skill_overlap)


def generate_how_to_improve_tool(missing_skills: list[str], skill_overlap: float) -> list[str]:
    """
    Generate how to improve suggestions.
    
    Args:
        missing_skills: List of missing skills
        skill_overlap: Skill overlap ratio (0.0 to 1.0)
        
    Returns:
        List of improvement suggestions
    """
    from agents.analyzer_writer_agent import _generate_how_to_improve
    return _generate_how_to_improve(missing_skills, skill_overlap)


analyzer_writer_agent = Agent(
    name="analyzer_writer",
    model=MODEL,
    description="Analyzes resume-job match and generates writing outputs (summary, cover letter, recruiter message).",
    instruction=(
        "You are an analyzer and writer. You MUST follow this exact workflow and at the end return ONLY the FINAL OUTPUT JSON (no other JSON objects, no explanations, no extra text):\n\n"
        "WRITING STYLE RULES (ALWAYS APPLY THESE WHEN WRITING OR SUGGESTING BULLETS):\n"
        "- Start every bullet with a strong action verb (Built, Led, Delivered, Improved), NOT with 'I' or 'I was responsible for'.\n"
        "- When you see phrases like 'I was responsible for...', 'I worked on...', 'I helped with...', rewrite them to start directly with the verb.\n"
        "  * Example: 'I was responsible for developing and implementing a new automated testing framework using Selenium and Java which reduced manual testing efforts by 80%'\n"
        "    → 'Built Selenium + Java automation framework → cut manual testing 80%'.\n"
        "- Compress long phrases into tight, impact-focused lines:\n"
        "  * 'Successfully led a team of 10 members...' → 'Led 10-member team...'\n"
        "  * 'Responsible for the development of...' → 'Developed...'\n"
        "  * 'Played a key role in increasing sales by 30%...' → 'Boosted sales 30%...'\n"
        "  * 'Worked on various projects involving Java, Spring...' → 'Java, Spring Boot, Microservices' (in skills or a short bullet).\n"
        "- Remove filler words: 'successfully', 'various', 'effectively', 'utilizing', 'assisted', 'helped', 'responsible for', etc.\n"
        "- Keep impact metrics (%, revenue, time saved, defects reduced) and make them prominent: 'cut manual testing 80%', 'reduced defects 25%', 'increased conversions 15%'.\n"
        "- Prefer short, punchy bullets over long sentences. If a bullet is longer than ~25 words, look for ways to:\n"
        "  * Drop setup phrases (e.g., 'In this role, I was responsible for...').\n"
        "  * Replace clauses with concise arrows or separators (e.g., '→' or ' - ').\n"
        "These style rules apply especially to any example bullets or rewrite suggestions you provide in strengths/how_to_improve.\n\n"
        "STEP 1: Calculate skill overlap\n"
        "- Inform the user: 'Calculating skill match between your resume and job requirements...'\n"
        "- Use calculate_skill_overlap_tool with resume_skills and job_skills\n"
        "- This returns a ratio (0.0 to 1.0)\n"
        "- Inform the user of the skill overlap ratio: 'Skill match: [ratio]%'\n\n"
        "STEP 2: Get experience score\n"
        "- Inform the user: 'Evaluating your experience against job requirements...'\n"
        "- Use get_experience_score_tool with resume_json and job_json\n"
        "- This returns an integer score (0 to 10)\n"
        "- Inform the user of the experience score: 'Experience match: [score]/10'\n\n"
        "STEP 3: Check education match\n"
        "- Inform the user: 'Checking education requirements...'\n"
        "- Use check_education_match_tool with education list from resume\n"
        "- This returns True/False\n\n"
        "STEP 4: Calculate final score\n"
        "- Inform the user: 'Calculating overall match score...'\n"
        "- Use calculate_final_score_tool with skill_overlap, experience_score, and edu_match\n"
        "- This returns final score (0 to 100)\n"
        "- Inform the user: 'Overall match score: [score]/100'\n\n"
        "STEP 5: Identify missing skills\n"
        "- Inform the user: 'Identifying skills to develop...'\n"
        "- Use identify_missing_skills_tool with resume_json and job_json\n"
        "- This returns list of missing hard skills\n\n"
        "STEP 6: Generate strengths\n"
        "- Inform the user: 'Analyzing your strengths for this role...'\n"
        "- Use generate_strengths_tool with resume_json, job_json, and skill_overlap\n"
        "- This returns list of strength strings\n\n"
        "STEP 7: Generate how to improve\n"
        "- Inform the user: 'Preparing improvement suggestions...'\n"
        "- Use generate_how_to_improve_tool with missing_skills and skill_overlap\n"
        "- This returns list of improvement suggestions\n\n"
        "STEP 8: Generate writing outputs\n"
        "- Inform the user: 'Generating tailored cover letter and summary...'\n"
        "- Use generate_summary_tool with resume_json, job_json, and final_score\n"
        "- Use generate_cover_letter_tool with resume_json, job_json, and final_score\n"
        "- Use generate_recruiter_message_tool with resume_json, job_json, and final_score\n"
        "- Validate word counts: summary (2-3 sentences), cover letter (280-320 words, never >340), recruiter message (1-2 sentences)\n"
        "- Inform the user: 'Writing outputs generated and validated'\n\n"
        "STEP 9: Build final output JSON\n"
        "- Construct JSON with all required fields:\n"
        "  - match_score: final_score\n"
        "  - score_breakdown: descriptive text\n"
        "  - missing_skills: from identify_missing_skills_tool\n"
        "  - strengths: from generate_strengths_tool\n"
        "  - how_to_improve: from generate_how_to_improve_tool\n"
        "  - optimized_summary: from generate_summary_tool\n"
        "  - cover_letter: from generate_cover_letter_tool\n"
        "  - recruiter_message: from generate_recruiter_message_tool\n"
        "  - job_title, company, job_url: from job_json\n"
        "  - _debug: {skill_overlap_ratio, experience_score, edu_match}\n\n"
        "STEP 10: Validate and return\n"
        "- Use validate_final_output_schema_tool to validate the JSON\n"
        "- The final JSON MUST match this shape exactly (Final Output JSON Schema), with no extra keys:\n"
        "  {\n"
        '    \"match_score\": null or integer,\n'
        '    \"score_breakdown\": \"\",\n'
        '    \"missing_skills\": [],\n'
        '    \"strengths\": [],\n'
        '    \"how_to_improve\": [],\n'
        '    \"optimized_summary\": \"\",\n'
        '    \"cover_letter\": \"\",\n'
        '    \"recruiter_message\": \"\",\n'
        '    \"job_title\": \"\",\n'
        '    \"company\": \"\",\n'
        '    \"job_url\": \"\",\n'
        '    \"_debug\": {}\n'
        "  }\n"
        "- Return ONLY this validated JSON object as your final answer. Do NOT return intermediate tool results such as {\"primary_url\": ..., \"backup_url\": ...}.\n\n"
        "CRITICAL: If any step fails, use fallback_tool to return a graceful error response. "
        "Do NOT skip steps. Follow the workflow in order. Your final answer must always be exactly one JSON object matching the Final Output JSON Schema."
    ),
    tools=[
        calculate_skill_overlap_tool,
        get_experience_score_tool,
        check_education_match_tool,
        calculate_final_score_tool,
        identify_missing_skills_tool,
        generate_strengths_tool,
        generate_how_to_improve_tool,
        generate_summary_tool,
        generate_cover_letter_tool,
        generate_recruiter_message_tool,
        validate_word_count_tool,
        validate_final_output_schema_tool,
        strip_debug_tool,
        fallback_tool  # Fallback handler available
    ],
    output_key="final_output"
)


# Root Agent: Sequential Pipeline
# Note: SequentialAgent stops on error by default (fail-fast behavior)
# If any agent fails, the entire pipeline stops immediately
# This prevents cascading failures and junk state propagation
# The fallback_tool is available to each sub-agent as a rescue mechanism
# Memory is enabled via MemoryService in the Runner (see adk_pipeline.py)
# This provides scratch memory, context accumulation, and state tracking for debugging
root_agent = SequentialAgent(
    name="job_match_pipeline",
    description="4-agent pipeline for resume parsing, job selection, extraction, analysis, and writing.",
    sub_agents=[
        resume_parser_agent,      # Has fallback_tool available
        job_selector_agent,        # Has fallback_tool available
        job_extractor_agent,       # Has fallback_tool available
        analyzer_writer_agent      # Has fallback_tool available
    ]
)

