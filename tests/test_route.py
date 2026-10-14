import pytest
from tools.route import routing_research, MAX_ITERATIONS
from config.structure import ResearchState

def test_routing_research_quality_low_iteration_low():
    state = ResearchState(
        topic="test",
        search_queries=[],
        raw_sources=[],
        quality_score=0.7,
        final_report="",
        iteration_count=MAX_ITERATIONS - 1,
        judge_feedback=""
    )
    result = routing_research(state)
    assert result == "planner_node"

def test_routing_research_quality_high():
    state = ResearchState(
        topic="test",
        search_queries=[],
        raw_sources=[],
        quality_score=0.8,
        final_report="",
        iteration_count=0,
        judge_feedback=""
    )
    result = routing_research(state)
    assert result == "writer_node"

def test_routing_research_circuit_breaker():
    state = ResearchState(
        topic="test",
        search_queries=[],
        raw_sources=[],
        quality_score=0.5,
        final_report="",
        iteration_count=MAX_ITERATIONS,
        judge_feedback=""
    )
    result = routing_research(state)
    assert result == "writer_node"
