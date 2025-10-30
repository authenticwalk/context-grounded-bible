#!/usr/bin/env python3
"""morphhb data extractor for Hebrew Bible verses.

This script extracts Hebrew morphological data from the OpenScriptures morphhb
repository and outputs it in our project's YAML format.

Usage:
    python3 morphhb_extractor.py "GEN 1:1"
    python3 morphhb_extractor.py "PSA 23:1" --format yaml
    python3 morphhb_extractor.py "ISA 53:5" --save
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import yaml
import xml.etree.ElementTree as ET

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from book_codes import parse_reference, USFM_TO_NAME
from hebrew_morphology import (
    parse_hebrew_morphology,
    parse_strongs_number,
    format_morphology_display
)


# Map USFM codes to morphhb book names (from morphhbXML-to-JSON.py)
USFM_TO_MORPHHB = {
    'GEN': 'Gen',
    'EXO': 'Exod',
    'LEV': 'Lev',
    'NUM': 'Num',
    'DEU': 'Deut',
    'JOS': 'Josh',
    'JDG': 'Judg',
    'RUT': 'Ruth',
    '1SA': '1Sam',
    '2SA': '2Sam',
    '1KI': '1Kgs',
    '2KI': '2Kgs',
    '1CH': '1Chr',
    '2CH': '2Chr',
    'EZR': 'Ezra',
    'NEH': 'Neh',
    'EST': 'Esth',
    'JOB': 'Job',
    'PSA': 'Ps',
    'PRO': 'Prov',
    'ECC': 'Eccl',
    'SNG': 'Song',
    'ISA': 'Isa',
    'JER': 'Jer',
    'LAM': 'Lam',
    'EZK': 'Ezek',
    'DAN': 'Dan',
    'HOS': 'Hos',
    'JOL': 'Joel',
    'AMO': 'Amos',
    'OBA': 'Obad',
    'JON': 'Jonah',
    'MIC': 'Mic',
    'NAM': 'Nah',
    'HAB': 'Hab',
    'ZEP': 'Zeph',
    'HAG': 'Hag',
    'ZEC': 'Zech',
    'MAL': 'Mal',
}

# Reverse mapping
MORPHHB_TO_USFM = {v: k for k, v in USFM_TO_MORPHHB.items()}


class MorphhbError(Exception):
    """Base exception for morphhb extraction errors."""
    pass


def find_morphhb_path() -> Path:
    """Find the morphhb data directory.

    Checks:
    1. data/morphhb/ (git submodule location)
    2. /tmp/morphhb/ (temporary clone location)

    Returns:
        Path to morphhb directory

    Raises:
        MorphhbError: If morphhb directory not found
    """
    # Check project submodule location
    project_root = Path(__file__).parent.parent.parent.parent
    submodule_path = project_root / 'data' / 'morphhb'

    if submodule_path.exists() and (submodule_path / 'index.js').exists():
        return submodule_path

    # Check /tmp location
    tmp_path = Path('/tmp/morphhb')
    if tmp_path.exists() and (tmp_path / 'index.js').exists():
        return tmp_path

    raise MorphhbError(
        "morphhb data not found. Please run:\n"
        "  git submodule update --init data/morphhb\n"
        "or clone to /tmp:\n"
        "  git clone https://github.com/openscriptures/morphhb.git /tmp/morphhb"
    )


def extract_from_xml(book: str, chapter: int, verse: int) -> List[Dict]:
    """Extract verse data from morphhb XML files.

    Args:
        book: morphhb book name (e.g., "Gen", "Ps")
        chapter: Chapter number (1-indexed)
        verse: Verse number (1-indexed)

    Returns:
        List of word dictionaries

    Raises:
        MorphhbError: If extraction fails
    """
    morphhb_path = find_morphhb_path()
    xml_file = morphhb_path / 'wlc' / f'{book}.xml'

    if not xml_file.exists():
        raise MorphhbError(f"XML file not found: {xml_file}")

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define namespace
        ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}

        # Find the verse
        verse_id = f"{book}.{chapter}.{verse}"
        verse_elem = root.find(f".//osis:verse[@osisID='{verse_id}']", ns)

        if verse_elem is None:
            raise MorphhbError(f"Verse not found: {verse_id}")

        # Extract words
        words = []
        word_elems = verse_elem.findall('.//osis:w', ns)

        for i, word_elem in enumerate(word_elems, 1):
            word_data = {
                'position': i,
                'text': word_elem.text or '',
                'lemma': word_elem.get('lemma', ''),
                'morph': word_elem.get('morph', ''),
                'id': word_elem.get('id', ''),
            }
            words.append(word_data)

        return words

    except ET.ParseError as e:
        raise MorphhbError(f"Failed to parse XML: {e}")


def extract_verse_data(book_code: str, chapter: int, verse: int) -> Dict:
    """Extract complete verse data with morphology.

    Args:
        book_code: USFM book code (e.g., "GEN", "PSA")
        chapter: Chapter number (1-indexed)
        verse: Verse number (1-indexed)

    Returns:
        Dictionary with verse data and morphology

    Raises:
        MorphhbError: If extraction fails
    """
    # Convert USFM to morphhb book name
    if book_code not in USFM_TO_MORPHHB:
        raise MorphhbError(f"Book '{book_code}' not in Hebrew Bible")

    morphhb_book = USFM_TO_MORPHHB[book_code]

    # Extract from XML
    raw_words = extract_from_xml(morphhb_book, chapter, verse)

    # Parse morphology for each word
    words = []
    for raw_word in raw_words:
        word = {
            'position': raw_word['position'],
            'text': raw_word['text'],
            'id': raw_word['id'],
        }

        # Parse Strong's number
        if raw_word['lemma']:
            strongs_data = parse_strongs_number(raw_word['lemma'])
            word['lemma'] = raw_word['lemma']
            word['strongs'] = strongs_data

        # Parse morphology
        if raw_word['morph']:
            morph_data = parse_hebrew_morphology(raw_word['morph'])
            word['morph_code'] = raw_word['morph']
            word['morphology'] = morph_data
            word['morphology_display'] = format_morphology_display(morph_data)

        words.append(word)

    # Combine words into full verse text
    verse_text = ' '.join(w['text'] for w in words)

    result = {
        'reference': f"{book_code} {chapter}:{verse}",
        'book': book_code,
        'chapter': chapter,
        'verse': verse,
        'testament': 'OT',
        'language': 'hebrew',
        'text': verse_text,
        'source': 'morphhb (Westminster Leningrad Codex)',
        'license': 'CC BY 4.0',
        'words': words,
    }

    return result


def format_text_output(data: Dict) -> str:
    """Format verse data as human-readable text.

    Args:
        data: Verse data dictionary

    Returns:
        Formatted string
    """
    lines = []
    lines.append(f"Reference: {data['reference']}")
    lines.append(f"Text: {data['text']}")
    lines.append(f"Source: {data['source']}")
    lines.append("")
    lines.append("Words:")
    lines.append("")

    for word in data['words']:
        lines.append(f"  {word['position']}. {word['text']}")

        if 'strongs' in word:
            strongs = word['strongs']
            if 'components' in strongs:
                # Compound (prefix + word)
                parts = []
                for comp in strongs['components']:
                    if 'prefix' in comp:
                        parts.append(f"{comp['prefix']} ({comp['meaning']})")
                    elif 'strongs' in comp:
                        parts.append(comp['strongs'])
                lines.append(f"     Strong's: {' + '.join(parts)}")
            elif 'strongs' in strongs:
                lines.append(f"     Strong's: {strongs['strongs']}")

        if 'morphology_display' in word:
            lines.append(f"     Morphology: {word['morphology_display']}")

        if 'id' in word:
            lines.append(f"     Word ID: {word['id']}")

        lines.append("")

    return '\n'.join(lines)


def format_yaml_output(data: Dict) -> str:
    """Format verse data as YAML.

    Args:
        data: Verse data dictionary

    Returns:
        YAML string
    """
    return yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)


def save_to_file(data: Dict, output_dir: Optional[Path] = None) -> Path:
    """Save verse data to YAML file following project structure.

    Args:
        data: Verse data dictionary
        output_dir: Optional output directory (default: project bible/ directory)

    Returns:
        Path to saved file
    """
    if output_dir is None:
        # Script is in .claude/skills/lexicon-bible/scripts/
        # Go up 5 levels to get to project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        output_dir = project_root / 'bible'

    # Create directory structure: bible/{book}/{chapter}/{verse}/
    book_dir = output_dir / data['book'] / str(data['chapter']) / str(data['verse'])
    book_dir.mkdir(parents=True, exist_ok=True)

    # Filename: {book}-{chapter}-{verse}-hebrew-morphology.yaml
    filename = f"{data['book']}-{data['chapter']}-{data['verse']}-hebrew-morphology.yaml"
    output_path = book_dir / filename

    # Write YAML
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    return output_path


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Extract Hebrew morphological data from morphhb',
        epilog='Example: python3 morphhb_extractor.py "GEN 1:1"'
    )
    parser.add_argument('reference', help='Bible reference (e.g., "GEN 1:1", "PSA 23:1")')
    parser.add_argument('--format', choices=['text', 'yaml'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--save', action='store_true',
                       help='Save output to bible/ directory')
    parser.add_argument('--output-dir', type=Path,
                       help='Custom output directory (default: project bible/ directory)')

    args = parser.parse_args()

    try:
        # Parse reference (returns tuple: book_code, chapter, verse)
        try:
            book_code, chapter, verse = parse_reference(args.reference)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            print("Format: BOOK CHAPTER:VERSE (e.g., 'GEN 1:1', 'PSA 23:1')", file=sys.stderr)
            return 1

        # Extract data
        data = extract_verse_data(book_code, chapter, verse)

        # Output
        if args.format == 'yaml':
            output = format_yaml_output(data)
        else:
            output = format_text_output(data)

        print(output)

        # Save to file if requested
        if args.save:
            saved_path = save_to_file(data, args.output_dir)
            print(f"\nSaved to: {saved_path}", file=sys.stderr)

        return 0

    except MorphhbError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
