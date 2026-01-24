"""Writer agent that synthesizes findings into a comprehensive answer."""

from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import config
from utils import get_logger

logger = get_logger(__name__)


class WriterState(TypedDict):
    """State for the writer agent."""
    question: str
    analysis: str
    search_results: List[dict]
    answer: str
    sources: List[str]


def create_writer_agent():
    """Create a writer agent that synthesizes research into an answer.
    
    Returns:
        Function that writes the final answer
    """
    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=config.WRITER_TEMPERATURE)
    
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert writer. Create a comprehensive, well-structured answer based on:
        - The original question
        - The analyst's findings
        - The source materials
        
        Your answer should:
        - Be clear, accurate, and well-reasoned
        - Include relevant details and examples
        - Cite sources appropriately
        - Address the question directly
        - Be balanced and objective
        
        Format your response with clear sections and cite sources using [1], [2], etc."""),
        ("user", """Question: {question}

Analyst's Findings:
{analysis}

Search Results:
{search_results}

Write a comprehensive answer:""")
    ])
    
    writer_chain = writer_prompt | llm
    
    def write(state: dict) -> dict:
        """Write the final answer."""
        question = state["question"]
        analysis = state.get("analysis", "")
        search_results = state.get("search_results", [])
        
        logger.info(f"Writing answer for question with {len(search_results)} sources")
        
        # Format search results
        formatted_results = []
        sources = []
        for idx, result in enumerate(search_results, 1):
            formatted_results.append(
                f"[{idx}] {result.get('title', 'N/A')}\n"
                f"    {result.get('content', 'N/A')[:config.ANALYSIS_TRUNCATE_LENGTH]}..."
            )
            sources.append(f"[{idx}] {result.get('title', 'N/A')} - {result.get('url', 'N/A')}")
        
        results_text = "\n\n".join(formatted_results)
        
        try:
            # Generate answer
            logger.info("Generating final answer")
            response = writer_chain.invoke({
                "question": question,
                "analysis": analysis,
                "search_results": results_text
            })
            
            answer = response.content
            logger.info("Answer generated successfully")
            
            return {
                "answer": answer,
                "sources": sources,
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}", exc_info=True)
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": sources,
            }
    
    return write
