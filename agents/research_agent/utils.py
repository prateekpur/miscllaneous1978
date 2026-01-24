"""Utility functions for the multi-agent research system."""

import logging
from typing import List
from pydantic import BaseModel, Field, field_validator


# Configure logging
def setup_logging(level=logging.INFO):
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


# Get logger
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


# Input Validation
class Question(BaseModel):
    """Validated question model."""
    text: str = Field(..., min_length=3, max_length=500)
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        """Validate question text."""
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty or whitespace only")
        if len(v) < 3:
            raise ValueError("Question must be at least 3 characters long")
        if len(v) > 500:
            raise ValueError("Question must be at most 500 characters long")
        return v


def validate_question(question: str) -> str:
    """Validate a question string.
    
    Args:
        question: The question to validate
        
    Returns:
        Validated and cleaned question text
        
    Raises:
        ValueError: If question is invalid
    """
    try:
        validated = Question(text=question)
        return validated.text
    except Exception as e:
        raise ValueError(f"Invalid question: {str(e)}")


# Structured Output Models
class SearchQueries(BaseModel):
    """Structured search queries output."""
    queries: List[str] = Field(..., min_length=1, max_length=3, description="List of search queries")
    
    @field_validator('queries')
    @classmethod
    def clean_queries(cls, v):
        """Clean and validate queries."""
        return [q.strip() for q in v if q.strip()]


class KeyFindings(BaseModel):
    """Structured key findings output."""
    findings: List[str] = Field(..., min_length=1, max_length=5, description="Key findings from analysis")
    
    @field_validator('findings')
    @classmethod
    def clean_findings(cls, v):
        """Clean and validate findings."""
        return [f.strip() for f in v if f.strip()]
