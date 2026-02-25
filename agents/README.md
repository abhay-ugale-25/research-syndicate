# 🤖 Agent Logic & Node Execution (`agent.py`)

**Purpose:** This file contains the individual micro-workers (nodes) that execute the cognitive and physical tasks of the research syndicate. Each function represents an isolated capability within the LangGraph workflow.

**Key Components:**
* `plan_research`: The reasoning engine. Acts as a Senior Data Scientist to decompose the user's topic into highly targeted, academic search queries.
* `execute_search`: The execution tool. Connects to the Tavily API to autonomously scrape the web based on the Planner's queries, utilizing advanced search depth to retrieve technical documentation.
* `judge_sources`: The evaluation engine. Acts as a strict academic peer-reviewer to grade the retrieved sources against a rigorous rubric, ensuring only high-quality data passes to the final stage.
* `write_report`: The synthesis engine. Consolidates the approved research data into a comprehensive, fully-cited Markdown report.