"""
Utility Functions
Helper functions for skill normalization, text cleanup, etc.
"""

import re
import unicodedata


def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize skills: tokenize, lowercase, deduplicate, limit to 10.
    
    Args:
        skills: Raw skill list
        
    Returns:
        Normalized skill list (max 10, deduplicated, lowercased)
        
    Example:
        ["React", "react", "React.js"] → ["react"]
        ["Node JS", "nodejs", "Node.js"] → ["nodejs"]
    """
    if not skills:
        return []
    
    normalized = []
    seen = set()
    
    for skill in skills:
        if not isinstance(skill, str):
            continue
        
        # Normalize: lowercase, strip whitespace
        skill_lower = skill.lower().strip()
        
        # Simplify common variations
        # Remove common suffixes/prefixes and normalize
        skill_normalized = re.sub(r'\.js$|\.jsx$', '', skill_lower)  # Remove .js, .jsx
        skill_normalized = re.sub(r'\s+', '', skill_normalized)  # Remove spaces (Node JS -> nodejs)
        skill_normalized = re.sub(r'[-_]', '', skill_normalized)  # Remove hyphens/underscores
        
        # Skip empty strings
        if not skill_normalized:
            continue
        
        # Deduplicate
        if skill_normalized not in seen:
            seen.add(skill_normalized)
            normalized.append(skill_normalized)
    
    # Limit to max 10 skills
    return normalized[:10]


def preprocess_resume_text(text: str) -> str:
    """
    Preprocess resume text before parsing.
    
    Args:
        text: Raw resume text
        
    Returns:
        Preprocessed text:
        - Normalize bullets
        - Strip unicode
        - Remove extra whitespace
        - Truncate to max 8000 characters
    """
    if not isinstance(text, str):
        return ""
    
    # Normalize unicode (remove special characters, normalize to ASCII where possible)
    # Keep basic unicode but normalize to NFKD form
    text = unicodedata.normalize('NFKD', text)
    
    # Normalize bullet points (•, -, *, etc. to a standard format)
    text = re.sub(r'^[\s]*[•\-\*\+]\s+', '- ', text, flags=re.MULTILINE)
    
    # Remove excessive whitespace (multiple spaces/tabs to single space)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Remove excessive newlines (more than 2 consecutive newlines to 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Truncate to max 8000 characters
    # Use meaningful truncation: always try to cut at word boundary
    if len(text) > 8000:
        # First, truncate to 8000 chars
        truncated = text[:8000]
        
        # Find the last space in the truncated text (word boundary)
        last_space = truncated.rfind(' ')
        last_newline = truncated.rfind('\n')
        
        # Prefer newline boundary (sentence/paragraph end), then space (word boundary)
        # Only use if it's reasonably close to 8000 (within last 200 chars) to avoid losing too much content
        truncate_at = max(last_newline, last_space)
        
        if truncate_at > 7800:  # If boundary is within last 200 chars, use it
            text = truncated[:truncate_at].rstrip()  # Remove trailing whitespace
        else:
            # No good boundary found, use blind truncate (should be rare)
            text = truncated
    
    return text


def count_words(text: str) -> int:
    """
    Count words in text for validation.
    
    Args:
        text: Text to count
        
    Returns:
        Word count
    """
    if not isinstance(text, str):
        return 0
    
    # Split by whitespace and filter empty strings
    words = [word for word in text.split() if word.strip()]
    return len(words)


def validate_word_count(text: str, min_words: int, max_words: int) -> bool:
    """
    Validate word count is within range.
    
    Args:
        text: Text to validate
        min_words: Minimum word count
        max_words: Maximum word count
        
    Returns:
        True if within range, False otherwise
    """
    word_count = count_words(text)
    return min_words <= word_count <= max_words
