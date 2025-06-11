#!/usr/bin/env python3
"""
First Name Generator

This script extracts unique first names from text files and exports them as JSON.
Each source file is expected to contain names in CSV format, with the name as the first column.
"""

import json
import os
from pathlib import Path
from typing import List, Set


# Constants
# Files are stored locally on the desktop
TXT_SOURCE_DIR = Path("/Users/katie.sipos/Desktop/names")

# Output file path for the processed names
OUTPUT_PATH = Path("data/first_names.json")


def extract_unique_names(directory: Path) -> List[str]:
    """
    Extract unique names from text files in the specified directory.

    Args:
        directory: Path object pointing to the directory containing name files

    Returns:
        A sorted list of unique names extracted from all files

    Note:
        Each text file should contain names in CSV format with the name as the first value
    """
    names: Set[str] = set()

    # Process each text file in the directory
    for file in directory.glob("*.txt"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Split on the comma and take the first value, which is the name
                    name = line.split(',')[0].strip()
                    if name:
                        names.add(name)
        except FileNotFoundError:
            print(f"⚠️  File not found: {file.name}")
        except PermissionError:
            print(f"⚠️  Permission denied when reading {file.name}")
        except Exception as e:
            print(f"⚠️  Error reading {file.name}: {e}")

    # Return names in alphabetical order
    return sorted(names)


def save_names_to_json(names: List[str], output_path: Path) -> None:
    """
    Save the list of names to a JSON file.

    Args:
        names: List of names to save
        output_path: Path where the JSON file will be saved
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_path.parent, exist_ok=True)

    # Write the names to a JSON file with pretty formatting
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(names, f, indent=2)

    print(f"✅ Extracted {len(names)} names to {output_path}")


def main() -> None:
    """Main function to orchestrate the name extraction and saving process."""
    try:
        # Extract unique names from source files
        names = extract_unique_names(TXT_SOURCE_DIR)

        # Validate that names were found
        if not names:
            print("⚠️  No names were found. Check if your source folder contains valid .txt files.")
            return

        # Save the names to a JSON file
        save_names_to_json(names, OUTPUT_PATH)

    except Exception as e:
        print(f"❌ Failed to complete the export: {e}")


if __name__ == "__main__":
    main()
