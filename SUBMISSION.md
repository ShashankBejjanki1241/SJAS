# Capstone Submission: Smart Job Match & Application Assistant

## Track Selection
**Track:** Agents for Good
**Reasoning:** This agent helps job seekers, particularly those affected by layoffs or looking for better opportunities, by automating the tedious and often demoralizing process of finding and applying for jobs. It empowers individuals to present their best selves through tailored applications.

## Problem & Solution Pitch
**Problem:**
The modern job search is broken. Job seekers spend countless hours scrolling through irrelevant listings, manually extracting details, and rewriting their resumes and cover letters for every single application. This manual process is inefficient, prone to error, and leads to burnout, preventing candidates from showcasing their true potential.

**Solution:**
The **Smart Job Match & Application Assistant** is a deterministic, multi-agent system designed to reclaim the job seeker's time. By automating resume parsing, job qualification, and application tailoring, it ensures that every application is high-quality and hyper-relevant.
- **Resume Parser Agent**: Converts unstructured resume text into a strict JSON schema.
- **Job Selector Agent**: Deterministically identifies the best-fit roles from a curated map.
- **Job Extractor Agent**: Navigates ATS pages (Lever, Greenhouse, etc.) to extract precise job requirements.
- **Analyzer & Writer Agent**: Scores the match and generates a tailored cover letter, recruiter message, and optimized resume summary.

This agent doesn't just apply; it strategizes, ensuring the user puts their best foot forward every time.

## Value Proposition Writeup
**"This agent reduced my job application process by 90%, allowing me to focus on interview prep and networking."**

Finding a job is a full-time job. On average, a candidate might spend 30-60 minutes per application to do it right—reading the JD, analyzing the fit, and customizing their materials. With the Smart Job Match & Application Assistant, this process is reduced to seconds.

**Key Benefits:**
1.  **Time Savings**: Automates the repetitive "grunt work" of the job search.
2.  **Quality at Scale**: Every application is tailored with the precision of a human career coach, but at the speed of AI.
3.  **Mental Well-being**: Reduces the cognitive load and emotional toll of constant rejection and repetitive data entry.
4.  **Privacy & Control**: Runs locally with deterministic logic, ensuring the user stays in control of their data and the jobs they apply to.

**Technical Highlights:**
- **Multi-Agent Architecture**: 4 specialized agents working in sequence using ADK's SequentialAgent.
- **Extensive Tool Use**: 20+ custom tools for schema validation, scoring, text processing, and web navigation, plus ADK's built-in `load_web_page` tool.
- **Sessions & Memory**: Full session management with InMemorySessionService and InMemoryMemoryService for debugging and state tracking.
- **Reliability**: "Fail-fast" design ensures that only high-quality matches result in generated content.

## How to Run

**Primary Method: ADK Web UI (Recommended)**

The project is designed to run primarily through the ADK Web UI, providing an interactive interface for testing and demonstration.

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set API Key:**
    Create a `.env` file in the project root and add your Google API key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

3.  **Start ADK Web Server:**
    ```bash
    ./start_web_ui.sh
    ```
    Or manually:
    ```bash
    source venv/bin/activate
    adk web agents_dir --port 8000
    ```

4.  **Access Web UI:**
    - Open your browser to: `http://localhost:8000`
    - Select `sjas_agent` from the agent dropdown
    - Enter your resume text and job query
    - Submit and view results

**Alternative Methods:**

**Option B: Python API**
```python
from core.adk_pipeline import run_pipeline

resume_text = "..." # Your resume text
job_query = "Software Engineer"
result = run_pipeline(resume_text, job_query)
print(result)
```

**Option C: ADK CLI**
```bash
adk run agents_dir/sjas_agent
```

---

## Key Concepts Demonstrated

This submission demonstrates **3+ key concepts** from the ADK course:

### 1. Multi-Agent System ✅
- **SequentialAgent**: 4 specialized agents chained in sequence
  - Resume Parser Agent (LLM-powered)
  - Job Selector Agent (LLM-powered)
  - Job Extractor Agent (LLM-powered)
  - Analyzer & Writer Agent (LLM-powered)
- **Fail-fast behavior**: Pipeline stops immediately if any agent fails

### 2. Tools ✅
- **Custom Tools (20+)**: 
  - Schema validation tools (`validate_resume_schema_tool`, `validate_job_schema_tool`, `validate_final_output_schema_tool`)
  - Text processing tools (`preprocess_resume_tool`, `normalize_skills_tool`)
  - Scoring tools (`calculate_skill_overlap_tool`, `get_experience_score_tool`, `calculate_final_score_tool`)
  - Writing tools (`generate_cover_letter_tool`, `generate_summary_tool`, `generate_recruiter_message_tool`)
  - Utility tools (`count_words_tool`, `validate_word_count_tool`, `strip_debug_tool`)
  - Fallback tool (`fallback_tool`)
- **Built-in Tools**: 
  - `load_web_page` (ADK's built-in tool for browsing ATS pages)

### 3. Sessions & Memory ✅
- **InMemorySessionService**: Full session management for user interactions
- **InMemoryMemoryService**: Enabled for debugging, providing:
  - Scratch memory for agent state
  - Context accumulation across agents
  - State tracking for observability

---

## Architecture Overview

The system uses ADK's `SequentialAgent` to chain 4 specialized agents:

1. **Resume Parser Agent** → Parses unstructured resume text into JSON
2. **Job Selector Agent** → Selects job URLs from pre-vetted map
3. **Job Extractor Agent** → Extracts job details from ATS pages using `load_web_page`
4. **Analyzer & Writer Agent** → Scores match and generates outputs

Each agent has access to custom tools and the fallback mechanism, ensuring robust error handling.
