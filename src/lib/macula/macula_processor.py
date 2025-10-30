#!/usr/bin/env python3
"""
Macula Source Language Processor
=================================

Processes Macula Hebrew and Greek XML files and generates YAML commentary files
following the Context-Grounded Bible project structure.

Output structure: ./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-source-language.yaml

Usage:
    python macula_processor.py --all                    # Process all verses
    python macula_processor.py --book JHN               # Process John
    python macula_processor.py --verse "JHN 1:1"        # Process single verse
    python macula_processor.py --testament NT           # Process NT only
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import yaml
import argparse
import re
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
CACHE_DIR = Path("/tmp/macula")
HEBREW_LOWFAT = CACHE_DIR / "hebrew" / "WLC" / "lowfat"
GREEK_LOWFAT = CACHE_DIR / "greek" / "Nestle1904" / "lowfat"
OUTPUT_DIR = Path("./bible/commentaries")

# Book mappings (USFM 3.0 codes)
HEBREW_BOOK_MAP = {
    "01-Gen": "GEN", "02-Exo": "EXO", "03-Lev": "LEV", "04-Num": "NUM", "05-Deu": "DEU",
    "06-Jos": "JOS", "07-Jdg": "JDG", "08-Rut": "RUT", "09-1Sa": "1SA", "10-2Sa": "2SA",
    "11-1Ki": "1KI", "12-2Ki": "2KI", "13-1Ch": "1CH", "14-2Ch": "2CH", "15-Ezr": "EZR",
    "16-Neh": "NEH", "17-Est": "EST", "18-Job": "JOB", "19-Psa": "PSA", "20-Pro": "PRO",
    "21-Ecc": "ECC", "22-Sng": "SNG", "23-Isa": "ISA", "24-Jer": "JER", "25-Lam": "LAM",
    "26-Ezk": "EZK", "27-Dan": "DAN", "28-Hos": "HOS", "29-Jol": "JOL", "30-Amo": "AMO",
    "31-Oba": "OBA", "32-Jon": "JON", "33-Mic": "MIC", "34-Nam": "NAM", "35-Hab": "HAB",
    "36-Zep": "ZEP", "37-Hag": "HAG", "38-Zec": "ZEC", "39-Mal": "MAL"
}

GREEK_BOOK_MAP = {
    "01-matthew": "MAT", "02-mark": "MRK", "03-luke": "LUK", "04-john": "JHN",
    "05-acts": "ACT", "06-romans": "ROM", "07-1corinthians": "1CO", "08-2corinthians": "2CO",
    "09-galatians": "GAL", "10-ephesians": "EPH", "11-philippians": "PHP", "12-colossians": "COL",
    "13-1thessalonians": "1TH", "14-2thessalonians": "2TH", "15-1timothy": "1TI",
    "16-2timothy": "2TI", "17-titus": "TIT", "18-philemon": "PHM", "19-hebrews": "HEB",
    "20-james": "JAS", "21-1peter": "1PE", "22-2peter": "2PE", "23-1john": "1JN",
    "24-2john": "2JN", "25-3john": "3JN", "26-jude": "JUD", "27-revelation": "REV"
}


def log(message):
    """Print timestamped log message."""
    logger.info(message)


def parse_verse_ref(ref_str):
    """
    Parse verse reference string like 'GEN 1:1' or 'JHN 1:1'.
    Returns (book, chapter, verse) tuple.
    """
    match = re.match(r'([A-Z0-9]+)\s+(\d+):(\d+)', ref_str)
    if match:
        return match.group(1), int(match.group(2)), int(match.group(3))
    return None, None, None


def extract_hebrew_word(word_elem, position):
    """Extract data from Hebrew word element."""
    word_data = {
        "position": position,
        "text": word_elem.text or "",
        "lemma": word_elem.get("lemma", ""),
        "transliteration": word_elem.get("transliteration", ""),
    }

    # IDs - for cross-referencing with other datasets
    ids = {}
    if word_elem.get("ref"):
        ids["ref"] = word_elem.get("ref")

    xml_id = word_elem.get("{http://www.w3.org/XML/1998/namespace}id")
    if xml_id:
        ids["wordID"] = xml_id

    if ids:
        word_data["ids"] = ids

    # Translation
    translation = {}
    if word_elem.get("english"):
        translation["english"] = word_elem.get("english")
    if word_elem.get("mandarin"):
        translation["mandarin"] = word_elem.get("mandarin")
    if word_elem.get("gloss"):
        translation["gloss"] = word_elem.get("gloss")
    if translation:
        word_data["translation"] = translation

    # Morphology
    morphology = {
        "class": word_elem.get("class", ""),
        "pos": word_elem.get("pos", ""),
        "morph": word_elem.get("morph", ""),
    }
    for field in ["gender", "number", "person", "state", "stem", "type"]:
        if word_elem.get(field):
            morphology[field] = word_elem.get(field)
    word_data["morphology"] = morphology

    # Lexical references
    lexical = {}
    if word_elem.get("stronglemma"):
        lexical["stronglemma"] = word_elem.get("stronglemma")
    if word_elem.get("strongnumberx"):
        lexical["strong"] = word_elem.get("strongnumberx")
    if lexical:
        word_data["lexical"] = lexical

    # Semantic domains
    semantic = {}
    sdbh = word_elem.get("sdbh", "")
    if sdbh:
        semantic["sdbh"] = sdbh.split() if " " in sdbh else [sdbh]

    lexdomain = word_elem.get("lexdomain", "")
    if lexdomain:
        semantic["lexdomain"] = lexdomain.split() if " " in lexdomain else [lexdomain]

    coredomain = word_elem.get("coredomain", "")
    if coredomain:
        semantic["coredomain"] = coredomain.split() if " " in coredomain else [coredomain]

    if word_elem.get("sensenumber"):
        semantic["sense"] = word_elem.get("sensenumber")

    if semantic:
        word_data["semantic"] = semantic

    # Greek cross-reference (LXX)
    if word_elem.get("greek") or word_elem.get("greekstrong"):
        lxx = {}
        if word_elem.get("greek"):
            lxx["text"] = word_elem.get("greek")
        if word_elem.get("greekstrong"):
            lxx["strong"] = word_elem.get("greekstrong")
        word_data["lxx"] = lxx

    # Syntax
    syntax = {}
    if word_elem.get("role"):
        syntax["role"] = word_elem.get("role")
    if word_elem.get("frame"):
        syntax["frame"] = word_elem.get("frame")
    if syntax:
        word_data["syntax"] = syntax

    # Discourse (participant/subject tracking)
    discourse = {}
    if word_elem.get("participantref"):
        discourse["participant"] = word_elem.get("participantref")
    if word_elem.get("subjref"):
        discourse["subject"] = word_elem.get("subjref")
    if discourse:
        word_data["discourse"] = discourse

    return word_data


def extract_greek_word(word_elem, position):
    """Extract data from Greek word element."""
    word_data = {
        "position": position,
        "text": word_elem.text or "",
        "lemma": word_elem.get("lemma", ""),
        "normalized": word_elem.get("normalized", ""),
    }

    # IDs - for cross-referencing with other datasets
    ids = {}
    if word_elem.get("ref"):
        ids["ref"] = word_elem.get("ref")

    xml_id = word_elem.get("{http://www.w3.org/XML/1998/namespace}id")
    if xml_id:
        ids["wordID"] = xml_id

    if ids:
        word_data["ids"] = ids

    # Translation
    translation = {}
    if word_elem.get("gloss"):
        translation["gloss"] = word_elem.get("gloss")
    if translation:
        word_data["translation"] = translation

    # Morphology
    morphology = {
        "class": word_elem.get("class", ""),
        "morph": word_elem.get("morph", ""),
    }
    for field in ["gender", "number", "person", "case", "tense", "voice", "mood", "type", "degree"]:
        if word_elem.get(field):
            morphology[field] = word_elem.get(field)

    # Article detection
    if word_elem.get("class") == "det":
        morphology["has_article"] = True

    word_data["morphology"] = morphology

    # Lexical references
    lexical = {}
    if word_elem.get("strong"):
        lexical["strong"] = word_elem.get("strong")
    if lexical:
        word_data["lexical"] = lexical

    # Semantic domains
    semantic = {}
    if word_elem.get("domain"):
        semantic["semanticDomain"] = word_elem.get("domain")
    if word_elem.get("ln"):
        semantic["ln"] = word_elem.get("ln")
    if semantic:
        word_data["semantic"] = semantic

    # Syntax
    syntax = {}
    if word_elem.get("role"):
        syntax["role"] = word_elem.get("role")
    if word_elem.get("frame"):
        syntax["frame"] = word_elem.get("frame")
    if word_elem.get("discontinuous"):
        syntax["discontinuous"] = word_elem.get("discontinuous")
    if word_elem.get("junction"):
        syntax["junction"] = word_elem.get("junction")
    if syntax:
        word_data["syntax"] = syntax

    # Discourse (referent/subject tracking)
    discourse = {}
    if word_elem.get("referent"):
        discourse["referent"] = word_elem.get("referent")
    if word_elem.get("subjref"):
        discourse["subject"] = word_elem.get("subjref")
    if discourse:
        word_data["discourse"] = discourse

    return word_data


def process_hebrew_verse(chapter_elem, verse_ref):
    """Process a single Hebrew verse and return structured data."""
    book, chapter, verse = parse_verse_ref(verse_ref)

    verse_data = {
        "source": "macula-hebrew",
        "version": "1.0.0",
        "language": "heb",
        "verse": f"{book} {chapter}:{verse}",
        "text": "",
        "words": []
    }

    # Find the sentence for this verse
    for sentence in chapter_elem.findall(".//sentence[@id]"):
        if sentence.get("id") == verse_ref:
            # Extract text
            p_elem = sentence.find("p")
            if p_elem is not None:
                verse_text = "".join(p_elem.itertext()).strip()
                # Remove the verse reference prefix
                verse_text = re.sub(r'^[A-Z]+\s+\d+:\d+\s+', '', verse_text)
                verse_data["text"] = verse_text

            # Extract words
            position = 1
            for word in sentence.findall(".//w"):
                word_data = extract_hebrew_word(word, position)
                if word_data["text"]:  # Only add if has text
                    verse_data["words"].append(word_data)
                    position += 1

            break

    return verse_data


def process_greek_verse(book_elem, verse_ref):
    """Process a single Greek verse and return structured data."""
    book, chapter, verse = parse_verse_ref(verse_ref)

    verse_data = {
        "source": "macula-greek",
        "version": "1.0.0",
        "language": "grc",
        "verse": f"{book} {chapter}:{verse}",
        "text": "",
        "words": []
    }

    # Find the sentence for this verse
    for sentence in book_elem.findall(".//sentence"):
        milestone = sentence.find(".//milestone[@id]")
        if milestone is not None and milestone.get("id") == verse_ref:
            # Extract text
            p_elem = sentence.find("p")
            if p_elem is not None:
                verse_text = "".join(p_elem.itertext()).strip()
                # Remove the verse reference prefix
                verse_text = re.sub(r'^[A-Z]+\s+\d+:\d+\s+', '', verse_text)
                verse_data["text"] = verse_text

            # Extract words
            position = 1
            for word in sentence.findall(".//w"):
                word_data = extract_greek_word(word, position)
                if word_data["text"]:  # Only add if has text
                    verse_data["words"].append(word_data)
                    position += 1

            break

    return verse_data


def save_verse_yaml(verse_data, output_dir):
    """Save verse data as YAML file."""
    # Parse verse reference
    verse_ref = verse_data["verse"]
    book, chapter, verse = parse_verse_ref(verse_ref)

    # Create directory structure
    verse_dir = output_dir / book / f"{chapter:03d}" / f"{verse:03d}"
    verse_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = f"{book}-{chapter:03d}-{verse:03d}-macula.yaml"
    filepath = verse_dir / filename

    # Save YAML
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(verse_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return filepath


def process_hebrew_file(xml_file, output_dir):
    """Process a single Hebrew XML file."""
    log(f"Processing {xml_file.name}...")

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        verse_count = 0
        for sentence in root.findall(".//sentence[@id]"):
            verse_ref = sentence.get("id")
            if verse_ref:
                verse_data = process_hebrew_verse(root, verse_ref)
                if verse_data["words"]:  # Only save if has words
                    save_verse_yaml(verse_data, output_dir)
                    verse_count += 1

        log(f"  ✓ Processed {verse_count} verses")
        return verse_count

    except Exception as e:
        log(f"  ✗ Error: {e}")
        return 0


def process_greek_file(xml_file, output_dir):
    """Process a single Greek XML file."""
    log(f"Processing {xml_file.name}...")

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        verse_count = 0
        for milestone in root.findall(".//milestone[@id]"):
            verse_ref = milestone.get("id")
            if verse_ref:
                verse_data = process_greek_verse(root, verse_ref)
                if verse_data["words"]:  # Only save if has words
                    save_verse_yaml(verse_data, output_dir)
                    verse_count += 1

        log(f"  ✓ Processed {verse_count} verses")
        return verse_count

    except Exception as e:
        log(f"  ✗ Error: {e}")
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process Macula datasets into YAML commentary files"
    )
    parser.add_argument("--all", action="store_true", help="Process all verses")
    parser.add_argument("--testament", choices=["OT", "NT"], help="Process testament")
    parser.add_argument("--nt", action="store_true", help="Process New Testament (shortcut for --testament NT)")
    parser.add_argument("--book", help="Process single book (e.g., JHN, GEN)")
    parser.add_argument("--verse", help="Process single verse (e.g., 'JHN 1:1')")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Test without writing files")

    args = parser.parse_args()

    # Handle --nt shortcut
    if args.nt:
        args.testament = "NT"

    if not CACHE_DIR.exists():
        log("ERROR: Macula cache not found. Run macula_fetcher.py first.")
        sys.exit(1)

    output_dir = Path(args.output)

    log("=" * 60)
    log("Macula Processor Starting")
    log("=" * 60)

    total_verses = 0

    # Handle single verse processing
    if args.verse:
        book, chapter, verse = parse_verse_ref(args.verse)
        if not book:
            log(f"ERROR: Invalid verse reference '{args.verse}'. Use format: 'JHN 1:1'")
            sys.exit(1)

        # Determine if OT or NT
        is_ot = book in ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT",
                         "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH",
                         "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER",
                         "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON",
                         "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL"]

        if is_ot:
            log(f"Processing Hebrew verse: {args.verse}")
            # Find the Hebrew file (need to map book code back to filename)
            # For now, process all Hebrew files and filter
            if HEBREW_LOWFAT.exists():
                for xml_file in sorted(HEBREW_LOWFAT.glob("*.xml")):
                    try:
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        for sentence in root.findall(".//sentence[@id]"):
                            if sentence.get("id") == args.verse:
                                verse_data = process_hebrew_verse(root, args.verse)
                                if verse_data["words"] and not args.dry_run:
                                    save_verse_yaml(verse_data, output_dir)
                                    total_verses = 1
                                    log(f"✓ Processed {args.verse}")
                                break
                        if total_verses > 0:
                            break
                    except Exception as e:
                        continue
        else:
            log(f"Processing Greek verse: {args.verse}")
            # Find the Greek file
            if GREEK_LOWFAT.exists():
                for xml_file in sorted(GREEK_LOWFAT.glob("*.xml")):
                    try:
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        for milestone in root.findall(".//milestone[@id]"):
                            if milestone.get("id") == args.verse:
                                verse_data = process_greek_verse(root, args.verse)
                                if verse_data["words"] and not args.dry_run:
                                    save_verse_yaml(verse_data, output_dir)
                                    total_verses = 1
                                    log(f"✓ Processed {args.verse}")
                                break
                        if total_verses > 0:
                            break
                    except Exception as e:
                        continue

        if total_verses == 0:
            log(f"WARNING: Verse '{args.verse}' not found in dataset")

    # Handle book processing
    elif args.book:
        book_code = args.book.upper()

        # Determine if OT or NT
        is_ot = book_code in ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT",
                              "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH",
                              "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER",
                              "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON",
                              "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL"]

        if is_ot:
            log(f"Processing Hebrew book: {book_code}")
            if HEBREW_LOWFAT.exists():
                # Find matching Hebrew files
                for xml_file in sorted(HEBREW_LOWFAT.glob("*.xml")):
                    # Check if this file is for the requested book
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    chapter_id = root.get("id", "")
                    if chapter_id.startswith(book_code):
                        if not args.dry_run:
                            total_verses += process_hebrew_file(xml_file, output_dir)
        else:
            log(f"Processing Greek book: {book_code}")
            if GREEK_LOWFAT.exists():
                # Map book code to filename
                book_file_map = {
                    "MAT": "01-matthew.xml", "MRK": "02-mark.xml", "LUK": "03-luke.xml",
                    "JHN": "04-john.xml", "ACT": "05-acts.xml", "ROM": "06-romans.xml",
                    "1CO": "07-1corinthians.xml", "2CO": "08-2corinthians.xml",
                    "GAL": "09-galatians.xml", "EPH": "10-ephesians.xml",
                    "PHP": "11-philippians.xml", "COL": "12-colossians.xml",
                    "1TH": "13-1thessalonians.xml", "2TH": "14-2thessalonians.xml",
                    "1TI": "15-1timothy.xml", "2TI": "16-2timothy.xml",
                    "TIT": "17-titus.xml", "PHM": "18-philemon.xml",
                    "HEB": "19-hebrews.xml", "JAS": "20-james.xml",
                    "1PE": "21-1peter.xml", "2PE": "22-2peter.xml",
                    "1JN": "23-1john.xml", "2JN": "24-2john.xml",
                    "3JN": "25-3john.xml", "JUD": "26-jude.xml",
                    "REV": "27-revelation.xml"
                }

                if book_code in book_file_map:
                    xml_file = GREEK_LOWFAT / book_file_map[book_code]
                    if xml_file.exists() and not args.dry_run:
                        total_verses += process_greek_file(xml_file, output_dir)
                else:
                    log(f"ERROR: Unknown book code '{book_code}'")

    # Handle bulk processing
    elif args.testament == "OT" or args.all:
        log("Processing Hebrew (OT)...")
        if HEBREW_LOWFAT.exists():
            for xml_file in sorted(HEBREW_LOWFAT.glob("*.xml")):
                if not args.dry_run:
                    total_verses += process_hebrew_file(xml_file, output_dir)
        else:
            log("Hebrew directory not found")

    if (args.testament == "NT" or args.all) and not args.verse:
        log("Processing Greek (NT)...")
        if GREEK_LOWFAT.exists():
            for xml_file in sorted(GREEK_LOWFAT.glob("*.xml")):
                if not args.dry_run:
                    total_verses += process_greek_file(xml_file, output_dir)
        else:
            log("Greek directory not found")

    log("=" * 60)
    log(f"✓ Processed {total_verses} verses total")
    log(f"Output directory: {output_dir}")
    log("=" * 60)


if __name__ == "__main__":
    main()
