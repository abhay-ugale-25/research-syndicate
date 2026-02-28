from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from config.structure import ResearchState, PlannerOutput, JudgeOutput
import os
from dotenv import load_dotenv

load_dotenv()

def plan_research(state: ResearchState):
    bulletin_board = state["topic"]
    gen_ai = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=os.getenv("GOOGLE_API_KEY"))    
    model = gen_ai.with_structured_output(PlannerOutput)
    system_prompt = f"""
    You are a senior-level data scientist architecting a rigorous research sprint. 
    Your only job is to look at the user's research topic and break it down into 3 to 5 highly specific, academic search queries. Do not answer the user's topic. 
    Do not write a report. 
    Only generate the search terms needed to find the best peer-reviewed papers and technical documentation.
    CRITICAL RULE: You must design these queries to find peer-reviewed research papers, NOT blogs. 
    Append terms like "arxiv", "IEEE", "research paper", "abstract", or "DOI" to your queries to force the search engine to return academic literature.
    """
    user_prompt = f"""
    Please generate the search queries for the following topic: {bulletin_board}
    """
    response = model.invoke([("system", system_prompt), ("user", user_prompt)])
    return {"search_queries": response.search_queries}

def execute_search(state: ResearchState):
    queries = state["search_queries"]
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    all_results = []
    for query in queries:
        tavily_response = tavily.search(
            query=query,
            max_results=5,
            search_depth='advanced',
            include_domains=[
                "arxiv.org", 
                "springer.com", 
                "sciencedirect.com", 
                "ieeexplore.ieee.org", 
                "researchgate.net",
                "nature.com"
            ]
        )
        all_results.extend(tavily_response["results"])
    return {"raw_sources": all_results}

def judge_sources(state: ResearchState):
    topic = state["topic"]
    sources = state["raw_sources"]
    formatted_sources = [f"URL: {source['url']}\nCONTENT: {source['content']}" for source in sources]
    gen_ai = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0, api_key=os.getenv("GOOGLE_API_KEY"))
    model = gen_ai.with_structured_output(JudgeOutput)
    system_prompt= f"""
    You are a strict academic peer-reviewer. 
    Your job is to evaluate if the provided research sources adequetly and accuractely cover the assigned topic.
    Points should be deducted for:
    - Marketing Material
    - Outdated Infromation
    - Irrelevant data
    
    Points should be added for:
    - Peer-reviewed papers
    - Deep Learning Documentation
    - Dense Techincal Content
    - Highly technical blog posts, technical articles, and whitepapers, similar content.
    """
    user_prompt= f"""
    topic: {topic},
    sources: {formatted_sources}
    """
    response = model.invoke([("system", system_prompt), ("user", user_prompt)])
    return {"quality_score": response.quality_score}

def write_report(state: ResearchState):
    topic = state["topic"]
    sources = state["raw_sources"]
    formatted_sources = [f"URL: {source['url']}\nCONTENT: {source['content']}" for source in sources]
    model = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.2, api_key=os.getenv("GOOGLE_API_KEY"))
    system_prompt= f"""
    You are a expert technical writer.
    Your job is to raw research sources and synthesize them into a comprehensive, well-structured Markdown report based on the user's topic.
    You should include inline citations, using URLs, whenever you state a fact.
    """
    user_prompt= f"""
    topic: {topic},
    sources: {formatted_sources}
    """
    response = model.invoke([("system", system_prompt), ("user", user_prompt)])
    return {"final_report": response.content}