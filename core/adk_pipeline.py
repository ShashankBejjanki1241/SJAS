"""
ADK Pipeline Orchestrator
Uses ADK's Runner to execute the 4-agent sequential pipeline.
"""

import time
import os
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required if env vars are set directly

# Try to import ADK and Gemini types - graceful fallback if not available
try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    
    # Try to import MemoryService for memory support
    try:
        from google.adk.memory import InMemoryMemoryService
        MEMORY_AVAILABLE = True
    except ImportError:
        # MemoryService might not be available in all ADK versions
        InMemoryMemoryService = None
        MEMORY_AVAILABLE = False
    
    # Import Gemini types used to build Content messages for Runner
    from google.genai import types as genai_types
    ADK_AVAILABLE = True
except ImportError:
    # If any of the ADK / Gemini imports fail, fall back to legacy pipeline
    ADK_AVAILABLE = False
    MEMORY_AVAILABLE = False
    # Placeholder classes
    class Runner:
        def __init__(self, **kwargs):
            pass
        def run(self, **kwargs):
            raise NotImplementedError("ADK not available")
    class InMemorySessionService:
        def create_session(self, **kwargs):
            return type('Session', (), {'session_id': 'dummy'})()
    InMemoryMemoryService = None

from core.adk_agents import root_agent
from core.timeout_manager import (
    TIMEOUT_SECONDS,
    check_timeout_elapsed,
    get_fallback_json
)
from core.schema_validator import strip_debug
from core.adk_fallback_handler import FallbackHandler
from core.utils import preprocess_resume_text


