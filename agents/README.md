# 🤖 Agent Logic & Node Execution (`agent.py`)

**Purpose:** This file contains the individual micro-workers (nodes) that execute the cognitive and physical tasks of the research syndicate. All node functions are implemented asynchronously (`async def`) using `await model.ainvoke()` for high-throughput, non-blocking execution within the LangGraph workflow.

**Key Components:**
* `plan_research`: The reasoning engine. Decomposes the user's topic into 3–5 targeted academic search queries. On retry cycles, it dynamically incorporates previous `judge_feedback` into the prompt to autonomously refine search strategy.
* `execute_search`: The execution tool. Uses `AsyncTavilyClient` to concurrently query Tavily with `asyncio.gather`, restricting searches to an academic domain whitelist (`arxiv.org`, `ieeexplore.ieee.org`, `nature.com`, `springer.com`, `sciencedirect.com`, `researchgate.net`).
* `judge_sources`: The evaluation engine. Grades accumulated sources against academic rigor rubrics, increments `iteration_count`, and generates actionable `feedback` to steer query refinement if quality falls below threshold.
* `write_report`: The synthesis engine. Consolidates approved research data into a comprehensive Markdown report with strict inline numbered citations (`[1]`, `[2]`) and a terminal `## References` section mapping numbers to source URLs.