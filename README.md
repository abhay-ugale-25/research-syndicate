# 🔬 Research Syndicate

Research Syndicate is a decentralized multi-agent system designed to automate rigorous academic research. Built with LangGraph, FastAPI, and Gemini, it orchestrates specialized AI agents to autonomously investigate complex topics, evaluate source quality, and synthesize fully-cited, peer-reviewed reports.

## 🧠 System Architecture

The system utilizes a directed acyclic graph (DAG) to route tasks between isolated micro-workers. It features an intelligent self-correcting loop that forces the system to re-plan if retrieved sources fail to meet academic standards.

* **Planner Node (`plan_research`):** Acts as a Senior Data Scientist. Decomposes the overarching topic into 3-5 highly specific, academic search queries designed to find peer-reviewed literature.
* **Search Node (`execute_search`):** The execution engine. Utilizes the Tavily API to scrape academic domains (arXiv, Springer, IEEE, Nature, etc.) based on the planner's queries.
* **Judge Node (`judge_sources`):** A strict academic peer-reviewer. Evaluates the retrieved HTML/text against a rigorous rubric, penalizing marketing material and rewarding dense technical documentation. 
* **Writer Node (`write_report`):** The synthesis engine. Consolidates the approved data into a comprehensive Markdown report, complete with inline numbered citations and a dedicated references section.

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI
* **Agent Orchestration:** LangGraph & LangChain Core
* **LLM Engine:** Google Gemini (2.5-Flash)
* **Search API:** Tavily Client

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abhay-ugale-25/research-syndicate.git
   cd research-syndicate
   ```

2. **Set up the environment:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 🚀 Usage Guide

You can interact with the Research Syndicate via the terminal or as a REST API.

### Option 1: Command Line Interface (CLI)
Run the state machine directly in your terminal. It will output the graph execution steps and render the final Markdown report using `rich`.

```bash
python main.py
```

### Option 2: REST API (FastAPI)
Launch the application as a web service.

```bash
uvicorn api:api --host 0.0.0.0 --port 8000
```
**Endpoint:** `POST /research`

**Payload:**
```json
{
  "topic": "Your research topic here"
}
```

### Option 3: Docker Deployment
For isolated execution, you can containerize the application. 

```bash
# Build the image
docker build -t research-syndicate .

# Run the container
docker run -d -p 8000:8000 --env-file .env research-syndicate
```

## 📂 Project Structure

* `/agents`: Contains the core logic and prompts for individual agent nodes (`agent.py`).
* `/config`: Defines the strict data schemas (`PlannerOutput`, `JudgeOutput`) and the global `ResearchState` shared memory object (`structure.py`).
* `/tools`: Houses the orchestration logic, node registration, and conditional routing to execute the LangGraph workflow (`route.py`).
* `api.py`: FastAPI endpoints.
* `main.py`: CLI execution script.
