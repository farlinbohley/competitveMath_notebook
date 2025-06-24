#!/usr/bin/env python3
import re

# Test with actual LaTeX text from the HTML
test_cases = [
    r"$\mathrm{(A) \ } 2\qquad \mathrm{(B) \ } 4\qquad \mathrm{(C) \ } 5\qquad \mathrm{(D) \ } 10\qquad \mathrm{(E) \ } 20$",
    r"$\mathrm{(A) \ } -8\qquad \mathrm{(B) \ } -4\qquad \mathrm{(C) \ } -2\qquad \mathrm{(D) \ } 4\qquad \mathrm{(E) \ } 8$",
    r"$\mathrm{(A) \ } 100\qquad \mathrm{(B) \ } 200\qquad \mathrm{(C) \ } 300\qquad \mathrm{(D) \ } 400\qquad \mathrm{(E) \ } 500$"
]

def test_pattern(pattern_desc, pattern, test_text):
    print(f"\n{pattern_desc}:")
    print(f"Pattern: {pattern}")
    print(f"Test text: {test_text}")
    try:
        matches = re.findall(pattern, test_text)
        print(f"Matches: {matches}")
        if matches:
            options = {}
            for letter, content in matches:
                options[letter] = content.strip()
            print(f"Options dict: {options}")
    except Exception as e:
        print(f"Error: {e}")

for i, test_text in enumerate(test_cases):
    print(f"\n=== Test case {i+1} ===")
    print(f"Original: {test_text}")
    
    # Split approach
    parts = test_text.split(r'\qquad')
    print(f"Split parts: {parts}")
    
    options = {}
    for part in parts:
        print(f"  Processing part: '{part}'")
        
        # Look for the pattern \mathrm{(X) \ } followed by content
        letter_match = re.search(r'\\mathrm\{\(([A-E])\) \\ \}', part)
        if letter_match:
            letter = letter_match.group(1)
            print(f"    Found letter: {letter}")
            
            # Extract content after the mathrm part
            content_start = letter_match.end()
            content = part[content_start:].strip()
            
            # Clean up content - remove trailing $ and other LaTeX stuff
            content = re.sub(r'[\$]+$', '', content).strip()
            print(f"    Raw content: '{content}'")
            
            if content:
                options[letter] = content
                print(f"    Added option {letter}: '{content}'")
    
    print(f"Final options: {options}")
    
    # Test alternative regex on full string
    print(f"\nAlternative full regex:")
    pattern = r'\\mathrm\{\(([A-E])\) \\ \} ([^\\]+?)(?=\\qquad|$)'
    matches = re.findall(pattern, test_text)
    print(f"Full regex matches: {matches}")
    if matches:
        alt_options = {letter: content.replace('$', '').strip() for letter, content in matches}
        print(f"Alternative options: {alt_options}")
    
    # Pattern 1: Simple approach
    test_pattern(
        "Simple pattern",
        r'\\mathrm\{\\(([A-E])\\) \\\\ \} ([^\\]+?)(?=\\qquad|$)',
        test_text
    )
    
    # Pattern 2: More flexible
    test_pattern(
        "Flexible pattern", 
        r'\\mathrm\{\\(([A-E])\\)[^}]*\} ([^\\]+?)(?=\\qquad|$)',
        test_text
    )
    
    # Pattern 3: Split approach
    print("\nSplit approach:")
    parts = test_text.split(r'\qquad')
    print(f"Split parts: {parts}")
    
    options = {}
    for part in parts:
        letter_match = re.search(r'\\mathrm\{\\(([A-E])\\)', part)
        if letter_match:
            letter = letter_match.group(1)
            # Extract content after the mathrm part
            content_start = letter_match.end()
            content = part[content_start:].strip()
            # Clean up content
            content = re.sub(r'[\\}$\s]+$', '', content).strip()
            if content:
                options[letter] = content
    
    print(f"Split result: {options}") 