"""
CSV formatter for PubMed paper data output.
"""

import csv
import io
from typing import List, Optional, TextIO
from datetime import date

from .models import Paper, Author


class CSVFormatter:
    """Formats PubMed paper data as CSV output."""
    
    def __init__(self) -> None:
        """Initialize CSV formatter."""
        self.fieldnames = [
            'PubmedID',
            'Title', 
            'Publication Date',
            'Non-academic Author(s)',
            'Company Affiliation(s)',
            'Corresponding Author Email'
        ]
    
    def format_papers(self, papers: List[Paper]) -> str:
        """
        Format papers as CSV string.
        
        Args:
            papers: List of Paper objects to format
            
        Returns:
            CSV formatted string
        """
        output = io.StringIO()
        self.write_papers(papers, output)
        return output.getvalue()
    
    def write_papers(self, papers: List[Paper], output_file: TextIO) -> None:
        """
        Write papers to CSV file.
        
        Args:
            papers: List of Paper objects to write
            output_file: File-like object to write to
        """
        writer = csv.DictWriter(output_file, fieldnames=self.fieldnames)
        writer.writeheader()
        
        for paper in papers:
            # Only include papers with at least one non-academic author
            non_academic_authors = paper.get_non_academic_authors()
            if not non_academic_authors:
                continue
                
            row = self._format_paper_row(paper, non_academic_authors)
            writer.writerow(row)
    
    def _format_paper_row(self, paper: Paper, non_academic_authors: List[Author]) -> dict:
        """
        Format a single paper as a CSV row.
        
        Args:
            paper: Paper object to format
            non_academic_authors: List of non-academic authors
            
        Returns:
            Dictionary representing CSV row
        """
        # Format non-academic author names
        author_names = []
        for author in non_academic_authors:
            name_parts = []
            if author.first_name:
                name_parts.append(author.first_name)
            if author.last_name:
                name_parts.append(author.last_name)
            if author.initials and not author.first_name:
                name_parts.append(author.initials)
            
            if name_parts:
                author_names.append(' '.join(name_parts))
        
        # Format company affiliations
        company_affiliations = paper.get_company_affiliations()
        
        # Format publication date
        pub_date_str = ""
        if paper.publication_date:
            pub_date_str = paper.publication_date.strftime('%Y-%m-%d')
        
        # Get corresponding author email
        corresponding_email = paper.get_corresponding_author_email()
        
        return {
            'PubmedID': paper.pubmed_id,
            'Title': paper.title,
            'Publication Date': pub_date_str,
            'Non-academic Author(s)': '; '.join(author_names),
            'Company Affiliation(s)': '; '.join(company_affiliations),
            'Corresponding Author Email': corresponding_email or ""
        }
    
    def save_to_file(self, papers: List[Paper], filename: str) -> None:
        """
        Save papers to CSV file.
        
        Args:
            papers: List of Paper objects to save
            filename: Output filename
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            self.write_papers(papers, csvfile)
    
    def print_to_console(self, papers: List[Paper]) -> None:
        """
        Print papers to console in CSV format.
        
        Args:
            papers: List of Paper objects to print
        """
        csv_content = self.format_papers(papers)
        print(csv_content)
    
    def get_filtered_papers(self, papers: List[Paper]) -> List[Paper]:
        """
        Get papers that have at least one non-academic author.
        
        Args:
            papers: List of Paper objects to filter
            
        Returns:
            List of filtered Paper objects
        """
        filtered_papers = []
        for paper in papers:
            non_academic_authors = paper.get_non_academic_authors()
            if non_academic_authors:
                filtered_papers.append(paper)
        
        return filtered_papers
    
    def get_statistics(self, papers: List[Paper]) -> dict:
        """
        Get statistics about the papers.
        
        Args:
            papers: List of Paper objects to analyze
            
        Returns:
            Dictionary with statistics
        """
        total_papers = len(papers)
        filtered_papers = self.get_filtered_papers(papers)
        papers_with_pharma = len(filtered_papers)
        
        all_companies = set()
        all_non_academic_authors = set()
        
        for paper in filtered_papers:
            companies = paper.get_company_affiliations()
            all_companies.update(companies)
            
            non_academic_authors = paper.get_non_academic_authors()
            for author in non_academic_authors:
                author_name = f"{author.first_name or ''} {author.last_name}".strip()
                all_non_academic_authors.add(author_name)
        
        return {
            'total_papers_retrieved': total_papers,
            'papers_with_pharma_authors': papers_with_pharma,
            'unique_companies': len(all_companies),
            'unique_non_academic_authors': len(all_non_academic_authors),
            'companies': list(all_companies),
            'filter_rate': papers_with_pharma / total_papers if total_papers > 0 else 0
        } 