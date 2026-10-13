# 🔄 Graph Orchestration & Routing (`route.py`)

**Purpose:** This file is the brain of the state machine. It imports the isolated asynchronous agent functions and wires them together into a cyclical, self-correcting workflow using LangGraph.

**Key Components:**
* **Node Registration:** Maps the asynchronous Python functions from `agent.py` to official graph nodes (`planner_node`, `search_node`, `judge_node`, `writer_node`).
* **Deterministic Edges:** Defines the guaranteed transitions of the workflow (e.g., START to Planner, Planner to Search, Search to Judge, Writer to END).
* **Circuit Breaker & Conditional Routing (`routing_research`):** The core intelligent traffic controller:
  * **Success Condition:** If `quality_score >= 0.8`, routes directly to `writer_node`.
  * **Circuit Breaker:** If `iteration_count >= MAX_ITERATIONS` (capped at `3`), forces routing to `writer_node` to prevent infinite loops and ensure guaranteed completion.
  * **Self-Correction:** If the score is $< 0.8$ and iteration limit is not exceeded, routes back to `planner_node` for adaptive query regeneration with judge feedback.
* **Graph Compilation:** Compiles the flow into an executable asynchronous application (`app = flow.compile()`).