#!/usr/bin/env python3
"""
Get Strong's Dictionary Entries
================================

Fetch Strong's dictionary entries by number or search by English word.

This script:
1. Looks up Strong's numbers directly (e.g., G0025, H0430)
2. Searches for English words across all Strong's entries
3. Merges all YAML files in each Strong's directory
4. Returns structured data with "words" as root node

Usage:
    # Lookup by Strong's numbers
    python get_strongs.py G0025 G5368 H0157

    # Search by English word (finds all Greek and Hebrew variants)
    python get_strongs.py --word love
    python get_strongs.py --word "believe" --word "faith"

    # Combined
    python get_strongs.py G0025 --word love

    # Save to file
    python get_strongs.py --word love --output love-words.yaml
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.yaml_merger import merge_directory_yaml_files

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
STRONGS_DIR = PROJECT_ROOT / "bible" / "words" / "strongs"


def normalize_strongs_number(number: str) -> Optional[str]:
    """
    Normalize a Strong's number to standard format (G0001, H0001).

    Args:
        number: Strong's number in various formats (G25, g25, 25, 0025, etc.)

    Returns:
        Normalized number (e.g., "G0025") or None if invalid
    """
    # Remove whitespace
    number = number.strip()

    # Check if has prefix
    match = re.match(r'^([GHgh])(\d+)$', number)
    if match:
        prefix = match.group(1).upper()
        num = match.group(2).zfill(4)
        return f"{prefix}{num}"

    # Plain number - we don't know if it's Greek or Hebrew without context
    # Return None to indicate we need more information
    if re.match(r'^\d+$', number):
        return None

    return None


def load_strongs_entry(strongs_number: str) -> Optional[Dict[str, Any]]:
    """
    Load a Strong's dictionary entry by number.
    Merges all YAML files in the Strong's directory.

    Args:
        strongs_number: Strong's number (e.g., "G0025", "H0430")

    Returns:
        Merged data dictionary or None if not found
    """
    strongs_dir = STRONGS_DIR / strongs_number

    if not strongs_dir.exists():
        return None

    try:
        # Merge all YAML files in the directory
        merged_data = merge_directory_yaml_files(strongs_dir, pattern="*.yaml")
        return merged_data if merged_data else None

    except Exception as e:
        print(f"Error loading Strong's entry {strongs_number}: {e}", file=sys.stderr)
        return None


def get_all_strongs_numbers() -> List[str]:
    """
    Get list of all available Strong's numbers.

    Returns:
        List of Strong's numbers (e.g., ["G0001", "G0002", ...])
    """
    if not STRONGS_DIR.exists():
        return []

    numbers = []
    for entry in STRONGS_DIR.iterdir():
        if entry.is_dir() and re.match(r'^[GH]\d{4}$', entry.name):
            numbers.append(entry.name)

    return sorted(numbers)


def search_strongs_by_word(search_word: str, case_sensitive: bool = False) -> List[str]:
    """
    Search Strong's dictionary for entries containing an English word.

    Searches in:
    - lemma (transliteration)
    - definition
    - kjv_usage

    Args:
        search_word: English word to search for
        case_sensitive: Whether to match case

    Returns:
        List of matching Strong's numbers
    """
    if not case_sensitive:
        search_word = search_word.lower()

    matching_numbers = []
    all_numbers = get_all_strongs_numbers()

    print(f"Searching {len(all_numbers)} Strong's entries for '{search_word}'...", file=sys.stderr)

    for strongs_num in all_numbers:
        entry = load_strongs_entry(strongs_num)
        if not entry:
            continue

        # Build searchable text
        searchable_parts = [
            entry.get("lemma", ""),
            entry.get("transliteration", ""),
            entry.get("definition", ""),
            entry.get("kjv_usage", ""),
        ]

        searchable_text = " ".join(str(part) for part in searchable_parts)

        if not case_sensitive:
            searchable_text = searchable_text.lower()

        # Check if word appears (as whole word)
        word_pattern = r'\b' + re.escape(search_word) + r'\b'
        if re.search(word_pattern, searchable_text):
            matching_numbers.append(strongs_num)

    print(f"Found {len(matching_numbers)} matches", file=sys.stderr)
    return matching_numbers


def fetch_strongs_entries(
    numbers: List[str] = None,
    words: List[str] = None,
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Fetch Strong's dictionary entries by numbers or words.

    Args:
        numbers: List of Strong's numbers to fetch
        words: List of English words to search for
        case_sensitive: Whether word search is case-sensitive

    Returns:
        Dictionary with structure:
        {
            "words": {
                "G0025": {...},
                "H0157": {...}
            },
            "metadata": {
                "total_entries": 3,
                "greek_entries": 2,
                "hebrew_entries": 1
            }
        }
    """
    all_numbers: Set[str] = set()

    # Add explicitly requested numbers
    if numbers:
        for num in numbers:
            normalized = normalize_strongs_number(num)
            if normalized:
                all_numbers.add(normalized)
            else:
                # Try both Greek and Hebrew for plain numbers
                for prefix in ['G', 'H']:
                    try:
                        padded = num.zfill(4)
                        test_num = f"{prefix}{padded}"
                        if (STRONGS_DIR / test_num).exists():
                            all_numbers.add(test_num)
                    except:
                        pass

    # Add numbers from word searches
    if words:
        for word in words:
            matching = search_strongs_by_word(word, case_sensitive)
            all_numbers.update(matching)

    # Fetch all entries
    entries = {}
    greek_count = 0
    hebrew_count = 0

    for strongs_num in sorted(all_numbers):
        entry = load_strongs_entry(strongs_num)
        if entry:
            entries[strongs_num] = entry

            if strongs_num.startswith('G'):
                greek_count += 1
            elif strongs_num.startswith('H'):
                hebrew_count += 1

    # Build result
    result = {
        "words": entries,
        "metadata": {
            "total_entries": len(entries),
            "greek_entries": greek_count,
            "hebrew_entries": hebrew_count
        }
    }

    # Add search info if applicable
    if words:
        result["metadata"]["search_words"] = words

    if numbers:
        result["metadata"]["requested_numbers"] = sorted(all_numbers)

    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch Strong's dictionary entries by number or search by English word",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Lookup specific Strong's numbers
  python get_strongs.py G0025 G5368

  # Search for all entries containing "love"
  python get_strongs.py --word love

  # Search for multiple words
  python get_strongs.py --word love --word beloved

  # Combined lookup and search
  python get_strongs.py G0025 --word love --output love-study.yaml
        """
    )

    parser.add_argument(
        "numbers",
        nargs="*",
        help="Strong's numbers to lookup (e.g., G0025, H0430)"
    )

    parser.add_argument(
        "--word", "-w",
        action="append",
        dest="words",
        help="English word to search for (can be used multiple times)"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output YAML file path (optional)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of YAML"
    )

    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Make word search case-sensitive"
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.numbers and not args.words:
        parser.error("Must provide at least one Strong's number or --word search term")

    try:
        # Fetch entries
        data = fetch_strongs_entries(
            numbers=args.numbers if args.numbers else None,
            words=args.words,
            case_sensitive=args.case_sensitive
        )

        # Check if any results
        if not data["words"]:
            print("No matching Strong's entries found", file=sys.stderr)
            sys.exit(1)

        # Output
        if args.output:
            if args.json:
                import json
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                with open(args.output, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"Saved {len(data['words'])} entries to: {args.output}", file=sys.stderr)
        else:
            if args.json:
                import json
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
