#!/usr/bin/env python3
"""
Source Languages Fetcher
========================

Fetches source language (Hebrew/Greek) word data for a given Bible verse.

This script:
1. Reads Macula commentary data for a verse (or generates it if missing)
2. Extracts all Strong's numbers from the source words
3. Looks up each Strong's number in the Strong's dictionary
4. Merges all Strong's data into a comprehensive reference

Usage:
    python source_languages_fetcher.py "JHN 3:16"
    python source_languages_fetcher.py "GEN 1:1" --output gen-1-1-source.yaml
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.yaml_merger import merge_directory_yaml_files, merge_yaml_data, save_merged_yaml
from constants.bible import BIBLE_STRUCTURE

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
MACULA_CACHE = PROJECT_ROOT / "bible" / "commentaries"
STRONGS_DIR = PROJECT_ROOT / "bible" / "words" / "strongs"


def parse_verse_ref(ref_str: str) -> Optional[tuple]:
    """
    Parse verse reference string like 'GEN 1:1' or 'JHN 3:16'.
    Returns (book, chapter, verse) tuple or None if invalid.
    """
    match = re.match(r'([A-Z0-9]+)\s+(\d+):(\d+)', ref_str.strip())
    if match:
        return match.group(1), int(match.group(2)), int(match.group(3))
    return None


def get_macula_file_path(book: str, chapter: int, verse: int) -> Path:
    """Get the path to the Macula commentary file for a verse."""
    return MACULA_CACHE / book / f"{chapter:03d}" / f"{verse:03d}" / f"{book}-{chapter:03d}-{verse:03d}-macula.yaml"


def load_macula_data(book: str, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
    """
    Load Macula commentary data for a verse.
    Returns None if file doesn't exist.
    """
    macula_file = get_macula_file_path(book, chapter, verse)

    if not macula_file.exists():
        return None

    try:
        with open(macula_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading Macula data: {e}", file=sys.stderr)
        return None


def generate_macula_data(verse_ref: str) -> Optional[Dict[str, Any]]:
    """
    Generate Macula data for a verse by calling macula_processor.
    Returns the loaded data or None if generation failed.
    """
    from lib.macula.macula_processor import main as process_macula
    import subprocess

    book, chapter, verse = parse_verse_ref(verse_ref)
    if not book:
        return None

    print(f"Generating Macula data for {verse_ref}...", file=sys.stderr)

    # Call macula_processor script
    processor_path = PROJECT_ROOT / "src" / "lib" / "macula" / "macula_processor.py"
    try:
        result = subprocess.run(
            [sys.executable, str(processor_path), "--verse", verse_ref],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )

        if result.returncode != 0:
            print(f"Failed to generate Macula data: {result.stderr}", file=sys.stderr)
            return None

        # Load the generated data
        return load_macula_data(book, chapter, verse)

    except Exception as e:
        print(f"Error generating Macula data: {e}", file=sys.stderr)
        return None


def extract_strongs_numbers(macula_data: Dict[str, Any]) -> List[str]:
    """
    Extract all Strong's numbers from Macula word data.
    Returns a list of unique Strong's numbers (e.g., ['G0001', 'G0002']).
    """
    strongs_numbers = []

    if "words" not in macula_data:
        return strongs_numbers

    # Determine language prefix (G for Greek, H for Hebrew)
    language = macula_data.get("language", "")
    prefix = "G" if language == "grc" else "H" if language == "heb" else ""

    for word in macula_data["words"]:
        # Hebrew words have 'lexical.strong' or 'lexical.stronglemma'
        # Greek words have 'lexical.strong'
        if "lexical" in word:
            lexical = word["lexical"]

            # Get Strong's number(s)
            strong = lexical.get("strong", "")
            stronglemma = lexical.get("stronglemma", "")

            # Handle multiple Strong's numbers (space-separated)
            for field in [strong, stronglemma]:
                if field:
                    # Convert to string if needed
                    field_str = str(field)

                    # Split on whitespace and extract numbers
                    for num in field_str.split():
                        # Check if already has prefix (e.g., "H0430a" or "G1063")
                        with_prefix = re.match(r'([HG]\d+)', num)
                        if with_prefix:
                            strongs_numbers.append(with_prefix.group(1))
                        else:
                            # Plain number (e.g., "1063") - add prefix and pad to 4 digits
                            plain_num = re.match(r'(\d+)', num)
                            if plain_num and prefix:
                                padded = plain_num.group(1).zfill(4)
                                strongs_numbers.append(f"{prefix}{padded}")

    # Return unique numbers, preserving order
    seen = set()
    unique_numbers = []
    for num in strongs_numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)

    return unique_numbers


def load_strongs_entry(strongs_number: str) -> Optional[Dict[str, Any]]:
    """
    Load a Strong's dictionary entry by number.
    Merges all files in the Strong's directory.
    Returns merged data or None if not found.
    """
    strongs_dir = STRONGS_DIR / strongs_number

    if not strongs_dir.exists():
        print(f"Warning: Strong's entry not found: {strongs_number}", file=sys.stderr)
        return None

    try:
        # Merge all YAML files in the directory
        merged_data = merge_directory_yaml_files(strongs_dir, pattern="*.yaml")
        return merged_data if merged_data else None

    except Exception as e:
        print(f"Error loading Strong's entry {strongs_number}: {e}", file=sys.stderr)
        return None


def fetch_source_languages(verse_ref: str, generate_if_missing: bool = True) -> Dict[str, Any]:
    """
    Fetch source language data for a verse.

    Args:
        verse_ref: Verse reference (e.g., "JHN 3:16")
        generate_if_missing: If True, generate Macula data if not cached

    Returns:
        Dictionary containing:
        - verse: Verse reference
        - macula: Full Macula data with source words
        - strongs: Merged Strong's dictionary entries for all words
        - words: List of words with their Strong's data embedded
    """
    parsed = parse_verse_ref(verse_ref)
    if not parsed:
        raise ValueError(f"Invalid verse reference: {verse_ref}")

    book, chapter, verse = parsed

    # Load or generate Macula data
    macula_data = load_macula_data(book, chapter, verse)

    if not macula_data and generate_if_missing:
        macula_data = generate_macula_data(verse_ref)

    if not macula_data:
        raise FileNotFoundError(
            f"Macula data not found for {verse_ref}. "
            "Run macula_processor.py first or ensure Macula datasets are downloaded."
        )

    # Extract Strong's numbers
    strongs_numbers = extract_strongs_numbers(macula_data)

    if not strongs_numbers:
        print(f"Warning: No Strong's numbers found in {verse_ref}", file=sys.stderr)

    # Load all Strong's entries
    strongs_entries = {}
    for strongs_num in strongs_numbers:
        entry = load_strongs_entry(strongs_num)
        if entry:
            strongs_entries[strongs_num] = entry

    # Build enhanced word list with Strong's data
    enhanced_words = []
    language = macula_data.get("language", "")
    prefix = "G" if language == "grc" else "H" if language == "heb" else ""

    if "words" in macula_data:
        for word in macula_data["words"]:
            enhanced_word = word.copy()

            # Add Strong's entry data
            if "lexical" in word:
                lexical = word["lexical"]
                strong_nums = []

                # Extract Strong's number(s)
                for field in [lexical.get("strong", ""), lexical.get("stronglemma", "")]:
                    if field:
                        field_str = str(field)
                        for num in field_str.split():
                            # Check if already has prefix
                            with_prefix = re.match(r'([HG]\d+)', num)
                            if with_prefix:
                                strong_nums.append(with_prefix.group(1))
                            else:
                                # Plain number - add prefix and pad
                                plain_num = re.match(r'(\d+)', num)
                                if plain_num and prefix:
                                    padded = plain_num.group(1).zfill(4)
                                    strong_nums.append(f"{prefix}{padded}")

                # Attach Strong's entries
                if strong_nums:
                    enhanced_word["strongs_data"] = {}
                    for num in strong_nums:
                        if num in strongs_entries:
                            enhanced_word["strongs_data"][num] = strongs_entries[num]

            enhanced_words.append(enhanced_word)

    # Build result
    result = {
        "verse": verse_ref,
        "language": macula_data.get("language", ""),
        "source": macula_data.get("source", ""),
        "text": macula_data.get("text", ""),
        "words": enhanced_words,
        "strongs_entries": strongs_entries,
        "metadata": {
            "verse_reference": verse_ref,
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "word_count": len(enhanced_words),
            "unique_strongs": len(strongs_entries)
        }
    }

    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch source language (Greek/Hebrew) data for Bible verses"
    )
    parser.add_argument("verse", help="Verse reference (e.g., 'JHN 3:16', 'GEN 1:1')")
    parser.add_argument("--output", "-o", help="Output YAML file path (optional)")
    parser.add_argument("--no-generate", action="store_true",
                       help="Don't generate Macula data if missing")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of YAML")

    args = parser.parse_args()

    try:
        # Fetch source language data
        data = fetch_source_languages(
            args.verse,
            generate_if_missing=not args.no_generate
        )

        # Output
        if args.output:
            if args.json:
                import json
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                save_merged_yaml(data, args.output)
            print(f"Saved to: {args.output}", file=sys.stderr)
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
