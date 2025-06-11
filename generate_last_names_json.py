#!/usr/bin/env python3
"""
Last Name Generator

This script scrapes a website to collect last names/surnames and exports them as JSON.
It processes pages for each letter of the alphabet and extracts names from HTML table cells.
"""

import json
import os
import string
import time
from pathlib import Path
from typing import List, Set

import requests
from bs4 import BeautifulSoup


# Constants
# Base URL for the website containing surname data
BASE_URL = "https://one-name.org/surnames_A-Z/"

# Only use lowercase letters for scraping (more efficient than using all letters)
LETTERS = list(string.ascii_lowercase)

# Output file path for the processed surnames
OUTPUT_PATH = Path("data/last_names.json")


def extract_surnames() -> List[str]:
    """
    Scrape surnames from a website by iterating through pages for each letter.

    Returns:
        A sorted list of unique surnames extracted from all pages

    Note:
        Uses a 1 second delay between requests to be respectful to the server
    """
    surnames: Set[str] = set()

    for letter in LETTERS:
        try:
            # Construct the URL for this letter's page
            url = f"{BASE_URL}?initial={letter}"
            print(f"🔍 Scraping letter {letter}...")

            # Request the page with a timeout to avoid hanging indefinitely
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse the HTML and find all table cells
            soup = BeautifulSoup(response.text, "html.parser")
            td_tags = soup.find_all("td")

            # Track how many new names we find for this letter
            count_before = len(surnames)

            # Process each table cell
            for td in td_tags:
                text = td.get_text(strip=True)
                # Only accept purely alphabetic names
                if text.isalpha():
                    surnames.add(text)

            print(f"→ Found {len(surnames) - count_before} new names for {letter}")

            # Be respectful to the server by adding a delay between requests
            time.sleep(1)

        except requests.RequestException as e:
            print(f"⚠️  Network error when scraping {letter}: {e}")
        except Exception as e:
            print(f"⚠️  Error scraping {letter}: {e}")

    # Return surnames in alphabetical order
    return sorted(surnames)


def save_surnames_to_json(surnames: List[str], output_path: Path) -> None:
    """
    Save the list of surnames to a JSON file.

    Args:
        surnames: List of surnames to save
        output_path: Path where the JSON file will be saved
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_path.parent, exist_ok=True)

    # Write the surnames to a JSON file with pretty formatting
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(surnames, f, indent=2)

    print(f"✅ Extracted {len(surnames)} surnames to {output_path}")


def main() -> None:
    """Main function to orchestrate the surname scraping and saving process."""
    try:
        # Get all surnames from A–Z pages
        surnames = extract_surnames()

        # Validate that surnames were found
        if not surnames:
            print("⚠️  No surnames were found. Check the site structure or your connection.")
            return

        # Save the surnames to a JSON file
        save_surnames_to_json(surnames, OUTPUT_PATH)

    except Exception as e:
        print(f"❌ Failed to complete the scraping: {e}")


if __name__ == "__main__":
    main()
