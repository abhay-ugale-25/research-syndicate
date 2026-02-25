# 🗂️ State & Schema Configuration (`structure.py`)

**Purpose:** This file acts as the foundational blueprint for the multi-agent system's data architecture. It strictly defines the "shared memory" that is passed between nodes and enforces the data shapes returned by the LLMs.

**Key Components:**
* `ResearchState (TypedDict)`: The global state object. It tracks the overarching topic, accumulates search queries and raw HTML/text sources (using `operator.add` to prevent overwriting), records the evaluation score, and stores the final synthesized report. It also includes tracking for iteration counts and feedback to support self-correcting loops.
* `PlannerOutput & JudgeOutput (Pydantic)`: Structured data models utilized by the `with_structured_output` methods. These guarantee that the LLMs return strictly formatted JSON (lists or floats) rather than conversational text, enabling programmatic routing.