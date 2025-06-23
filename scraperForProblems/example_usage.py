#!/usr/bin/env python3
"""
Example usage of the AMC 10 Problem Scraper

This script demonstrates various ways to use the scraper programmatically.
"""

from scraper import AMCScraper
import json

def example_single_problem():
    """Example: Scrape a single problem"""
    print("Example 1: Scraping a single problem")
    print("-" * 40)
    
    scraper = AMCScraper()
    problem_data = scraper.scrape_problem(2023, 'A', 1)
    
    if problem_data:
        print(f"Problem: {problem_data['problem'][:100]}...")
        print(f"Number of options: {len(problem_data['options'])}")
        print(f"Number of solutions: {len(problem_data['solutions'])}")
    print()

def example_full_contest():
    """Example: Scrape a full contest"""
    print("Example 2: Scraping a full contest")
    print("-" * 40)
    
    scraper = AMCScraper()
    contest_data = scraper.scrape_contest(2022, 'B')
    
    print(f"Problems scraped: {len(contest_data)}")
    print(f"Problem numbers: {sorted(contest_data.keys(), key=int)}")
    
    # Save to file
    scraper.save_contest_data(2022, 'B', contest_data)
    print()

def example_year_range():
    """Example: Scrape multiple years"""
    print("Example 3: Scraping multiple years")
    print("-" * 40)
    
    scraper = AMCScraper()
    years = [2020, 2021]
    contests = ['A', 'B']
    
    scraper.scrape_years(years, contests)
    print(f"Scraped {len(years)} years × {len(contests)} contests = {len(years) * len(contests)} total contests")
    print()

def example_custom_output():
    """Example: Use custom output directory"""
    print("Example 4: Custom output directory")
    print("-" * 40)
    
    custom_dir = "./my_amc_problems"
    scraper = AMCScraper(output_dir=custom_dir)
    
    # Scrape one contest to custom directory
    contest_data = scraper.scrape_contest(2021, 'A')
    scraper.save_contest_data(2021, 'A', contest_data)
    
    print(f"Data saved to: {custom_dir}/2021_AMC_10A.json")
    print()

def example_error_handling():
    """Example: Demonstrate error handling"""
    print("Example 5: Error handling")
    print("-" * 40)
    
    scraper = AMCScraper()
    
    # Try to scrape a problem that likely doesn't exist
    problem_data = scraper.scrape_problem(1999, 'A', 30)  # AMC 10 only has 25 problems
    
    if problem_data is None:
        print("Problem not found (as expected)")
    print()

if __name__ == "__main__":
    print("AMC 10 Scraper - Usage Examples")
    print("=" * 40)
    print()
    
    # Note: Comment out examples you don't want to run
    # to avoid making too many requests
    
    example_single_problem()
    # example_full_contest()
    # example_year_range()
    # example_custom_output()
    example_error_handling()
    
    print("\nFor command-line usage, see README.md")