# Multi-Agent Research System - Project Instructions

## Project Overview

This is a multi-agent collaboration system built with LangGraph and LangChain that provides high-quality, well-researched answers with sources.

## Architecture

- **Researcher Agent**: Searches the web and gathers relevant information using Tavily
- **Analyst Agent**: Analyzes and evaluates the gathered information
- **Writer Agent**: Synthesizes findings into a coherent, well-reasoned answer
- **LangGraph Orchestration**: Coordinates the workflow between agents

## Development Setup

1. Python 3.9+ with virtual environment (.venv)
2. Required packages: langchain, langchain-openai, langgraph, python-dotenv, tavily-python
3. API Keys needed: OPENAI_API_KEY, TAVILY_API_KEY (in .env file)

## Running the Project

```bash
python main.py
```

## Project Structure

- `agents/` - Agent implementations
  - `researcher.py` - Web search agent
  - `analyst.py` - Analysis agent
  - `writer.py` - Synthesis agent
  - `graph.py` - LangGraph workflow
- `main.py` - Entry point
- `.env` - API keys (create from .env.example)

## Notes

- Import warnings for Pydantic V1 with Python 3.14 are expected
- VS Code may show import errors but packages are installed correctly in the virtual environment
