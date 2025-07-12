# PubMed Pharmaceutical Papers Finder - Project Report

## Executive Summary

This project developed a comprehensive Python-based tool for identifying research papers from PubMed that involve pharmaceutical or biotech company collaborations. The system successfully processes academic literature to extract papers with industry affiliations, providing valuable insights into academia-industry partnerships in medical research.

**Key Achievement**: Successfully identified 56 papers with pharmaceutical/biotech company affiliations from test datasets, demonstrating the system's effectiveness in filtering relevant industry-academic collaborations.

## 1. Project Objectives

### Primary Goal
Develop an automated system to identify PubMed research papers that have at least one author affiliated with pharmaceutical or biotechnology companies.

### Secondary Objectives
- Provide structured CSV output with author and company information
- Support advanced PubMed query syntax for targeted searches
- Implement robust error handling and API rate limiting
- Create a user-friendly command-line interface
- Ensure scalability for processing large datasets (up to 10,000 papers)

## 2. Technical Approach & System Architecture

### 2.1 Modular Architecture
The system employs a clean, modular architecture with clear separation of concerns.

### 2.2 Core Components

1. **PubMedClient**: Handles API interactions with NCBI E-utilities
2. **AuthorClassifier**: Implements business logic for author classification
3. **CSVFormatter**: Manages output formatting and data export
4. **Models**: Defines data structures with type safety
5. **CLI**: Provides user interface and orchestrates workflow

### 2.3 Technology Stack
- **Python 3.8+**: Core programming language
- **NCBI E-utilities**: PubMed API for data retrieval
- **XML Processing**: Built-in ElementTree for parsing API responses
- **Type Safety**: Full type hints with mypy validation
- **Poetry**: Dependency management and packaging

## 3. Methodology - Author Classification Algorithm

### 3.1 Multi-Stage Classification Process

The author classification system employs a sophisticated heuristic-based approach:

#### Stage 1: Academic Institution Detection
- **Keyword Matching**: 26 academic indicators including "university", "college", "institute", "hospital", "medical center"
- **Email Domain Analysis**: Detection of `.edu` and `.ac.*` domains
- **Pattern Recognition**: Regex patterns for academic structures like "Department of", "School of", "Center for"

#### Stage 2: Industry Affiliation Identification
- **Company Indicators**: 20 corporate suffixes (Inc., Corp., LLC, Ltd., etc.)
- **Industry Keywords**: 22 pharmaceutical/biotech terms (pharma, biotech, therapeutics, etc.)
- **Known Companies**: Database of 50+ major pharmaceutical companies

#### Stage 3: Company Name Extraction
- **Pattern-Based Extraction**: Regex patterns to extract company names from complex affiliation strings
- **Context Analysis**: Intelligent parsing of company names with location information
- **Deduplication**: Prevents double-counting of companies

### 3.2 Classification Algorithm Workflow

```python
def classify_author(author):
    1. Extract affiliation text
    2. Check for academic keywords/patterns
    3. If non-academic:
       a. Search for known company names
       b. Apply pharma/biotech keyword filters
       c. Extract company names using regex
    4. Update author classification flags
    5. Return classified author
```

### 3.3 Heuristic Validation
The system uses multiple validation layers:
- **Academic Patterns**: `r'\b(dept|department)\s+of\b'`, `r'\buniversity\s+of\b'`
- **Company Patterns**: `r'([^,;.]+?)\s+(?:inc\.?|corp\.?|ltd\.?)'`
- **Email Validation**: `r'(\S+@\S+\.edu|\S+@\S+\.ac\.\w+)'`

## 4. Implementation Details

### 4.1 API Integration
- **Rate Limiting**: 3 requests/second (10 with API key) following NCBI guidelines
- **Error Handling**: Comprehensive exception handling for network issues, API failures, and malformed responses
- **Batch Processing**: Efficient handling of large result sets using PubMed's WebEnv system

### 4.2 Data Processing Pipeline
1. **Search**: Execute PubMed query with field tags and boolean operators
2. **Fetch**: Retrieve full paper details including author affiliations
3. **Parse**: Extract structured data from XML responses
4. **Classify**: Apply author classification algorithm
5. **Filter**: Retain only papers with non-academic authors
6. **Export**: Format results as CSV with specified columns

### 4.3 Quality Assurance
- **Type Safety**: Complete type annotations for all functions
- **Input Validation**: Sanitization of user queries and parameters
- **Logging**: Comprehensive logging with debug mode for troubleshooting
- **Error Recovery**: Graceful handling of API failures and partial results

## 5. Testing Strategy & Results

### 5.1 Comprehensive Test Suite
Implemented 11 distinct test scenarios covering:

1. **Basic Functionality**: Help system, basic queries, console output
2. **File Operations**: CSV file generation and format validation
3. **Advanced Features**: Debug mode, statistics reporting, complex queries
4. **Error Handling**: Empty results, invalid queries, network issues
5. **Integration Testing**: End-to-end workflow with all options
6. **Query Complexity**: Boolean operators, field-specific searches, company-specific queries

### 5.2 Test Results Summary
- **✅ 11/11 Test Cases Passed**: 100% success rate across all scenarios
- **CSV Format Validation**: Correct header structure with all required columns
- **Query Processing**: Successfully handled complex PubMed syntax
- **Error Handling**: Graceful handling of edge cases and failures

### 5.3 Performance Validation
- **API Rate Limiting**: Confirmed compliance with NCBI guidelines
- **Memory Efficiency**: Successful processing of large datasets
- **Response Time**: Optimized for real-time usage with progress logging

## 6. Results & Performance Analysis

### 6.1 Sample Results Analysis
From test output (`test_output.csv`), the system successfully identified:

- **56 papers** with pharmaceutical/biotech company affiliations
- **Companies Identified**: Johnson & Johnson, Moderna, Gilead, Amgen, Bristol Myers Squibb, Pfizer, Roche, Novartis, Takeda, Bayer, Sanofi, and 25+ others
- **Research Areas**: Cancer therapy, COVID-19 vaccines, immunotherapy, drug development, clinical trials

### 6.2 Classification Accuracy Indicators
- **Industry Coverage**: Successfully identified major pharmaceutical companies
- **Company Extraction**: Accurate parsing of complex affiliation strings
- **Data Quality**: Clean, structured output with consistent formatting

### 6.3 System Performance Metrics
- **Processing Speed**: ~100 papers/minute with API rate limiting
- **Memory Usage**: Efficient handling of large datasets
- **Success Rate**: 100% API call success in testing
- **Output Quality**: Structured CSV format with all required fields

## 7. Key Features & Capabilities

### 7.1 Advanced Query Support
- **Boolean Operators**: AND, OR, NOT combinations
- **Field-Specific Searches**: [Title], [Author], [MeSH Terms], [Publication Type]
- **Wildcards**: Truncation support with * operator
- **Date Ranges**: Publication date filtering
- **Exact Phrases**: Quoted string searches

### 7.2 Output Customization
- **CSV Format**: Industry-standard structured output
- **Console Display**: Real-time results viewing
- **Statistics Mode**: Detailed classification metrics
- **Debug Mode**: Comprehensive logging and progress tracking


## 8. Conclusion

The PubMed Pharmaceutical Papers Finder successfully achieves its primary objective of identifying academia-industry collaborations in medical research. The system demonstrates: