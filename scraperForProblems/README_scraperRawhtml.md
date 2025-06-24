# AMC Raw HTML Scraper

This script downloads raw HTML content from Art of Problem Solving (AoPS) AMC 10 problem pages for further analysis and processing.

## Features

- Downloads complete HTML content from AoPS AMC 10 problem pages
- Supports year ranges (e.g., 2020-2024)
- Supports both A and B contests
- Rate limiting to respect server resources
- Progress tracking for batch downloads
- Error handling for missing pages

## Installation

Ensure you have the required dependencies installed:

```bash
pip install requests
```

## Usage

### Basic Usage

Download a single year (both A and B contests):
```bash
python scraperRawhtml.py --years 2024
```

### Download Specific Contest Type

Download only A contests for a year:
```bash
python scraperRawhtml.py --years 2024 --contests A
```

Download only B contests:
```bash
python scraperRawhtml.py --years 2024 --contests B
```

### Year Ranges

Download multiple years:
```bash
python scraperRawhtml.py --years 2020-2024
```

Download from a year to current year:
```bash
python scraperRawhtml.py --years 2022-
```

### Advanced Options

Custom output directory:
```bash
python scraperRawhtml.py --years 2024 --output-dir /path/to/output
```

Adjust rate limiting delay (in seconds):
```bash
python scraperRawhtml.py --years 2020-2024 --delay 2.0
```

## Output

HTML files are saved in the format:
- `YYYY_AMC_10{A|B}_Problems.html`

Default output directory:
- `scraperForProblems/raw_html/`

## Examples

1. Download all 2024 contests:
   ```bash
   python scraperRawhtml.py --years 2024
   ```

2. Download 2020-2024 B contests only:
   ```bash
   python scraperRawhtml.py --years 2020-2024 --contests B
   ```

3. Download 2022 to current year with 2-second delay:
   ```bash
   python scraperRawhtml.py --years 2022- --delay 2
   ```

## Notes

- The scraper includes a user-agent header for educational use
- Default delay between requests is 1 second
- The script detects non-existent pages and reports them
- Progress is logged to console during batch downloads 