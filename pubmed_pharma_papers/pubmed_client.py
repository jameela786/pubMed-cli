"""
PubMed API client for fetching research papers using NCBI E-utilities.
"""

import time
import re
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date
from urllib.parse import urlencode, quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import xml.etree.ElementTree as ET
import json

from .models import Paper, Author, Journal, SearchResult, PubMedAPIResponse


class PubMedClient:
    """Client for interacting with PubMed E-utilities API."""
    
    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None, 
                 tool_name: str = "get-papers-list") -> None:
        """
        Initialize PubMed client.
        
        Args:
            email: Email address for API identification
            api_key: NCBI API key for increased rate limits
            tool_name: Tool name for API identification
        """
        self.email = email
        self.api_key = api_key
        self.tool_name = tool_name
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        
        # Rate limiting: 3 requests/second without API key, 10 with API key
        self.rate_limit = 10 if api_key else 3
        self.last_request_time = 0.0
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, url: str, retries: int = 3) -> str:
        """
        Make HTTP request with rate limiting and error handling.
        
        Args:
            url: URL to request
            retries: Number of retries on failure
            
        Returns:
            Response text
            
        Raises:
            Exception: If request fails after retries
        """
        # Rate limiting
        time_since_last = time.time() - self.last_request_time
        min_interval = 1.0 / self.rate_limit
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            self.logger.debug(f"Rate limiting: sleeping {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        for attempt in range(retries):
            try:
                self.logger.debug(f"Making request to: {url}")
                request = Request(url, headers={
                    'User-Agent': f'{self.tool_name}/1.0 (mailto:{self.email or "unknown@example.com"})'
                })
                
                with urlopen(request, timeout=30) as response:
                    self.last_request_time = time.time()
                    data = response.read().decode('utf-8')
                    self.logger.debug(f"Response received: {len(data)} characters")
                    return data
                    
            except (HTTPError, URLError) as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                if attempt == retries - 1:
                    raise Exception(f"Request failed after {retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
                
        raise Exception("Request failed after all retries")
    
    def _build_search_url(self, query: str, retmax: int = 10000, retstart: int = 0) -> str:
        """
        Build esearch URL.
        
        Args:
            query: Search query
            retmax: Maximum results to return
            retstart: Starting position
            
        Returns:
            Complete esearch URL
        """
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': str(retmax),
            'retstart': str(retstart),
            'usehistory': 'y',
            'tool': self.tool_name
        }
        
        if self.email:
            params['email'] = self.email
        if self.api_key:
            params['api_key'] = self.api_key
            
        return f"{self.base_url}/esearch.fcgi?" + urlencode(params)
    
    def _build_fetch_url(self, web_env: str, query_key: str, 
                        retmax: int = 100, retstart: int = 0) -> str:
        """
        Build efetch URL.
        
        Args:
            web_env: Web environment from esearch
            query_key: Query key from esearch
            retmax: Maximum results to return
            retstart: Starting position
            
        Returns:
            Complete efetch URL
        """
        params = {
            'db': 'pubmed',
            'WebEnv': web_env,
            'query_key': query_key,
            'retmax': str(retmax),
            'retstart': str(retstart),
            'retmode': 'xml',
            'tool': self.tool_name
        }
        
        if self.email:
            params['email'] = self.email
        if self.api_key:
            params['api_key'] = self.api_key
            
        return f"{self.base_url}/efetch.fcgi?" + urlencode(params)
    
    def _build_fetch_url_by_ids(self, pubmed_ids: List[str]) -> str:
        """
        Build efetch URL using explicit PubMed IDs.
        
        Args:
            pubmed_ids: List of PubMed IDs to fetch
            
        Returns:
            Complete efetch URL
        """
        params = {
            'db': 'pubmed',
            'id': ','.join(pubmed_ids),
            'retmode': 'xml',
            'tool': self.tool_name
        }
        
        if self.email:
            params['email'] = self.email
        if self.api_key:
            params['api_key'] = self.api_key
            
        return f"{self.base_url}/efetch.fcgi?" + urlencode(params)
    
    def search(self, query: str, max_results: int = 10000) -> SearchResult:
        """
        Search PubMed for papers matching the query.
        
        Args:
            query: Search query in PubMed format
            max_results: Maximum number of results to return
            
        Returns:
            SearchResult object with search results
        """
        self.logger.info(f"Searching PubMed for: {query}")
        
        try:
            url = self._build_search_url(query, retmax=max_results)
            response = self._make_request(url)
            
            # Parse XML response
            root = ET.fromstring(response)
            
            # Extract results
            count_elem = root.find('.//Count')
            total_results = int(count_elem.text) if count_elem is not None else 0
            
            # Extract PubMed IDs
            pubmed_ids = []
            for id_elem in root.findall('.//Id'):
                pubmed_ids.append(id_elem.text)
            
            # Extract web environment and query key for efetch
            web_env_elem = root.find('.//WebEnv')
            query_key_elem = root.find('.//QueryKey')
            
            web_env = web_env_elem.text if web_env_elem is not None else None
            query_key = query_key_elem.text if query_key_elem is not None else None
            
            self.logger.info(f"Found {total_results} results, retrieved {len(pubmed_ids)} IDs")
            
            return SearchResult(
                query=query,
                total_results=total_results,
                pubmed_ids=pubmed_ids,
                web_env=web_env,
                query_key=query_key
            )
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return SearchResult(
                query=query,
                total_results=0,
                pubmed_ids=[],
                web_env=None,
                query_key=None
            )
    
    def fetch_papers(self, search_result: SearchResult, 
                    batch_size: int = 100) -> PubMedAPIResponse:
        """
        Fetch paper details from PubMed.
        
        Args:
            search_result: SearchResult from search()
            batch_size: Number of papers to fetch per request
            
        Returns:
            PubMedAPIResponse with paper details
        """
        papers = []
        total_to_fetch = len(search_result.pubmed_ids)
        
        if total_to_fetch == 0:
            return PubMedAPIResponse(
                success=True,
                papers=[],
                total_count=0,
                retrieved_count=0
            )
        
        self.logger.info(f"Fetching {total_to_fetch} papers (batch size: {batch_size})")
        
        # For small result sets, fetch by explicit IDs to avoid WebEnv issues
        if total_to_fetch <= 50:
            self.logger.debug("Using direct ID fetching for small result set")
            try:
                url = self._build_fetch_url_by_ids(search_result.pubmed_ids)
                response = self._make_request(url)
                papers = self._parse_papers_xml(response)
                
                self.logger.debug(f"Retrieved {len(papers)} papers from direct ID fetch")
                
            except Exception as e:
                self.logger.error(f"Failed to fetch papers by IDs: {e}")
                return PubMedAPIResponse(
                    success=False,
                    papers=[],
                    error_message=f"Failed to fetch papers: {e}"
                )
        else:
            # For large result sets, use WebEnv approach with proper limiting
            if not search_result.web_env or not search_result.query_key:
                return PubMedAPIResponse(
                    success=False,
                    papers=[],
                    error_message="Invalid search result: missing web_env or query_key"
                )
            
            for start in range(0, total_to_fetch, batch_size):
                try:
                    current_batch_size = min(batch_size, total_to_fetch - start)
                    self.logger.debug(f"Fetching batch starting at {start} (size: {current_batch_size})")
                    
                    url = self._build_fetch_url(
                        search_result.web_env, 
                        search_result.query_key,
                        retmax=current_batch_size,
                        retstart=start
                    )
                    
                    response = self._make_request(url)
                    batch_papers = self._parse_papers_xml(response)
                    papers.extend(batch_papers)
                    
                    self.logger.debug(f"Retrieved {len(batch_papers)} papers from batch")
                    
                except Exception as e:
                    self.logger.error(f"Failed to fetch batch starting at {start}: {e}")
                    continue
        
        self.logger.info(f"Successfully fetched {len(papers)} papers (requested: {total_to_fetch})")
        
        return PubMedAPIResponse(
            success=True,
            papers=papers,
            total_count=total_to_fetch,
            retrieved_count=len(papers)
        )
    
    def _parse_papers_xml(self, xml_content: str) -> List[Paper]:
        """
        Parse XML response from efetch into Paper objects.
        
        Args:
            xml_content: XML response from efetch
            
        Returns:
            List of Paper objects
        """
        papers = []
        
        try:
            root = ET.fromstring(xml_content)
            
            # Handle both PubmedArticle and PubmedBookArticle
            for article_elem in root.findall('.//PubmedArticle'):
                paper = self._parse_single_paper(article_elem)
                if paper:
                    papers.append(paper)
                    
        except ET.ParseError as e:
            self.logger.error(f"XML parsing error: {e}")
        except Exception as e:
            self.logger.error(f"Error parsing papers: {e}")
            
        return papers
    
    def _parse_single_paper(self, article_elem: ET.Element) -> Optional[Paper]:
        """
        Parse a single PubmedArticle element into a Paper object.
        
        Args:
            article_elem: PubmedArticle XML element
            
        Returns:
            Paper object or None if parsing fails
        """
        try:
            # Extract basic information
            medline_citation = article_elem.find('.//MedlineCitation')
            if medline_citation is None:
                return None
            
            # PubMed ID
            pmid_elem = medline_citation.find('.//PMID')
            pubmed_id = pmid_elem.text if pmid_elem is not None else ""
            
            # Title
            title_elem = medline_citation.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else ""
            
            # Abstract
            abstract_elem = medline_citation.find('.//Abstract/AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else None
            
            # Publication date
            pub_date = self._parse_publication_date(medline_citation)
            
            # Journal information
            journal = self._parse_journal(medline_citation)
            
            # Authors
            authors = self._parse_authors(medline_citation)
            
            # DOI
            doi = self._parse_doi(medline_citation)
            
            # PMC ID
            pmc_id = self._parse_pmc_id(article_elem)
            
            return Paper(
                pubmed_id=pubmed_id,
                title=title,
                publication_date=pub_date,
                authors=authors,
                journal=journal,
                abstract=abstract,
                doi=doi,
                pmc_id=pmc_id
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing single paper: {e}")
            return None
    
    def _parse_publication_date(self, citation_elem: ET.Element) -> Optional[date]:
        """Parse publication date from citation element."""
        try:
            # Try DateCompleted first, then DateCreated
            date_elem = citation_elem.find('.//DateCompleted')
            if date_elem is None:
                date_elem = citation_elem.find('.//DateCreated')
            if date_elem is None:
                date_elem = citation_elem.find('.//PubDate')
            
            if date_elem is not None:
                year_elem = date_elem.find('.//Year')
                month_elem = date_elem.find('.//Month')
                day_elem = date_elem.find('.//Day')
                
                year = int(year_elem.text) if year_elem is not None else None
                month = int(month_elem.text) if month_elem is not None else 1
                day = int(day_elem.text) if day_elem is not None else 1
                
                if year:
                    return date(year, month, day)
                    
        except (ValueError, AttributeError):
            pass
            
        return None
    
    def _parse_journal(self, citation_elem: ET.Element) -> Journal:
        """Parse journal information from citation element."""
        journal_elem = citation_elem.find('.//Journal')
        
        if journal_elem is not None:
            title_elem = journal_elem.find('.//Title')
            issn_elem = journal_elem.find('.//ISSN')
            volume_elem = journal_elem.find('.//Volume')
            issue_elem = journal_elem.find('.//Issue')
            
            # Try to get page information
            pages_elem = citation_elem.find('.//Pagination/MedlinePgn')
            
            return Journal(
                title=title_elem.text if title_elem is not None else "",
                issn=issn_elem.text if issn_elem is not None else None,
                volume=volume_elem.text if volume_elem is not None else None,
                issue=issue_elem.text if issue_elem is not None else None,
                pages=pages_elem.text if pages_elem is not None else None
            )
        
        return Journal(title="", issn=None, volume=None, issue=None, pages=None)
    
    def _parse_authors(self, citation_elem: ET.Element) -> List[Author]:
        """Parse authors from citation element."""
        authors = []
        
        author_list_elem = citation_elem.find('.//AuthorList')
        if author_list_elem is not None:
            for author_elem in author_list_elem.findall('.//Author'):
                # Get author name information
                last_name_elem = author_elem.find('.//LastName')
                first_name_elem = author_elem.find('.//ForeName')
                initials_elem = author_elem.find('.//Initials')
                
                # Get affiliation
                affiliation_elem = author_elem.find('.//AffiliationInfo/Affiliation')
                affiliation = affiliation_elem.text if affiliation_elem is not None else None
                
                # Extract email from affiliation if present
                email = None
                if affiliation:
                    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', affiliation)
                    if email_match:
                        email = email_match.group(0)
                
                author = Author(
                    first_name=first_name_elem.text if first_name_elem is not None else None,
                    last_name=last_name_elem.text if last_name_elem is not None else "",
                    initials=initials_elem.text if initials_elem is not None else None,
                    affiliation=affiliation,
                    email=email,
                    is_corresponding=False  # Will be determined later
                )
                
                authors.append(author)
        
        return authors
    
    def _parse_doi(self, citation_elem: ET.Element) -> Optional[str]:
        """Parse DOI from citation element."""
        # DOI can be in different locations
        doi_elem = citation_elem.find('.//ELocationID[@EIdType="doi"]')
        if doi_elem is not None:
            return doi_elem.text
            
        # Try alternative location
        for elocation in citation_elem.findall('.//ELocationID'):
            if elocation.get('EIdType') == 'doi':
                return elocation.text
                
        return None
    
    def _parse_pmc_id(self, article_elem: ET.Element) -> Optional[str]:
        """Parse PMC ID from article element."""
        pmc_elem = article_elem.find('.//OtherID[@Source="NLM"]')
        if pmc_elem is not None and pmc_elem.text and pmc_elem.text.startswith('PMC'):
            return pmc_elem.text
            
        return None
    
    def search_and_fetch(self, query: str, max_results: int = 10000) -> PubMedAPIResponse:
        """
        Search and fetch papers in one operation.
        
        Args:
            query: Search query in PubMed format
            max_results: Maximum number of results to return
            
        Returns:
            PubMedAPIResponse with paper details
        """
        self.logger.info(f"Starting search and fetch for: {query}")
        
        # Search for papers
        search_result = self.search(query, max_results)
        
        if search_result.total_results == 0:
            return PubMedAPIResponse(
                success=True,
                papers=[],
                total_count=0,
                retrieved_count=0
            )
        
        # Limit the number of IDs to actually fetch based on max_results
        actual_ids_to_fetch = min(len(search_result.pubmed_ids), max_results)
        if actual_ids_to_fetch < len(search_result.pubmed_ids):
            search_result.pubmed_ids = search_result.pubmed_ids[:actual_ids_to_fetch]
            self.logger.info(f"Limited fetch to {actual_ids_to_fetch} papers as requested")
        
        # Fetch paper details
        return self.fetch_papers(search_result) 