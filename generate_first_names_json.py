import json
from pathlib import Path
import os


# Files are stored locally on my desktop
TXT_SOURCE_DIR = Path("/Users/katie.sipos/Desktop/names")

# Where I want to names saved to
OUTPUT_PATH = Path("data/first_names.json")

# Extract the unique names from the files from the baby name registry.
def extract_unique_names(directory):
    names = set()
    # For each file saved in my local folder
    for file in directory.glob("*.txt"):
        try:
            with open(file, 'r') as f:
                for line in f:
                    # Split on the comma and take the first value, which is the name
                    name = line.split(',')[0].strip()
                    if name:
                        names.add(name)
        except Exception as e:
            print(f"⚠️  Error reading {file.name}: {e}")
    return sorted(names)

if __name__ == "__main__":
    try:
        # Call function with location of text files
        names = extract_unique_names(TXT_SOURCE_DIR)
        if not names:
            print("⚠️  No names were found. Check if your source folder contains valid .txt files.")
        else:
            # Create the output directory if it doesn't exist
            os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
            with open(OUTPUT_PATH, 'w') as f:
                # Add names to the file, make it a little human readable
                json.dump(names, f, indent=2)
            print(f"✅ Extracted {len(names)} names to {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Failed to complete the export: {e}")
