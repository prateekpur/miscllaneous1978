"""Configuration management for the multi-agent research system."""

import os
from typing import Optional


class Config:
    """Configuration settings for the research system."""
    
    # LLM Settings
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    RESEARCHER_TEMPERATURE: float = float(os.getenv("RESEARCHER_TEMP", "0"))
    ANALYST_TEMPERATURE: float = float(os.getenv("ANALYST_TEMP", "0"))
    WRITER_TEMPERATURE: float = float(os.getenv("WRITER_TEMP", "0.3"))
    
    # Search Settings
    MAX_SEARCH_QUERIES: int = int(os.getenv("MAX_SEARCH_QUERIES", "3"))
    MAX_RESULTS_PER_QUERY: int = int(os.getenv("MAX_RESULTS_PER_QUERY", "3"))
    
    # Content Processing
    CONTENT_TRUNCATE_LENGTH: int = int(os.getenv("CONTENT_TRUNCATE_LENGTH", "300"))
    ANALYSIS_TRUNCATE_LENGTH: int = int(os.getenv("ANALYSIS_TRUNCATE_LENGTH", "200"))
    MAX_KEY_FINDINGS: int = int(os.getenv("MAX_KEY_FINDINGS", "5"))
    
    # Input Validation
    MAX_QUESTION_LENGTH: int = int(os.getenv("MAX_QUESTION_LENGTH", "500"))
    MIN_QUESTION_LENGTH: int = int(os.getenv("MIN_QUESTION_LENGTH", "3"))
    
    # API Keys
    @staticmethod
    def get_openai_api_key() -> Optional[str]:
        """Get OpenAI API key from environment."""
        return os.getenv("OPENAI_API_KEY")
    
    @staticmethod
    def get_tavily_api_key() -> Optional[str]:
        """Get Tavily API key from environment."""
        return os.getenv("TAVILY_API_KEY")
    
    @staticmethod
    def validate_api_keys() -> tuple[bool, list[str]]:
        """Validate that required API keys are present.
        
        Returns:
            Tuple of (is_valid, missing_keys)
        """
        missing = []
        if not Config.get_openai_api_key():
            missing.append("OPENAI_API_KEY")
        if not Config.get_tavily_api_key():
            missing.append("TAVILY_API_KEY")
        
        return len(missing) == 0, missing


# Singleton config instance
config = Config()
