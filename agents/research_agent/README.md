# Multi-Agent Research System

A collaborative multi-agent system built with LangGraph and LangChain that provides high-quality, well-researched answers with sources.

## Overview

This system uses multiple specialized AI agents that collaborate to answer complex questions:

- **Researcher Agent**: Searches the web and gathers relevant information
- **Analyst Agent**: Analyzes and evaluates the gathered information
- **Writer Agent**: Synthesizes findings into a coherent, well-reasoned answer

## Features

- Multi-agent collaboration for comprehensive answers
- Web search integration for up-to-date information
- Source citation and verification
- Reasoning transparency

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     - OpenAI API key (for LLM)
     - Tavily API key (for web search)

3. **Run the system**:
   ```bash
   python main.py
   ```

## Usage

```python
from agents.graph import create_research_graph

# Create the agent graph
graph = create_research_graph()

# Ask a question
question = "What are the latest developments in quantum computing?"
result = graph.invoke({"question": question})

print(result["answer"])
print("Sources:", result["sources"])
```

## Project Structure

```
research_agent/
├── agents/
│   ├── __init__.py
│   ├── researcher.py    # Web search and information gathering
│   ├── analyst.py       # Information analysis and evaluation
│   ├── writer.py        # Answer synthesis
│   └── graph.py         # LangGraph orchestration
├── tests/               # Comprehensive unit tests
│   ├── __init__.py
│   ├── test_researcher.py
│   ├── test_analyst.py
│   ├── test_writer.py
│   ├── test_graph.py
│   └── README.md        # Testing documentation
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── pytest.ini           # Test configuration
├── .env.example         # Environment template
└── README.md           # Documentation
```

## Testing

Run the comprehensive test suite with 100% code coverage:

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=agents --cov-report=term-missing

# Run specific test file
pytest tests/test_researcher.py -v
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Requirements

- Python 3.9+
- OpenAI API key
- Tavily API key (for web search)

## License

MIT
