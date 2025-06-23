#!/usr/bin/env python3
"""Test script to verify AMC scraper functionality"""

from scraper import AMCScraper
import json

def test_single_problem():
    """Test scraping a single problem"""
    scraper = AMCScraper()
    
    # Test with 2024 AMC 10A Problem 1 (which we know exists)
    print("Testing scraper with 2024 AMC 10A Problem 1...")
    result = scraper.scrape_problem(2024, 'A', 1)
    
    if result:
        print("\nScraped data:")
        print(json.dumps(result, indent=2))
        
        # Verify structure
        assert 'problem' in result, "Missing 'problem' key"
        assert 'options' in result, "Missing 'options' key"
        assert 'solutions' in result, "Missing 'solutions' key"
        
        print("\n✓ Structure validation passed")
        
        # Check if we got actual content
        if result['problem']:
            print(f"✓ Problem text found ({len(result['problem'])} characters)")
        else:
            print("✗ No problem text found")
            
        if result['options']:
            print(f"✓ Options found ({len(result['options'])} options)")
        else:
            print("✗ No options found")
            
        if result['solutions']:
            print(f"✓ Solutions found ({len(result['solutions'])} solutions)")
        else:
            print("✗ No solutions found")
    else:
        print("✗ Failed to scrape problem")

if __name__ == "__main__":
    test_single_problem()