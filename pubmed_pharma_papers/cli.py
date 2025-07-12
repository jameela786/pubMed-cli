"""
Command-line interface for the PubMed pharma papers tool.
"""

import argparse
import logging
import sys
from typing import Optional

from .pubmed_client import PubMedClient
from .author_classifier import AuthorClassifier
from .csv_formatter import CSVFormatter
from .models import Paper


def setup_logging(debug: bool = False) -> None:
    """
    Setup logging configuration.
    
    Args:
        debug: Whether to enable debug logging
    """
    level = logging.DEBUG if debug else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for the CLI.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description='Fetch research papers from PubMed API and identify pharmaceutical/biotech company affiliations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "cancer drug development"
  %(prog)s "SARS-CoV-2 vaccine" --file results.csv --debug
  %(prog)s "machine learning AND drug discovery" --file ml_drugs.csv
  
Query format:
  The tool supports PubMed's full query syntax including:
  - Boolean operators: AND, OR, NOT
  - Field tags: [Title], [Author], [Journal], [MeSH Terms]
  - Wildcards: * (truncation)
  - Phrases: "exact phrase"
  
Examples of advanced queries:
  - "machine learning"[Title] AND "drug discovery"[MeSH Terms]
  - (cancer OR tumor) AND (pharmaceutical OR biotech)
  - "clinical trial"[Publication Type] AND vaccine*
        """
    )
    
    parser.add_argument(
        'query',
        help='Search query in PubMed format'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Print debug information during execution'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Specify the filename to save the results (CSV format). If not provided, results are printed to console.'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=10000,
        help='Maximum number of results to retrieve (default: 10000)'
    )
    
    parser.add_argument(
        '--email',
        type=str,
        help='Email address for NCBI API identification (recommended)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='NCBI API key for increased rate limits'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display statistics about the search results'
    )
    
    return parser


def process_papers(papers: list, classifier: AuthorClassifier, debug: bool = False) -> list:
    """
    Process papers through the author classification pipeline.
    
    Args:
        papers: List of Paper objects
        classifier: AuthorClassifier instance
        debug: Whether to show debug information
        
    Returns:
        List of processed Paper objects
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing {len(papers)} papers for author classification")
    
    processed_papers = []
    
    for i, paper in enumerate(papers):
        if debug and i % 100 == 0:
            logger.debug(f"Processing paper {i+1}/{len(papers)}: {paper.title[:50]}...")
        
        # Classify authors
        classified_authors = classifier.classify_authors(paper.authors)
        
        # Update paper with classified authors
        paper.authors = classified_authors
        
        # Only keep papers with at least one non-academic author
        if paper.get_non_academic_authors():
            processed_papers.append(paper)
    
    logger.info(f"Found {len(processed_papers)} papers with non-academic authors")
    
    return processed_papers


def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        logger.info("Initializing PubMed client...")
        client = PubMedClient(
            email=args.email,
            api_key=args.api_key,
            tool_name="get-papers-list"
        )
        
        classifier = AuthorClassifier()
        formatter = CSVFormatter()
        
        # Search and fetch papers
        logger.info(f"Searching for papers with query: {args.query}")
        response = client.search_and_fetch(args.query, args.max_results)
        
        if not response.success:
            logger.error(f"Failed to fetch papers: {response.error_message}")
            sys.exit(1)
        
        if not response.papers:
            logger.info("No papers found matching the query.")
            sys.exit(0)
        
        logger.info(f"Retrieved {len(response.papers)} papers (max requested: {args.max_results})")
        
        # Process papers through classification
        processed_papers = process_papers(response.papers, classifier, args.debug)
        
        if not processed_papers:
            logger.info("No papers found with pharmaceutical/biotech company affiliations.")
            sys.exit(0)
        
        # Output results
        if args.file:
            logger.info(f"Saving results to {args.file}")
            formatter.save_to_file(processed_papers, args.file)
            logger.info(f"Results saved to {args.file}")
        else:
            logger.info("Printing results to console")
            formatter.print_to_console(processed_papers)
        
        # Display statistics if requested
        if args.stats:
            print_statistics(response.papers, processed_papers, classifier, formatter)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def print_statistics(all_papers: list, filtered_papers: list, 
                    classifier: AuthorClassifier, formatter: CSVFormatter) -> None:
    """
    Print statistics about the search and classification results.
    
    Args:
        all_papers: List of all retrieved papers
        filtered_papers: List of papers with non-academic authors
        classifier: AuthorClassifier instance
        formatter: CSVFormatter instance
    """
    print("\n" + "="*50)
    print("SEARCH AND CLASSIFICATION STATISTICS")
    print("="*50)
    
    # Overall statistics
    print(f"Total papers retrieved: {len(all_papers)}")
    print(f"Papers with pharma/biotech authors: {len(filtered_papers)}")
    print(f"Filter rate: {len(filtered_papers)/len(all_papers)*100:.1f}%")
    
    # Get detailed statistics from formatter
    stats = formatter.get_statistics(all_papers)
    print(f"Unique companies identified: {stats['unique_companies']}")
    print(f"Unique non-academic authors: {stats['unique_non_academic_authors']}")
    
    # Show top companies
    if stats['companies']:
        print(f"\nTop companies found:")
        for i, company in enumerate(sorted(stats['companies'])[:10], 1):
            print(f"  {i}. {company}")
        if len(stats['companies']) > 10:
            print(f"  ... and {len(stats['companies']) - 10} more")
    
    # Author classification statistics
    all_authors = []
    for paper in all_papers:
        all_authors.extend(paper.authors)
    
    if all_authors:
        author_stats = classifier.get_statistics(all_authors)
        print(f"\nAuthor classification:")
        print(f"  Total authors: {author_stats['total_authors']}")
        print(f"  Non-academic authors: {author_stats['non_academic_authors']}")
        print(f"  Authors with company affiliations: {author_stats['authors_with_companies']}")
    
    print("="*50)


if __name__ == "__main__":
    main() 