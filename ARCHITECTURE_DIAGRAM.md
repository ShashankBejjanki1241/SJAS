# Smart Job Match & Application Assistant - Architecture Diagrams

This document contains Mermaid diagrams visualizing the architecture, flow, and components of the SJAS system.

## 1. High-Level Architecture Flow

```mermaid
graph TB
    Start([User Input:<br/>Resume Text + Job Query]) --> Parser[Resume Parser Agent]
    
    Parser -->|Parsed Resume JSON| Selector[Job Selector Agent]
    Selector -->|Primary + Backup URLs| Extractor[Job Extractor Agent]
    Extractor -->|Extracted Job JSON| Analyzer[Analyzer & Writer Agent]
    
    Analyzer -->|Final Output JSON| End([Output:<br/>Match Score, Cover Letter, etc.])
    
    Parser -.->|Error| Fallback[Fallback Handler]
    Selector -.->|Error| Fallback
    Extractor -.->|Error| Fallback
    Analyzer -.->|Error| Fallback
    
    Fallback -->|Fallback JSON| End
    
    Timeout[Timeout Manager<br/>55s limit] -.->|Timeout| Fallback
    
    classDef agentStyle fill:#e1f5ff,stroke:#333,stroke-width:2px
    classDef errorStyle fill:#ffe1e1,stroke:#333,stroke-width:2px
    classDef timeoutStyle fill:#fff4e1,stroke:#333,stroke-width:2px
    
    class Parser,Selector,Extractor,Analyzer agentStyle
    class Fallback errorStyle
    class Timeout timeoutStyle
```

## 2. Detailed Agent Flow with Tools

```mermaid
graph LR
    subgraph "Agent 1: Resume Parser"
        A1[Resume Parser Agent] --> T1A[preprocess_resume_tool]
        A1 --> T1B[normalize_skills_tool]
        A1 --> T1C[validate_resume_schema_tool]
        A1 --> T1D[fallback_tool]
        T1A --> O1[Parsed Resume JSON<br/>output_key: parsed_resume]
    end
    
    subgraph "Agent 2: Job Selector"
        A2[Job Selector Agent] --> T2A[select_job_tool]
        A2 --> T2B[fallback_tool]
        T2A --> O2[Selected URLs<br/>output_key: selected_job_urls]
    end
    
    subgraph "Agent 3: Job Extractor"
        A3[Job Extractor Agent] --> T3A[extract_job_tool]
        A3 --> T3B[load_web_page<br/>ADK Tool]
        A3 --> T3C[validate_job_schema_tool]
        A3 --> T3D[fallback_tool]
        T3A --> T3B
        T3B --> O3[Extracted Job JSON<br/>output_key: extracted_job]
    end
    
    subgraph "Agent 4: Analyzer & Writer"
        A4[Analyzer & Writer Agent] --> T4A[calculate_skill_overlap_tool]
        A4 --> T4B[get_experience_score_tool]
        A4 --> T4C[check_education_match_tool]
        A4 --> T4D[calculate_final_score_tool]
        A4 --> T4E[identify_missing_skills_tool]
        A4 --> T4F[generate_strengths_tool]
        A4 --> T4G[generate_how_to_improve_tool]
        A4 --> T4H[generate_summary_tool]
        A4 --> T4I[generate_cover_letter_tool]
        A4 --> T4J[generate_recruiter_message_tool]
        A4 --> T4K[validate_word_count_tool]
        A4 --> T4L[validate_final_output_schema_tool]
        A4 --> T4M[strip_debug_tool]
        A4 --> T4N[fallback_tool]
        T4A --> T4D
        T4B --> T4D
        T4C --> T4D
        T4D --> T4H
        T4D --> T4I
        T4D --> T4J
        T4A --> T4E
        T4A --> T4F
        T4D --> T4G
        T4I --> T4K
        T4J --> T4K
        T4H --> T4L
        T4I --> T4L
        T4J --> T4L
        T4L --> O4[Final Output JSON<br/>output_key: final_output]
    end
    
    O1 --> A2
    O2 --> A3
    O3 --> A4
    
    classDef agentStyle fill:#e1f5ff,stroke:#333,stroke-width:2px
    classDef toolStyle fill:#fff4e1,stroke:#333,stroke-width:2px
    
    class A1,A2,A3,A4 agentStyle
    class T3B toolStyle
```

## 3. Sequential Agent Pipeline (ADK)

