"""
Data models for PubMed paper information with type hints.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import date


@dataclass
class Author:
    """Represents an author with their affiliation information."""
    
    first_name: Optional[str]
    last_name: str
    initials: Optional[str] 
    affiliation: Optional[str]
    email: Optional[str]
    is_corresponding: bool = False
    is_non_academic: bool = False
    company_affiliations: List[str] = None
    
    def __post_init__(self) -> None:
        """Initialize mutable default values."""
        if self.company_affiliations is None:
            self.company_affiliations = []


@dataclass
class Journal:
    """Represents journal information."""
    
    title: str
    issn: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    pages: Optional[str]


@dataclass
class Paper:
    """Represents a PubMed paper with all relevant information."""
    
    pubmed_id: str
    title: str
    publication_date: Optional[date]
    authors: List[Author]
    journal: Journal
    abstract: Optional[str]
    doi: Optional[str]
    pmc_id: Optional[str]
    
    def get_non_academic_authors(self) -> List[Author]:
        """Get list of authors with non-academic affiliations."""
        return [author for author in self.authors if author.is_non_academic]
    
    def get_company_affiliations(self) -> List[str]:
        """Get unique list of company affiliations from all authors."""
        companies = set()
        for author in self.authors:
            companies.update(author.company_affiliations)
        return list(companies)
    
    def get_corresponding_author_email(self) -> Optional[str]:
        """Get email of the corresponding author."""
        for author in self.authors:
            if author.is_corresponding and author.email:
                return author.email
        return None


@dataclass
class PubMedAPIResponse:
    """Represents the response from PubMed API calls."""
    
    success: bool
    papers: List[Paper]
    error_message: Optional[str] = None
    total_count: int = 0
    retrieved_count: int = 0


@dataclass
class SearchResult:
    """Represents PubMed search results."""
    
    query: str
    total_results: int
    pubmed_ids: List[str]
    web_env: Optional[str] = None
    query_key: Optional[str] = None 