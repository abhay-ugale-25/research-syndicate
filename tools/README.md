# 🔄 Graph Orchestration & Routing (`route.py`)

**Purpose:** This file is the brain of the state machine. It imports the isolated agent functions and wires them together into a cyclical, directed acyclic graph (DAG) using LangGraph.

**Key Components:**
* **Node Registration:** Maps the standard Python functions from `agent.py` to official graph nodes.
* **Deterministic Edges:** Defines the guaranteed transitions of the workflow (e.g., the Planner always hands off to the Searcher).
* **Conditional Routing (`routing_research`):** The core intelligent loop. This function acts as a traffic controller, evaluating the `quality_score` produced by the Judge node. If the score is >= 0.8, it routes to the Writer node. If it falls below the threshold, it forces the system back to the Planner node for autonomous self-correction.
* **Graph Compilation:** Locks the architecture into an executable application (`app = flow.compile()`).