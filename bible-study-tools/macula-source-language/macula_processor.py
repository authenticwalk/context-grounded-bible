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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


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
        "ref": word_elem.get("ref", ""),
        "xml_id": word_elem.get("{http://www.w3.org/XML/1998/namespace}id", ""),
        "unicode": word_elem.text or "",
        "lemma": word_elem.get("lemma", ""),
        "transliteration": word_elem.get("transliteration", ""),
        "class": word_elem.get("class", ""),
        "pos": word_elem.get("pos", ""),
        "morph": word_elem.get("morph", ""),
        "english": word_elem.get("english", ""),
        "mandarin": word_elem.get("mandarin", ""),
        "gloss": word_elem.get("gloss", ""),
    }

    # Morphological fields
    for field in ["gender", "number", "person", "state", "stem", "type"]:
        if word_elem.get(field):
            word_data[field] = word_elem.get(field)

    # Lexical references
    for field in ["stronglemma", "strongnumberx"]:
        if word_elem.get(field):
            word_data[field] = word_elem.get(field)

    # Semantic domains
    sdbh = word_elem.get("sdbh", "")
    if sdbh:
        word_data["sdbh"] = sdbh.split() if " " in sdbh else sdbh

    lexdomain = word_elem.get("lexdomain", "")
    if lexdomain:
        word_data["lexdomain"] = lexdomain.split() if " " in lexdomain else lexdomain

    coredomain = word_elem.get("coredomain", "")
    if coredomain:
        word_data["coredomain"] = coredomain.split() if " " in coredomain else coredomain

    if word_elem.get("sensenumber"):
        word_data["sensenumber"] = word_elem.get("sensenumber")

    # Greek cross-reference
    if word_elem.get("greek"):
        word_data["greek"] = word_elem.get("greek")
    if word_elem.get("greekstrong"):
        word_data["greekstrong"] = word_elem.get("greekstrong")

    # Syntactic role
    if word_elem.get("role"):
        word_data["role"] = word_elem.get("role")
    if word_elem.get("frame"):
        word_data["frame"] = word_elem.get("frame")

    return word_data


def extract_greek_word(word_elem, position):
    """Extract data from Greek word element."""
    word_data = {
        "position": position,
        "ref": word_elem.get("ref", ""),
        "xml_id": word_elem.get("{http://www.w3.org/XML/1998/namespace}id", ""),
        "unicode": word_elem.text or "",
        "lemma": word_elem.get("lemma", ""),
        "normalized": word_elem.get("normalized", ""),
        "class": word_elem.get("class", ""),
        "morph": word_elem.get("morph", ""),
        "gloss": word_elem.get("gloss", ""),
    }

    # Morphological fields
    for field in ["gender", "number", "person", "case", "tense", "voice", "mood"]:
        if word_elem.get(field):
            word_data[field] = word_elem.get(field)

    # Article detection
    if word_elem.get("class") == "det":
        word_data["has_article"] = True

    # Lexical references
    if word_elem.get("strong"):
        word_data["strong"] = word_elem.get("strong")

    # Semantic domains
    if word_elem.get("domain"):
        word_data["domain"] = word_elem.get("domain")
    if word_elem.get("ln"):
        word_data["ln"] = word_elem.get("ln")

    # Syntactic role
    if word_elem.get("role"):
        word_data["role"] = word_elem.get("role")

    return word_data


def process_hebrew_verse(chapter_elem, verse_ref):
    """Process a single Hebrew verse and return structured data."""
    book, chapter, verse = parse_verse_ref(verse_ref)

    verse_data = {
        "verse": {
            "reference": f"{book} {chapter}:{verse}",
            "book_code": book,
            "chapter": chapter,
            "verse": verse,
            "testament": "OT"
        },
        "tool": {
            "name": "macula-source-language",
            "version": "1.0.0",
            "generated_date": datetime.now().strftime("%Y-%m-%d")
        },
        "source": {
            "dataset": "MACULA Hebrew Linguistic Datasets",
            "url": "https://github.com/Clear-Bible/macula-hebrew",
            "license": "CC BY 4.0",
            "copyright": "Biblica, Inc (2022-2024)",
            "citation": "MACULA Hebrew Linguistic Datasets, available at https://github.com/Clear-Bible/macula-hebrew/",
            "definitions": "./MACULA-FIELD-DEFINITIONS.md",
            "base_text": "Westminster Leningrad Codex"
        },
        "source_text": {
            "language": "heb"
        },
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
                verse_data["source_text"]["unicode"] = verse_text

            # Extract words
            position = 1
            for word in sentence.findall(".//w"):
                word_data = extract_hebrew_word(word, position)
                if word_data["unicode"]:  # Only add if has text
                    verse_data["words"].append(word_data)
                    position += 1

            # Extract syntax rule if available
            for wg in sentence.findall(".//wg[@rule]"):
                if wg.get("head") == "true":
                    verse_data["syntax"] = {"word_order": wg.get("rule")}
                    break

            break

    return verse_data


def process_greek_verse(book_elem, verse_ref):
    """Process a single Greek verse and return structured data."""
    book, chapter, verse = parse_verse_ref(verse_ref)

    verse_data = {
        "verse": {
            "reference": f"{book} {chapter}:{verse}",
            "book_code": book,
            "chapter": chapter,
            "verse": verse,
            "testament": "NT"
        },
        "tool": {
            "name": "macula-source-language",
            "version": "1.0.0",
            "generated_date": datetime.now().strftime("%Y-%m-%d")
        },
        "source": {
            "dataset": "MACULA Greek Linguistic Datasets",
            "url": "https://github.com/Clear-Bible/macula-greek",
            "license": "CC BY 4.0",
            "copyright": "Biblica, Inc (2022-2024)",
            "citation": "MACULA Greek Linguistic Datasets, available at https://github.com/Clear-Bible/macula-greek/",
            "definitions": "./MACULA-FIELD-DEFINITIONS.md",
            "base_text": "Nestle1904"
        },
        "source_text": {
            "language": "grc"
        },
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
                verse_data["source_text"]["unicode"] = verse_text

            # Extract words
            position = 1
            for word in sentence.findall(".//w"):
                word_data = extract_greek_word(word, position)
                if word_data["unicode"]:  # Only add if has text
                    verse_data["words"].append(word_data)
                    position += 1

            # Extract syntax rule if available
            for wg in sentence.findall(".//wg[@rule]"):
                if wg.get("class") == "cl":
                    verse_data["syntax"] = {"word_order": wg.get("rule")}
                    break

            break

    return verse_data


def save_verse_yaml(verse_data, output_dir):
    """Save verse data as YAML file."""
    book = verse_data["verse"]["book_code"]
    chapter = verse_data["verse"]["chapter"]
    verse = verse_data["verse"]["verse"]

    # Create directory structure
    verse_dir = output_dir / book / f"{chapter:03d}" / f"{verse:03d}"
    verse_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = f"{book}-{chapter:03d}-{verse:03d}-source-language.yaml"
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
    parser.add_argument("--book", help="Process single book (e.g., JHN, GEN)")
    parser.add_argument("--verse", help="Process single verse (e.g., 'JHN 1:1')")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Test without writing files")

    args = parser.parse_args()

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
