"""Unit tests for the graph orchestration."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.graph import create_research_graph, run_research, ResearchState


class TestResearchGraph:
    """Test suite for the research graph orchestration."""
    
    @pytest.fixture
    def mock_agents(self):
        """Mock all agents."""
        with patch('agents.graph.create_researcher_agent') as mock_researcher, \
             patch('agents.graph.create_analyst_agent') as mock_analyst, \
             patch('agents.graph.create_writer_agent') as mock_writer:
            
            # Mock researcher
            researcher = MagicMock()
            researcher.return_value = {
                "search_queries": ["query1", "query2"],
                "search_results": [
                    {"title": "Test 1", "url": "http://test1.com", "content": "Content 1"},
                    {"title": "Test 2", "url": "http://test2.com", "content": "Content 2"}
                ]
            }
            mock_researcher.return_value = researcher
            
            # Mock analyst
            analyst = MagicMock()
            analyst.return_value = {
                "analysis": "Test analysis of the search results",
                "key_findings": ["Finding 1", "Finding 2", "Finding 3"]
            }
            mock_analyst.return_value = analyst
            
            # Mock writer
            writer = MagicMock()
            writer.return_value = {
                "answer": "This is a comprehensive answer based on research.",
                "sources": ["[1] Test 1 - http://test1.com", "[2] Test 2 - http://test2.com"]
            }
            mock_writer.return_value = writer
            
            yield {
                "researcher": mock_researcher,
                "analyst": mock_analyst,
                "writer": mock_writer
            }
    
    def test_create_research_graph_success(self, mock_agents):
        """Test successful creation of research graph."""
        graph = create_research_graph()
        assert graph is not None
    
    def test_graph_workflow_order(self, mock_agents):
        """Test that graph executes agents in correct order."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            graph = create_research_graph()
            
            # Execute the graph
            result = graph.invoke({"question": "Test question"})
            
            # All agents should be called
            assert mock_agents["researcher"].called
            assert mock_agents["analyst"].called
            assert mock_agents["writer"].called
    
    def test_graph_state_propagation(self, mock_agents):
        """Test that state is properly propagated through the graph."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            graph = create_research_graph()
            
            initial_state = {"question": "What is quantum computing?"}
            result = graph.invoke(initial_state)
            
            # Final state should contain all components
            assert "question" in result
            assert "search_queries" in result
            assert "search_results" in result
            assert "analysis" in result
            assert "key_findings" in result
            assert "answer" in result
            assert "sources" in result
    
    def test_research_state_type(self):
        """Test ResearchState TypedDict structure."""
        state: ResearchState = {
            "question": "Test question",
            "search_queries": ["query1", "query2"],
            "search_results": [{"title": "Test", "url": "http://test.com"}],
            "analysis": "Test analysis",
            "key_findings": ["Finding 1"],
            "answer": "Test answer",
            "sources": ["[1] Test - http://test.com"]
        }
        
        assert "question" in state
        assert "search_queries" in state
        assert "search_results" in state
        assert "analysis" in state
        assert "key_findings" in state
        assert "answer" in state
        assert "sources" in state
    
    def test_run_research_convenience_function(self, mock_agents):
        """Test the run_research convenience function."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            result = run_research("Test question")
            
            assert result is not None
            assert "question" in result
            assert "answer" in result
    
    def test_graph_with_minimal_state(self, mock_agents):
        """Test graph execution with minimal initial state."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            graph = create_research_graph()
            
            # Only provide question
            result = graph.invoke({"question": "Test"})
            
            # Should still complete successfully
            assert result is not None
            assert "answer" in result
    
    def test_graph_nodes_exist(self, mock_agents):
        """Test that all required nodes are added to the graph."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            with patch('agents.graph.StateGraph') as mock_graph_class:
                mock_graph_instance = MagicMock()
                mock_graph_class.return_value = mock_graph_instance
                
                create_research_graph()
                
                # Verify nodes were added
                add_node_calls = [call[0][0] for call in mock_graph_instance.add_node.call_args_list]
                assert "researcher" in add_node_calls
                assert "analyst" in add_node_calls
                assert "writer" in add_node_calls
    
    def test_graph_edges_defined(self, mock_agents):
        """Test that edges are properly defined in the graph."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            with patch('agents.graph.StateGraph') as mock_graph_class:
                mock_graph_instance = MagicMock()
                mock_graph_class.return_value = mock_graph_instance
                
                create_research_graph()
                
                # Verify entry point
                mock_graph_instance.set_entry_point.assert_called_once_with("researcher")
                
                # Verify edges exist
                assert mock_graph_instance.add_edge.called
                
                # Check edge definitions
                edge_calls = mock_graph_instance.add_edge.call_args_list
                edge_pairs = [(call[0][0], call[0][1]) for call in edge_calls]
                
                assert ("researcher", "analyst") in edge_pairs
                assert ("analyst", "writer") in edge_pairs
    
    def test_graph_compilation(self, mock_agents):
        """Test that graph is compiled successfully."""
        with patch.dict('os.environ', {'TAVILY_API_KEY': 'test-key', 'OPENAI_API_KEY': 'test-key'}):
            with patch('agents.graph.StateGraph') as mock_graph_class:
                mock_graph_instance = MagicMock()
                mock_compiled = MagicMock()
                mock_graph_instance.compile.return_value = mock_compiled
                mock_graph_class.return_value = mock_graph_instance
                
                graph = create_research_graph()
                
                # Verify compilation was called
                mock_graph_instance.compile.assert_called_once()
                assert graph == mock_compiled
