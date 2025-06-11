# Data Scripts

👋 This repository contains scripts for collecting data from various sources to populate the database for my website [Lore & More](https://ohitsmetables.com/), which is a resource for world building and TTRPG game prep.


## Overview

The repository includes scripts to:

1. Extract first names from local text files (CSV format)

### First Name Generator (`generate_first_names_json.py`)

**Data Source**: The script processes files from the SSA's published dataset of most popular baby names by year. These files are stored in `.txt` format with comma-separated values.

**Process**:
- Reads all `.txt` files from a configurable source directory (`/Users/katie.sipos/Desktop/names/`)
- Extracts the first column from each line, which contains the first name
- Deduplicates names (using a set data structure)
- Sorts names alphabetically
- Exports the unique names as a JSON array to `data/first_names.json`

**Key Features**:
- Error handling for file access issues
- Progress and status reporting in terminal
- UTF-8 encoding support for international names
- Type hints for better code readability and IDE support

**Example Usage**:
```bash
python generate_first_names_json.py
# ✅ Extracted 18,452 names to data/first_names.json
```

The output file is used in a random name generator for the Lore & More website.


2. Scrape last names from [one-name.org](https://one-name.org/surnames_a-z/)

### Last Name Generator (`generate_last_names_json.py`)

**Data Source**: The script scrapes surname data from the [one-name.org](https://one-name.org/surnames_a-z/) website, which contains a comprehensive list of surnames organized alphabetically.

**Process**:
- Iterates through each letter of the alphabet
- Makes HTTP requests to pages for each letter (e.g., `?initial=a`, `?initial=b`, etc.)
- Parses the HTML response using BeautifulSoup to extract surname text from table cells
- Filters to only include pure alphabetical names (no special characters)
- Deduplicates and sorts the extracted surnames
- Exports the unique surnames as a JSON array to `data/last_names.json`

**Key Features**:
- Polite web scraping with 1-second delay between requests
- Network error handling with timeout protection
- Progress indicators showing names found per letter
- Type hints for better code readability

**Example Usage**:
```bash
python generate_last_names_json.py

# 🔍 Scraping letter a...
# → Found 2,547 new names for a
# ...
# ✅ Extracted 15,873 surnames to data/last_names.json
```

The output file is used alongside first names in the random name generator.

---

These are just manual scripts to run locally for now, but my plan is to automate these in some way to be used directory from the Lore & More site.

## Setup and Requirements

### Prerequisites

- Python 3.6+
- Local directory with first name data files (for `generate_first_names_json.py`). This can be anything! It's just hardcoded for my own local directory right now

### Dependencies

- Required Python packages:
  - `requests` - For making HTTP requests to web sources
  - `beautifulsoup4` - For parsing HTML content


## Data Sources

### First Names
- **Source**: Social Security Administration (SSA) baby name data
- **Format**: Text files with comma-separated values
- **Location**: Local directory (`/Users/katie.sipos/Desktop/names/`)
- **Content**: Each file contains yearly records of popular baby names
- **Output**: `data/first_names.json` - Alphabetically sorted array of unique names

### Last Names
- **Source**: [one-name.org/surnames_a-z/](https://one-name.org/surnames_a-z/)
- **Format**: Web-based data scraped from HTML tables
- **Content**: Comprehensive list of surnames organized alphabetically
- **Output**: `data/last_names.json` - Alphabetically sorted array of unique surnames

## Usage in Lore & More

These name datasets are used to power random character generators and other world-building tools on the [Lore & More](https://ohitsmetables.com/) website. The JSON format makes it easy to integrate with web applications and database imports.
