# Multi-Agent Automation Platform 🔥

A powerful, stateful multi-agent system orchestrator built with FastAPI, Vue 3, Celery, and LangGraph.

## 🌟 Features

- **Multi-Agent Workflow (LangGraph)**: Implements a `Planner -> Executor -> Reviewer` cycle.
- **LLM Integration**: Uses LangChain and OpenAI for intelligent task decomposition and execution.
- **Tool Calling**: Agents can browse the web, send emails, and post tweets (mocked).
- **Asynchronous Task Queue**: Powered by Celery and Redis to handle long-running agent workflows.
- **Persistent State**: SQLAlchemy + PostgreSQL to track task statuses and histories.
- **Modern Dashboard**: Vue 3 + Vite frontend with real-time polling to monitor agent progress.
- **Dockerized**: Easy setup using Docker Compose.

## 🚀 Quick Start (Docker)

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in your `OPENAI_API_KEY`:
   ```bash
   cp .env.example .env
   ```
3. Start the services:
   ```bash
   docker-compose up -d --build
   ```
4. Access the frontend dashboard at `http://localhost:8080`.
5. API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

## 🏗️ Architecture

- `backend/agents`: Contains Planner, Executor, and Reviewer logic.
- `backend/core`: Orchestrator utilizing LangGraph to route agent states.
- `backend/tools`: Custom tools for LLMs.
- `backend/workers`: Celery workers processing background AI tasks.
- `frontend/`: Vue 3 application.
