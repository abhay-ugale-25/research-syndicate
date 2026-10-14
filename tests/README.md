# 🧪 Automated Test Suite (`tests/`)

**Purpose:** This directory contains the automated test suite for Research Syndicate. Built with `pytest`, `pytest-mock`, and FastAPI's `TestClient`, it provides fast, deterministic test coverage for API payload validation, response serialization, state routing, and circuit breaker safety without making live external API calls.

**Key Test Modules:**
* `test_api.py`:
  * **Payload Validation:** Tests input sanitization on `POST /research` to verify that empty strings, whitespace-only queries, short queries (< 3 chars), and oversized topics (> 500 chars) are rejected with `HTTP 422 Unprocessable Entity`.
  * **Mocked End-to-End Pipeline:** Uses `pytest-mock` to mock `ChatGoogleGenerativeAI` (`with_structured_output`, `ainvoke`) and `AsyncTavilyClient`, validating source accumulation, execution timing, quality scoring, and response model serialization (`HTTP 200 OK`).
* `test_route.py`:
  * **Conditional Routing:** Tests the `routing_research` function to verify correct routing between `planner_node` and `writer_node`.
  * **Quality Threshold:** Validates that `quality_score < 0.8` routes back to `planner_node` when under the iteration limit, while `quality_score >= 0.8` proceeds to `writer_node`.
  * **Circuit Breaker:** Validates that reaching `iteration_count >= MAX_ITERATIONS (3)` forces routing to `writer_node` regardless of quality score, preventing infinite loops.

**Running the Tests:**
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test module
pytest tests/test_api.py
pytest tests/test_route.py
```
