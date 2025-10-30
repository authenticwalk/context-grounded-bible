#!/usr/bin/env python3
"""Main entry point for fetching lexical data for Bible verses.

This script fetches Strong's numbers, morphological parsing, and lexical
definitions from BibleHub and outputs structured YAML data.

Usage:
    python3 lexicon_fetcher.py "MAT 5:3"
    python3 lexicon_fetcher.py "JHN 3:16"
    python3 lexicon_fetcher.py "GEN 1:1"
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# Add script directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from biblehub_lexicon import fetch_lexicon_data, LexiconFetchError
from biblehub_text import fetch_text_variants, TextFetchError
from book_codes import parse_reference as parse_usfm_reference, USFM_TO_NAME

# Try to import morphhb extractor (may not be available)
try:
    from morphhb_extractor import extract_verse_data, MorphhbError
    MORPHHB_AVAILABLE = True
except ImportError:
    MORPHHB_AVAILABLE = False


def determine_testament(book_code: str) -> str:
    """
    Determine if book is Old Testament (Hebrew) or New Testament (Greek).

    Args:
        book_code: USFM book code

    Returns:
        'OT' or 'NT'
    """
    # New Testament books (Matthew through Revelation)
    nt_books = {
        'MAT', 'MRK', 'LUK', 'JHN', 'ACT',
        'ROM', 'CO1', 'CO2', 'GAL', 'EPH', 'PHP', 'COL',
        'TH1', 'TH2', 'TI1', 'TI2', 'TIT', 'PHM',
        'HEB', 'JAS', 'PE1', 'PE2', 'JN1', 'JN2', 'JN3', 'JUD', 'REV'
    }

    return 'NT' if book_code in nt_books else 'OT'


def merge_morphhb_data(biblehub_words: List[Dict], morphhb_data: Optional[Dict]) -> List[Dict]:
    """
    Merge morphhb data into BibleHub lexical data.

    morphhb provides superior morphological data for Hebrew, so we prefer it
    over BibleHub when both are available.

    Args:
        biblehub_words: Word list from BibleHub
        morphhb_data: Verse data from morphhb (None if not available)

    Returns:
        Merged word list with morphhb enhancements
    """
    if not morphhb_data or 'words' not in morphhb_data:
        return biblehub_words

    morphhb_words = morphhb_data['words']

    # If word counts match, merge by position (ideal case)
    if len(biblehub_words) == len(morphhb_words):
        merged = []
        for bh_word, mhb_word in zip(biblehub_words, morphhb_words):
            word = bh_word.copy()

            # Add morphhb-specific data
            if 'id' in mhb_word:
                word['morphhb_id'] = mhb_word['id']

            # Prefer morphhb morphology (more accurate)
            if 'morphology' in mhb_word:
                word['morphhb_morphology'] = mhb_word['morphology']
                word['morphhb_morph_code'] = mhb_word.get('morph_code', '')
                word['morphhb_display'] = mhb_word.get('morphology_display', '')

            # Prefer morphhb Strong's (includes prefixes)
            if 'strongs' in mhb_word:
                word['morphhb_strongs'] = mhb_word['strongs']
                word['morphhb_lemma'] = mhb_word.get('lemma', '')

            # Add Hebrew text from morphhb
            if 'text' in mhb_word:
                word['morphhb_text'] = mhb_word['text']

            merged.append(word)

        return merged

    # If word counts don't match, use morphhb as primary data source
    # since it has more accurate word segmentation
    # But keep BibleHub glosses as they're in English

    # Create mapping of Strong's numbers from BibleHub for quick lookup
    biblehub_glosses = {}
    for bh_word in biblehub_words:
        if 'strongs' in bh_word:
            # Extract base Strong's number (remove prefixes/suffixes)
            strongs = bh_word['strongs'].replace('H', '').replace('h', '')
            # Remove letter suffixes like 'a', 'b'
            base_strongs = strongs.rstrip('abcdefghijklmnopqrstuvwxyz')
            biblehub_glosses[base_strongs] = {
                'gloss': bh_word.get('gloss', ''),
                'nasb': bh_word.get('nasb', ''),
                'transliteration': bh_word.get('transliteration', ''),
                'origin': bh_word.get('origin', '')
            }

    # Build result from morphhb words, enhanced with BibleHub glosses where available
    merged = []
    for mhb_word in morphhb_words:
        word = {
            'position': mhb_word['position'],
            'original': mhb_word.get('text', ''),
            'morphhb_text': mhb_word.get('text', ''),
        }

        # Add morphhb word ID
        if 'id' in mhb_word:
            word['morphhb_id'] = mhb_word['id']

        # Add morphhb morphology
        if 'morphology' in mhb_word:
            word['morphhb_morphology'] = mhb_word['morphology']
            word['morphhb_morph_code'] = mhb_word.get('morph_code', '')
            word['morphhb_display'] = mhb_word.get('morphology_display', '')

        # Add morphhb Strong's (with prefixes)
        if 'strongs' in mhb_word:
            word['morphhb_strongs'] = mhb_word['strongs']
            word['morphhb_lemma'] = mhb_word.get('lemma', '')

            # Try to find matching BibleHub gloss
            # Extract base Strong's number from morphhb data
            lemma = mhb_word.get('lemma', '')
            if lemma:
                # Handle compound lemmas like "b/7225"
                parts = lemma.split('/')
                for part in parts:
                    part = part.replace(' ', '')
                    base_num = part.rstrip('abcdefghijklmnopqrstuvwxyz')
                    if base_num and base_num in biblehub_glosses:
                        word.update(biblehub_glosses[base_num])
                        break

        merged.append(word)

    return merged


def format_output_yaml(book: str, chapter: int, verse: int, words: List[Dict], variants: Optional[List[Dict]] = None) -> str:
    """
    Format lexical data as YAML.

    Args:
        book: USFM book code
        chapter: Chapter number
        verse: Verse number
        words: List of word data dictionaries
        variants: Optional list of textual variants

    Returns:
        YAML formatted string
    """
    testament = determine_testament(book)
    language = 'greek' if testament == 'NT' else 'hebrew'

    data = {
        'reference': f'{book} {chapter}:{verse}',
        'testament': testament,
        'language': language,
        'words': words
    }

    if variants:
        data['manuscripts'] = variants

    return yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)


def format_output_text(book: str, chapter: int, verse: int, words: List[Dict], variants: Optional[List[Dict]] = None) -> str:
    """
    Format lexical data as human-readable text.

    Args:
        book: USFM book code
        chapter: Chapter number
        verse: Verse number
        words: List of word data dictionaries
        variants: Optional list of textual variants

    Returns:
        Formatted text string
    """
    testament = determine_testament(book)
    language = 'Greek' if testament == 'NT' else 'Hebrew'

    lines = []
    lines.append(f"Lexical Data for {book} {chapter}:{verse}")
    lines.append(f"Testament: {testament} ({language})")
    lines.append("=" * 80)
    lines.append("")

    for word in words:
        lines.append(f"Word {word['position']}:")

        if 'original' in word:
            lines.append(f"  Original: {word['original']}")

        if 'transliteration' in word:
            lines.append(f"  Transliteration: {word['transliteration']}")

        if 'strongs' in word:
            lines.append(f"  Strong's: {word['strongs']}")

        if 'morphology' in word:
            lines.append(f"  Morphology: {word['morphology']}")

        if 'parsing' in word and word['parsing']:
            parsed_parts = []
            parsing = word['parsing']
            if 'pos' in parsing:
                parsed_parts.append(f"POS: {parsing['pos']}")
            if 'case' in parsing:
                parsed_parts.append(f"case: {parsing['case']}")
            if 'gender' in parsing:
                parsed_parts.append(f"gender: {parsing['gender']}")
            if 'number' in parsing:
                parsed_parts.append(f"number: {parsing['number']}")
            if 'tense' in parsing:
                parsed_parts.append(f"tense: {parsing['tense']}")
            if 'voice' in parsing:
                parsed_parts.append(f"voice: {parsing['voice']}")
            if 'mood' in parsing:
                parsed_parts.append(f"mood: {parsing['mood']}")
            if 'person' in parsing:
                parsed_parts.append(f"person: {parsing['person']}")
            if parsed_parts:
                lines.append(f"  Parsing: {', '.join(parsed_parts)}")

        if 'gloss' in word:
            lines.append(f"  Gloss: {word['gloss']}")

        if 'root' in word:
            lines.append(f"  Root: {word['root']}")

        # Display morphhb data if available (for OT verses)
        if 'morphhb_display' in word:
            lines.append(f"  morphhb Morphology: {word['morphhb_display']}")

        if 'morphhb_strongs' in word:
            strongs = word['morphhb_strongs']
            if 'components' in strongs:
                # Compound (prefix + word)
                parts = []
                for comp in strongs['components']:
                    if 'prefix' in comp:
                        parts.append(f"{comp['prefix']} ({comp['meaning']})")
                    elif 'strongs' in comp:
                        parts.append(comp['strongs'])
                lines.append(f"  morphhb Strong's: {' + '.join(parts)}")
            elif 'strongs' in strongs:
                lines.append(f"  morphhb Strong's: {strongs['strongs']}")

        if 'morphhb_id' in word:
            lines.append(f"  morphhb Word ID: {word['morphhb_id']}")

        lines.append("")

    # Add manuscript variants if available
    if variants and len(variants) > 0:
        lines.append("=" * 80)
        lines.append(f"Manuscript Traditions ({len(variants)} found)")
        lines.append("=" * 80)
        lines.append("")

        for variant in variants:
            lines.append(f"{variant['name']}:")
            text = variant['text']
            # Wrap long text
            if len(text) > 76:
                lines.append(f"  {text[:76]}")
                lines.append(f"  {text[76:]}")
            else:
                lines.append(f"  {text}")
            lines.append("")

    return '\n'.join(lines)


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Fetch lexical data for Bible verses',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "MAT 5:3"
  %(prog)s "John 3:16"
  %(prog)s "GEN 1:1" --format yaml
  %(prog)s "ROM 8:28" --format text
        """
    )

    parser.add_argument(
        'reference',
        help='Bible reference (e.g., "MAT 5:3", "John 3:16")'
    )

    parser.add_argument(
        '--format',
        choices=['yaml', 'text'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Bypass cache and fetch fresh data'
    )

    parser.add_argument(
        '--with-variants',
        action='store_true',
        help='Include textual variants from multiple manuscript traditions'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress informational messages'
    )

    args = parser.parse_args()

    try:
        # Parse reference using book_codes.parse_reference
        # It accepts formats like "MAT 5:3" or "MAT.5.3"
        book, chapter, verse = parse_usfm_reference(args.reference)

        # Fetch lexicon data from BibleHub
        use_cache = not args.no_cache
        words = fetch_lexicon_data(book, chapter, verse, use_cache=use_cache)

        # For OT verses, try to enhance with morphhb data
        testament = determine_testament(book)
        if MORPHHB_AVAILABLE and testament == 'OT':
            try:
                morphhb_data = extract_verse_data(book, chapter, verse)
                words = merge_morphhb_data(words, morphhb_data)
                if not args.quiet:
                    print(f"Note: Enhanced with morphhb morphological data", file=sys.stderr)
            except MorphhbError as e:
                if not args.quiet:
                    print(f"Note: morphhb data not available ({e})", file=sys.stderr)
            except Exception as e:
                if not args.quiet:
                    print(f"Warning: Could not fetch morphhb data: {e}", file=sys.stderr)

        # Optionally fetch textual variants
        variants = None
        if args.with_variants:
            try:
                variants = fetch_text_variants(book, chapter, verse)
            except TextFetchError as e:
                print(f"Warning: Could not fetch variants: {e}", file=sys.stderr)

        # Format output
        if args.format == 'yaml':
            output = format_output_yaml(book, chapter, verse, words, variants)
        else:
            output = format_output_text(book, chapter, verse, words, variants)

        print(output)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except LexiconFetchError as e:
        print(f"Error fetching lexicon data: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
