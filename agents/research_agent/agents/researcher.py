"""Researcher agent that gathers information from web searches."""

from typing import TypedDict, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tavily import TavilyClient

from config import config
from utils import get_logger, SearchQueries

logger = get_logger(__name__)


class ResearcherState(TypedDict):
    """State for the researcher agent."""
    question: str
    search_results: List[dict]
    search_queries: List[str]


def create_researcher_agent(tavily_api_key: str = None):
    """Create a researcher agent that searches the web for information.
    
    Args:
        tavily_api_key: Tavily API key for web search
        
    Returns:
        Function that performs research given a question
    """
    api_key = tavily_api_key or config.get_tavily_api_key()
    if not api_key:
        logger.error("TAVILY_API_KEY not found in environment")
        raise ValueError("TAVILY_API_KEY not found in environment")
    
    tavily_client = TavilyClient(api_key=api_key)
    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=config.RESEARCHER_TEMPERATURE)
    
    # Structured output parser
    parser = PydanticOutputParser(pydantic_object=SearchQueries)
    
    query_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research assistant. Generate 2-3 specific search queries 
        to find comprehensive information about the question. Make queries specific and diverse.
        
        {format_instructions}"""),
        ("user", "Question: {question}")
    ])
    
    query_chain = query_prompt | llm | parser
    
    def _search_single_query(query: str) -> list:
        """Search a single query with error handling."""
        try:
            logger.info(f"Searching for: {query}")
            results = tavily_client.search(query, max_results=config.MAX_RESULTS_PER_QUERY)
            if "results" in results:
                logger.info(f"Found {len(results['results'])} results for '{query}'")
                return results["results"]
            return []
        except Exception as e:
            logger.error(f"Search error for '{query}': {e}", exc_info=True)
            return []
    
    def research(state: dict) -> dict:
        """Perform web research on the question."""
        question = state["question"]
        logger.info(f"Starting research for question: {question}")
        
        try:
            # Generate search queries with structured output
            response = query_chain.invoke({
                "question": question,
                "format_instructions": parser.get_format_instructions()
            })
            queries = response.queries[:config.MAX_SEARCH_QUERIES]
            logger.info(f"Generated {len(queries)} search queries")
            
        except Exception as e:
            logger.error(f"Error generating queries: {e}", exc_info=True)
            # Fallback to simple query
            queries = [question]
        
        # Perform concurrent searches
        all_results = []
        with ThreadPoolExecutor(max_workers=config.MAX_SEARCH_QUERIES) as executor:
            future_to_query = {executor.submit(_search_single_query, q): q for q in queries}
            for future in future_to_query:
                try:
                    results = future.result(timeout=30)
                    all_results.extend(results)
                except Exception as e:
                    query = future_to_query[future]
                    logger.error(f"Failed to get results for '{query}': {e}")
        
        logger.info(f"Research complete. Found {len(all_results)} total results")
        return {
            "search_queries": queries,
            "search_results": all_results,
        }
    
    return research
