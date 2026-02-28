from fastapi import FastAPI
from pydantic import BaseModel
from tools.route import app as graph_app

class research_query(BaseModel):
    topic: str

api = FastAPI(
    title="Research Syndicate",
    description="A multi agent research app."
)

@api.post("/research")
def start_app(request: research_query):
    inital_state = {
        'topic': request.topic,
        'search_queries': [],
        'raw_sources': [],
        'quality_score': 0.0,
        'final_report': '',
        'iteration_count': 0,
        'judge_feedback': '' 
    }

    research = graph_app.invoke(inital_state, config={"recursion_limit": 5})

    return {"report": research['final_report']}