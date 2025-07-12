#!/bin/bash

# get-papers-list "SARS-CoV-2 vaccine" --file results.csv --max-results 2

echo "=== PubMed Pharma Papers - Comprehensive Testing ==="
echo "Starting test scenarios..."

# Test 1: Help functionality
echo -e "\n1. Testing help functionality..."
echo "Command: get-papers-list --help"
get-papers-list --help > /dev/null && echo "✅ Help command works" || echo "❌ Help command failed"

# Test 2: Basic query with console output
echo -e "\n2. Testing basic query (console output)..."
echo "Command: get-papers-list \"pfizer\" --max-results 3"
get-papers-list "pfizer" --max-results 3 > /dev/null 2>&1 && echo "✅ Basic query works" || echo "❌ Basic query failed"

# Test 3: File output
echo -e "\n3. Testing file output..."
echo "Command: get-papers-list \"biotech\" --max-results 2 --file test1.csv"
get-papers-list "biotech" --max-results 2 --file test1.csv > /dev/null 2>&1
if [ -f "test1.csv" ]; then
    echo "✅ File output works (test1.csv created)"
    rm test1.csv
else
    echo "❌ File output failed"
fi

# Test 4: Debug mode
echo -e "\n4. Testing debug mode..."
echo "Command: get-papers-list \"moderna\" --max-results 2 --debug --file test2.csv"
get-papers-list "moderna" --max-results 2 --debug --file test2.csv > /dev/null 2>&1
if [ -f "test2.csv" ]; then
    echo "✅ Debug mode works (test2.csv created)"
    rm test2.csv
else
    echo "❌ Debug mode failed"
fi

# Test 5: Statistics
echo -e "\n5. Testing statistics display..."
echo "Command: get-papers-list \"pharmaceutical\" --max-results 5 --stats"
get-papers-list "pharmaceutical" --max-results 5 --stats > /dev/null 2>&1 && echo "✅ Statistics works" || echo "❌ Statistics failed"

# Test 6: Complex query
echo -e "\n6. Testing complex PubMed query..."
echo "Command: get-papers-list '\"drug discovery\"[Title] AND biotech' --max-results 2"
get-papers-list '"drug discovery"[Title] AND biotech' --max-results 2 > /dev/null 2>&1 && echo "✅ Complex query works" || echo "❌ Complex query failed"

# Test 7: Error handling (empty result)
echo -e "\n7. Testing error handling (empty results)..."
echo "Command: get-papers-list \"nonexistentcompanyname12345\" --max-results 1"
get-papers-list "nonexistentcompanyname12345" --max-results 1 > /dev/null 2>&1 && echo "✅ Error handling works" || echo "❌ Error handling failed"

# Test 8: Boolean query operators
echo -e "\n8. Testing boolean query operators..."
echo "Command: get-papers-list \"cancer AND pharmaceutical\" --max-results 2"
get-papers-list "cancer AND pharmaceutical" --max-results 2 > /dev/null 2>&1 && echo "✅ Boolean operators work" || echo "❌ Boolean operators failed"

# Test 9: Field-specific search
echo -e "\n9. Testing field-specific search..."
echo "Command: get-papers-list '\"biotech\"[Title]' --max-results 2"
get-papers-list '"biotech"[Title]' --max-results 2 > /dev/null 2>&1 && echo "✅ Field-specific search works" || echo "❌ Field-specific search failed"

# Test 10: Integration test with all options
echo -e "\n10. Testing integration (all options)..."
echo "Command: get-papers-list \"pharmaceutical innovation\" --file integration.csv --debug --stats --max-results 5"
get-papers-list "pharmaceutical innovation" --file integration.csv --debug --stats --max-results 5 > /dev/null 2>&1
if [ -f "integration.csv" ]; then
    row_count=$(wc -l < integration.csv)
    echo "✅ Integration test works (integration.csv created with $row_count lines)"
    rm integration.csv
else
    echo "❌ Integration test failed"
fi

# Test 11: Company-specific search with stats
echo -e "\n11. Testing company-specific search with statistics..."
echo "Command: get-papers-list \"Roche\" --max-results 3 --stats"
get-papers-list "Roche" --max-results 3 --stats > /dev/null 2>&1 && echo "✅ Company search with stats works" || echo "❌ Company search with stats failed"

echo -e "\n=== Testing Complete ==="
echo "All core functionality has been tested."
echo -e "\nTo run individual tests, use any of the commands shown above."
echo -e "\nFor detailed output, remove '> /dev/null 2>&1' from any command." 