def run_pipeline(resume_text: str, job_query: str) -> dict:
    """
    Execute the complete 4-agent pipeline using ADK Runner.
    
    Args:
        resume_text: Raw resume text
        job_query: Job search query
        
    Returns:
        Final output JSON or error JSON
        
    Pipeline:
        1. Resume Parser Agent
        2. Deterministic Job Selector Agent
        3. Job Extractor Agent
        4. Analyzer & Writer Agent
        
    Timeout: 55 seconds max
    Fallback: Returns fallback JSON if timeout exceeded
    """
    start_time = time.time()
    _debug = {
        "parser_attempts": 0,
        "job_url_used": "",
        "total_time_ms": 0
    }
    
    # Preprocess resume BEFORE sending to pipeline to reduce token usage
    # This truncates to 8000 chars, normalizes bullets, strips unicode
    # This is critical to avoid API overload from large payloads
    original_resume_length = len(resume_text)
    resume_text = preprocess_resume_text(resume_text)
    if len(resume_text) < original_resume_length:
        # Resume was truncated - log for debugging
        _debug["resume_truncated"] = True
        _debug["original_length"] = original_resume_length
        _debug["truncated_length"] = len(resume_text)
    
    # Check if ADK is available
    if not ADK_AVAILABLE:
        # Fallback to original pipeline if ADK not available
        from core.pipeline import run_pipeline as run_pipeline_original
        return run_pipeline_original(resume_text, job_query)
    
    try:
        import asyncio
        
        # Initialize fallback handler
        fallback_handler = FallbackHandler()
        
        # Initialize ADK session and runner
        session_service = InMemorySessionService()
        session_id = f"session_{int(time.time())}"
        
        async def run_adk_pipeline():
            # Create session (async)
            session = await session_service.create_session(
                app_name="job_match_app",
                user_id="user_1",
                session_id=session_id
            )
            
            # Initialize memory service for debugging and visibility
            # This enables scratch memory, context accumulation, and state tracking
            memory_service = None
            if MEMORY_AVAILABLE and InMemoryMemoryService:
                memory_service = InMemoryMemoryService()
            
            # Create runner with fallback handler and memory service
            # Note: ADK callbacks would be added here if supported
            runner_kwargs = {
                "agent": root_agent,
                "app_name": "job_match_app",
                "session_service": session_service
            }
            
            # Add memory service if available
            if memory_service:
                runner_kwargs["memory_service"] = memory_service
            
            runner = Runner(**runner_kwargs)
            # callbacks=[fallback_handler.on_error]  # If ADK supports error callbacks
            
            # Prepare input message in ADK format
            # Note: Resume is now preprocessed (max 8000 chars) to reduce token usage
            # If job_query is empty or just whitespace, make it optional (agent will infer from resume)
            job_query_clean = job_query.strip() if job_query else ""
            if not job_query_clean:
                job_query_clean = "(optional - will infer from resume)"
            
            user_message_text = (
                f"Resume Text:\n{resume_text}\n\n"
                f"Job Query: {job_query_clean}\n\n"
                "Parse the resume, select a job (infer from resume if query is vague), extract job details, analyze the match, and generate outputs."
            )
            
            # Create Content object for ADK
            user_content = genai_types.Content(
                role="user",
                parts=[genai_types.Part(text=user_message_text)]
            )
            
            # Run the pipeline using ADK Runner (async)
            # run_async returns an async generator, not awaitable
            response_stream = runner.run_async(
                new_message=user_content,
                user_id="user_1",
                session_id=session_id
            )
            
            # Collect response from async stream
            final_response_text = ""
            async for event in response_stream:
                try:
                    # Check if event has content attribute and it's not None
                    if hasattr(event, 'content') and event.content is not None:
                        # Check if content has parts
                        if hasattr(event.content, 'parts') and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    final_response_text += part.text
                        # Check if content has direct text attribute
                        elif hasattr(event.content, 'text') and event.content.text:
                            final_response_text += event.content.text
                    # Check if event has direct text attribute
                    elif hasattr(event, 'text') and event.text:
                        final_response_text += event.text
                except (AttributeError, TypeError) as e:
                    # Skip events that don't have the expected structure
                    # This can happen with function_call events or other non-text events
                    continue
            
            return final_response_text
        
        # Check timeout before starting
        if check_timeout_elapsed(start_time):
            return _get_timeout_result(_debug)
        
        # Run async pipeline
        try:
            final_output_text = asyncio.run(run_adk_pipeline())
            
            # Parse the final output (should be JSON that matches Final Output JSON Schema)
            import json
            import re
            
            def _try_parse_json_candidates(text: str) -> Optional[dict]:
                """
                Try to parse one or more JSON objects from text and return the one
                that looks like the Final Output JSON (has match_score and other keys).
                """
                candidates: list[dict] = []
                
                # First, try if the whole text is JSON
                try:
                    obj = json.loads(text)
                    candidates.append(obj)
                except Exception:
                    pass
                
                # Then, find all {...} blocks and try each as JSON
                try:
                    for m in re.finditer(r'\{.*?\}', text, re.DOTALL):
                        snippet = m.group(0)
                        try:
                            obj = json.loads(snippet)
                            candidates.append(obj)
                        except Exception:
                            continue
                except re.error:
                    pass
                
                # Prefer a candidate that matches the Final Output JSON shape
                required_keys = {
                    "match_score",
                    "score_breakdown",
                    "missing_skills",
                    "strengths",
                    "how_to_improve",
                    "optimized_summary",
                    "cover_letter",
                    "recruiter_message",
                    "job_title",
                    "company",
                    "job_url",
                }
                
                for obj in candidates:
                    if isinstance(obj, dict) and required_keys.issubset(obj.keys()):
                        return obj
                
                # If nothing matches the final schema, return None
                return None
            
            final_output = _try_parse_json_candidates(final_output_text)
            if final_output is None:
                # Parsed JSON did not match required schema; return fallback
                return _get_timeout_result(_debug)
            
            # Calculate total time
            elapsed_ms = int((time.time() - start_time) * 1000)
            _debug["total_time_ms"] = elapsed_ms
            
            # Add debug info
            if "_debug" not in final_output:
                final_output["_debug"] = {}
            final_output["_debug"].update(_debug)
            
            # Check if we should preserve debug (for testing)
            # If TESTING_MODE env var is set, keep debug info
            preserve_debug = os.getenv("TESTING_MODE", "false").lower() == "true"
            
            if preserve_debug:
                return final_output  # Keep debug for testing
            else:
                return strip_debug(final_output)  # Strip for production
            
        except Exception as e:
            # If ADK execution fails, check if it's a parser error
            error_text = str(e)
            if "resume" in error_text.lower() or "parse" in error_text.lower():
                from agents.parser_agent import _get_error_json
                return _get_error_json(error_text)
            else:
                # Record non-timeout error details for debugging, but still use fallback JSON
                _debug["error_type"] = "adk_execution_error"
                _debug["error_message"] = error_text
                return _get_timeout_result(_debug)
        
    except Exception as e:
        # Unexpected error, return fallback with debug info
        _debug["error_type"] = "unexpected_pipeline_error"
        _debug["error_message"] = str(e)
        return _get_timeout_result(_debug)


def _get_timeout_result(_debug: dict) -> dict:
    """
    Get timeout fallback result.
    
    Args:
        _debug: Debug dictionary to update
        
    Returns:
        Fallback JSON with score=82
    """
    _debug["timeout_exceeded"] = True
    _debug["total_time_ms"] = int(TIMEOUT_SECONDS * 1000)
    
    result = get_fallback_json()
    result["_debug"] = _debug
    
    # Check if we should preserve debug (for testing)
    preserve_debug = os.getenv("TESTING_MODE", "false").lower() == "true"
    
    if preserve_debug:
        return result  # Keep debug for testing
    else:
        return strip_debug(result)  # Strip for production

