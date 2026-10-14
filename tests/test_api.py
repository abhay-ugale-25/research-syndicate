import pytest
from fastapi.testclient import TestClient
from api import api
from unittest.mock import AsyncMock

client = TestClient(api)

# Test payload validation
def test_post_research_empty_topic():
    response = client.post("/research", json={"topic": ""})
    assert response.status_code == 422

def test_post_research_whitespace_topic():
    response = client.post("/research", json={"topic": "   "})
    assert response.status_code == 422

def test_post_research_short_topic():
    response = client.post("/research", json={"topic": "AI"})
    assert response.status_code == 422

def test_post_research_long_topic():
    response = client.post("/research", json={"topic": "A" * 501})
    assert response.status_code == 422

@pytest.fixture
def mock_external_apis(mocker):
    # Mock ChatGoogleGenerativeAI
    mock_llm = mocker.patch("agents.agent.ChatGoogleGenerativeAI", autospec=True)
    mock_model = AsyncMock()

    # Configure mock responses for with_structured_output and standard ainvoke
    def mock_with_structured_output(schema):
        mock_structured_model = AsyncMock()
        if schema.__name__ == "PlannerOutput":
            mock_structured_model.ainvoke.return_value = mocker.Mock(search_queries=["query 1", "query 2"])
        elif schema.__name__ == "JudgeOutput":
            mock_structured_model.ainvoke.return_value = mocker.Mock(quality_score=0.9, feedback="Good")
        return mock_structured_model

    mock_llm.return_value.with_structured_output.side_effect = mock_with_structured_output

    # Writer output
    mock_llm.return_value.ainvoke.return_value = mocker.Mock(content="# Final Report")

    # Mock AsyncTavilyClient
    mock_tavily = mocker.patch("agents.agent.AsyncTavilyClient", autospec=True)
    mock_tavily.return_value.search = AsyncMock(return_value={"results": [{"url": "http://example.com", "content": "Sample content"}]})

    return mock_llm, mock_tavily

def test_post_research_success(mock_external_apis):
    response = client.post("/research", json={"topic": "Machine Learning"})
    assert response.status_code == 200
    data = response.json()
    assert data["report"] == "# Final Report"
    assert data["total_sources"] == 2 # 2 queries, each returning 1 result
    assert "execution_time_seconds" in data
    assert data["quality_score"] == 0.9
    assert data["iteration_count"] == 1
