#!/usr/bin/env python3
"""
Raw HTML Scraper for AMC 10 Problems from Art of Problem Solving (AoPS) Wiki
Downloads and saves the complete HTML content for AMC 10A and 10B problem pages
"""

import argparse
import os
import time
from typing import List, Tuple
import requests
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AMCRawHTMLScraper:
    """Scraper for downloading raw HTML from AoPS AMC 10 problem pages"""
    
    BASE_URL = "https://artofproblemsolving.com/wiki/index.php/{year}_AMC_10{contest}_Problems"
    
    def __init__(self, output_dir: str = "scraperForProblems/raw_html", delay: float = 1.0):
        """
        Initialize the scraper
        
        Args:
            output_dir: Directory to save raw HTML files
            delay: Delay between requests in seconds (for rate limiting)
        """
        self.output_dir = output_dir
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AMC Problem Scraper; Educational Use)'
        })
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
    def download_html(self, year: int, contest: str) -> Tuple[bool, str]:
        """
        Download HTML for a specific AMC 10 contest
        
        Args:
            year: Year of the contest
            contest: Contest type ('A' or 'B')
            
        Returns:
            Tuple of (success, message)
        """
        url = self.BASE_URL.format(year=year, contest=contest)
        filename = f"{year}_AMC_10{contest}_Problems.html"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            logger.info(f"Downloading {year} AMC 10{contest} from {url}")
            
            # Make the request
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if the page exists (AoPS returns 200 even for non-existent pages)
            if "There is currently no text in this page" in response.text:
                return False, f"Page does not exist for {year} AMC 10{contest}"
            
            # Save the HTML content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            logger.info(f"Successfully saved to {filepath}")
            return True, f"Successfully downloaded {year} AMC 10{contest}"
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error downloading {year} AMC 10{contest}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error for {year} AMC 10{contest}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def scrape_range(self, start_year: int, end_year: int, contests: List[str]) -> dict:
        """
        Scrape a range of years and contests
        
        Args:
            start_year: Starting year (inclusive)
            end_year: Ending year (inclusive)
            contests: List of contest types to scrape ('A' and/or 'B')
            
        Returns:
            Dictionary with results summary
        """
        results = {
            'successful': [],
            'failed': [],
            'total': 0
        }
        
        total_tasks = (end_year - start_year + 1) * len(contests)
        completed = 0
        
        logger.info(f"Starting to scrape {total_tasks} contests from {start_year} to {end_year}")
        
        for year in range(start_year, end_year + 1):
            for contest in contests:
                # Update progress
                completed += 1
                progress = (completed / total_tasks) * 100
                logger.info(f"Progress: {completed}/{total_tasks} ({progress:.1f}%)")
                
                # Download the HTML
                success, message = self.download_html(year, contest)
                
                if success:
                    results['successful'].append(f"{year} AMC 10{contest}")
                else:
                    results['failed'].append(f"{year} AMC 10{contest}: {message}")
                
                results['total'] += 1
                
                # Rate limiting
                if completed < total_tasks:
                    time.sleep(self.delay)
        
        return results
    
    def print_summary(self, results: dict):
        """Print a summary of the scraping results"""
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        print(f"Total contests processed: {results['total']}")
        print(f"Successful downloads: {len(results['successful'])}")
        print(f"Failed downloads: {len(results['failed'])}")
        
        if results['successful']:
            print("\nSuccessfully downloaded:")
            for item in sorted(results['successful']):
                print(f"  ✓ {item}")
        
        if results['failed']:
            print("\nFailed downloads:")
            for item in results['failed']:
                print(f"  ✗ {item}")
        
        print("\nHTML files saved to:", os.path.abspath(self.output_dir))


def parse_year_range(year_string: str) -> Tuple[int, int]:
    """
    Parse year range from string
    
    Args:
        year_string: String like "2020", "2020-2023", or "2020-"
        
    Returns:
        Tuple of (start_year, end_year)
    """
    current_year = datetime.now().year
    
    if '-' in year_string:
        parts = year_string.split('-')
        start = int(parts[0])
        end = int(parts[1]) if parts[1] else current_year
        return start, end
    else:
        year = int(year_string)
        return year, year


def main():
    parser = argparse.ArgumentParser(
        description='Download raw HTML from AoPS AMC 10 problem pages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --years 2024                    # Download 2024 AMC 10A and 10B
  %(prog)s --years 2020-2024               # Download 2020-2024 AMC 10A and 10B
  %(prog)s --years 2023 --contests A       # Download only 2023 AMC 10A
  %(prog)s --years 2020-2024 --contests B  # Download only B contests for 2020-2024
  %(prog)s --years 2022- --delay 2         # Download 2022 to current year with 2s delay
        """
    )
    
    parser.add_argument(
        '--years',
        type=str,
        required=True,
        help='Year or year range (e.g., "2024", "2020-2024", "2022-")'
    )
    
    parser.add_argument(
        '--contests',
        nargs='+',
        choices=['A', 'B'],
        default=['A', 'B'],
        help='Contest types to download (default: both A and B)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='scraperForProblems/raw_html',
        help='Output directory for HTML files (default: scraperForProblems/raw_html)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    # Parse year range
    try:
        start_year, end_year = parse_year_range(args.years)
    except ValueError:
        parser.error(f"Invalid year format: {args.years}")
        return
    
    # Validate years
    current_year = datetime.now().year
    if start_year < 2000 or end_year > current_year:
        parser.error(f"Years should be between 2000 and {current_year}")
        return
    
    if start_year > end_year:
        parser.error("Start year cannot be greater than end year")
        return
    
    # Create scraper and run
    scraper = AMCRawHTMLScraper(output_dir=args.output_dir, delay=args.delay)
    
    print(f"\nScraping AMC 10 problems from {start_year} to {end_year}")
    print(f"Contests: {', '.join(args.contests)}")
    print(f"Output directory: {os.path.abspath(args.output_dir)}")
    print(f"Rate limit delay: {args.delay}s between requests")
    print("\n")
    
    results = scraper.scrape_range(start_year, end_year, args.contests)
    scraper.print_summary(results)


if __name__ == "__main__":
    main() 