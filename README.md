# PubMed Pharmaceutical Papers Finder

A Python program to fetch research papers from PubMed API and identify papers with at least one author affiliated with a pharmaceutical or biotech company. The program returns results as a CSV file with detailed author and company information.

## Features

- **PubMed API Integration**: Fetches papers using NCBI E-utilities with full query syntax support
- **Author Classification**: Identifies non-academic authors using sophisticated heuristics
- **Company Detection**: Recognizes pharmaceutical and biotech company affiliations
- **CSV Output**: Exports results in structured CSV format with required columns
- **Command-line Interface**: Easy-to-use CLI with multiple options
- **Rate Limiting**: Respects NCBI API guidelines (3 requests/second, 10 with API key)
- **Error Handling**: Robust error handling for API failures and invalid queries
- **Type Safety**: Fully typed Python code using type hints
- **Logging**: Comprehensive logging with debug mode support

## Installation

### Prerequisites

- Python 3.8 or higher

### Quick Installation

1. **Clone or download the project**:
   ```bash
   # If you have the project files
   cd pubmed-pharma-papers
   ```

2. **Install dependencies**:
```bash
poetry install
```

## Usage

### Basic Usage

```bash
get-papers-list "cancer drug development"
```

### Save Results to File

```bash
get-papers-list "SARS-CoV-2 vaccine" --file results.csv
```

### Enable Debug Mode

```bash
get-papers-list "machine learning AND drug discovery" --debug
```

### Use API Key for Higher Rate Limits

```bash
get-papers-list "biotech cancer therapy" --api-key YOUR_API_KEY --email your@email.com
```

### Show Statistics

```bash
get-papers-list "pharmaceutical clinical trials" --stats
```

### Advanced Query Examples

The tool supports PubMed's full query syntax:

```bash
# Search specific fields
get-papers-list '"machine learning"[Title] AND "drug discovery"[MeSH Terms]'

# Boolean operators
get-papers-list '(cancer OR tumor) AND (pharmaceutical OR biotech)'

# Publication types
get-papers-list '"clinical trial"[Publication Type] AND vaccine*'

# Date ranges
get-papers-list 'COVID-19 AND "2020"[Date - Publication] : "2023"[Date - Publication]'
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `query` | Search query in PubMed format (required) |
| `-h, --help` | Show help message and exit |
| `-d, --debug` | Enable debug logging |
| `-f, --file FILENAME` | Save results to CSV file (default: print to console) |
| `--max-results N` | Maximum number of results to retrieve (default: 10000) |
| `--email EMAIL` | Email address for NCBI API identification |
| `--api-key KEY` | NCBI API key for increased rate limits |
| `--stats` | Display search and classification statistics |

## Output Format

The program outputs CSV files with the following columns:

- **PubmedID**: Unique identifier for the paper
- **Title**: Title of the paper
- **Publication Date**: Date the paper was published (YYYY-MM-DD format)
- **Non-academic Author(s)**: Names of authors affiliated with non-academic institutions
- **Company Affiliation(s)**: Names of pharmaceutical/biotech companies
- **Corresponding Author Email**: Email address of the corresponding author

### Sample Output

```csv
PubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author Email
12345678,Novel Drug Discovery Using AI,2023-01-15,John Smith; Jane Doe,Pfizer Inc.; Roche,john.smith@pfizer.com
87654321,Biotech Innovations in Cancer Treatment,2023-02-20,Michael Johnson,Genentech,m.johnson@gene.com
```

## Code Organization

The project is organized as follows:

```
pubmed-pharma-papers/
├── pubmed_pharma_papers/           # Main package directory
│   ├── __init__.py                 # Package initialization
│   ├── models.py                   # Data models with type hints
│   ├── pubmed_client.py            # PubMed API client
│   ├── author_classifier.py        # Author classification logic
│   ├── csv_formatter.py            # CSV output formatting
│   └── cli.py                      # Command-line interface
├── pyproject.toml                  # Poetry configuration
├── README.md                       # This file
└── requirements.txt                # Pip requirements (if needed)
```

### Module Descriptions

- **`models.py`**: Contains data classes for Paper, Author, Journal, and other entities
- **`pubmed_client.py`**: Handles PubMed API interactions using E-utilities
- **`author_classifier.py`**: Implements heuristics to identify non-academic authors
- **`csv_formatter.py`**: Formats and outputs results in CSV format
- **`cli.py`**: Command-line interface using argparse

## Author Classification Heuristics

The program uses multiple heuristics to identify non-academic authors:

### Academic Institution Indicators
- University-related keywords: "university", "college", "school", "institute"
- Hospital and medical center keywords: "hospital", "medical center", "clinic"
- Research institution keywords: "research center", "laboratory", "national institutes"
- Government institution keywords: "government", "federal", "ministry"

### Company Indicators
- Corporate suffixes: "Inc.", "Corp.", "LLC", "Ltd.", "PLC"
- Pharmaceutical keywords: "pharmaceutical", "pharma", "biotech", "biotechnology"
- Known company names: Pfizer, Roche, Novartis, etc.
- Business keywords: "consulting", "services", "solutions", "technologies"

### Email Domain Analysis
- Academic domains: `.edu`, `.ac.uk`, `.ac.*`
- Corporate domains: company-specific domains

## API Rate Limiting

The program respects NCBI API guidelines:
- **Without API key**: 3 requests per second
- **With API key**: 10 requests per second

To obtain an API key:
1. Visit [NCBI API Key Registration](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/)
2. Create an account and generate an API key
3. Use the key with `--api-key` option

## Error Handling

The program handles various error conditions:
- Invalid PubMed queries
- Network timeouts and connection errors
- API rate limit exceeded
- Malformed XML responses
- File I/O errors

## Dependencies

### Core Dependencies
- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and analysis
- **argparse**: Command-line argument parsing (built-in)
- **xml.etree.ElementTree**: XML parsing (built-in)
- **csv**: CSV file operations (built-in)
- **logging**: Logging functionality (built-in)
- **typing**: Type hints (built-in)
- **dataclasses**: Data classes (built-in)
- **datetime**: Date/time operations (built-in)

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

## Tools and Libraries Used

This project was built using the following tools and libraries:

- **Python 3.8+**: Programming language
- **NCBI E-utilities**: PubMed API for paper retrieval
- **LLM used in developement**: ChatGPT (https://chatgpt.com/share/687240d4-bacc-8005-8ac9-3fa8a727f2a7)
- **Poetry**: Dependency management and packaging
- **Type hints**: For better code quality and IDE support
- **Logging**: For debugging and monitoring
- **CSV**: For structured data output
- **Regular expressions**: For text pattern matching
- **XML parsing**: For processing PubMed API responses

## Examples

### Basic Search
```bash
get-papers-list "cancer immunotherapy"
```

### Search with Company Filter
```bash
get-papers-list "monoclonal antibody" --file antibody_papers.csv
```

### Advanced Search with Statistics
```bash
get-papers-list '"clinical trial"[Publication Type] AND (pharma* OR biotech*)' --stats --debug
```

### Using API Key
```bash
export NCBI_API_KEY="your_api_key_here"
get-papers-list "COVID-19 vaccine development" --api-key $NCBI_API_KEY --email your@email.com
```

## Troubleshooting

### Debug Mode

Enable debug mode to see detailed logging:
```bash
get-papers-list "your query" --debug
```