```mermaid
graph TB
    subgraph "ADK Runner"
        Runner[ADK Runner<br/>InMemorySessionService<br/>InMemoryMemoryService]
    end
    
    subgraph "Root Agent: SequentialAgent"
        Root[SequentialAgent<br/>job_match_pipeline]
    end
    
    subgraph "Sub-Agents (Sequential Execution)"
        A1[Resume Parser Agent<br/>model: gemini-2.5-flash-lite]
        A2[Job Selector Agent<br/>model: gemini-2.5-flash-lite]
        A3[Job Extractor Agent<br/>model: gemini-2.5-flash-lite]
        A4[Analyzer & Writer Agent<br/>model: gemini-2.5-flash-lite]
    end
    
    Runner --> Root
    Root --> A1
    A1 -->|State: parsed_resume| A2
    A2 -->|State: selected_job_urls| A3
    A3 -->|State: extracted_job| A4
    A4 -->|State: final_output| Result[Final Result]
    
    A1 -.->|Fail-Fast| Error[Pipeline Stops]
    A2 -.->|Fail-Fast| Error
    A3 -.->|Fail-Fast| Error
    A4 -.->|Fail-Fast| Error
    
    classDef rootStyle fill:#d4edda,stroke:#333,stroke-width:2px
    classDef agentStyle fill:#e1f5ff,stroke:#333,stroke-width:2px
    classDef errorStyle fill:#ffe1e1,stroke:#333,stroke-width:2px
    
    class Root rootStyle
    class A1,A2,A3,A4 agentStyle
    class Error errorStyle
```

## 4. Data Flow Diagram

```mermaid
flowchart TD
    Input[User Input:<br/>resume_text: str<br/>job_query: str] --> Pipeline[ADK Pipeline Runner]
    
    Pipeline --> Parser[Resume Parser Agent]
    Parser -->|JSON| ResumeData{Resume JSON Schema:<br/>name, years_of_experience,<br/>current_title, skills,<br/>education, work_history}
    
    ResumeData --> Selector[Job Selector Agent]
    Selector -->|Query| JobMap[job_map.json<br/>Categories: python, backend,<br/>data, default]
    JobMap -->|URLs| URLs{Selected URLs:<br/>primary_url<br/>backup_url}
    
    URLs --> Extractor[Job Extractor Agent]
    Extractor -->|Browse| ATS[ATS Pages:<br/>Lever / Greenhouse /<br/>AshbyHQ / Workable]
    ATS -->|Extract| JobData{Job JSON Schema:<br/>job_title, company,<br/>skills, responsibilities,<br/>experience_level, job_url}
    
    JobData --> Analyzer[Analyzer & Writer Agent]
    Analyzer -->|Calculate| Score[Match Score:<br/>40% Skills +<br/>40% Experience +<br/>20% Education]
    
    Analyzer -->|Generate| Output{Final Output JSON:<br/>match_score, score_breakdown,<br/>missing_skills, strengths,<br/>how_to_improve, optimized_summary,<br/>cover_letter, recruiter_message,<br/>job_title, company, job_url}
    
    Output -->|Strip _debug| Final[Final Output<br/>User-Facing JSON]
    
    classDef dataStyle fill:#e1f5ff,stroke:#333,stroke-width:2px
    classDef outputStyle fill:#d4edda,stroke:#333,stroke-width:2px
    classDef atsStyle fill:#fff4e1,stroke:#333,stroke-width:2px
    
    class ResumeData,JobData dataStyle
    class Output outputStyle
    class ATS atsStyle
```

## 5. Component Architecture

```mermaid
graph TB
    subgraph "Entry Points"
        CLI[ADK CLI<br/>adk run sjas_agent]
        API[Python API<br/>core.adk_pipeline.run_pipeline]
        Web[ADK Web UI<br/>adk web]
    end
    
    subgraph "Core ADK Integration"
        AgentDef[core/adk_agents.py<br/>4 Agents + Root SequentialAgent]
        Pipeline[core/adk_pipeline.py<br/>ADK Runner Orchestration]
        Entry[sjas_agent/agent.py<br/>ADK Entrypoint]
    end
    
    subgraph "Agent Implementations"
        ParserAgent[agents/parser_agent.py]
        SelectorAgent[agents/selector_agent.py]
        ExtractorAgent[agents/extractor_agent.py]
        AnalyzerAgent[agents/analyzer_writer_agent.py]
    end
    
    subgraph "Core Utilities"
        Schema[core/schema_validator.py<br/>JSON Schema Validation]
        Utils[core/utils.py<br/>Text Processing, Normalization]
        Timeout[core/timeout_manager.py<br/>55s Timeout + Fallback]
        Fallback[core/adk_fallback_handler.py<br/>Error Recovery]
    end
    
    subgraph "Resources"
        JobMap[resources/job_map.json<br/>Pre-vetted Job URLs]
        Stopwords[resources/stopwords.json<br/>Skill Normalization]
    end
    
    subgraph "External Services"
        ADK[Google ADK<br/>Agent Framework]
        Gemini[Gemini LLM<br/>gemini-2.5-flash-lite]
        WebPage[ADK load_web_page<br/>ATS Page Browsing]
    end
    
    CLI --> Entry
    API --> Pipeline
    Web --> Entry
    
    Entry --> AgentDef
    Pipeline --> AgentDef
    AgentDef --> ParserAgent
    AgentDef --> SelectorAgent
    AgentDef --> ExtractorAgent
    AgentDef --> AnalyzerAgent
    
    ParserAgent --> Schema
    ParserAgent --> Utils
    SelectorAgent --> JobMap
    ExtractorAgent --> WebPage
    AnalyzerAgent --> Schema
    AnalyzerAgent --> Utils
    
    AgentDef --> ADK
    ADK --> Gemini
    ADK --> WebPage
    
    Pipeline --> Timeout
    Pipeline --> Fallback
    Pipeline --> Schema
    
    classDef coreStyle fill:#d4edda,stroke:#333,stroke-width:2px
    classDef externalStyle fill:#fff4e1,stroke:#333,stroke-width:2px
    
    class AgentDef,Pipeline coreStyle
    class ADK,Gemini externalStyle
```

