from langgraph.graph import StateGraph, START, END
from agents.agent import plan_research, execute_search, judge_sources, write_report
from config.structure import ResearchState

flow = StateGraph(ResearchState)
flow.add_node("planner_node", plan_research)
flow.add_node("search_node", execute_search)
flow.add_node("judge_node", judge_sources)
flow.add_node("writer_node", write_report)

def routing_research(state: ResearchState):
    if state["quality_score"] >= 0.8:
        return "writer_node"
    else:
        return "planner_node"

flow.add_edge(START, "planner_node")
flow.add_edge("planner_node", "search_node")
flow.add_edge("search_node", "judge_node")
flow.add_conditional_edges("judge_node", routing_research)
flow.add_edge("writer_node", END)

app = flow.compile()