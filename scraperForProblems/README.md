# AMC 10 Problem Scraper

This Python script scrapes AMC 10A and AMC 10B problems from the Art of Problem Solving (AoPS) Wiki.

## Features

- Scrapes problem statements, multiple-choice options, and all solutions
- Handles both AMC 10A and AMC 10B contests
- Configurable year ranges
- Saves data in structured JSON format
- Robust error handling for missing pages (404 errors)
- Respectful scraping with delays between requests

## Installation

1. Navigate to the scraper directory:
   ```bash
   cd scraperForProblems
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The script can be run from the command line with various options:

### Basic Usage

Scrape a single year (both A and B contests):
```bash
python scraper.py --years 2023
```

### Scrape Multiple Years

Scrape a range of years:
```bash
python scraper.py --years 2020-2023
```

### Scrape Specific Contests

Scrape only AMC 10A:
```bash
python scraper.py --years 2023 --contests A
```

Scrape only AMC 10B:
```bash
python scraper.py --years 2023 --contests B
```

### Custom Output Directory

Specify a custom output directory:
```bash
python scraper.py --years 2023 --output-dir /path/to/output
```

## Output Format

The scraper saves data in JSON format with the following structure:

```json
{
  "1": {
    "problem": "Text of the problem",
    "options": ["(A) option1", "(B) option2", "(C) option3", "(D) option4", "(E) option5"],
    "solutions": ["Solution 1: solution text", "Solution 2: solution text", ...]
  },
  "2": {
    ...
  }
}
```

Files are named using the pattern: `YYYY_AMC_10{A|B}.json`

## Default Output Location

By default, files are saved to: `../Competitive-Math-Notebook-Library/AMC10/`

## Examples

1. Scrape all AMC 10 problems from 2020 to 2023:
   ```bash
   python scraper.py --years 2020-2023
   ```

2. Scrape only AMC 10A problems from 2022:
   ```bash
   python scraper.py --years 2022 --contests A
   ```

3. Scrape AMC 10B problems from 2021 and save to a custom directory:
   ```bash
   python scraper.py --years 2021 --contests B --output-dir ./my_problems
   ```

## Notes

- The script includes a 0.5-second delay between requests to be respectful to the AoPS server
- If a problem page doesn't exist (404 error), the script will log a warning and continue
- The scraper handles various HTML formats used on the AoPS Wiki
- LaTeX expressions are preserved in the output

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are installed correctly
2. Check your internet connection
3. Verify that the AoPS Wiki is accessible
4. Check the log output for specific error messages

## License

This scraper is for educational purposes only. Please respect the AoPS Wiki's terms of service and use the scraped content appropriately.