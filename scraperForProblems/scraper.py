#!/usr/bin/env python3
"""
AMC 10 Problem Scraper for Art of Problem Solving Wiki
Scrapes AMC 10A and AMC 10B problems, options, and solutions
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AMCScraper:
    """Scraper for AMC 10 problems from AoPS Wiki"""
    
    BASE_URL = "https://artofproblemsolving.com/wiki/index.php/{year}_AMC_10{contest}_Problems/Problem_{number}"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    def __init__(self, output_dir: str = "Competitive-Math-Notebook-Library/AMC10"):
        self.output_dir = output_dir
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update(self.HEADERS)
        return session
    
    def scrape_problem(self, year: int, contest: str, problem_num: int) -> Optional[Dict]:
        """Scrape a single problem from the AoPS Wiki"""
        url = self.BASE_URL.format(year=year, contest=contest, number=problem_num)
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract problem data
            problem_data = {
                "problem": self._extract_problem_text(soup),
                "options": self._extract_options(soup),
                "solutions": self._extract_solutions(soup)
            }
            
            return problem_data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"Problem {problem_num} for {year} AMC 10{contest} not found (404)")
            else:
                logger.error(f"HTTP error for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def _extract_problem_text(self, soup: BeautifulSoup) -> str:
        """Extract the problem text from the page"""
        # Find the Problem section
        problem_header = soup.find('span', {'id': 'Problem', 'class': 'mw-headline'})
        if not problem_header:
            problem_header = soup.find('span', {'class': 'mw-headline'}, text='Problem')
        
        if problem_header:
            # Get the parent h2 tag and find the next sibling paragraphs
            h2_tag = problem_header.parent
            problem_text_parts = []
            
            current = h2_tag.next_sibling
            while current:
                if current.name == 'h2':  # Stop at next section
                    break
                if current.name == 'p':
                    text = current.get_text(strip=True)
                    if text:
                        problem_text_parts.append(text)
                elif hasattr(current, 'get_text'):
                    text = current.get_text(strip=True)
                    if text and not text.startswith('$'):  # Skip pure LaTeX
                        problem_text_parts.append(text)
                current = current.next_sibling
            
            # Join and clean up the problem text
            problem_text = ' '.join(problem_text_parts)
            
            # Clean up LaTeX formatting
            problem_text = re.sub(r'\$([^$]+)\$', r'$\1$', problem_text)
            problem_text = re.sub(r'\s+', ' ', problem_text).strip()
            
            return problem_text
        
        return ""
    
    def _extract_options(self, soup: BeautifulSoup) -> List[str]:
        """Extract multiple choice options from the problem text"""
        options = []
        
        # Look for the standard format: (A) option1 (B) option2 etc.
        problem_section = soup.find('span', {'id': 'Problem', 'class': 'mw-headline'})
        if not problem_section:
            problem_section = soup.find('span', {'class': 'mw-headline'}, text='Problem')
        
        if problem_section:
            h2_tag = problem_section.parent
            current = h2_tag.next_sibling
            
            while current:
                if current.name == 'h2':
                    break
                if hasattr(current, 'get_text'):
                    text = current.get_text()
                    # Look for options pattern
                    option_pattern = r'\(([A-E])\)\s*~?\s*([^(]+?)(?=\([A-E]\)|$)'
                    matches = re.findall(option_pattern, text)
                    if matches:
                        for letter, option_text in matches:
                            options.append(f"({letter}) {option_text.strip()}")
                current = current.next_sibling
        
        # If we found exactly 5 options, return them
        if len(options) == 5:
            return options
        
        # Otherwise, try a different pattern
        content = soup.get_text()
        textbf_pattern = r'\\textbf\{?\(([A-E])\)\}?\s*~?\s*([^\\]+?)(?=\\textbf|$)'
        matches = re.findall(textbf_pattern, content)
        
        if matches:
            options = [f"({letter}) {option.strip()}" for letter, option in matches[:5]]
        
        return options
    
    def _extract_solutions(self, soup: BeautifulSoup) -> List[str]:
        """Extract all solutions from the page"""
        solutions = []
        
        # Find all solution headers
        solution_headers = soup.find_all('span', {'class': 'mw-headline'})
        
        for header in solution_headers:
            header_text = header.get_text(strip=True)
            # Check if this is a solution header
            if re.match(r'^Solution\s*\d*', header_text, re.IGNORECASE):
                solution_content = []
                h2_tag = header.parent
                current = h2_tag.next_sibling
                
                while current:
                    # Stop at next h2 (next section)
                    if current.name == 'h2':
                        break
                    if hasattr(current, 'get_text'):
                        text = current.get_text(strip=True)
                        if text and not text.startswith('~'):  # Skip attributions
                            solution_content.append(text)
                    current = current.next_sibling
                
                if solution_content:
                    solution_text = ' '.join(solution_content)
                    # Clean up the solution text
                    solution_text = re.sub(r'\s+', ' ', solution_text).strip()
                    solutions.append(f"{header_text}: {solution_text}")
        
        return solutions
    
    def scrape_contest(self, year: int, contest: str) -> Dict[str, Dict]:
        """Scrape all problems for a given year and contest"""
        logger.info(f"Scraping {year} AMC 10{contest}...")
        contest_data = {}
        
        # AMC 10 has 25 problems
        for problem_num in range(1, 26):
            logger.info(f"Scraping problem {problem_num}...")
            problem_data = self.scrape_problem(year, contest, problem_num)
            
            if problem_data:
                contest_data[str(problem_num)] = problem_data
            
            # Be respectful to the server
            time.sleep(0.5)
        
        return contest_data
    
    def save_contest_data(self, year: int, contest: str, data: Dict[str, Dict]):
        """Save contest data to JSON file"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        filename = f"{year}_AMC_10{contest}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved data to {filepath}")
    
    def scrape_years(self, years: List[int], contests: List[str]):
        """Scrape multiple years and contests"""
        for year in years:
            for contest in contests:
                contest_data = self.scrape_contest(year, contest)
                if contest_data:
                    self.save_contest_data(year, contest, contest_data)
                else:
                    logger.warning(f"No data scraped for {year} AMC 10{contest}")


def parse_year_range(year_spec: str) -> List[int]:
    """Parse year specification (e.g., '2020', '2020-2023')"""
    if '-' in year_spec:
        start, end = year_spec.split('-')
        return list(range(int(start), int(end) + 1))
    else:
        return [int(year_spec)]


def main():
    parser = argparse.ArgumentParser(
        description='Scrape AMC 10 problems from Art of Problem Solving Wiki'
    )
    parser.add_argument(
        '--years',
        type=str,
        required=True,
        help='Year(s) to scrape (e.g., "2023" or "2020-2023")'
    )
    parser.add_argument(
        '--contests',
        nargs='+',
        choices=['A', 'B'],
        default=['A', 'B'],
        help='Contest versions to scrape (default: both A and B)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='Competitive-Math-Notebook-Library/AMC10',
        help='Output directory for JSON files'
    )
    
    args = parser.parse_args()
    
    # Parse years
    years = parse_year_range(args.years)
    
    # Create scraper and run
    scraper = AMCScraper(output_dir=args.output_dir)
    scraper.scrape_years(years, args.contests)
    
    logger.info("Scraping completed!")


if __name__ == "__main__":
    main()