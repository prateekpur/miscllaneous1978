# Test Suite for Multi-Agent Research System

Comprehensive unit tests for all agents and graph orchestration.

## Running Tests

### Run all tests:

```bash
pytest tests/
```

### Run with verbose output:

```bash
pytest tests/ -v
```

### Run with coverage report:

```bash
pytest tests/ --cov=agents --cov-report=term-missing
```

### Run specific test file:

```bash
pytest tests/test_researcher.py -v
pytest tests/test_analyst.py -v
pytest tests/test_writer.py -v
pytest tests/test_graph.py -v
```

### Run specific test:

```bash
pytest tests/test_researcher.py::TestResearcherAgent::test_research_generates_queries -v
```

## Test Coverage

Current test coverage: **100%** across all agent modules

- `agents/researcher.py` - 100%
- `agents/analyst.py` - 100%
- `agents/writer.py` - 100%
- `agents/graph.py` - 100%

## Test Structure

### Researcher Agent Tests (`test_researcher.py`)

- ✅ Agent creation and API key validation
- ✅ Query generation from questions
- ✅ Web search execution
- ✅ Result aggregation from multiple queries
- ✅ Error handling for failed searches
- ✅ Query limiting (max 3 queries)

### Analyst Agent Tests (`test_analyst.py`)

- ✅ Agent creation
- ✅ Analysis generation from search results
- ✅ Key findings extraction
- ✅ Search result formatting
- ✅ Empty results handling
- ✅ Bullet point parsing
- ✅ Content truncation
- ✅ Missing field handling

### Writer Agent Tests (`test_writer.py`)

- ✅ Agent creation
- ✅ Answer generation
- ✅ Source formatting and citation
- ✅ Component integration (question, analysis, results)
- ✅ Empty data handling
- ✅ Content truncation
- ✅ Temperature setting verification
- ✅ Sequential source numbering

### Graph Orchestration Tests (`test_graph.py`)

- ✅ Graph creation and compilation
- ✅ Workflow execution order
- ✅ State propagation between agents
- ✅ Node and edge definitions
- ✅ Convenience function (`run_research`)
- ✅ Minimal state handling

## Test Fixtures

All tests use mocks for external dependencies:

- **LangChain LLM**: Mocked to avoid API calls
- **Tavily Search**: Mocked to avoid web requests
- **Responses**: Pre-defined realistic mock responses

## Continuous Integration

Tests are designed to run in CI/CD pipelines without requiring API keys.

## Adding New Tests

When adding new functionality:

1. Create test methods in appropriate test file
2. Use existing fixtures or create new ones
3. Follow naming convention: `test_<functionality>`
4. Ensure mocks are properly configured
5. Run tests to verify coverage remains at 100%

Example:

```python
def test_new_feature(self, mock_llm, sample_state):
    """Test description."""
    agent = create_agent()
    result = agent(sample_state)

    assert "expected_key" in result
    assert isinstance(result["expected_key"], expected_type)
```
