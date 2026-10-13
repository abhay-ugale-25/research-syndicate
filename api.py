import time
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

load_dotenv()  
from tools.route import app as graph_app

class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The academic or technical topic to research."
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Topic cannot be empty or contain only whitespace.")
        if len(trimmed) < 3:
            raise ValueError("Topic must be at least 3 characters long after trimming whitespace.")
        return trimmed

# Backwards compatibility alias
research_query = ResearchRequest

class ResearchResponse(BaseModel):
    report: str = Field(description="Synthesized markdown research report with citations.")
    total_sources: int = Field(description="Total count of raw sources retrieved across iterations.")
    execution_time_seconds: float = Field(description="Total execution time of the research pipeline in seconds.")
    quality_score: float = Field(default=0.0, description="Final quality score evaluated by the judge.")
    iteration_count: int = Field(default=0, description="Total number of research iterations executed.")

api = FastAPI(
    title="Research Syndicate",
    description="A multi agent research app."
)

@api.post("/research", response_model=ResearchResponse)
async def start_app(request: ResearchRequest):
    initial_state = {
        'topic': request.topic,
        'search_queries': [],
        'raw_sources': [],
        'quality_score': 0.0,
        'final_report': '',
        'iteration_count': 0,
        'judge_feedback': '' 
    }

    start_time = time.perf_counter()
    research = await graph_app.ainvoke(initial_state, config={"recursion_limit": 15})
    execution_time = round(time.perf_counter() - start_time, 2)

    raw_sources = research.get("raw_sources") or []

    return ResearchResponse(
        report=research.get("final_report", ""),
        total_sources=len(raw_sources),
        execution_time_seconds=execution_time,
        quality_score=research.get("quality_score", 0.0),
        iteration_count=research.get("iteration_count", 0)
    )
