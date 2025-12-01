#!/bin/bash

# Smart Job Match & Application Assistant - ADK Web UI Startup Script
# This script starts the ADK web UI with the correct agent directory

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting ADK Web UI...${NC}"
echo ""

# Check if we're in the project root
if [ ! -d "agents_dir" ] || [ ! -d "agents_dir/sjas_agent" ]; then
    echo -e "${RED}❌ Error: agents_dir/sjas_agent not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo "Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo -e "${RED}❌ Virtual environment not found${NC}"
        exit 1
    fi
fi

# Kill any existing process on port 8000
echo "Checking for existing processes on port 8000..."
if lsof -ti:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Killing existing process on port 8000...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Verify agent structure
echo "Verifying agent structure..."
if [ ! -f "agents_dir/sjas_agent/agent.py" ] || [ ! -f "agents_dir/sjas_agent/__init__.py" ]; then
    echo -e "${RED}❌ Agent files not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Agent structure verified${NC}"
echo ""

# Start ADK web UI
echo -e "${GREEN}Starting ADK Web Server...${NC}"
echo "Access at: ${GREEN}http://localhost:8000${NC}"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the ADK web UI with the agents directory
# This ensures only agent directories are shown in the dropdown
# The web UI is the PRIMARY way to interact with this agent
echo -e "${GREEN}Starting ADK Web Server...${NC}"
echo "Access at: ${GREEN}http://localhost:8000${NC}"
echo ""
echo "In the web UI:"
echo "  1. Select 'sjas_agent' from the dropdown"
echo "  2. Enter your resume text"
echo "  3. Enter job query (e.g., 'DEMO: Software Engineer' or 'python developer')"
echo "  4. Submit and view results"
echo ""
echo "Press Ctrl+C to stop"
echo ""

adk web agents_dir --port 8000
