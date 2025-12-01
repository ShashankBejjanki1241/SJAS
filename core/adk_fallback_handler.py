"""
ADK Fallback Handler
Provides callback-based fallback handling for the root agent.
"""

from typing import Optional
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from core.timeout_manager import get_fallback_json


class FallbackHandler:
    """
    Callback handler for ADK that provides fallback behavior on errors.
    
    This handler can be attached to the Runner to catch errors and return
    graceful fallback responses instead of crashing.
    """
    
    def __init__(self):
        self.fallback_triggered = False
        self.error_type = None
        self.error_message = None
    
    async def on_error(
        self,
        event: Event,
        context: InvocationContext
    ) -> Optional[Event]:
        """
        Called when an error occurs during agent execution.
        
        Args:
            event: The error event
            context: Invocation context
            
        Returns:
            Optional event to replace the error, or None to propagate error
        """
        # Mark that fallback was triggered
        self.fallback_triggered = True
        
        # Extract error information
        error_str = str(event) if event else "Unknown error"
        self.error_message = error_str
        
        # Determine error type
        if "timeout" in error_str.lower():
            self.error_type = "timeout"
        elif "parser" in error_str.lower() or "parse" in error_str.lower():
            self.error_type = "parser_error"
        elif "extract" in error_str.lower():
            self.error_type = "extraction_error"
        elif "selector" in error_str.lower() or "select" in error_str.lower():
            self.error_type = "selection_error"
        elif "analyzer" in error_str.lower() or "analyze" in error_str.lower():
            self.error_type = "analysis_error"
        else:
            self.error_type = "unknown_error"
        
        # Get fallback JSON
        fallback_result = get_fallback_json()
        
        # Add error information to debug
        if "_debug" not in fallback_result:
            fallback_result["_debug"] = {}
        
        fallback_result["_debug"].update({
            "fallback_triggered": True,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "error_context": "ADK callback handler"
        })
        
        # Update score_breakdown
        fallback_result["score_breakdown"] = f"Fallback mode activated: {self.error_type}"
        if self.error_message:
            fallback_result["score_breakdown"] += f" - {self.error_message[:100]}"
        
        # Return a new event with fallback result
        # Note: This is a simplified approach - actual implementation may vary
        # based on ADK's event structure
        return None  # Return None to let ADK handle the error normally
        # For actual fallback, we'd need to create a proper Event with the fallback JSON
    
    def get_fallback_result(self) -> dict:
        """
        Get the fallback result after an error.
        
        Returns:
            Fallback JSON dictionary
        """
        if not self.fallback_triggered:
            return {}
        
        result = get_fallback_json()
        
        if "_debug" not in result:
            result["_debug"] = {}
        
        result["_debug"].update({
            "fallback_triggered": True,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "error_context": "ADK callback handler"
        })
        
        result["score_breakdown"] = f"Fallback mode activated: {self.error_type}"
        if self.error_message:
            result["score_breakdown"] += f" - {self.error_message[:100]}"
        
        return result

