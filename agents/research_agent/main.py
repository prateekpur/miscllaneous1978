"""Main entry point for the multi-agent research system."""

from dotenv import load_dotenv
from agents.graph import run_research
from config import config
from utils import setup_logging, get_logger, validate_question

# Setup logging
setup_logging()
logger = get_logger(__name__)


def main():
    """Run the research system."""
    # Load environment variables
    load_dotenv()
    
    # Validate API keys
    is_valid, missing_keys = config.validate_api_keys()
    if not is_valid:
        logger.error(f"Missing API keys: {', '.join(missing_keys)}")
        print(f"Error: Missing API keys: {', '.join(missing_keys)}")
        print("Please create a .env file with your API keys (see .env.example)")
        return
    
    logger.info("Multi-Agent Research System started")
    print("=" * 80)
    print("Multi-Agent Research System")
    print("=" * 80)
    print()
    
    # Get question from user
    question = input("Enter your question (or press Enter for demo): ").strip()
    
    if not question:
        question = "What are the latest developments in quantum computing in 2026?"
        print(f"Using demo question: {question}")
    
    # Validate question
    try:
        question = validate_question(question)
        logger.info(f"Validated question: {question}")
    except ValueError as e:
        logger.error(f"Invalid question: {e}")
        print(f"\nError: {e}")
        return
    
    print()
    print("🔍 Starting research...")
    print()
    
    try:
        # Run the research workflow
        logger.info("Starting research workflow")
        result = run_research(question)
        logger.info("Research workflow completed successfully")
        
        print("=" * 80)
        print("RESEARCH COMPLETE")
        print("=" * 80)
        print()
        
        print("📊 Search Queries Used:")
        for i, query in enumerate(result.get("search_queries", []), 1):
            print(f"  {i}. {query}")
        print()
        
        print("🔑 Key Findings:")
        for finding in result.get("key_findings", []):
            print(f"  • {finding}")
        print()
        
        print("=" * 80)
        print("ANSWER:")
        print("=" * 80)
        print(result.get("answer", "No answer generated"))
        print()
        
        print("=" * 80)
        print("SOURCES:")
        print("=" * 80)
        for source in result.get("sources", []):
            print(f"  {source}")
        print()
        
        logger.info("Results displayed successfully")
        
    except Exception as e:
        logger.error(f"Error during research: {e}", exc_info=True)
        print(f"\nError during research: {e}")
        print("Please check the logs for more details.")


if __name__ == "__main__":
    main()
