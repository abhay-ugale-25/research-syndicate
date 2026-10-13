import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import AsyncTavilyClient
from config.structure import ResearchState, PlannerOutput, JudgeOutput

load_dotenv()

async def plan_research(state: ResearchState):
    topic = state["topic"]
    judge_feedback = state.get("judge_feedback", "")
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
    Please generate the search queries for the following topic: {topic}
    """
    if judge_feedback:
        user_prompt += f"""
    
    PREVIOUS FEEDBACK FROM JUDGE (Address these shortcomings in the new search queries):
    {judge_feedback}
    """
    response = await model.ainvoke([("system", system_prompt), ("user", user_prompt)])
    return {"search_queries": response.search_queries}

async def execute_search(state: ResearchState):
    queries = state["search_queries"]
    tavily = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    async def search_single_query(query: str):
        tavily_response = await tavily.search(
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
        return tavily_response.get("results", [])

    results_lists = await asyncio.gather(*(search_single_query(query) for query in queries))
    all_results = [result for results in results_lists for result in results]
    return {"raw_sources": all_results}

async def judge_sources(state: ResearchState):
    topic = state["topic"]
    sources = state["raw_sources"]
    current_iteration = state.get("iteration_count", 0) + 1
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
    response = await model.ainvoke([("system", system_prompt), ("user", user_prompt)])
    return {
        "quality_score": response.quality_score,
        "judge_feedback": response.feedback,
        "iteration_count": current_iteration
    }

async def write_report(state: ResearchState):
    topic = state["topic"]
    sources = state["raw_sources"]
    formatted_sources = [f"URL: {source['url']}\nCONTENT: {source['content']}" for source in sources]
    model = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.2, api_key=os.getenv("GOOGLE_API_KEY"))
    system_prompt= f"""
    You are a expert technical writer.
    Your job is to raw research sources and synthesize them into a comprehensive, well-structured Markdown report based on the user's topic.
    You should include inline citations, using URLs, whenever you state a fact.
    CRITICAL CITATION RULES:
    1. You must use inline numbered citations like [1], [2] whenever you state a fact.
    2. You MUST include a "## References" section at the absolute end of your report.
    3. In the References section, you must list every number used in the text and pair it with its exact URL from the provided sources. 
    Format the references like this: 
    [1] URL
    [2] URL
    """
    user_prompt= f"""
    topic: {topic},
    sources: {formatted_sources}
    """
    response = await model.ainvoke([("system", system_prompt), ("user", user_prompt)])
    return {"final_report": response.content}