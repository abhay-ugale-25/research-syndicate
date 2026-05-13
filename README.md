# Research Syndicate

If you want to research a highly technical topic, you usually have to dig through dozens of Google search pages, skip past SEO marketing blogs, and manually parse complex whitepapers. It takes hours of manual filtering just to find reliable information.

Research Syndicate automates that entire workflow. It is a headless, multi-agent system built on LangGraph that acts like a strict team of academic researchers. You give it a topic, and the agents work in a loop to find, verify, and summarize peer-reviewed data into a cited report.

### How the Swarm Works

Instead of relying on a single prompt, the architecture uses a cyclical graph of specialized nodes. They check each other's work to prevent hallucinations.

1. **The Planner:** Takes the user's topic and writes highly specific search queries designed to pull from academic databases (like arXiv or IEEE) rather than generic websites.
2. **The Scraper:** Uses the Tavily API to extract the raw text from those specific sources.
3. **The Judge (Quality Control):** This node acts as a strict reviewer. It grades the retrieved sources. If it spots marketing fluff or irrelevant data, it fails the search and routes the system back to the Planner to generate better queries.
4. **The Writer:** Once the Judge approves the sources (score of 0.8 or higher), this final agent synthesizes the raw data into a clean Markdown report with strict inline URL citations.

### The Tech Stack

* **Agent Orchestration:** LangGraph / LangChain
* **LLM Engine:** Google Gemini 2.5 Flash
* **Search API:** Tavily
* **Backend Framework:** FastAPI
* **Deployment:** Docker

### Hitting the Endpoint

**POST** `/research`

**Payload:**

```json
{
  "topic": "What is the current state of multi-agent reinforcement learning in 2026?"
}

```

**Response:**

```json
{
  "report": "# Multi-Agent Reinforcement Learning: 2026 Landscape\n\nMulti-agent reinforcement learning (MARL) has seen massive shifts... [1]. \n\n## References\n[1] https://arxiv.org/abs/..."
}

```

### Getting it Running Locally

The easiest way to spin this up is using Docker.

First, create a `.env` file at the root with your keys:

```env
GOOGLE_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key

```

Then, build and run the container:

```bash
docker build -t research-syndicate .
docker run -p 8000:8000 --env-file .env research-syndicate

```

If you prefer to run it bare-metal, just install the `requirements.txt` and run `uvicorn api:api --reload`.
You can test the agentic loop directly at `http://127.0.0.1:8000/docs`.
