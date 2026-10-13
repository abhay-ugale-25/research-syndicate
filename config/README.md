# 🗂️ State & Schema Configuration (`structure.py`)

**Purpose:** This file acts as the foundational blueprint for the multi-agent system's data architecture. It strictly defines the "shared memory" that is passed between nodes and enforces the data shapes returned by the LLMs.

**Key Components:**
* `ResearchState (TypedDict)`: The global state object. It tracks the overarching topic, accumulates search queries and raw HTML/text sources (using `operator.add` to prevent overwriting), records the evaluation score, stores constructive judge critique, tracks iteration counts to power self-correcting loops and circuit breakers, and stores the final synthesized report.
* `PlannerOutput & JudgeOutput (Pydantic)`: Structured data models utilized by LLM `with_structured_output` calls. These guarantee strictly formatted data rather than conversational text:
  * `PlannerOutput`: Enforces a list of 3 to 5 targeted academic search queries.
  * `JudgeOutput`: Enforces a `quality_score` strictly bounded between `0.0` and `1.0` via `Field(ge=0.0, le=1.0)` and requires an actionable `feedback: str` field to guide query refinement on retries.