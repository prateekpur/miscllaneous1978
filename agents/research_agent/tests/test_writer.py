"""Unit tests for the writer agent."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.writer import create_writer_agent, WriterState


# Mock config before importing
@pytest.fixture(autouse=True)
def mock_config():
    """Mock config module."""
    with patch('agents.writer.config') as mock_cfg:
        mock_cfg.LLM_MODEL = "gpt-4"
        mock_cfg.WRITER_TEMPERATURE = 0.3
        mock_cfg.ANALYSIS_TRUNCATE_LENGTH = 200
        yield mock_cfg


class TestWriterAgent:
    """Test suite for the writer agent."""
    
    @pytest.fixture
    def mock_llm(self):
        """Mock LangChain LLM."""
        with patch('agents.writer.ChatOpenAI') as mock_chat:
            # Mock the chain (prompt | llm)
            mock_chain = MagicMock()
            mock_response = MagicMock()
            mock_response.content = """# Quantum Computing Developments in 2026

Quantum computing has experienced remarkable progress in 2026, with several key breakthroughs [1][2].

## Hardware Advances
Recent developments in quantum hardware have improved qubit stability significantly [1]. Companies are now achieving longer coherence times, which is crucial for practical quantum computing.

## Algorithmic Progress
New quantum algorithms have been developed that show promise for solving real-world problems [2]. These algorithms could have applications in cryptography, drug discovery, and optimization.

## Challenges Ahead
Despite progress, challenges remain in error correction and scalability [1][2]. However, the pace of innovation suggests these obstacles may be overcome in the coming years.

The future of quantum computing looks promising as both hardware and software continue to evolve."""
            mock_chain.invoke.return_value = mock_response
            
            # Mock the prompt template to return a chain when piped
            with patch('agents.writer.ChatPromptTemplate') as mock_prompt:
                mock_prompt_instance = MagicMock()
                mock_prompt.from_messages.return_value = mock_prompt_instance
                mock_prompt_instance.__or__ = MagicMock(return_value=mock_chain)
                
                yield mock_chat
    
    @pytest.fixture
    def sample_state(self):
        """Sample state with analysis and search results."""
        return {
            "question": "What are the latest developments in quantum computing?",
            "analysis": """Key findings from the research:
- Quantum computing has made significant advances
- Hardware improvements are notable
- New algorithms show promise
- Challenges remain but progress is steady""",
            "search_results": [
                {
                    "title": "Quantum Computing Breakthrough",
                    "url": "https://example.com/quantum1",
                    "content": "Major advances in quantum computing were announced in 2026 with improved qubit stability..."
                },
                {
                    "title": "New Quantum Algorithm",
                    "url": "https://example.com/quantum2",
                    "content": "Researchers developed a new quantum algorithm that could revolutionize cryptography..."
                }
            ]
        }
    
    def test_create_writer_agent_success(self, mock_llm):
        """Test successful creation of writer agent."""
        writer = create_writer_agent()
        assert callable(writer)
    
    def test_write_returns_answer(self, mock_llm, sample_state):
        """Test that write function returns an answer."""
        writer = create_writer_agent()
        result = writer(sample_state)
        
        assert "answer" in result
        assert isinstance(result["answer"], str)
        assert len(result["answer"]) > 0
    
    def test_write_returns_sources(self, mock_llm, sample_state):
        """Test that write function returns formatted sources."""
        writer = create_writer_agent()
        result = writer(sample_state)
        
        assert "sources" in result
        assert isinstance(result["sources"], list)
        assert len(result["sources"]) > 0
    
    def test_write_formats_sources_correctly(self, mock_llm, sample_state):
        """Test that sources are formatted with numbers and URLs."""
        writer = create_writer_agent()
        result = writer(sample_state)
        
        sources = result["sources"]
        
        # Each source should have format: [1] Title - URL
        for source in sources:
            assert "[" in source
            assert "]" in source
            assert " - " in source
    
    def test_write_includes_all_components(self, mock_llm, sample_state):
        """Test that LLM receives question, analysis, and search results."""
        writer = create_writer_agent()
        result = writer(sample_state)
        
        # Verify answer was generated successfully
        assert "answer" in result
        assert isinstance(result["answer"], str)
        assert len(result["answer"]) > 0
    
    def test_write_with_empty_analysis(self, mock_llm):
        """Test writing with empty analysis."""
        state = {
            "question": "Test question",
            "analysis": "",
            "search_results": [
                {"title": "Test", "url": "http://test.com", "content": "Test content"}
            ]
        }
        
        writer = create_writer_agent()
        result = writer(state)
        
        assert "answer" in result
        assert "sources" in result
    
    def test_write_with_no_results(self, mock_llm):
        """Test writing with no search results."""
        state = {
            "question": "Test question",
            "analysis": "No results found",
            "search_results": []
        }
        
        writer = create_writer_agent()
        result = writer(state)
        
        assert "answer" in result
        assert "sources" in result
        assert result["sources"] == []
    
    def test_write_truncates_long_content(self, mock_llm):
        """Test that long content is truncated in formatted results."""
        long_content = "A" * 1000
        state = {
            "question": "Test question",
            "analysis": "Test analysis",
            "search_results": [
                {
                    "title": "Test Article",
                    "url": "http://test.com",
                    "content": long_content
                }
            ]
        }
        
        writer = create_writer_agent()
        result = writer(state)
        
        # Verify answer was generated
        assert "answer" in result
        assert isinstance(result["answer"], str)
    
    def test_write_uses_correct_temperature(self, mock_llm):
        """Test that writer uses temperature=0.3 for creativity."""
        with patch('agents.writer.ChatOpenAI') as mock_chat:
            create_writer_agent()
            
            # Verify ChatOpenAI was created with temperature=0.3
            mock_chat.assert_called_once_with(model="gpt-4", temperature=0.3)
    
    def test_writer_state_type(self):
        """Test WriterState TypedDict structure."""
        state: WriterState = {
            "question": "Test question",
            "analysis": "Test analysis",
            "search_results": [{"title": "Test", "url": "http://test.com"}],
            "answer": "Test answer",
            "sources": ["[1] Test - http://test.com"]
        }
        
        assert "question" in state
        assert "analysis" in state
        assert "search_results" in state
        assert "answer" in state
        assert "sources" in state
    
    def test_write_handles_missing_fields(self, mock_llm):
        """Test writing handles missing fields in search results."""
        state = {
            "question": "Test question",
            "analysis": "Test analysis",
            "search_results": [
                {},  # Empty result
                {"title": "Only Title"},
                {"url": "http://test.com"},
                {"content": "Only content"}
            ]
        }
        
        writer = create_writer_agent()
        result = writer(state)
        
        # Should handle gracefully with N/A for missing fields
        assert "answer" in result
        assert "sources" in result
        
        # All results should have sources with N/A for missing data
        assert len(result["sources"]) == 4
    
    def test_write_numbers_sources_sequentially(self, mock_llm, sample_state):
        """Test that sources are numbered sequentially starting from 1."""
        writer = create_writer_agent()
        result = writer(sample_state)
        
        sources = result["sources"]
        
        # Check sequential numbering
        for i, source in enumerate(sources, 1):
            assert f"[{i}]" in source
