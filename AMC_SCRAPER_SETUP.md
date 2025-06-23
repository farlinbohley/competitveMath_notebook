# AMC 10 Problem Scraper Setup Guide

## What Was Created

I've created a complete Python scraper for AMC 10 problems from the Art of Problem Solving Wiki. Here's what's included:

### Directory Structure
```
scraperForProblems/
├── scraper.py          # Main scraper script
├── requirements.txt    # Python dependencies
├── README.md          # Detailed documentation
├── test_scraper.py    # Test script to verify functionality
└── example_usage.py   # Examples of how to use the scraper

Competitive-Math-Notebook-Library/
└── AMC10/             # Output directory for scraped problems (JSON files)
```

## Quick Start

1. **Install dependencies:**
   ```bash
   cd scraperForProblems
   pip install -r requirements.txt
   ```

2. **Test the scraper:**
   ```bash
   python test_scraper.py
   ```

3. **Scrape problems:**
   ```bash
   # Scrape 2023 AMC 10A and 10B
   python scraper.py --years 2023
   
   # Scrape multiple years
   python scraper.py --years 2020-2023
   
   # Scrape only AMC 10A from 2022
   python scraper.py --years 2022 --contests A
   ```

## Features

- ✅ Scrapes problem text, multiple-choice options, and all solutions
- ✅ Handles both AMC 10A and AMC 10B contests
- ✅ Saves data in structured JSON format
- ✅ Skips missing problems (404 errors) gracefully
- ✅ Includes delay between requests to be respectful to the server
- ✅ Command-line interface with flexible options
- ✅ Programmatic API for custom usage

## Output Format

Problems are saved as JSON files with this structure:
```json
{
  "1": {
    "problem": "Problem text here...",
    "options": ["(A) option1", "(B) option2", ...],
    "solutions": ["Solution 1: text", "Solution 2: text", ...]
  },
  "2": { ... }
}
```

## Dependencies

The scraper uses:
- `requests` - For HTTP requests
- `beautifulsoup4` - For HTML parsing
- `lxml` - For improved HTML parsing performance
- `urllib3` - For connection pooling and retries

All dependencies are compatible with Python 3.8+ (tested with Python 3.13.3).

## Note

Please use this scraper responsibly and in accordance with the AoPS Wiki's terms of service.