"""
Author classifier module for identifying non-academic authors and 
pharmaceutical/biotech company affiliations.
"""

import re
from typing import List, Set, Tuple, Optional
from .models import Author


class AuthorClassifier:
    """Classifies authors based on their affiliations to identify non-academic institutions."""
    
    def __init__(self) -> None:
        """Initialize the classifier with predefined patterns and keywords."""
        self.academic_keywords = {
            'university', 'university of', 'college', 'institute', 'institut',
            'school', 'medical school', 'hospital', 'medical center', 'clinic',
            'research center', 'research centre', 'laboratory', 'lab', 'department',
            'faculty', 'academy', 'academia', 'national institutes', 'nih',
            'national institute', 'center for', 'centre for', 'medical college',
            'graduate school', 'postgraduate', 'doctoral', 'phd', 'research institute',
            'government', 'federal', 'public health', 'ministry', 'department of health',
            'national health', 'veterans affairs', 'va medical', 'cancer center',
            'memorial', 'children\'s hospital', 'foundation', 'nonprofit', 'non-profit'
        }
        
        self.pharma_biotech_keywords = {
            'pharmaceutical', 'pharmaceuticals', 'pharma', 'biotech', 'biotechnology',
            'biopharmaceutical', 'drug', 'drugs', 'therapeutics', 'bioscience',
            'biosciences', 'life sciences', 'medicine', 'medical devices',
            'diagnostics', 'genomics', 'proteomics', 'clinical research',
            'contract research', 'cro', 'clinical trials', 'drug development',
            'vaccine', 'vaccines', 'biologics', 'biosimilar', 'biosimilars',
            'medical technology', 'medtech', 'healthcare', 'health care'
        }
        
        self.company_indicators = {
            'inc', 'inc.', 'incorporated', 'corp', 'corp.', 'corporation',
            'ltd', 'ltd.', 'limited', 'llc', 'l.l.c.', 'company', 'co.',
            'plc', 'p.l.c.', 'gmbh', 'ag', 'sa', 's.a.', 'nv', 'b.v.',
            'pty', 'pty.', 'proprietary', 'enterprises', 'holdings',
            'international', 'global', 'worldwide', 'group', 'solutions',
            'technologies', 'systems', 'services', 'consulting'
        }
        
        # Known pharmaceutical and biotech companies (partial list)
        self.known_companies = {
            'pfizer', 'roche', 'novartis', 'johnson & johnson', 'j&j',
            'merck', 'bristol myers squibb', 'abbvie', 'amgen', 'gilead',
            'biogen', 'genentech', 'bayer', 'sanofi', 'glaxosmithkline',
            'gsk', 'astrazeneca', 'eli lilly', 'takeda', 'boehringer ingelheim',
            'vertex', 'celgene', 'illumina', 'thermo fisher', 'agilent',
            'waters', 'perkinelmer', 'danaher', 'beckman coulter',
            'bd', 'becton dickinson', 'abbott', 'medtronic', 'boston scientific',
            'stryker', 'zimmer biomet', 'intuitive surgical', 'edwards lifesciences',
            'baxter', 'fresenius', 'hospira', 'regeneron', 'moderna',
            'biontech', 'curevac', 'novavax', 'ionis', 'alnylam',
            'bluebird bio', 'spark therapeutics', 'kite pharma', 'car-t',
            'chimeric antigen receptor', 'crispr', 'editas', 'intellia',
            'sangamo', 'precision biosciences', 'beam therapeutics'
        }
    
    def classify_author(self, author: Author) -> Author:
        """
        Classify an author based on their affiliation.
        
        Args:
            author: Author object to classify
            
        Returns:
            Author object with updated classification
        """
        if not author.affiliation:
            return author
            
        affiliation_lower = author.affiliation.lower()
        
        # Check if author is non-academic
        is_academic = self._is_academic_affiliation(affiliation_lower)
        author.is_non_academic = not is_academic
        
        # If non-academic, check for pharmaceutical/biotech companies
        if author.is_non_academic:
            companies = self._extract_company_affiliations(affiliation_lower)
            author.company_affiliations = companies
            
        return author
    
    def _is_academic_affiliation(self, affiliation: str) -> bool:
        """
        Determine if an affiliation is academic.
        
        Args:
            affiliation: Affiliation string (lowercase)
            
        Returns:
            True if academic, False otherwise
        """
        # Check for academic keywords
        for keyword in self.academic_keywords:
            if keyword in affiliation:
                return True
                
        # Check for email domains that indicate academic institutions
        email_match = re.search(r'(\S+@\S+\.edu|\S+@\S+\.ac\.\w+)', affiliation)
        if email_match:
            return True
            
        # Check for specific academic patterns
        academic_patterns = [
            r'\b(dept|department)\s+of\b',
            r'\b(division|div)\s+of\b',
            r'\b(center|centre)\s+for\b',
            r'\b(school|college)\s+of\b',
            r'\buniversity\s+of\b',
            r'\b(research|medical)\s+(center|centre)\b',
            r'\b(teaching|university)\s+hospital\b',
            r'\bmedical\s+school\b'
        ]
        
        for pattern in academic_patterns:
            if re.search(pattern, affiliation):
                return True
                
        return False
    
    def _extract_company_affiliations(self, affiliation: str) -> List[str]:
        """
        Extract pharmaceutical/biotech company names from affiliation.
        
        Args:
            affiliation: Affiliation string (lowercase)
            
        Returns:
            List of identified company names
        """
        companies = []
        
        # Check for known companies
        for company in self.known_companies:
            if company.lower() in affiliation:
                companies.append(company.title())
                
        # Check for pharmaceutical/biotech keywords with company indicators
        if self._has_pharma_biotech_keywords(affiliation):
            company_name = self._extract_company_name(affiliation)
            if company_name and company_name not in [c.lower() for c in companies]:
                companies.append(company_name.title())
                
        return companies
    
    def _has_pharma_biotech_keywords(self, affiliation: str) -> bool:
        """
        Check if affiliation contains pharmaceutical or biotech keywords.
        
        Args:
            affiliation: Affiliation string (lowercase)
            
        Returns:
            True if pharma/biotech keywords found
        """
        for keyword in self.pharma_biotech_keywords:
            if keyword in affiliation:
                return True
        return False
    
    def _extract_company_name(self, affiliation: str) -> Optional[str]:
        """
        Extract company name from affiliation string.
        
        Args:
            affiliation: Affiliation string (lowercase)
            
        Returns:
            Extracted company name or None
        """
        # Look for company indicators
        for indicator in self.company_indicators:
            if indicator in affiliation:
                # Try to extract the company name before the indicator
                pattern = rf'([^,;.]+?)\s+{re.escape(indicator)}'
                match = re.search(pattern, affiliation)
                if match:
                    company_name = match.group(1).strip()
                    # Clean up the company name
                    company_name = re.sub(r'^\W+|\W+$', '', company_name)
                    if len(company_name) > 3:  # Avoid very short matches
                        return company_name
                        
        # If no company indicator found, try to extract from context
        # Look for patterns like "Company Name, Location" or "Company Name Inc"
        patterns = [
            r'([^,;.]+?)\s+(?:inc\.?|corp\.?|ltd\.?|llc\.?|plc\.?)',
            r'([^,;.]+?)\s+(?:pharmaceutical|pharma|biotech|biotechnology)',
            r'([^,;.]+?)\s+(?:therapeutics|bioscience|life sciences)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, affiliation)
            if match:
                company_name = match.group(1).strip()
                company_name = re.sub(r'^\W+|\W+$', '', company_name)
                if len(company_name) > 3:
                    return company_name
                    
        return None
    
    def classify_authors(self, authors: List[Author]) -> List[Author]:
        """
        Classify a list of authors.
        
        Args:
            authors: List of Author objects to classify
            
        Returns:
            List of classified Author objects
        """
        return [self.classify_author(author) for author in authors]
    
    def get_statistics(self, authors: List[Author]) -> dict:
        """
        Get statistics about author classifications.
        
        Args:
            authors: List of classified Author objects
            
        Returns:
            Dictionary with classification statistics
        """
        total_authors = len(authors)
        non_academic_authors = len([a for a in authors if a.is_non_academic])
        authors_with_companies = len([a for a in authors if a.company_affiliations])
        
        all_companies = set()
        for author in authors:
            all_companies.update(author.company_affiliations)
            
        return {
            'total_authors': total_authors,
            'non_academic_authors': non_academic_authors,
            'authors_with_companies': authors_with_companies,
            'unique_companies': len(all_companies),
            'companies': list(all_companies)
        } 