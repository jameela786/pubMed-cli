"""
pubmed-pharma-papers: A Python package for fetching PubMed research papers
and identifying pharmaceutical/biotech company affiliations.
"""

__version__ = "0.1.0"
__author__ = "Jameela"
__email__ = "jameelashaik7799@gmail.com"

from .pubmed_client import PubMedClient
from .author_classifier import AuthorClassifier
from .csv_formatter import CSVFormatter
from .models import Paper, Author, Journal

__all__ = [
    "PubMedClient",
    "AuthorClassifier", 
    "CSVFormatter",
    "Paper",
    "Author",
    "Journal",
] 