"""
ADK Integration Module
Provides wrappers for ADK (Agents Development Kit) functions.
"""

import json
import re
from typing import Optional


# Try to import Google Generative AI SDK (used by ADK)
# This allows direct LLM calls from within ADK tools
try:
    import google.generativeai as genai
    import os
    from dotenv import load_dotenv
    
    # Load .env to get API key
    load_dotenv()
    
    # Initialize genai with API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        ADK_AVAILABLE = True
    else:
        ADK_AVAILABLE = False
except ImportError:
    ADK_AVAILABLE = False


def llm_call(prompt: str, response_format: Optional[str] = None, **kwargs) -> str:
    """
    Call Google Generative AI LLM with a prompt.
    
    Uses the same SDK that ADK uses, allowing direct LLM calls from within ADK tools.
    
    Args:
        prompt: The prompt to send to the LLM
        response_format: Optional format hint ("json", "text", etc.) - currently unused
        **kwargs: Additional arguments (model, temperature, etc.)
        
    Returns:
        LLM response as string
        
    Raises:
        NotImplementedError: If Google Generative AI SDK is not available
        Exception: If LLM call fails
    """
    if not ADK_AVAILABLE:
        raise NotImplementedError(
            "Google Generative AI SDK is not available. Please install google-generativeai and set GOOGLE_API_KEY in .env"
        )
    
    # Get model from kwargs or use default
    model_name = kwargs.get("model", os.getenv("ADK_MODEL", "gemini-2.5-flash-lite"))
    
    # Create model instance
    model = genai.GenerativeModel(model_name)
    
    # Generate content
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"LLM call failed: {str(e)}")


def browse_page(url: str, **kwargs) -> str:
    """
    Browse a page using ADK browse_page tool.
    
    Args:
        url: URL to browse
        **kwargs: Additional arguments for browse_page
        
    Returns:
        Page content as string
        
    Raises:
        NotImplementedError: If ADK is not available
        Exception: If browse_page fails
    """
    if not ADK_AVAILABLE:
        raise NotImplementedError(
            "ADK is not available. Please install ADK and set ADK_AVAILABLE = True in core/adk_integration.py"
        )
    
    # Call actual ADK browse_page
    # page_content = _adk_browse_page(url, **kwargs)
    # return page_content
    
    # Placeholder - replace with actual ADK call when available
    raise NotImplementedError(
        "ADK browse_page integration not yet configured. "
        "Uncomment ADK imports and set ADK_AVAILABLE = True in core/adk_integration.py"
    )


def llm_call_json(prompt: str, **kwargs) -> dict:
    """
    Call ADK LLM and parse JSON response.
    
    Args:
        prompt: The prompt to send to the LLM
        **kwargs: Additional arguments for ADK LLM call
        
    Returns:
        Parsed JSON as dictionary
        
    Raises:
        NotImplementedError: If ADK is not available
        json.JSONDecodeError: If response is not valid JSON
        Exception: If LLM call fails
    """
    response = llm_call(prompt, response_format="json", **kwargs)
    
    # Try to parse JSON
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Sometimes LLM returns JSON wrapped in markdown code blocks
        # Try to extract JSON from markdown
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to find JSON object in response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        
        raise json.JSONDecodeError(f"Could not parse JSON from LLM response: {response[:200]}", response, 0)


def llm_call_integer(prompt: str, min_value: int = 0, max_value: int = 10, **kwargs) -> int:
    """
    Call ADK LLM and extract integer from response.
    
    Args:
        prompt: The prompt to send to the LLM
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        **kwargs: Additional arguments for ADK LLM call
        
    Returns:
        Integer extracted from response (clamped to min_value-max_value range)
        
    Raises:
        NotImplementedError: If ADK is not available
        ValueError: If no integer found in response
        Exception: If LLM call fails
    """
    response = llm_call(prompt, **kwargs)
    
    # Extract integer from response
    match = re.search(r'\d+', response)
    if not match:
        raise ValueError(f"No integer found in LLM response: {response[:200]}")
    
    score = int(match.group())
    # Clamp to valid range
    return max(min_value, min(max_value, score))

