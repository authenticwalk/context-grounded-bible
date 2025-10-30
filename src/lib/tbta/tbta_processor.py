#!/usr/bin/env python3
"""
TBTA (The Bible Translator's Assistant) Processor
==================================================

Processes TBTA JSON export files and generates YAML commentary files
following the Context-Grounded Bible project structure.

Output structure: ./bible/commentaries/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-tbta.yaml

Usage:
    python tbta_processor.py --all                    # Process all verses
    python tbta_processor.py --book GEN               # Process Genesis
    python tbta_processor.py --verse "GEN 1:1"        # Process single verse
    python tbta_processor.py --chapter "GEN 1"        # Process Genesis chapter 1
    python tbta_processor.py --dry-run --book GEN     # Test without writing files
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import yaml
import argparse
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
TBTA_JSON_DIR = Path("/tmp/tbta_db_export/json")
OUTPUT_DIR = Path("./bible/commentaries")

# Book name to USFM code mapping
BOOK_NAME_MAP = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM", "Deuteronomy": "DEU",
    "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT",
    "1Samuel": "1SA", "1_Samuel": "1SA",  # TBTA uses underscores
    "2Samuel": "2SA", "2_Samuel": "2SA",  # TBTA uses underscores
    "1Kings": "1KI", "1_Kings": "1KI",    # TBTA uses underscores
    "2Kings": "2KI", "2_Kings": "2KI",    # TBTA uses underscores
    "1Chronicles": "1CH", "2Chronicles": "2CH",
    "Ezra": "EZR", "Nehemiah": "NEH", "Esther": "EST", "Job": "JOB", "Psalms": "PSA",
    "Proverbs": "PRO", "Ecclesiastes": "ECC", "SongofSongs": "SNG", "Isaiah": "ISA",
    "Jeremiah": "JER", "Lamentations": "LAM", "Ezekiel": "EZK", "Daniel": "DAN",
    "Hosea": "HOS", "Joel": "JOL", "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON",
    "Micah": "MIC", "Nahum": "NAM", "Habakkuk": "HAB", "Zephaniah": "ZEP",
    "Haggai": "HAG", "Zechariah": "ZEC", "Malachi": "MAL",
    "Matthew": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN", "Acts": "ACT",
    "Romans": "ROM", "1Corinthians": "1CO", "2Corinthians": "2CO", "Galatians": "GAL",
    "Ephesians": "EPH", "Philippians": "PHP", "Colossians": "COL",
    "1Thessalonians": "1TH", "1_Thessalonians": "1TH",  # TBTA uses underscores
    "2Thessalonians": "2TH", "2_Thessalonians": "2TH",  # TBTA uses underscores
    "1Timothy": "1TI", "2Timothy": "2TI", "Titus": "TIT", "Philemon": "PHM", "Hebrews": "HEB",
    "James": "JAS", "1Peter": "1PE", "2Peter": "2PE",
    "1John": "1JN", "2John": "2JN", "2_John": "2JN",  # TBTA uses underscores
    "3John": "3JN", "Jude": "JUD",
    "Revelation": "REV", "Revelations": "REV"  # TBTA has typo - "Revelations"
}

# USFM code to book name (for reverse lookup)
USFM_TO_BOOK_NAME = {v: k for k, v in BOOK_NAME_MAP.items()}


def log(message):
    """Print timestamped log message."""
    logger.info(message)


def parse_filename(filename):
    """
    Parse TBTA filename like '00_001_001_Genesis.json'
    Returns (book_name, chapter, verse) tuple
    """
    match = re.match(r'(\d+)_(\d+)_(\d+)_([^.]+)\.json', filename)
    if match:
        book_index = int(match.group(1))
        chapter = int(match.group(2))
        verse = int(match.group(3))
        book_name = match.group(4)
        return book_name, chapter, verse
    return None, None, None


def parse_verse_ref(ref_str):
    """
    Parse verse reference string like 'GEN 1:1'.
    Returns (book_code, chapter, verse) tuple.
    """
    match = re.match(r'([A-Z0-9]+)\s+(\d+):(\d+)', ref_str)
    if match:
        return match.group(1), int(match.group(2)), int(match.group(3))
    return None, None, None


# Nullish values to filter out
NULLISH_VALUES = {
    "Not Applicable",
    "Unspecified",
    # NOTE: "No" is meaningful (e.g., "Implicit: No" vs field absent)
    # NOTE: "Space" and "Period" mark structural elements not in original Greek - keep them
    ".",   # Empty placeholder in TBTA codes (just a dot by itself)
}

# Parts that are structural markers - KEEP THESE (not noise, meaningful)
# Space/Period show where these appear in rendering (not in original Greek)
SKIP_PARTS = set()  # Don't skip anything now


def is_nullish(value):
    """Check if a value is nullish and should be filtered."""
    # Only check string values against NULLISH_VALUES set
    if isinstance(value, str):
        if value in NULLISH_VALUES:
            return True
        if value.strip() == "":
            return True
    return False


def extract_clause_data(clause_elem):
    """Recursively extract data from a clause element, filtering nullish values."""
    if not isinstance(clause_elem, dict):
        return clause_elem

    # Extract all fields, recursively processing children and filtering nullish
    result = {}
    for key, value in clause_elem.items():
        # Skip if value is nullish
        if is_nullish(value):
            continue

        if key == "Children" and isinstance(value, list):
            # Recursively process children and filter out None values
            children = [extract_clause_data(child) for child in value]
            children = [c for c in children if c is not None]
            if children:  # Only add if there are non-null children
                result["children"] = children
        elif isinstance(value, dict):
            extracted = extract_clause_data(value)
            if extracted:  # Only add if not empty
                result[key] = extracted
        elif isinstance(value, list):
            items = [extract_clause_data(item) if isinstance(item, dict) else item for item in value]
            items = [i for i in items if i is not None and not is_nullish(i)]
            if items:  # Only add if not empty
                result[key] = items
        else:
            result[key] = value

    return result if result else None


def process_tbta_verse(json_file):
    """Process a single TBTA JSON file and return structured data."""
    book_name, chapter, verse = parse_filename(json_file.name)

    if not book_name:
        return None

    # Get USFM book code
    book_code = BOOK_NAME_MAP.get(book_name)
    if not book_code:
        log(f"WARNING: Unknown book name '{book_name}'")
        return None

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            tbta_data = json.load(f)
    except Exception as e:
        log(f"ERROR reading {json_file}: {e}")
        return None

    verse_data = {
        "verse": f"{book_code}.{chapter:03d}.{verse:03d}",
        "source": "tbta",
        "version": "1.0.0",
        "clauses": []
    }

    # Process each clause variant in the data
    if isinstance(tbta_data, list):
        for clause in tbta_data:
            clause_data = extract_clause_data(clause)
            if clause_data:  # Only add if not None/empty
                verse_data["clauses"].append(clause_data)
    elif isinstance(tbta_data, dict):
        clause_data = extract_clause_data(tbta_data)
        if clause_data:
            verse_data["clauses"].append(clause_data)

    return verse_data, book_code, chapter, verse


def save_verse_yaml(verse_data, book_code, chapter, verse, output_dir):
    """Save verse data as YAML file."""
    # Create directory structure
    verse_dir = output_dir / book_code / f"{chapter:03d}" / f"{verse:03d}"
    verse_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = f"{book_code}-{chapter:03d}-{verse:03d}-tbta.yaml"
    filepath = verse_dir / filename

    # Save YAML
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(verse_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return filepath


def process_verse_file(json_file, output_dir, dry_run=False):
    """Process a single TBTA JSON file."""
    result = process_tbta_verse(json_file)

    if not result:
        return 0

    verse_data, book_code, chapter, verse = result

    if not dry_run:
        save_verse_yaml(verse_data, book_code, chapter, verse, output_dir)

    return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process TBTA JSON files into YAML commentary files"
    )
    parser.add_argument("--all", action="store_true", help="Process all verses")
    parser.add_argument("--book", help="Process single book (e.g., GEN, MAT)")
    parser.add_argument("--chapter", help="Process single chapter (e.g., 'GEN 1')")
    parser.add_argument("--verse", help="Process single verse (e.g., 'GEN 1:1')")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Test without writing files")

    args = parser.parse_args()

    if not TBTA_JSON_DIR.exists():
        log(f"ERROR: TBTA JSON directory not found: {TBTA_JSON_DIR}")
        log("Please ensure tbta_db_export is cloned to /tmp/tbta_db_export")
        sys.exit(1)

    output_dir = Path(args.output)

    log("=" * 60)
    log("TBTA Processor Starting")
    if args.dry_run:
        log("DRY RUN MODE - No files will be written")
    log("=" * 60)

    total_verses = 0
    json_files = []

    # Determine which files to process
    if args.verse:
        # Single verse
        book_code, chapter, verse = parse_verse_ref(args.verse)
        if not book_code:
            log(f"ERROR: Invalid verse reference '{args.verse}'. Use format: 'GEN 1:1'")
            sys.exit(1)

        book_name = USFM_TO_BOOK_NAME.get(book_code)
        if not book_name:
            log(f"ERROR: Unknown book code '{book_code}'")
            sys.exit(1)

        # Find the matching file
        # Format: 00_001_001_Genesis.json (need to determine book index)
        for json_file in TBTA_JSON_DIR.glob(f"*_{chapter:03d}_{verse:03d}_{book_name}.json"):
            json_files.append(json_file)
            break

        if not json_files:
            log(f"WARNING: File not found for {args.verse}")

    elif args.chapter:
        # Single chapter
        match = re.match(r'([A-Z0-9]+)\s+(\d+)', args.chapter)
        if not match:
            log(f"ERROR: Invalid chapter reference '{args.chapter}'. Use format: 'GEN 1'")
            sys.exit(1)

        book_code = match.group(1)
        chapter = int(match.group(2))

        book_name = USFM_TO_BOOK_NAME.get(book_code)
        if not book_name:
            log(f"ERROR: Unknown book code '{book_code}'")
            sys.exit(1)

        # Find all verses in this chapter
        json_files = sorted(TBTA_JSON_DIR.glob(f"*_{chapter:03d}_*_{book_name}.json"))

    elif args.book:
        # Entire book
        book_code = args.book.upper()
        book_name = USFM_TO_BOOK_NAME.get(book_code)
        if not book_name:
            log(f"ERROR: Unknown book code '{book_code}'")
            sys.exit(1)

        json_files = sorted(TBTA_JSON_DIR.glob(f"*_{book_name}.json"))

    elif args.all:
        # All files
        json_files = sorted(TBTA_JSON_DIR.glob("*.json"))

    else:
        log("ERROR: Must specify --all, --book, --chapter, or --verse")
        parser.print_help()
        sys.exit(1)

    # Process files
    log(f"Found {len(json_files)} file(s) to process")

    for json_file in json_files:
        try:
            total_verses += process_verse_file(json_file, output_dir, args.dry_run)

            if total_verses % 100 == 0 and total_verses > 0:
                log(f"  Processed {total_verses} verses...")
        except Exception as e:
            log(f"ERROR processing {json_file.name}: {e}")

    log("=" * 60)
    log(f"✓ Processed {total_verses} verses total")
    if not args.dry_run:
        log(f"Output directory: {output_dir}")
    log("=" * 60)


if __name__ == "__main__":
    main()
