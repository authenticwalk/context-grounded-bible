#!/usr/bin/env python3
"""
Strong's Dictionary Fetcher

This script fetches Strong's Hebrew and Greek dictionary data from the
openscriptures/strongs repository and generates YAML files for each entry.

Directory structure: bible/words/strongs/{strongs-number}/{strongs-number}.strongs.yaml

Strong's numbers use leading zeros:
- Greek: G0001-G5624 (4 digits)
- Hebrew: H0001-H8674 (4 digits)

Data sources:
- Greek: https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js
- Hebrew: https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.js
"""

import os
import re
import json
import yaml
import urllib.request
from pathlib import Path
from typing import Dict, Any

# Configuration
BASE_DIR = Path(__file__).parent
BIBLE_WORDS_DIR = BASE_DIR / "bible" / "words" / "strongs"

GREEK_URL = "https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js"
HEBREW_URL = "https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.js"


def download_file(url: str) -> str:
    """Download a file from URL and return its contents as string."""
    print(f"Downloading {url}...")
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


def parse_javascript_dict(js_content: str) -> Dict[str, Any]:
    """
    Parse JavaScript dictionary variable into Python dict.

    The JS files contain: var strongsGreekDictionary = { ... }
    We need to extract the JSON object part.
    """
    # Find the start of the object (first {)
    start_idx = js_content.find('{')
    # Find the closing of the object (matching })
    end_idx = js_content.rfind('}')

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find object boundaries in JavaScript file")

    # Extract the object content
    json_str = js_content[start_idx:end_idx + 1]

    # Parse as JSON
    return json.loads(json_str)


def format_strongs_number(strongs_num: str) -> str:
    """
    Format Strong's number with leading zeros.

    Examples:
        G1 -> G0001
        H157 -> H0157
        G5624 -> G5624
    """
    # Extract the prefix (G or H) and the number
    prefix = strongs_num[0]
    number = int(strongs_num[1:])

    # Format with 4-digit zero padding
    return f"{prefix}{number:04d}"


def create_strongs_yaml(strongs_num: str, entry: Dict[str, Any]) -> str:
    """
    Create YAML content for a Strong's entry.

    Format:
    ---
    strongs_number: G0001 or H0001
    language: greek or hebrew
    lemma: original language word
    transliteration: ...
    pronunciation: ...
    definition: ...
    kjv_usage: ...
    derivation: ...
    source: openscriptures/strongs
    license: CC-BY-SA
    """
    # Determine language
    language = "greek" if strongs_num.startswith('G') else "hebrew"

    # Build the YAML structure
    yaml_data = {
        "strongs_number": strongs_num,
        "language": language,
    }

    # Add fields based on what's available
    if "lemma" in entry:
        yaml_data["lemma"] = entry["lemma"]

    # Transliteration (different field names for Greek vs Hebrew)
    if "translit" in entry:
        yaml_data["transliteration"] = entry["translit"]
    elif "xlit" in entry:
        yaml_data["transliteration"] = entry["xlit"]

    # Pronunciation (Hebrew only)
    if "pron" in entry:
        yaml_data["pronunciation"] = entry["pron"]

    # Definition
    if "strongs_def" in entry:
        yaml_data["definition"] = entry["strongs_def"].strip()

    # KJV usage
    if "kjv_def" in entry:
        yaml_data["kjv_usage"] = entry["kjv_def"].strip()

    # Derivation/etymology
    if "derivation" in entry:
        yaml_data["derivation"] = entry["derivation"].strip()

    # Metadata
    yaml_data["source"] = "openscriptures/strongs"
    yaml_data["license"] = "CC-BY-SA"

    # Convert to YAML
    return yaml.dump(yaml_data, allow_unicode=True, sort_keys=False, default_flow_style=False)


def create_strongs_file(strongs_num: str, entry: Dict[str, Any]):
    """Create a YAML file for a Strong's entry with formatted number."""
    # Format the Strong's number with leading zeros
    formatted_num = format_strongs_number(strongs_num)

    # Create directory structure
    strongs_dir = BIBLE_WORDS_DIR / formatted_num
    strongs_dir.mkdir(parents=True, exist_ok=True)

    # Create YAML file
    yaml_path = strongs_dir / f"{formatted_num}.strongs.yaml"
    yaml_content = create_strongs_yaml(formatted_num, entry)

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    return yaml_path


def process_dictionary(url: str, dict_name: str):
    """Download and process a Strong's dictionary (Greek or Hebrew)."""
    print(f"\n{'='*60}")
    print(f"Processing {dict_name} dictionary...")
    print(f"{'='*60}\n")

    # Download the JS file
    js_content = download_file(url)

    # Parse the JavaScript dictionary
    print(f"Parsing {dict_name} dictionary...")
    dictionary = parse_javascript_dict(js_content)

    print(f"Found {len(dictionary)} entries in {dict_name} dictionary")

    # Process each entry
    created_count = 0
    for strongs_num, entry in dictionary.items():
        try:
            yaml_path = create_strongs_file(strongs_num, entry)
            created_count += 1

            if created_count % 100 == 0:
                print(f"  Created {created_count} files...")
        except Exception as e:
            print(f"  Error processing {strongs_num}: {e}")

    print(f"\n✓ Created {created_count} {dict_name} Strong's files")


def main():
    """Main entry point."""
    print("Strong's Dictionary Fetcher")
    print("="*60)
    print(f"Output directory: {BIBLE_WORDS_DIR}")
    print("Format: Using 4-digit zero-padded Strong's numbers")
    print("  Greek: G0001-G5624")
    print("  Hebrew: H0001-H8674\n")

    # Create base directory
    BIBLE_WORDS_DIR.mkdir(parents=True, exist_ok=True)

    # Process Greek dictionary
    try:
        process_dictionary(GREEK_URL, "Greek")
    except Exception as e:
        print(f"\n✗ Error processing Greek dictionary: {e}")

    # Process Hebrew dictionary
    try:
        process_dictionary(HEBREW_URL, "Hebrew")
    except Exception as e:
        print(f"\n✗ Error processing Hebrew dictionary: {e}")

    print("\n" + "="*60)
    print("✓ Strong's Dictionary Fetcher completed!")
    print("="*60)


if __name__ == "__main__":
    main()
