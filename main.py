from rich.console import Console
from rich.markdown import Markdown
from tools.route import app

if __name__ == "__main__":
    console = Console()
    inital_state = {
        'topic': 'What is the current state of agentic AI in 2026?',
        'search_queries': [],
        'raw_sources': [],
        'quality_score': 0.0,
        'final_report': '',
        'iteration_count': 0,
        'judge_feedback': '' 
    }
    
    console.print(f"Graph is running for topic: {inital_state['topic']}")
    console.print(f"It may take a few minutes to generate the report. Please be patient.")
    result = app.invoke(inital_state, config={"recursion_limit": 5})
    console.print(Markdown(result["final_report"]))