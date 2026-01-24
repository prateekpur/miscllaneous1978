"""Unit tests for the researcher agent."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.researcher import create_researcher_agent, ResearcherState


# Mock config before importing
@pytest.fixture(autouse=True)
def mock_config():
    """Mock config module."""
    with patch('agents.researcher.config') as mock_cfg:
        mock_cfg.LLM_MODEL = "gpt-4"
        mock_cfg.RESEARCHER_TEMPERATURE = 0
        mock_cfg.MAX_SEARCH_QUERIES = 3
        mock_cfg.MAX_RESULTS_PER_QUERY = 3
        mock_cfg.get_tavily_api_key = Mock(return_value="test-key")
        yield mock_cfg


class TestResearcherAgent:
    """Test suite for the researcher agent."""
    
    @pytest.fixture
    def mock_tavily_client(self):
        """Mock Tavily client."""
        with patch('agents.researcher.TavilyClient') as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            yield mock_instance
    
    @pytest.fixture
    def mock_llm(self):
        """Mock LangChain LLM."""
        # Import SearchQueries for creating mock response
        from utils import SearchQueries
        
        with patch('agents.researcher.ChatOpenAI') as mock_chat:
            # Mock the chain (prompt | llm | parser)
            mock_chain = MagicMock()
            
            # Create actual SearchQueries object instead of mock
            mock_response = SearchQueries(
                queries=["quantum computing advances", "quantum algorithms 2026", "quantum hardware developments"]
            )
            mock_chain.invoke.return_value = mock_response
            
            # Mock the prompt template to return a chain when piped
            with patch('agents.researcher.ChatPromptTemplate') as mock_prompt, \
                 patch('agents.researcher.PydanticOutputParser') as mock_parser:
                mock_prompt_instance = MagicMock()
                mock_prompt.from_messages.return_value = mock_prompt_instance
                # When you pipe prompt | llm, it should return something that can be piped again
                mock_intermediate = MagicMock()
                mock_intermediate.__or__ = MagicMock(return_value=mock_chain)
                mock_prompt_instance.__or__ = MagicMock(return_value=mock_intermediate)
                
                mock_parser_instance = MagicMock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.get_format_instructions.return_value = "Format instructions"
                
                yield mock_chat
    
    @pytest.fixture
    def sample_search_results(self):
        """Sample search results from Tavily."""
        return {
            "results": [
                {
                    "title": "Quantum Computing Breakthrough 2026",
                    "url": "https://example.com/quantum1",
                    "content": "Major advances in quantum computing were announced...",
                    "score": 0.95
                },
                {
                    "title": "New Quantum Algorithm",
                    "url": "https://example.com/quantum2",
                    "content": "Researchers developed a new quantum algorithm...",
                    "score": 0.88
                }
            ]
        }
    
    def test_create_researcher_agent_success(self, mock_tavily_client, mock_llm, mock_config):
        """Test successful creation of researcher agent."""
        researcher = create_researcher_agent()
        assert callable(researcher)
    
    def test_create_researcher_agent_missing_api_key(self, mock_config):
        """Test that missing API key raises ValueError."""
        mock_config.get_tavily_api_key = Mock(return_value=None)
        with pytest.raises(ValueError, match="TAVILY_API_KEY not found"):
            create_researcher_agent()
    
    def test_research_generates_queries(self, mock_tavily_client, mock_llm, mock_config, sample_search_results):
        """Test that research function generates search queries."""
        mock_tavily_client.search.return_value = sample_search_results
        
        researcher = create_researcher_agent()
        state = {"question": "What are the latest developments in quantum computing?"}
        
        result = researcher(state)
        
        # Check that queries were generated
        assert "search_queries" in result
        assert len(result["search_queries"]) > 0
        assert isinstance(result["search_queries"], list)
    
    def test_research_performs_searches(self, mock_tavily_client, mock_llm, mock_config, sample_search_results):
        """Test that research function performs web searches."""
        mock_tavily_client.search.return_value = sample_search_results
        
        researcher = create_researcher_agent()
        state = {"question": "What are the latest developments in quantum computing?"}
        
        result = researcher(state)
        
        # Verify searches were performed
        assert mock_tavily_client.search.called
        assert "search_results" in result
        assert len(result["search_results"]) > 0
    
    def test_research_aggregates_results(self, mock_tavily_client, mock_llm, mock_config, sample_search_results):
        """Test that results from multiple queries are aggregated."""
        mock_tavily_client.search.return_value = sample_search_results
        
        researcher = create_researcher_agent()
        state = {"question": "What are the latest developments in quantum computing?"}
        
        result = researcher(state)
        
        # Check that results are aggregated
        assert "search_results" in result
        # Should have results from multiple queries (3 queries * 2 results each)
        assert len(result["search_results"]) >= 2
    
    def test_research_handles_search_errors(self, mock_tavily_client, mock_llm, mock_config):
        """Test that search errors are handled gracefully."""
        # Mock search to raise an exception
        mock_tavily_client.search.side_effect = Exception("API Error")
        
        researcher = create_researcher_agent()
        state = {"question": "Test question"}
        
        # Should not raise exception
        result = researcher(state)
        
        # Should return empty results
        assert "search_results" in result
        assert result["search_results"] == []
    
    def test_research_limits_queries(self, mock_tavily_client, mock_llm, mock_config, sample_search_results):
        """Test that number of queries is limited."""
        # Mock parser to return many queries
        with patch('agents.researcher.PydanticOutputParser') as mock_parser:
            mock_chain = MagicMock()
            mock_response = MagicMock()
            mock_response.queries = [f"Query {i}" for i in range(10)]
            mock_chain.invoke.return_value = mock_response
            
            mock_parser_instance = MagicMock()
            mock_parser.return_value = mock_parser_instance
            mock_parser_instance.get_format_instructions.return_value = "Format instructions"
            
            with patch('agents.researcher.ChatPromptTemplate') as mock_prompt:
                mock_prompt_instance = MagicMock()
                mock_prompt.from_messages.return_value = mock_prompt_instance
                mock_prompt_instance.__or__ = MagicMock(return_value=mock_chain)
                
                mock_tavily_client.search.return_value = sample_search_results
                
                researcher = create_researcher_agent()
                state = {"question": "Test question"}
                
                result = researcher(state)
                
                # Should limit to MAX_SEARCH_QUERIES (3)
                assert len(result["search_queries"]) <= 3
    
    def test_researcher_state_type(self):
        """Test ResearcherState TypedDict structure."""
        state: ResearcherState = {
            "question": "Test question",
            "search_results": [{"title": "Test", "url": "http://test.com"}],
            "search_queries": ["query1", "query2"]
        }
        
        assert "question" in state
        assert "search_results" in state
        assert "search_queries" in state
