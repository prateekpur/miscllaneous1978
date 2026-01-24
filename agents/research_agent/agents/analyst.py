"""Analyst agent that evaluates and synthesizes research findings."""

from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from config import config
from utils import get_logger, KeyFindings

logger = get_logger(__name__)


class AnalystState(TypedDict):
    """State for the analyst agent."""
    question: str
    search_results: List[dict]
    analysis: str
    key_findings: List[str]


def create_analyst_agent():
    """Create an analyst agent that evaluates research results.
    
    Returns:
        Function that analyzes research results
    """
    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=config.ANALYST_TEMPERATURE)
    
    # Structured output parser for key findings
    parser = PydanticOutputParser(pydantic_object=KeyFindings)
    
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert analyst. Review the search results and:
        1. Identify key findings and themes
        2. Evaluate source credibility and consistency
        3. Note any conflicting information
        4. Highlight the most relevant insights for answering the question
        
        Be thorough and critical in your analysis."""),
        ("user", """Question: {question}
        
Search Results:
{search_results}

Provide your analysis:""")
    ])
    
    findings_prompt = ChatPromptTemplate.from_messages([
        ("system", """Extract the key findings from this analysis as a list.
        
        {format_instructions}"""),
        ("user", "Analysis: {analysis}")
    ])
    
    analysis_chain = analysis_prompt | llm
    findings_chain = findings_prompt | llm | parser
    
    def analyze(state: dict) -> dict:
        """Analyze the research results."""
        question = state["question"]
        search_results = state.get("search_results", [])
        
        logger.info(f"Analyzing {len(search_results)} search results")
        
        if not search_results:
            logger.warning("No search results to analyze")
            return {
                "analysis": "No search results available for analysis.",
                "key_findings": ["No data available"],
            }
        
        # Format search results for analysis
        formatted_results = []
        for idx, result in enumerate(search_results, 1):
            formatted_results.append(
                f"{idx}. {result.get('title', 'N/A')}\n"
                f"   URL: {result.get('url', 'N/A')}\n"
                f"   Content: {result.get('content', 'N/A')[:config.CONTENT_TRUNCATE_LENGTH]}..."
            )
        
        results_text = "\n\n".join(formatted_results)
        
        try:
            # Perform analysis
            logger.info("Generating analysis")
            response = analysis_chain.invoke({
                "question": question,
                "search_results": results_text
            })
            
            analysis = response.content
            logger.info("Analysis generated successfully")
            
            # Extract key findings with structured output
            try:
                findings_response = findings_chain.invoke({
                    "analysis": analysis,
                    "format_instructions": parser.get_format_instructions()
                })
                key_findings = findings_response.findings[:config.MAX_KEY_FINDINGS]
                logger.info(f"Extracted {len(key_findings)} key findings")
            except Exception as e:
                logger.error(f"Error extracting key findings: {e}", exc_info=True)
                # Fallback to simple extraction
                key_findings = [
                    line.strip("- ").strip()
                    for line in analysis.split("\n")
                    if line.strip().startswith("-") or line.strip().startswith("•")
                ][:config.MAX_KEY_FINDINGS]
                
                if not key_findings:
                    key_findings = ["See full analysis"]
            
            return {
                "analysis": analysis,
                "key_findings": key_findings,
            }
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}", exc_info=True)
            return {
                "analysis": f"Error during analysis: {str(e)}",
                "key_findings": ["Analysis failed"],
            }
    
    return analyze
