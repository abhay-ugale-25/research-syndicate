import operator
from typing import List, Annotated, TypedDict
from pydantic import BaseModel, Field

class ResearchState(TypedDict):
    topic: str
    search_queries: List[str]
    raw_sources: Annotated[List[dict], operator.add]
    quality_score: float
    final_report: str
    iteration_count: int
    judge_feedback: str
    
class PlannerOutput(BaseModel):
    search_queries: List[str] = Field(description="A list of 3 to 5 highly specific, academic search engine queries based on the user's topic.")

class JudgeOutput(BaseModel):
    quality_score: float = Field(description="This is a score between 0.0 to 1.0 evaluating academic rigor of provided sources.")
