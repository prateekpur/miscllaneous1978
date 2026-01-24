"""LangGraph orchestration for multi-agent research system."""

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from .researcher import create_researcher_agent
from .analyst import create_analyst_agent
from .writer import create_writer_agent


class ResearchState(TypedDict):
    """Overall state for the research graph."""
    question: str
    search_queries: List[str]
    search_results: List[dict]
    analysis: str
    key_findings: List[str]
    answer: str
    sources: List[str]


def create_research_graph():
    """Create the multi-agent research graph.
    
    Returns:
        Compiled LangGraph for research workflow
    """
    # Create agents
    researcher = create_researcher_agent()
    analyst = create_analyst_agent()
    writer = create_writer_agent()
    
    # Define the graph
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)
    workflow.add_node("writer", writer)
    
    # Define the flow
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_research(question: str):
    """Run the research workflow.
    
    Args:
        question: The question to research
        
    Returns:
        dict: Contains answer, sources, and intermediate results
    """
    graph = create_research_graph()
    result = graph.invoke({"question": question})
    return result
