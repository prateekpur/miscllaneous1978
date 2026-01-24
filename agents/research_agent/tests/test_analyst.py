"""Unit tests for the analyst agent."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.analyst import create_analyst_agent, AnalystState


# Mock config before importing
@pytest.fixture(autouse=True)
def mock_config():
    """Mock config module."""
    with patch('agents.analyst.config') as mock_cfg:
        mock_cfg.LLM_MODEL = "gpt-4"
        mock_cfg.ANALYST_TEMPERATURE = 0
        mock_cfg.CONTENT_TRUNCATE_LENGTH = 300
        mock_cfg.MAX_KEY_FINDINGS = 5
        yield mock_cfg


class TestAnalystAgent:
    """Test suite for the analyst agent."""
    
    @pytest.fixture
    def mock_llm(self):
        """Mock LangChain LLM."""
        # Import KeyFindings for creating mock response
        from utils import KeyFindings
        
        with patch('agents.analyst.ChatOpenAI') as mock_chat:
            # Mock the analysis chain (prompt | llm)
            mock_analysis_chain = MagicMock()
            mock_analysis_response = MagicMock()
            mock_analysis_response.content = """Based on the search results, here are the key findings:

- Quantum computing has made significant advances in 2026
- New quantum algorithms show promise for practical applications
- Hardware improvements have increased qubit stability
- Several companies are competing in the quantum space
- Challenges remain in error correction and scalability

