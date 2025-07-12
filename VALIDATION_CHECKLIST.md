# PubMed Pharmaceutical Papers - Validation Checklist

## Quick Validation Steps

### **1. Run the Test Suite**
```bash
./test_scenarios.sh
```
**Expected**: All 12 tests should pass with ✅ green checkmarks

### **2. Check CSV Format**
Open any generated CSV file and verify:
- [ ] Header: `PubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author Email`
- [ ] Data rows have consistent comma separation
- [ ] No malformed entries or missing columns

### **3. Spot Check 5 Random Entries**
For each entry, verify:
- [ ] **PubmedID**: 8-digit number (e.g., 40639020)
- [ ] **Title**: Meaningful scientific paper title
- [ ] **Company**: Known pharmaceutical/biotech company
- [ ] **Authors**: Names that make sense (not university names)

### **4. Manual Validation Test**
```bash
# Generate small test with known companies
get-papers-list "Pfizer" --max-results 5 --file validation_test.csv

# Check results
head -10 validation_test.csv
```

**Expected**: All entries should have Pfizer or other pharma companies

### **5. Edge Case Testing**
```bash
# Test with academic-only query
get-papers-list "Harvard University" --max-results 3 --file academic_test.csv

# Check if file is empty or has minimal entries
wc -l academic_test.csv
```

**Expected**: Very few or no entries (academic papers filtered out)

### **6. Complex Query Test**
```bash
# Test advanced search
get-papers-list '"drug discovery"[Title] AND pharmaceutical' --max-results 3 --file complex_test.csv
```

**Expected**: Should find papers about drug discovery with pharma authors

### **7. Statistics Validation**
```bash
get-papers-list "biotech" --max-results 10 --stats
```

**Expected**: Should show breakdown of companies, authors, and filter rates

## **Quick Validation Questions**

### **A. Are the companies real?**
- [ ] Moderna, Pfizer, J&J, Merck, Roche, Takeda = ✅ Major pharma companies
- [ ] Sungen Biotech, Allodx, Biogen = ✅ Known biotech companies
- [ ] Random university names = ❌ Should NOT appear

### **B. Are the papers relevant?**
- [ ] Titles mention drugs, vaccines, therapeutics, clinical trials
- [ ] Research areas: cancer, immunotherapy, COVID-19, drug development
- [ ] NOT: Pure academic research without industry involvement

### **C. Is the data clean?**
- [ ] No duplicate PubMed IDs
- [ ] Dates in YYYY-MM-DD format (when available)
- [ ] Author names separated by semicolons
- [ ] Company names properly capitalized

### **D. Are exclusions working?**
- [ ] No papers with only university authors
- [ ] No papers from academic hospitals only
- [ ] No government-only research papers

## **Common Issues to Check**

### **❌ False Positives (Should NOT appear)**
- Hospital systems without industry involvement
- University medical centers
- Government research labs
- Academic conferences/societies

### **❌ False Negatives (Missing companies)**
- Misspelled company names
- International pharmaceutical companies
- Biotech companies not in database
- Contract research organizations (CROs)

### **❌ Data Quality Issues**
- Malformed CSV (missing commas, quotes)
- Encoding problems with special characters
- Empty required fields
- Inconsistent date formats

## **Validation Report Template**

```
VALIDATION RESULTS:
==================
Test Suite: [PASS/FAIL] - X/12 tests passed
CSV Format: [PASS/FAIL] - Headers and structure correct
Sample Check: [PASS/FAIL] - X/5 random entries validated
Edge Cases: [PASS/FAIL] - Academic filtering working
Company Accuracy: [PASS/FAIL] - Known companies identified
Data Quality: [PASS/FAIL] - Clean, consistent formatting

OVERALL ASSESSMENT: [PRODUCTION READY/NEEDS FIXES]
CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
```

## **Final Validation Command**

```bash
# Complete validation test
get-papers-list "pharmaceutical OR biotech" --max-results 20 --file final_validation.csv --stats --debug

# Check results
echo "Total papers found:"
wc -l final_validation.csv
echo "Sample entries:"
head -5 final_validation.csv
echo "Companies identified:"
grep -o '[^,]*' final_validation.csv | sort | uniq -c | sort -nr
```

**Expected**: Should find 15-20 papers with major pharmaceutical companies and provide detailed statistics about the classification process. 