## 6. Error Handling & Fallback Flow

```mermaid
graph TB
    Start[Agent Execution] --> Try{Execute Agent}
    
    Try -->|Success| Validate{Schema Valid?}
    Try -->|Error| Catch[Exception Caught]
    
    Validate -->|Yes| Next[Pass to Next Agent]
    Validate -->|No| SchemaError[Schema Validation Error]
    
    Catch --> FallbackTool[fallback_tool<br/>Available to All Agents]
    SchemaError --> FallbackTool
    
    FallbackTool --> FallbackJSON[Generate Fallback JSON<br/>Graceful Error Response]
    
    Next -->|Last Agent?| Final[Final Output]
    Next -->|Not Last| NextAgent[Next Agent in Pipeline]
    NextAgent --> Try
    
    subgraph "Timeout Protection"
        TimeoutCheck{Time < 55s?}
        TimeoutCheck -->|Yes| Continue[Continue Execution]
        TimeoutCheck -->|No| TimeoutFallback[Timeout Fallback JSON<br/>score=82]
    end
    
    Final --> TimeoutCheck
    FallbackJSON --> TimeoutCheck
    Continue --> Final
    TimeoutFallback --> End[Return to User]
    Final --> End
    
    classDef errorStyle fill:#ffe1e1,stroke:#333,stroke-width:2px
    
    class FallbackTool,TimeoutFallback,FallbackJSON errorStyle
```

## 7. Job Selection Logic Flow

```mermaid
graph TD
    Query[Job Query Input] --> CheckDemo{Starts with<br/>'DEMO:'?}
    
    CheckDemo -->|Yes| Default[Return Default Job<br/>from job_map.json]
    CheckDemo -->|No| ExactMatch{Exact Category<br/>Match?}
    
    ExactMatch -->|Yes| ExactURL[Return URLs from<br/>Matched Category]
    ExactMatch -->|No| FuzzyMatch{Fuzzy Match<br/>via Tags?}
    
    FuzzyMatch -->|Yes| FuzzyURL[Return URLs from<br/>Matched Category]
    FuzzyMatch -->|No| Fallback[Return Default Job<br/>from job_map.json]
    
    Default --> Result{Result:<br/>primary_url<br/>backup_url}
    ExactURL --> Result
    FuzzyURL --> Result
    Fallback --> Result
    
    Result --> Extractor[Job Extractor Agent]
    
    classDef defaultStyle fill:#d4edda,stroke:#333,stroke-width:2px
    classDef resultStyle fill:#e1f5ff,stroke:#333,stroke-width:2px
    
    class Default,Fallback defaultStyle
    class Result resultStyle
```

## 8. Scoring Algorithm Flow

```mermaid
graph LR
    Resume[Parsed Resume] --> Skills[Resume Skills<br/>Normalized, Max 10]
    Job[Extracted Job] --> JobSkills[Job Skills<br/>Hard Skills Only, Max 10]
    
    Skills --> Overlap[calculate_skill_overlap_tool<br/>Hard Skill Overlap Ratio]
    JobSkills --> Overlap
    
    Resume --> Experience[get_experience_score_tool<br/>LLM-based Scoring<br/>0-10 Integer]
    Job --> Experience
    
    Resume --> Education[check_education_match_tool<br/>Contains bachelor/master?]
    
    Overlap --> Score[calculate_final_score_tool]
    Experience --> Score
    Education --> Score
    
    Score --> Formula[Formula:<br/>40% × skill_overlap +<br/>40% × experience_score/10 +<br/>20% × edu_match]
    
    Formula --> FinalScore[Final Match Score<br/>0-100 Integer]
    
    classDef toolStyle fill:#e1f5ff,stroke:#333,stroke-width:2px
    classDef scoreStyle fill:#d4edda,stroke:#333,stroke-width:2px
    
    class Overlap,Experience,Education toolStyle
    class Formula,FinalScore scoreStyle
```

## Usage

These diagrams can be rendered in:
- GitHub (native Mermaid support)
- Markdown viewers with Mermaid support
- Online Mermaid editors: https://mermaid.live
- Documentation tools (GitBook, Notion, etc.)

## Notes

- **Fail-Fast Behavior**: SequentialAgent stops immediately if any sub-agent fails
- **Timeout Protection**: Global 55-second timeout enforced at pipeline level
- **Schema Validation**: All JSON outputs validated before passing to next agent
- **Fallback Mechanism**: Each agent has access to `fallback_tool` for graceful error handling
- **ADK Integration**: Uses ADK's `load_web_page` tool for ATS browsing (no external libraries)
- **Memory Enabled**: `InMemoryMemoryService` provides debugging and state tracking

