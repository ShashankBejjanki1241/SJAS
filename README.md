# Smart Job Match & Application Assistant

A deterministic 4-agent pipeline for resume parsing, job selection, job extraction, analysis, scoring, and writing.

**Developers:** Varun Kumar Bejjanki & Shashank Bejjanki

## Architecture

The system consists of 4 sequential agents:

1. **Resume Parser Agent** - Parses raw resume text into structured JSON
2. **Deterministic Job Selector Agent** - Selects job URL from pre-vetted job_map.json
3. **Job Extractor Agent** - Extracts job information from ATS pages
4. **Analyzer & Writer Agent** - Analyzes match and generates writing outputs

### Architecture Diagrams

Comprehensive Mermaid diagrams are available in [`ARCHITECTURE_DIAGRAM.md`](ARCHITECTURE_DIAGRAM.md), including:
- High-level architecture flow
- Detailed agent flow with tools
- Sequential agent pipeline (ADK)
- Data flow diagram
- Component architecture
- Error handling & fallback flow
- Job selection logic
- Scoring algorithm flow

Quick reference: See [`ARCHITECTURE_DIAGRAM.md`](ARCHITECTURE_DIAGRAM.md) for the main flow diagram.

## Features

- Strict JSON schema enforcement
- Deterministic job selection
- ATS-safe extraction (Lever, Greenhouse, AshbyHQ, Workable only)
- Bulletproof experience scoring
- Hard skill-only missing skills detection
- Premium output fields (cover letter, recruiter message, optimized summary)
- Graceful structured error output
- 55-second global timeout

## Project Structure

```
/project-root
    /agents_dir              # ADK agents directory (for adk web)
        /sjas_agent          # Main agent (appears in ADK web UI)
            __init__.py
            agent.py
    /agents                  # Agent implementations
        parser_agent.py
        selector_agent.py
        extractor_agent.py
        analyzer_writer_agent.py
    /core                    # Core modules
        adk_agents.py
        adk_pipeline.py
        pipeline.py
        timeout_manager.py
        schema_validator.py
        utils.py
    /resources
        job_map.json
        stopwords.json
    /tests
        test_parser.py
        test_selector.py
        test_extractor.py
        test_analyzer_writer.py
    README.md
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

That's it. No virtual environments, no complex build steps. Just install and run.

## Usage

### Python API

```python
from core.adk_pipeline import run_pipeline

resume_text = "Your resume text here..."
job_query = "Python Developer"

result = run_pipeline(resume_text, job_query)
print(result)
```

## Demo Mode

Use "DEMO:" prefix in job query to force default job:

```python
result = run_pipeline(resume_text, "DEMO: Python Developer")
```

## Requirements

- Python 3.8 or higher
- ADK (Agents Development Kit) for browse_page tool
- Pre-vetted job URLs in `resources/job_map.json`

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the pipeline:

   **Option A: Python API**
   ```python
   from core.adk_pipeline import run_pipeline
   
   resume_text = "Your resume text here..."
   job_query = "Python Developer"
   result = run_pipeline(resume_text, job_query)
   ```

   **Option B: ADK Web UI**
   ```bash
   ./start_web_ui.sh
   # Then open http://localhost:8000
   # Select 'sjas_agent' from the dropdown
   ```

   **Option C: ADK CLI**
   ```bash
   adk run agents_dir/sjas_agent
   ```

## Testing

```bash
# Run all tests
python -m pytest tests/
```

pytest is included in `requirements.txt`.

## License

MIT

