# 🚀 Smart Job Match & Application Assistant

<div align="center">

> **Transform your job search with AI-powered automation**  
> Reduce application time by **90%** while improving quality

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-1.18.0+-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/google/adk)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash%20Lite-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)]()

[![Agents for Good](https://img.shields.io/badge/Track-Agents%20for%20Good-brightgreen?style=for-the-badge)](https://www.kaggle.com/)
[![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-blue?style=for-the-badge)](https://github.com/google/adk)
[![Tools](https://img.shields.io/badge/Tools-20%2B-orange?style=for-the-badge)](https://github.com/google/adk)
[![Time Savings](https://img.shields.io/badge/Time%20Savings-90%25-brightgreen?style=for-the-badge)]()

**Built with:** Google ADK • Gemini 2.5 Flash Lite • Python  
**Developers:** Varun Kumar Bejjanki & Shashank Bejjanki  
**Repository:** [GitHub](https://github.com/ShashankBejjanki1241/SJAS) • [Documentation](ARCHITECTURE_DIAGRAM.md)

[![Quick Start](https://img.shields.io/badge/Quick%20Start-Get%20Started-brightgreen?style=for-the-badge&logo=rocket)](https://github.com/ShashankBejjanki1241/SJAS#-quick-start)
[![Features](https://img.shields.io/badge/Features-View%20All-blue?style=for-the-badge)](https://github.com/ShashankBejjanki1241/SJAS#-key-features)
[![Architecture](https://img.shields.io/badge/Architecture-Diagrams-purple?style=for-the-badge)](https://github.com/ShashankBejjanki1241/SJAS#️-architecture)
[![Documentation](https://img.shields.io/badge/Docs-Read%20More-orange?style=for-the-badge)](https://github.com/ShashankBejjanki1241/SJAS#-documentation)

---

### 🏆 Competition Submission

**Track:** Agents for Good  
**Key Concepts:** Multi-Agent System • Tools (20+) • Sessions & Memory  
**Impact:** 90% Time Reduction • Production-Ready • Open Source

---

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#️-architecture)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Key Concepts Demonstrated](#-key-concepts-demonstrated)
- [Project Structure](#-project-structure)
- [Configuration](#️-configuration)
- [Testing](#-testing)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Use Cases](#-use-cases)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Smart Job Match & Application Assistant** is a production-ready, multi-agent AI system that revolutionizes the job search experience. Built with Google's ADK (Agents Development Kit), it automates the entire application process—from resume parsing to generating tailored cover letters—reducing time from **30-60 minutes to seconds**.

### The Problem We Solve

Job searching is broken. The average job seeker faces:

- ⏱️ **Time Consumption**: 30-60 minutes per application
- 😫 **Burnout**: Repetitive data entry and customization
- 📉 **Quality Issues**: Generic applications that don't stand out
- 🎯 **Poor Matching**: Difficulty finding relevant opportunities
- 💼 **Full-Time Job**: Job searching becomes a job itself

### Our Solution

A **4-agent sequential AI pipeline** that:

- ✅ **Parses** unstructured resume text into structured JSON
- ✅ **Matches** jobs intelligently using resume-based inference
- ✅ **Extracts** precise requirements from ATS pages
- ✅ **Generates** tailored cover letters, summaries, and recruiter messages
- ✅ **Scores** matches and provides actionable insights

**Result:** **90% time savings** with **higher quality** applications.

### Impact Metrics

- ⚡ **90% Time Reduction**: From 30-60 minutes to 10-15 seconds
- 📈 **Quality Improvement**: Tailored, professional applications every time
- 🎯 **Better Matching**: Intelligent inference from resume content
- 💪 **Reduced Stress**: Automated repetitive tasks

---

## ✨ Key Features

### 🧠 Intelligent Job Matching

#### Smart Resume Inference ⭐ *Unique Feature*
- **Conversational Queries**: Handles vague queries like "I need help finding a job"
- **Automatic Category Detection**: Analyzes resume (title, skills, work history) to infer best job category
- **No Manual Selection**: System intelligently determines the right job type

#### Deterministic Selection
- **Pre-Vetted URLs**: 13 verified job URLs from trusted ATS platforms
- **Multiple Categories**: Python, Backend, Data Engineering, and more
- **Robust Fallbacks**: 4 URLs per category with automatic failover

### 📝 Comprehensive Output Generation

#### Match Analysis
- **Match Score**: 0-100 score based on:
  - 40% Skills overlap
  - 40% Experience match
  - 20% Education requirements
- **Score Breakdown**: Detailed explanation of scoring
- **Missing Skills**: Identifies gaps with actionable suggestions
- **Strengths**: Highlights your best qualifications
- **Improvement Tips**: Specific recommendations to boost your match

#### Professional Writing
- **Cover Letter**: 280-320 words, professionally tailored with call-to-action
- **Recruiter Message**: 1-2 sentence concise pitch for LinkedIn/email
- **Optimized Summary**: 2-3 sentence resume summary
- **Word Count Validation**: Ensures all outputs meet requirements

### 🛡️ Production-Ready Reliability

#### Error Handling
- **Fail-Fast Design**: Pipeline stops immediately on errors
- **Graceful Fallbacks**: Structured error responses
- **Schema Validation**: All outputs validated against strict JSON schemas
- **Timeout Protection**: 55-second global timeout with fallback

#### User Experience
- **Progress Feedback**: Real-time messages showing agent activity
- **Transparency**: Users know exactly what's happening
- **Structured Output**: Consistent JSON format for easy integration

### 🔧 Technical Excellence

#### Tool Ecosystem
- **20+ Custom Tools**: Schema validation, scoring, text processing, content generation
- **ADK Integration**: Uses ADK's `load_web_page` for ATS browsing
- **No External Libraries**: No BeautifulSoup, requests, Playwright, or Selenium
- **Hard Skills Only**: Intelligent filtering for technical skills

#### Architecture
- **Multi-Agent System**: 4 specialized agents in sequence
- **Session Management**: Full observability with InMemorySessionService
- **Memory Services**: Context accumulation and state tracking
- **Modular Design**: Easy to extend and customize

---

## 🏗️ Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────┐
│                    User Input                            │
│         (Resume Text + Job Query)                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          SequentialAgent (Root Agent)                    │
│    Orchestrates 4 specialized sub-agents                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│ Agent 1:  │→ │ Agent 2:  │→ │ Agent 3:  │→ │ Agent 4:  │
│ Resume    │  │ Job       │  │ Job       │  │ Analyzer  │
│ Parser    │  │ Selector  │  │ Extractor │  │ & Writer  │
└───────────┘  └───────────┘  └───────────┘  └───────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
Structured    Job URLs      Job Details    Final Output
Resume JSON   (Primary +    (Skills,       (Score, Cover
              Backup)       Requirements)  Letter, etc.)
```

### Agent Details

#### 1. Resume Parser Agent
**Purpose**: Convert unstructured resume text into structured JSON

**Process**:
1. Preprocess text (normalize bullets, strip unicode, truncate to 8000 chars)
2. Extract structured data:
   - Name, years of experience, current title
   - Skills (normalized, deduplicated, max 10)
   - Education history
   - Work history (max 4 points per job)
3. Validate against strict JSON schema

**Tools Used**:
- `preprocess_resume_tool`
- `normalize_skills_tool`
- `validate_resume_schema_tool`
- `fallback_tool`

#### 2. Job Selector Agent ⭐ *Unique Feature*
**Purpose**: Intelligently select job URLs based on query or resume analysis

**Process**:
1. Check for DEMO mode (`DEMO:` prefix)
2. Try exact category match
3. Try fuzzy match via tags
4. **Smart Inference**: If query is vague, analyze resume to infer category
   - Analyzes: current title, skills, work history roles
   - Returns: best matching category (e.g., "data", "python", "backend")
5. Return primary + backup URLs

**Tools Used**:
- `select_job_tool`
- `infer_job_category_from_resume_tool` ⭐
- `fallback_tool`

**Example**:
```
Query: "I need help finding a job"
Resume: Data Engineer with Hadoop, Spark, AWS
→ System infers "data" category
→ Returns data engineering job URLs
```

#### 3. Job Extractor Agent
**Purpose**: Extract job information from ATS pages

**Process**:
1. Browse ATS page using ADK's `load_web_page`
2. Extract:
   - Job title, company
   - Hard skills only (max 10)
   - Responsibilities (max 6)
   - Experience level
   - Job URL
3. Validate extracted data
4. Fallback to backup URL if primary fails

**Tools Used**:
- `extract_job_tool`
- `load_web_page` (ADK built-in)
- `validate_job_schema_tool`
- `fallback_tool`

**Supported ATS Platforms**:
- Lever (`jobs.lever.co`)
- Greenhouse (`boards.greenhouse.io`)
- AshbyHQ (`jobs.ashbyhq.com`)
- Workable (`apply.workable.com`)

#### 4. Analyzer & Writer Agent
**Purpose**: Analyze match and generate writing outputs

**Process**:
1. Calculate skill overlap ratio (0.0 to 1.0)
2. Score experience match (0-10 integer via LLM)
3. Check education requirements (boolean)
4. Calculate final match score (0-100)
5. Identify missing skills
6. Generate strengths and improvement suggestions
7. Generate:
   - Optimized summary (2-3 sentences)
   - Cover letter (280-320 words)
   - Recruiter message (1-2 sentences)
8. Validate word counts
9. Validate final output schema

**Tools Used**:
- `calculate_skill_overlap_tool`
- `get_experience_score_tool`
- `check_education_match_tool`
- `calculate_final_score_tool`
- `identify_missing_skills_tool`
- `generate_strengths_tool`
- `generate_how_to_improve_tool`
- `generate_summary_tool`
- `generate_cover_letter_tool`
- `generate_recruiter_message_tool`
- `validate_word_count_tool`
- `validate_final_output_schema_tool`
- `strip_debug_tool`
- `fallback_tool`

### Architecture Diagrams

Comprehensive Mermaid diagrams are available in [`ARCHITECTURE_DIAGRAM.md`](ARCHITECTURE_DIAGRAM.md), including:
- High-level architecture flow
- Detailed agent flow with tools
- Sequential agent pipeline (ADK)
- Data flow diagram
- Component architecture
- Error handling & fallback flow
- Job selection logic (with resume inference)
- Scoring algorithm flow

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.8 or higher
- **Google API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **ADK**: Agents Development Kit (installed via `requirements.txt`)

### Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/ShashankBejjanki1241/SJAS.git
cd SJAS
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
ADK_MODEL=gemini-2.5-flash-lite  # Optional, defaults to gemini-2.5-flash-lite
```

### Running the System

#### **Option 1: ADK Web UI (Recommended)** ⭐

The primary and most user-friendly way to interact with the system:

```bash
./start_web_ui.sh
```

**Then:**
1. Open your browser to `http://localhost:8000`
2. Select `sjas_agent` from the agent dropdown
3. Paste your resume text in the text area
4. Enter a job query (see examples below)
5. Click Submit and watch the agents work
6. View comprehensive results

**Example Queries:**
- `DEMO:` - Fastest test, uses default job
- `I need help finding a job` - Shows smart resume inference ⭐
- `python developer` - Specific category match
- `data engineer` - Fuzzy category match
- `backend engineer` - Tag-based matching

#### **Option 2: Python API**

```python
from core.adk_pipeline import run_pipeline

resume_text = """
John Doe
Data Engineer
Email: john@example.com
Phone: (555) 123-4567

EXPERIENCE:

Senior Data Engineer | Tech Corp | 2020-Present
- Built ETL pipelines using Hadoop and Spark processing large datasets
- Managed AWS infrastructure including S3, EC2, and Redshift data warehouse
- Optimized SQL queries reducing query execution time by 40%
- Designed scalable data warehouse architecture supporting 10TB+ daily ingestion

Data Engineer | Startup Inc | 2018-2020
- Developed Python scripts for data extraction and transformation
- Created data pipelines processing 1M+ records daily
- Worked with PostgreSQL and MongoDB databases

EDUCATION:
Bachelor of Science in Computer Science | State University | 2018

SKILLS:
Python, SQL, Hadoop, Spark, AWS (S3, EC2, Redshift), PostgreSQL, MongoDB, ETL, Data Pipeline
"""

# Smart inference example
job_query = "I need help finding a job"

result = run_pipeline(resume_text, job_query)
print(result)
```

#### **Option 3: ADK CLI**

```bash
adk run agents_dir/sjas_agent
```

---

## 💡 Usage Examples

### Example 1: Conversational Query (Smart Inference)

```python
resume_text = "..." # Your resume
job_query = "I need help finding a job"

result = run_pipeline(resume_text, job_query)
# System automatically infers job category from resume
# Returns: Data engineering jobs if resume shows data engineering experience
```

### Example 2: Specific Category

```python
job_query = "python developer"
# Returns: Python/backend category jobs
```

### Example 3: DEMO Mode

```python
job_query = "DEMO:"
# Returns: Default job for quick testing
```

### Example Output

```json
{
  "match_score": 85,
  "score_breakdown": "40% skills (0.8), 40% experience (8/10), 20% education (1.0)",
  "missing_skills": ["Kubernetes", "Docker"],
  "strengths": [
    "Strong Python experience with 6+ years",
    "AWS expertise in S3, EC2, and Redshift",
    "ETL pipeline experience with Hadoop and Spark"
  ],
  "how_to_improve": [
    "Learn containerization technologies (Kubernetes, Docker)",
    "Gain experience with cloud orchestration tools"
  ],
  "optimized_summary": "Data Engineer with 6+ years of experience building scalable ETL pipelines using Hadoop, Spark, and AWS. Proven track record of optimizing data processing workflows and managing large-scale data infrastructure.",
  "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Data Engineer position at Spring & Bond. With over 6 years of experience in data engineering, I have a proven track record of building and optimizing ETL pipelines that process millions of records daily.\n\nIn my current role at Tech Corp, I designed and implemented data pipelines using Hadoop and Spark, reducing query execution time by 40%. I also managed AWS infrastructure including S3, EC2, and Redshift, supporting over 10TB of daily data ingestion. My experience with Python, SQL, and various data technologies aligns perfectly with your requirements.\n\nI am excited about the opportunity to contribute to your data engineering team and would welcome the chance to discuss how my skills can help drive your data initiatives forward.\n\nSincerely,\nJohn Doe",
  "recruiter_message": "Hi! I'm a Data Engineer with 6+ years of experience building ETL pipelines with Hadoop, Spark, and AWS. I'd love to discuss how I can contribute to your team.",
  "job_title": "Data Engineer",
  "company": "Spring & Bond",
  "job_url": "https://jobs.ashbyhq.com/springandbond/8d07d70b-7626-410a-bef7-9c68e855192b"
}
```

---

## 🎓 Key Concepts Demonstrated

<div align="center">

[![Multi-Agent](https://img.shields.io/badge/Concept-Multi--Agent%20System-blue?style=for-the-badge&logo=robot&logoColor=white)](#1-multi-agent-system-)
[![Tools](https://img.shields.io/badge/Concept-Tools%20(20%2B)-orange?style=for-the-badge&logo=tools&logoColor=white)](#2-tools-)
[![Sessions](https://img.shields.io/badge/Concept-Sessions%20%26%20Memory-green?style=for-the-badge&logo=database&logoColor=white)](#3-sessions--memory-)

</div>

This project demonstrates **3+ key concepts** from the ADK course:

### 1. Multi-Agent System ✅

**SequentialAgent Architecture:**
- 4 specialized agents chained in sequence
- Each agent has a specific role and responsibility
- State passing between agents via output keys
- Fail-fast behavior: Pipeline stops immediately on errors

**Agents:**
- **Resume Parser Agent** (LLM-powered)
- **Job Selector Agent** (LLM-powered with smart inference)
- **Job Extractor Agent** (LLM-powered)
- **Analyzer & Writer Agent** (LLM-powered)

### 2. Tools ✅

**Custom Tools (20+):**
- **Schema Validation**: `validate_resume_schema_tool`, `validate_job_schema_tool`, `validate_final_output_schema_tool`
- **Text Processing**: `preprocess_resume_tool`, `normalize_skills_tool`
- **Scoring**: `calculate_skill_overlap_tool`, `get_experience_score_tool`, `calculate_final_score_tool`
- **Writing**: `generate_cover_letter_tool`, `generate_summary_tool`, `generate_recruiter_message_tool`
- **Utility**: `count_words_tool`, `validate_word_count_tool`, `strip_debug_tool`
- **Inference**: `infer_job_category_from_resume_tool` ⭐
- **Fallback**: `fallback_tool`

**Built-in Tools:**
- `load_web_page` (ADK's built-in tool for browsing ATS pages)

### 3. Sessions & Memory ✅

**InMemorySessionService:**
- Full session management for user interactions
- Tracks conversation state
- Enables multi-turn interactions

**InMemoryMemoryService:**
- Scratch memory for agent state
- Context accumulation across agents
- State tracking for observability
- Debugging support

---

## 📁 Project Structure

```
SJAS/
├── agents_dir/                    # ADK agents directory (for adk web)
│   └── sjas_agent/                # Main agent (appears in ADK web UI)
│       ├── __init__.py
│       └── agent.py               # ADK entry point
│
├── agents/                        # Agent implementations
│   ├── parser_agent.py            # Resume parsing logic
│   ├── selector_agent.py          # Job selection + inference logic
│   ├── extractor_agent.py         # Job extraction logic
│   └── analyzer_writer_agent.py   # Analysis + writing logic
│
├── core/                          # Core modules
│   ├── adk_agents.py              # All 4 agents + 20+ tools
│   ├── adk_pipeline.py            # Pipeline orchestration
│   ├── schema_validator.py        # JSON schema validation
│   ├── timeout_manager.py         # Timeout handling
│   ├── utils.py                   # Utility functions
│   ├── adk_integration.py         # ADK integration utilities
│   └── adk_fallback_handler.py    # Error recovery
│
├── resources/
│   ├── job_map.json               # Pre-vetted job URLs (13 verified)
│   └── stopwords.json             # Skill normalization
│
├── tests/                         # Test suite (8 test files)
│   ├── test_parser.py
│   ├── test_selector.py
│   ├── test_extractor.py
│   ├── test_analyzer_writer.py
│   ├── test_pipeline.py
│   ├── test_schema_validator.py
│   ├── test_timeout_manager.py
│   └── test_utils.py
│
├── Documents/                     # Internal guides (git-ignored)
│   ├── ADK_UI_DEMO_GUIDE.md
│   └── EVALUATION_CHECKLIST.md
│
├── README.md                      # This file
├── SUBMISSION.md                  # Competition submission details
├── ARCHITECTURE_DIAGRAM.md        # Comprehensive architecture diagrams
├── requirements.txt               # Dependencies
├── start_web_ui.sh                # ADK web UI startup script
├── pytest.ini                     # Test configuration
└── .gitignore                     # Git ignore rules
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional
ADK_MODEL=gemini-2.5-flash-lite  # Default model
```

### Job Map Configuration

The `resources/job_map.json` file contains pre-vetted job URLs organized by category:

```json
{
  "python": {
    "tags": ["python", "backend"],
    "urls": [
      "https://jobs.lever.co/nava/...",
      "https://jobs.lever.co/ro/...",
      ...
    ]
  },
  "backend": {
    "tags": ["backend", "api"],
    "urls": [...]
  },
  "data": {
    "tags": ["data", "etl", "pipeline"],
    "urls": [...]
  },
  "default": {
    "tags": ["*"],
    "urls": [...]
  }
}
```

**Categories:**
- `python`: Python/backend roles
- `backend`: Backend engineering roles
- `data`: Data engineering roles
- `default`: Fallback option

Each category has **4 verified URLs** from trusted ATS platforms.

---

## 🧪 Testing

### Run All Tests

```bash
python -m pytest tests/
```

### Run Specific Test

```bash
python -m pytest tests/test_parser.py
```

### Test Coverage

```bash
python -m pytest tests/ --cov=agents --cov=core
```

All tests use pytest and are included in `requirements.txt`.

---

## ⚡ Performance

### Speed Metrics

- **Total Pipeline Time**: 10-15 seconds (average)
- **Resume Parsing**: 2-3 seconds
- **Job Selection**: <1 second
- **Job Extraction**: 3-5 seconds
- **Analysis & Writing**: 5-7 seconds

### Timeout Protection

- **Global Timeout**: 55 seconds
- **Fallback**: Returns structured error JSON if timeout exceeded
- **Graceful Degradation**: System always returns useful output

### Resource Usage

- **Memory**: Minimal (in-memory processing)
- **API Calls**: Optimized to reduce LLM calls
- **Network**: Only for ATS page browsing

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: Agent not appearing in ADK Web UI dropdown

**Solution:**
```bash
# Verify agent structure
ls -la agents_dir/sjas_agent/
# Should show: __init__.py and agent.py

# Restart web UI
./start_web_ui.sh
```

#### Issue: "API key not found" error

**Solution:**
```bash
# Check .env file exists
cat .env
# Should contain: GOOGLE_API_KEY=your_key_here

# Verify it's in project root
pwd
# Should be: /path/to/SJAS
```

#### Issue: Job extraction fails

**Solution:**
- Check internet connection
- Verify job URL is from allowed domain (lever.co, greenhouse.io, ashbyhq.com, workable.com)
- System will automatically fallback to backup URL or default job

#### Issue: Timeout errors

**Solution:**
- Check API key is valid
- Verify network connection
- System will return fallback JSON if timeout exceeded

### Getting Help

1. Check [SUBMISSION.md](SUBMISSION.md) for detailed documentation
2. Review [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) for architecture details
3. Open an issue on GitHub

---

## ❓ FAQ

### Q: How accurate is the job matching?

**A:** The system uses a combination of:
- Skill overlap ratio (40% weight)
- Experience match score (40% weight)
- Education requirements (20% weight)

The match score (0-100) provides a reliable indicator of fit.

### Q: Can I use my own job URLs?

**A:** Yes! Update `resources/job_map.json` with your own URLs. Ensure they're from allowed ATS domains.

### Q: What if my resume format is unusual?

**A:** The system handles unstructured text well. However, for best results:
- Use plain text (no PDF formatting)
- Include clear sections (Experience, Skills, Education)
- List skills explicitly

### Q: How does smart resume inference work?

**A:** When you enter a vague query like "I need help finding a job", the system:
1. Analyzes your current title
2. Examines your skills
3. Reviews your work history roles
4. Matches against job categories in `job_map.json`
5. Returns the best matching category

### Q: Can I customize the output format?

**A:** The output follows a strict JSON schema. You can modify the agent instructions in `core/adk_agents.py` to customize outputs.

### Q: Is my data stored?

**A:** No. The system uses in-memory processing. No data is stored or transmitted beyond API calls to Gemini.

---

## 🎯 Use Cases

### For Job Seekers

- **Quick Applications**: Generate tailored applications in seconds
- **Skill Gap Analysis**: Identify missing skills and get improvement suggestions
- **Resume Optimization**: Get optimized summaries and bullet points
- **Time Savings**: Focus on networking and interviews instead of application writing
- **Multiple Applications**: Apply to multiple jobs efficiently

### For Career Coaches

- **Client Assessment**: Quickly assess client-job fit
- **Resume Review**: Get AI-powered resume analysis
- **Application Quality**: Ensure clients submit high-quality applications

### For Recruiters

- **Candidate Matching**: Quickly assess candidate-job fit
- **Quality Applications**: Receive well-crafted, relevant applications
- **Efficiency**: Process more applications with better quality

---

## 🌟 Unique Features

### 1. Smart Resume Inference ⭐

Unlike other systems that require specific job queries, our system can handle conversational queries like "I need help finding a job" by analyzing the resume to infer the best job category.

**How it works:**
- Analyzes current title (e.g., "Data Engineer" → "data" category)
- Examines skills (e.g., "Hadoop", "Spark" → "data" category)
- Reviews work history (e.g., "Data Engineer" roles → "data" category)
- Returns best matching category automatically

### 2. Real-Time Progress Feedback

Every agent provides transparent progress messages, so users know exactly what's happening at each step:
- "Preprocessing resume text..."
- "Inferring job category from your resume..."
- "Detected data category based on your background"
- "Extracting job details from ATS page..."
- "Generating tailored cover letter..."

### 3. Production-Ready Error Handling

Comprehensive fallback mechanisms ensure the system always returns structured, useful output even when errors occur:
- Schema validation at every step
- Automatic fallback to backup URLs
- Graceful error messages
- Timeout protection

### 4. Hard Skills Only

Intelligent filtering ensures only technical skills are extracted and matched, avoiding soft skills that don't contribute to matching:
- Filters out: "communication", "leadership", "teamwork"
- Keeps: "Python", "Kubernetes", "AWS", "SQL"

---

## 📚 Documentation

### Main Documentation

- **[README.md](README.md)**: This file - comprehensive project overview
- **[SUBMISSION.md](SUBMISSION.md)**: Competition submission details
- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)**: Comprehensive architecture diagrams

### Code Documentation

- **Docstrings**: All functions have detailed docstrings
- **Type Hints**: Full type annotations for better IDE support
- **Comments**: Inline comments explain complex logic

### External Resources

- [Google ADK Documentation](https://github.com/google/adk)
- [Gemini API Documentation](https://ai.google.dev/docs)

---

## 🤝 Contributing

This is a competition submission project. For questions, feedback, or contributions:

1. **Open an Issue**: Report bugs or suggest features
2. **Fork the Repository**: Create your own version
3. **Submit Pull Requests**: Share improvements

### Development Setup

```bash
# Clone repository
git clone https://github.com/ShashankBejjanki1241/SJAS.git
cd SJAS

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Make changes and test
./start_web_ui.sh
```

---

## 📄 License

MIT License - see LICENSE file for details.

**Copyright (c) 2024 Varun Kumar Bejjanki & Shashank Bejjanki**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

---

## 🙏 Acknowledgments

### Technologies

- **Google ADK**: For the powerful agent framework
- **Gemini Models**: For LLM capabilities
- **Python Community**: For excellent libraries and tools

### ATS Platforms

- **Lever**: For job postings
- **Greenhouse**: For job postings
- **AshbyHQ**: For job postings
- **Workable**: For job postings

### Inspiration

Built for **Agents for Good** track - helping job seekers save time and reduce stress in their job search journey.

---

## 📞 Contact & Support

<div align="center">

### 👥 Developers

**Varun Kumar Bejjanki** & **Shashank Bejjanki**

### 🔗 Links

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShashankBejjanki1241/SJAS)
[![Issues](https://img.shields.io/badge/GitHub-Issues-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShashankBejjanki1241/SJAS/issues)
[![Documentation](https://img.shields.io/badge/Docs-Architecture%20Diagram-blue?style=for-the-badge)](ARCHITECTURE_DIAGRAM.md)
[![Submission](https://img.shields.io/badge/Competition-Submission-green?style=for-the-badge)](SUBMISSION.md)

### 💬 Support

- 📧 **Open an Issue**: [GitHub Issues](https://github.com/ShashankBejjanki1241/SJAS/issues)
- 📖 **Documentation**: Check [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) and [SUBMISSION.md](SUBMISSION.md)
- ❓ **FAQ**: Review the [FAQ section](#-faq) above
- 🔍 **Troubleshooting**: See [Troubleshooting guide](#-troubleshooting)

</div>

---

<div align="center">

---

### ⭐ Star this Repository

If you find this project helpful, please consider giving it a star on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/ShashankBejjanki1241/SJAS?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShashankBejjanki1241/SJAS/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ShashankBejjanki1241/SJAS?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShashankBejjanki1241/SJAS/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/ShashankBejjanki1241/SJAS?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShashankBejjanki1241/SJAS/watchers)

---

**Built with ❤️ for Agents for Good**

*Reducing job search time by 90% • One application at a time*

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Google ADK](https://img.shields.io/badge/Powered%20by-Google%20ADK-4285F4?style=flat-square&logo=google&logoColor=white)](https://github.com/google/adk)
[![Uses Gemini AI](https://img.shields.io/badge/Uses-Gemini%20AI-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)

[⬆ Back to Top](#-smart-job-match--application-assistant)

---

**© 2024 Varun Kumar Bejjanki & Shashank Bejjanki. All rights reserved.**

</div>
