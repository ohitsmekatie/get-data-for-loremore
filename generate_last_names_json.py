import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
import os

BASE_URL = "https://one-name.org/surnames_A-Z/"
LETTERS = [chr(i) for i in range(ord("A"), ord("Z")+1)]

OUTPUT_PATH = Path("data/last_names.json")

def extract_surnames():
    surnames = set()
    for letter in LETTERS:
        try:
            url = f"{BASE_URL}?initial={letter}"
            print(f"🔍 Scraping letter {letter}...")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            td_tags = soup.find_all("td")

            count_before = len(surnames)
            for td in td_tags:
                text = td.get_text(strip=True)
                if text.isalpha():
                    surnames.add(text)
            print(f"→ Found {len(surnames) - count_before} new names for {letter}")

            time.sleep(1)  # Be polite to the server

        except Exception as e:
            print(f"⚠️  Error scraping {letter}: {e}")

    return sorted(surnames)

if __name__ == "__main__":
    try:
        # Get all surnames from A–Z pages
        names = extract_surnames()
        if not names:
            print("⚠️  No surnames were found. Check the site structure or your connection.")
        else:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
            with open(OUTPUT_PATH, 'w') as f:
                # Save names to file, indented for readability
                json.dump(names, f, indent=2)
            print(f"✅ Extracted {len(names)} surnames to {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Failed to complete the scraping: {e}")
