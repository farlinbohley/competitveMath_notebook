#!/usr/bin/env python3
"""
Reusable AMC 10 Problems Scraper
Extracts problems, options, and solutions from raw HTML files from a target directory.
"""

import os
import json
import re
import sys
from bs4 import BeautifulSoup
from pathlib import Path

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text

def extract_options_from_latex_img(img_tag):
    """Extract options from LaTeX image alt text.

    This function tokenises the LaTeX alt text on ``\qquad`` – the delimiter used
    on AoPS to separate the answer choices – and then pulls out the option label
    *(A)* .. *(E)* together with the accompanying text (which may itself be a
    LaTeX snippet such as ``-\\frac{2}{3}``).  The raw LaTeX for each choice is
    kept (lightly cleaned) because translating every possible mathematical
    construct to plain text reliably is non-trivial and not required for the
    JSON structure.
    """

    options = {}

    if not img_tag or not img_tag.get("alt"):
        return options

    alt_text = img_tag.get("alt", "")

    # Strip surrounding dollar signs if present
    alt_text = alt_text.strip("$")

    # Split on AoPS separator between answer choices
    tokens = re.split(r"\\qquad", alt_text)

    for tok in tokens:
        # Example token forms:
        #   "\\mathrm{(A) \\ } 2" or "(C) 0"
        #   may still contain spaces / LaTeX commands
        letter_match = re.search(r"\(([A-E])\)", tok)
        if not letter_match:
            continue
        letter = letter_match.group(1)

        # Everything after the option label is the text of the choice
        # Remove up to and including the closing parenthesis & optional brackets
        content_part = re.split(r"\)" , tok, maxsplit=1)
        option_text = content_part[1] if len(content_part) > 1 else ""

        # Light clean-up
        option_text = option_text.replace("\\", "\\")  # keep backslashes
        option_text = clean_text(option_text)

        if option_text:
            options[letter] = option_text

    return options

def parse_html_file(file_path):
    """Parse a single HTML file and extract problems"""
    problems = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all problem sections
    problem_sections = soup.find_all('h2')
    
    for section in problem_sections:
        span = section.find('span', class_='mw-headline')
        if not span or not span.get('id'):
            continue
            
        section_id = span.get('id')
        if not section_id.startswith('Problem_'):
            continue
            
        # Extract problem number
        problem_num = section_id.replace('Problem_', '')
        if not problem_num.isdigit():
            continue
            
        # Get the content after this header until the next header
        problem_content = []
        current = section.next_sibling
        
        while current and (not hasattr(current, 'name') or current.name != 'h2'):
            if hasattr(current, 'get_text'):
                problem_content.append(current)
            current = current.next_sibling
        
        # Extract problem text, options and solution link
        problem_text_parts = []
        options = {}
        solutions = []

        for element in problem_content:
            if not hasattr(element, 'name'):
                continue

            # Paragraph handling – may contain text, options, or the solution link
            if element.name == 'p':
                # Capture <a>Solution</a> links early
                sol_link = element.find('a', string=lambda x: x and x.strip().lower() == 'solution')
                if sol_link and sol_link.get('href'):
                    full_url = f"https://artofproblemsolving.com{sol_link['href']}"
                    solutions.append({"title": "Solution", "url": full_url})

                # Check for LaTeX images carrying the options
                img_tags = element.find_all('img', class_='latex')

                found_options = False
                for img in img_tags:
                    extracted_options = extract_options_from_latex_img(img)
                    if extracted_options:
                        options.update(extracted_options)
                        found_options = True

                # Collect problem statement text (omit the Solution-only paragraph)
                text = element.get_text(separator=" ")
                if text:
                    text = text.strip()

                if not found_options and (not sol_link):
                    problem_text_parts.append(text)
        
        problem_text = clean_text(' '.join(problem_text_parts))
        
        if problem_text:  # Only add if we found actual problem content
            problems[problem_num] = {
                "problem": problem_text,
                "options": options,
                "solutions": solutions
            }
    
    return problems

def process_directory(html_dir):
    """Processes all HTML files in a given directory."""
    if not html_dir.exists():
        print(f"Directory {html_dir} not found!")
        return

    all_problems = {}
    html_files = sorted(html_dir.glob("*.html"))

    for html_file in html_files:
        print(f"Processing {html_file.name}...")
        
        filename = html_file.stem
        parts = filename.split('_')
        if len(parts) >= 3:
            year = parts[0]
            contest_name = f"{parts[1]}_{parts[2]}" # e.g., "AMC_10A"
            contest_key = f"{year}_{contest_name}_Problems"
            
            problems = parse_html_file(html_file)
            
            if problems:
                all_problems[contest_key] = problems
                print(f"  Found {len(problems)} problems")

    output_file = html_dir / f"{html_dir.name}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_problems, f, indent=2, ensure_ascii=False)
    
    print(f"\nConsolidated data for {html_dir.name} saved to {output_file}")
    total_problems = sum(len(p) for p in all_problems.values())
    print(f"Total problems extracted: {total_problems}\n")

def main():
    """Main function to process all HTML files and create consolidated JSON"""
    
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <directory1> <directory2> ...")
        return

    for dir_name in sys.argv[1:]:
        html_dir = Path(dir_name)
        process_directory(html_dir)


if __name__ == "__main__":
    main()