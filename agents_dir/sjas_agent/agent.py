"""
SJAS Agent - Main Agent Code
This is the main agent file required by ADK.
It imports and exports the root_agent from our core module.
"""

# This file is the ADK-required entrypoint.
# It imports the root_agent defined in core/adk_agents.py
# and exposes it for ADK (adk run, adk web, adk api_server).

import sys
import os
from pathlib import Path

# Add project root directory to path to import our modules
# This MUST happen before any imports from core/
# Path structure: agents_dir/sjas_agent/agent.py -> go up 2 levels to project root
parent_dir = Path(__file__).parent.parent.parent
parent_dir_str = str(parent_dir)
if parent_dir_str not in sys.path:
    sys.path.insert(0, parent_dir_str)

# Explicitly load .env file from parent directory (project root)
# This guarantees API keys load in all environments:
# - Kaggle notebook
# - Local machine
# - Cloud Run
# - VS Code 
try:
    from dotenv import load_dotenv
    
    # Construct absolute path to .env file in project root
    # This ensures it works regardless of current working directory
    env_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),  # sjas_agent/ directory
        "..", "..",  # Go up 2 levels to project root (agents_dir -> project root)
        ".env"  # .env file
    )
    env_path = os.path.abspath(env_path)  # Resolve to absolute path
    
    # Load .env file if it exists
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # Fallback: try loading from current directory
        load_dotenv()
except ImportError:
    # dotenv not available, environment variables must be set directly
    pass

# Import root_agent from our core module
# This is the SequentialAgent that chains all 4 agents
from core.adk_agents import root_agent

# Model override: Allow command-line model specification
# Usage: MODEL=gemini-1.5-flash adk run sjas_agent
if "MODEL" in os.environ:
    model_override = os.environ["MODEL"]
    # Update model for all sub-agents
    if hasattr(root_agent, "sub_agents") and root_agent.sub_agents:
        for sub_agent in root_agent.sub_agents:
            if hasattr(sub_agent, "model"):
                sub_agent.model = model_override
    # Also update MODEL in core module for consistency
    import core.adk_agents
    core.adk_agents.MODEL = model_override

# ADK requires root_agent to be defined in this file
# root_agent is already defined in core/adk_agents.py
# We're just re-exporting it here for ADK compatibility
# Make sure root_agent is explicitly available at module level for ADK discovery

# Verify root_agent is accessible
assert root_agent is not None, "root_agent must be imported from core.adk_agents"

__all__ = ["root_agent"]

