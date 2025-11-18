"""
Utility Functions
Helper functions for skill normalization, text cleanup, etc.
"""

def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize skills: tokenize, lowercase, deduplicate, limit to 10.
    
    Args:
        skills: Raw skill list
        
    Returns:
        Normalized skill list (max 10, deduplicated, lowercased)
        
    Example:
        ["React", "react", "React.js"] → ["react"]
    """
    # TODO: Implement skill normalization
    pass

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
    # TODO: Implement text preprocessing
    pass

def count_words(text: str) -> int:
    """
    Count words in text for validation.
    
    Args:
        text: Text to count
        
    Returns:
        Word count
    """
    return len(text.split())

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