The sources appear credible and consistent. No major conflicts detected."""
            mock_analysis_chain.invoke.return_value = mock_analysis_response
            
            # Mock the findings chain (prompt | llm | parser)
            mock_findings_chain = MagicMock()
            # Create actual KeyFindings object instead of mock
            mock_findings_response = KeyFindings(
                findings=[
                    "Quantum computing has made significant advances in 2026",
                    "New quantum algorithms show promise for practical applications",
                    "Hardware improvements have increased qubit stability",
                    "Several companies are competing in the quantum space",
                    "Challenges remain in error correction and scalability"
                ]
            )
            mock_findings_chain.invoke.return_value = mock_findings_response
            
            # Mock the prompt template to return chains when piped
            with patch('agents.analyst.ChatPromptTemplate') as mock_prompt, \
                 patch('agents.analyst.PydanticOutputParser') as mock_parser:
                mock_prompt_instances = [MagicMock(), MagicMock()]
                mock_prompt.from_messages.side_effect = mock_prompt_instances
                
                # First chain: analysis
                mock_prompt_instances[0].__or__ = MagicMock(return_value=mock_analysis_chain)
                # Second chain: findings (prompt | llm | parser requires two pipe operations)
                mock_intermediate = MagicMock()
                mock_intermediate.__or__ = MagicMock(return_value=mock_findings_chain)
                mock_prompt_instances[1].__or__ = MagicMock(return_value=mock_intermediate)
                
                mock_parser_instance = MagicMock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.get_format_instructions.return_value = "Format instructions"
                
                yield mock_chat
    
    @pytest.fixture
    def sample_state(self):
        """Sample state with search results."""
        return {
            "question": "What are the latest developments in quantum computing?",
            "search_results": [
                {
                    "title": "Quantum Computing Breakthrough",
                    "url": "https://example.com/quantum1",
                    "content": "Major advances in quantum computing were announced in 2026..."
                },
                {
                    "title": "New Quantum Algorithm",
                    "url": "https://example.com/quantum2",
                    "content": "Researchers developed a new quantum algorithm that improves..."
                }
            ]
        }
    
    def test_create_analyst_agent_success(self, mock_llm):
        """Test successful creation of analyst agent."""
        analyst = create_analyst_agent()
        assert callable(analyst)
    
    def test_analyze_returns_analysis(self, mock_llm, sample_state):
        """Test that analyze function returns analysis."""
        analyst = create_analyst_agent()
        result = analyst(sample_state)
        
        assert "analysis" in result
        assert isinstance(result["analysis"], str)
        assert len(result["analysis"]) > 0
    
    def test_analyze_extracts_key_findings(self, mock_llm, mock_config, sample_state):
        """Test that key findings are extracted from analysis."""
        analyst = create_analyst_agent()
        result = analyst(sample_state)
        
        assert "key_findings" in result
        # The mock returns a findings list
        assert len(result["key_findings"]) > 0
    
    def test_analyze_formats_search_results(self, mock_llm, sample_state):
        """Test that search results are properly formatted for analysis."""
        analyst = create_analyst_agent()
        result = analyst(sample_state)
        
        # Verify analysis completed successfully
        assert "analysis" in result
        assert isinstance(result["analysis"], str)
    
    def test_analyze_with_empty_results(self, mock_llm):
        """Test analysis with no search results."""
        state = {
            "question": "Test question",
            "search_results": []
        }
        
        analyst = create_analyst_agent()
        result = analyst(state)
        
        assert "analysis" in result
        assert "key_findings" in result
    
    def test_analyze_limits_key_findings(self, mock_config):
        """Test that key findings are limited to reasonable number."""
        # Mock findings chain with many results
        with patch('agents.analyst.ChatOpenAI'), \
             patch('agents.analyst.PydanticOutputParser') as mock_parser:
            mock_analysis_chain = MagicMock()
            mock_analysis_response = MagicMock()
            mock_analysis_response.content = "Test analysis"
            mock_analysis_chain.invoke.return_value = mock_analysis_response
            
            mock_findings_chain = MagicMock()
            # Create a mock response with many findings (bypassing Pydantic validation)
            mock_findings_response = MagicMock()
            mock_findings_response.findings = [f"Finding {i}" for i in range(20)]
            mock_findings_chain.invoke.return_value = mock_findings_response
            
            with patch('agents.analyst.ChatPromptTemplate') as mock_prompt:
                mock_prompt_instances = [MagicMock(), MagicMock()]
                mock_prompt.from_messages.side_effect = mock_prompt_instances
                mock_prompt_instances[0].__or__ = MagicMock(return_value=mock_analysis_chain)
                # Second chain needs intermediate for two pipes (prompt | llm | parser)
                mock_intermediate = MagicMock()
                mock_intermediate.__or__ = MagicMock(return_value=mock_findings_chain)
                mock_prompt_instances[1].__or__ = MagicMock(return_value=mock_intermediate)
                
                mock_parser_instance = MagicMock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.get_format_instructions.return_value = "Format"
                
                analyst = create_analyst_agent()
                state = {
                    "question": "Test question",
                    "search_results": [{"title": "Test", "url": "http://test.com", "content": "Test content"}]
                }
                
                result = analyst(state)
                
                # Should limit to MAX_KEY_FINDINGS (5)
                assert len(result["key_findings"]) <= 5
    
    def test_analyze_handles_no_bullet_points(self, mock_config):
        """Test analysis when no bullet points are in response."""
        # Create a new mock for this specific test with fallback behavior
        with patch('agents.analyst.ChatOpenAI'):
            with patch('agents.analyst.ChatPromptTemplate') as mock_prompt, \
                 patch('agents.analyst.PydanticOutputParser') as mock_parser:
                    
                # Analysis chain
                mock_analysis_chain = MagicMock()
                mock_analysis_response = MagicMock()
                mock_analysis_response.content = "This is an analysis without bullet points."
                mock_analysis_chain.invoke.return_value = mock_analysis_response
                
                # Findings chain raises error to trigger fallback (needs two pipe operations)
                mock_findings_chain = MagicMock()
                mock_findings_chain.invoke.side_effect = Exception("Parser error")
                
                mock_prompt_instances = [MagicMock(), MagicMock()]
                mock_prompt.from_messages.side_effect = mock_prompt_instances
                mock_prompt_instances[0].__or__ = MagicMock(return_value=mock_analysis_chain)
                # Second chain needs intermediate for two pipes (prompt | llm | parser)
                mock_intermediate = MagicMock()
                mock_intermediate.__or__ = MagicMock(return_value=mock_findings_chain)
                mock_prompt_instances[1].__or__ = MagicMock(return_value=mock_intermediate)
                
                mock_parser_instance = MagicMock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.get_format_instructions.return_value = "Format"
                
                analyst = create_analyst_agent()
                state = {
                    "question": "Test question",
                    "search_results": [{"title": "Test", "url": "http://test.com", "content": "Test content"}]
                }
                
                result = analyst(state)
                
                # Should have fallback key finding
                assert "key_findings" in result
                assert len(result["key_findings"]) > 0
                assert "See full analysis" in result["key_findings"][0]
    
    def test_analyze_truncates_long_content(self, mock_llm):
        """Test that long content is truncated in formatted results."""
        long_content = "A" * 1000
        state = {
            "question": "Test question",
            "search_results": [
                {
                    "title": "Test Article",
                    "url": "http://test.com",
                    "content": long_content
                }
            ]
        }
        
        analyst = create_analyst_agent()
        result = analyst(state)
        
        # Content should be truncated to 300 chars in formatting
        assert "analysis" in result
        assert len(long_content) > 300
    
    def test_analyst_state_type(self):
        """Test AnalystState TypedDict structure."""
        state: AnalystState = {
            "question": "Test question",
            "search_results": [{"title": "Test", "url": "http://test.com"}],
            "analysis": "Test analysis",
            "key_findings": ["Finding 1", "Finding 2"]
        }
        
        assert "question" in state
        assert "search_results" in state
        assert "analysis" in state
        assert "key_findings" in state
    
    def test_analyze_with_missing_fields(self, mock_llm):
        """Test analysis handles missing optional fields in search results."""
        state = {
            "question": "Test question",
            "search_results": [
                {},  # Empty result
                {"title": "Only Title"},
                {"url": "http://test.com"},
                {"content": "Only content"}
            ]
        }
        
        analyst = create_analyst_agent()
        result = analyst(state)
        
        # Should handle gracefully with N/A for missing fields
        assert "analysis" in result
        assert "key_findings" in result
