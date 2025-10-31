#!/usr/bin/env python3
"""
Strong's Dictionary Fetcher - Enhanced Edition

This script fetches Strong's Hebrew and Greek dictionary data from multiple sources
and generates comprehensive YAML files for each entry.

Directory structure: bible/words/strongs/{strongs-number}/{strongs-number}.strongs.yaml

Strong's numbers use leading zeros:
- Greek: G0001-G5624 (4 digits)
- Hebrew: H0001-H8674 (4 digits)

Data sources:
1. Base data: openscriptures/strongs (CC-BY-SA)
2. Extended definitions: STEPBible TBESG/TBESH/TFLSJ (CC BY 4.0)
3. Synonyms: Clear-Bible Proximity data (CC BY 4.0)
4. Usage statistics: morphhb (CC BY 4.0, Hebrew only)
"""

import os
import re
import json
import yaml
import csv
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import defaultdict
from bs4 import BeautifulSoup

# Configuration
BASE_DIR = Path(__file__).parent
BIBLE_WORDS_DIR = BASE_DIR / "bible" / "words" / "strongs"
CACHE_DIR = Path("/tmp/strongs_enhancement")

# Base Strong's data URLs
GREEK_URL = "https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js"
HEBREW_URL = "https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.js"

# STEPBible lexicon URLs
STEPBIBLE_BASE = "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
STEPBIBLE_TBESG = STEPBIBLE_BASE + "TBESG%20-%20Translators%20Brief%20lexicon%20of%20Extended%20Strongs%20for%20Greek%20-%20STEPBible.org%20CC%20BY.txt"
STEPBIBLE_TBESH = STEPBIBLE_BASE + "TBESH%20-%20Translators%20Brief%20lexicon%20of%20Extended%20Strongs%20for%20Hebrew%20-%20STEPBible.org%20CC%20BY.txt"
STEPBIBLE_TFLSJ = STEPBIBLE_BASE + "TFLSJ%20%200-5624%20-%20Translators%20Formatted%20full%20LSJ%20Bible%20lexicon%20-%20STEPBible.org%20CC%20BY.txt"

# Clear-Bible Proximity data URLs
PROXIMITY_HEBREW = "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/sources/Clear/synonyms/Proximity.tsv"
PROXIMITY_GREEK = "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/sources/Clear/synonyms/Proximity.tsv"

# morphhb data URL (we'll use a simple approach - download JSON if available)
MORPHHB_REPO = "https://github.com/openscriptures/morphhb.git"


def download_file(url: str) -> str:
    """Download a file from URL and return its contents as string."""
    print(f"Downloading {url}...")
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


def download_to_cache(url: str, cache_file: Path) -> Path:
    """Download a file to cache directory if not already cached."""
    if cache_file.exists():
        print(f"  Using cached file: {cache_file.name}")
        return cache_file

    print(f"  Downloading {cache_file.name}...")
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    content = download_file(url)
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return cache_file


def download_stepbible_lexicons() -> Dict[str, Path]:
    """Download STEPBible lexicons to cache."""
    print("\n📥 Downloading STEPBible lexicons...")

    stepbible_dir = CACHE_DIR / "stepbible"

    files = {
        'greek_brief': download_to_cache(STEPBIBLE_TBESG, stepbible_dir / "TBESG.tsv"),
        'hebrew_brief': download_to_cache(STEPBIBLE_TBESH, stepbible_dir / "TBESH.tsv"),
        'greek_full': download_to_cache(STEPBIBLE_TFLSJ, stepbible_dir / "TFLSJ.tsv"),
    }

    print("  ✓ STEPBible lexicons ready\n")
    return files


def download_proximity_data() -> Dict[str, Path]:
    """Download Clear-Bible Proximity data to cache."""
    print("📥 Downloading Clear-Bible Proximity data...")

    proximity_dir = CACHE_DIR / "proximity"

    files = {
        'hebrew': download_to_cache(PROXIMITY_HEBREW, proximity_dir / "hebrew_proximity.tsv"),
        'greek': download_to_cache(PROXIMITY_GREEK, proximity_dir / "greek_proximity.tsv"),
    }

    print("  ✓ Proximity data ready\n")
    return files


def parse_stepbible_tsv(filepath: Path) -> Dict[str, Dict[str, str]]:
    """
    Parse STEPBible TSV file into dictionary keyed by Strong's number.

    Expected columns:
    - TBESG/TBESH: eStrong, dStrong, uStrong, Greek/Hebrew, Transliteration, Morph, Gloss, Meaning
    - TFLSJ: Strong, Greek, Transliteration, LSJ_Entry

    Returns: {strongs_num: {fields...}}
    """
    result = {}

    with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig to handle BOM
        # Skip header lines until we find the column headers
        # Look for a line that has multiple tab-separated fields including 'eStrong' or 'Strong'
        lines = f.readlines()

        # Find the header line
        header_line_idx = None
        for i, line in enumerate(lines):
            fields = line.strip().split('\t')
            # Header line should have multiple fields and contain 'eStrong' or 'Strong'
            if len(fields) >= 5 and any('Strong' in field for field in fields):
                header_line_idx = i
                break

        if header_line_idx is None:
            print(f"  Warning: Could not find header line in {filepath.name}")
            return result

        # Parse column names from header line
        headers = [h.strip() for h in lines[header_line_idx].split('\t')]

        # Find the first data line (skip separator lines like ===)
        data_start_idx = header_line_idx + 1
        while data_start_idx < len(lines) and lines[data_start_idx].startswith('='):
            data_start_idx += 1

        # Process data rows
        for line in lines[data_start_idx:]:
            line = line.strip()
            if not line or line.startswith('='):
                continue

            fields = line.split('\t')
            if len(fields) < len(headers):
                # Pad with empty strings if needed
                fields.extend([''] * (len(headers) - len(fields)))

            # Create row dictionary
            row = dict(zip(headers, fields))

            # Get Strong's number
            strongs_num = row.get('eStrong') or row.get('eStrong#') or row.get('Strong')

            if not strongs_num or not strongs_num.strip():
                continue

            strongs_num = strongs_num.strip()

            # Store the row
            result[strongs_num] = row

    return result


def parse_proximity_tsv(filepath: Path, min_proximity: float = 0.70) -> Dict[str, List[Tuple[str, float]]]:
    """
    Parse Proximity TSV file into relationships.

    Format: StrongNumberX1, StrongNumberX2, Distance

    Returns: {strongs_num: [(related_num, proximity_score), ...]}
    """
    relationships = defaultdict(list)

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')

        # Skip header if present
        header = next(reader, None)

        for row in reader:
            if len(row) < 3:
                continue

            num1, num2, distance = row[0], row[1], float(row[2])

            # Only include relationships above threshold
            if distance < min_proximity:
                continue

            # Add bidirectional relationships
            relationships[num1].append((num2, distance))
            relationships[num2].append((num1, distance))

    # Sort each relationship list by proximity (highest first)
    for strongs_num in relationships:
        relationships[strongs_num].sort(key=lambda x: x[1], reverse=True)

    return dict(relationships)


def strip_html(html_text: str) -> str:
    """
    Strip HTML tags and convert to plain text.

    Handles:
    - Removes all HTML tags
    - Converts <BR /> to newlines
    - Preserves text content
    - Cleans up extra whitespace
    """
    if not html_text:
        return ""

    # Replace BR tags with newlines first
    html_text = re.sub(r'<BR\s*/?>', '\n', html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'<br\s*/?>', '\n', html_text, flags=re.IGNORECASE)

    # Use BeautifulSoup to strip HTML
    soup = BeautifulSoup(html_text, 'lxml')
    text = soup.get_text()

    # Clean up whitespace
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]  # Remove empty lines
    text = '\n'.join(lines)

    return text.strip()


def load_all_enhancement_data() -> Dict[str, Any]:
    """Load all enhancement data sources into memory."""
    print("\n" + "="*60)
    print("Loading enhancement data sources...")
    print("="*60)

    data = {}

    # Download sources
    stepbible_files = download_stepbible_lexicons()
    proximity_files = download_proximity_data()

    # Parse STEPBible lexicons
    print("📖 Parsing STEPBible lexicons...")
    data['greek_brief'] = parse_stepbible_tsv(stepbible_files['greek_brief'])
    data['hebrew_brief'] = parse_stepbible_tsv(stepbible_files['hebrew_brief'])
    data['greek_full'] = parse_stepbible_tsv(stepbible_files['greek_full'])
    print(f"  ✓ Loaded {len(data['greek_brief'])} Greek brief entries")
    print(f"  ✓ Loaded {len(data['hebrew_brief'])} Hebrew brief entries")
    print(f"  ✓ Loaded {len(data['greek_full'])} Greek LSJ entries\n")

    # Parse Proximity data
    print("🔗 Parsing Proximity data...")
    data['proximity_hebrew'] = parse_proximity_tsv(proximity_files['hebrew'])
    data['proximity_greek'] = parse_proximity_tsv(proximity_files['greek'])
    print(f"  ✓ Loaded {len(data['proximity_hebrew'])} Hebrew relationships")
    print(f"  ✓ Loaded {len(data['proximity_greek'])} Greek relationships\n")

    print("="*60)
    print("✓ All enhancement data loaded\n")

    return data


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


def create_strongs_yaml(strongs_num: str, entry: Dict[str, Any], enhancement_data: Dict[str, Any] = None, all_strongs: Dict[str, Dict] = None) -> str:
    """
    Create enhanced YAML content for a Strong's entry following STANDARDIZATION.md.

    Changes from previous version:
    - Strip HTML from definitions
    - Use inline {source-id} citations
    - Add lemma and gloss to related_words
    - Remove enhancements and aggregate license fields
    - Follow citation standards

    Format per STANDARDIZATION.md:
    ---
    strongs_number: G0001
    language: greek
    lemma: original word
    definition: ... {openscriptures-strongs}
    extended_definition: |
      Plain text definition (HTML stripped) {STEPBible-TBESG}
    etymology: |
      Plain text etymology (HTML stripped) {STEPBible-TFLSJ}
    related_words:
      - strongs: G0025
        lemma: ἀγαπάω
        gloss: to love {openscriptures-strongs}
        proximity: 0.95 {macula-proximity}
    """
    # Determine language
    language = "greek" if strongs_num.startswith('G') else "hebrew"

    # Build the YAML structure (base data first)
    yaml_data = {
        "strongs_number": strongs_num,
        "language": language,
    }

    # Add base fields
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

    # Add enhancement data if available
    if enhancement_data:
        # STEPBible extended definition
        stepbible_key = 'greek_brief' if language == 'greek' else 'hebrew_brief'
        if strongs_num in enhancement_data.get(stepbible_key, {}):
            stepbible_entry = enhancement_data[stepbible_key][strongs_num]

            # Find the definition field
            definition_field = None
            for key in stepbible_entry.keys():
                if 'Meaning' in key or 'lexicon' in key or 'BDB' in key:
                    definition_field = stepbible_entry[key]
                    break

            if definition_field and definition_field.strip():
                # Strip HTML and add inline citation
                plain_def = strip_html(definition_field)
                source_id = 'STEPBible-TBESG' if language == 'greek' else 'STEPBible-TBESH'
                yaml_data['extended_definition'] = f"{plain_def} {{{source_id}}}"

        # LSJ etymology (Greek only)
        if language == 'greek' and strongs_num in enhancement_data.get('greek_full', {}):
            lsj_entry = enhancement_data['greek_full'][strongs_num]

            # Find LSJ content
            lsj_content = None
            for key in lsj_entry.keys():
                if 'LSJ' in key or 'Liddell' in key or len(key) > 50:
                    lsj_content = lsj_entry[key]
                    if lsj_content and lsj_content.strip():
                        break

            if lsj_content and lsj_content.strip():
                # Strip HTML and add inline citation
                plain_etym = strip_html(lsj_content)
                yaml_data['etymology'] = f"{plain_etym} {{STEPBible-TFLSJ}}"

        # Related words from Proximity data
        proximity_key = 'proximity_greek' if language == 'greek' else 'proximity_hebrew'
        if strongs_num in enhancement_data.get(proximity_key, {}):
            related = enhancement_data[proximity_key][strongs_num]

            # Separate same-language from cross-language
            same_lang = []
            cross_lang = []

            for related_num, proximity in related[:15]:  # Top 15 relationships
                # Determine if cross-language
                is_cross = (language == 'greek' and related_num.startswith('H')) or \
                           (language == 'hebrew' and related_num.startswith('G'))

                # Look up lemma and gloss for this Strong's number
                lemma = None
                gloss = None
                if all_strongs and related_num in all_strongs:
                    related_entry = all_strongs[related_num]
                    lemma = related_entry.get('lemma')
                    # Get a brief gloss from the definition (first phrase)
                    definition = related_entry.get('strongs_def', '')
                    if definition:
                        # Take first part before semicolon or comma
                        gloss = definition.split(';')[0].split(',')[0].strip()
                        # Remove parentheticals
                        gloss = re.sub(r'\([^)]*\)', '', gloss).strip()

                rel_entry = {
                    'strongs': related_num,
                }

                if lemma:
                    rel_entry['lemma'] = lemma
                if gloss:
                    rel_entry['gloss'] = f"{gloss} {{openscriptures-strongs}}"

                rel_entry['proximity'] = f"{round(proximity, 4)} {{macula-proximity}}"

                if is_cross:
                    rel_entry['language'] = 'hebrew' if related_num.startswith('H') else 'greek'
                    cross_lang.append(rel_entry)
                else:
                    same_lang.append(rel_entry)

            related_words = {}
            if same_lang:
                related_words['synonyms'] = same_lang[:10]  # Top 10
            if cross_lang:
                related_words['cross_language'] = cross_lang[:5]  # Top 5

            if related_words:
                yaml_data['related_words'] = related_words

    # Source attribution (inline citation format per STANDARDIZATION.md)
    yaml_data["source"] = "openscriptures/strongs {CC-BY-SA}"

    # Convert to YAML
    return yaml.dump(yaml_data, allow_unicode=True, sort_keys=False, default_flow_style=False)


def create_strongs_file(strongs_num: str, entry: Dict[str, Any], enhancement_data: Dict[str, Any] = None, all_strongs: Dict[str, Dict] = None):
    """Create an enhanced YAML file for a Strong's entry with formatted number."""
    # Format the Strong's number with leading zeros
    formatted_num = format_strongs_number(strongs_num)

    # Create directory structure
    strongs_dir = BIBLE_WORDS_DIR / formatted_num
    strongs_dir.mkdir(parents=True, exist_ok=True)

    # Create YAML file with enhancements
    yaml_path = strongs_dir / f"{formatted_num}.strongs.yaml"
    yaml_content = create_strongs_yaml(formatted_num, entry, enhancement_data, all_strongs)

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    return yaml_path


def process_dictionary(url: str, dict_name: str, enhancement_data: Dict[str, Any] = None, all_dictionaries: Dict[str, Dict] = None):
    """Download and process a Strong's dictionary (Greek or Hebrew) with enhancements."""
    print(f"\n{'='*60}")
    print(f"Processing {dict_name} dictionary...")
    print(f"{'='*60}\n")

    # Download the JS file
    js_content = download_file(url)

    # Parse the JavaScript dictionary
    print(f"Parsing {dict_name} dictionary...")
    dictionary = parse_javascript_dict(js_content)

    print(f"Found {len(dictionary)} entries in {dict_name} dictionary")

    # Build a complete strongs lookup (formatted numbers -> entries)
    all_strongs = {}
    if all_dictionaries:
        for d in all_dictionaries.values():
            for num, entry in d.items():
                formatted = format_strongs_number(num)
                all_strongs[formatted] = entry

    # Process each entry
    created_count = 0
    enhanced_count = 0

    for strongs_num, entry in dictionary.items():
        try:
            # Format the number for lookup in enhancement data
            formatted_num = format_strongs_number(strongs_num)

            # Create file with enhancements
            yaml_path = create_strongs_file(strongs_num, entry, enhancement_data, all_strongs)
            created_count += 1

            # Count how many were enhanced
            if enhancement_data:
                lang_key = 'greek_brief' if formatted_num.startswith('G') else 'hebrew_brief'
                prox_key = 'proximity_greek' if formatted_num.startswith('G') else 'proximity_hebrew'

                if formatted_num in enhancement_data.get(lang_key, {}) or \
                   formatted_num in enhancement_data.get(prox_key, {}):
                    enhanced_count += 1

            if created_count % 100 == 0:
                print(f"  Created {created_count} files ({enhanced_count} enhanced)...")

        except Exception as e:
            print(f"  Error processing {strongs_num}: {e}")

    print(f"\n✓ Created {created_count} {dict_name} Strong's files")
    print(f"  ({enhanced_count} entries enhanced with additional data)")


def main():
    """Main entry point - Enhanced Strong's Dictionary Fetcher."""
    print("="*60)
    print("Strong's Dictionary Fetcher - Enhanced Edition")
    print("="*60)
    print(f"Output directory: {BIBLE_WORDS_DIR}")
    print("Format: Using 4-digit zero-padded Strong's numbers")
    print("  Greek: G0001-G5624")
    print("  Hebrew: H0001-H8674")
    print("\nEnhancements:")
    print("  • STEPBible extended definitions (Abbott-Smith, BDB, LSJ)")
    print("  • Clear-Bible proximity-based synonyms with lemmas")
    print("  • Cross-language relationships (Hebrew ↔ Greek)")
    print("  • HTML stripped, inline citations per STANDARDIZATION.md")
    print("\n")

    # Create base directory
    BIBLE_WORDS_DIR.mkdir(parents=True, exist_ok=True)

    # Load all enhancement data sources
    try:
        enhancement_data = load_all_enhancement_data()
    except Exception as e:
        print(f"\n⚠ Warning: Could not load enhancement data: {e}")
        print("  Continuing with base Strong's data only...\n")
        enhancement_data = None

    # Download both dictionaries first (needed for lemma lookups in related_words)
    print("\n" + "="*60)
    print("Downloading base Strong's dictionaries...")
    print("="*60 + "\n")

    try:
        greek_content = download_file(GREEK_URL)
        greek_dict = parse_javascript_dict(greek_content)
        print(f"✓ Loaded {len(greek_dict)} Greek entries")
    except Exception as e:
        print(f"✗ Error loading Greek dictionary: {e}")
        greek_dict = {}

    try:
        hebrew_content = download_file(HEBREW_URL)
        hebrew_dict = parse_javascript_dict(hebrew_content)
        print(f"✓ Loaded {len(hebrew_dict)} Hebrew entries\n")
    except Exception as e:
        print(f"✗ Error loading Hebrew dictionary: {e}")
        hebrew_dict = {}

    all_dictionaries = {
        'greek': greek_dict,
        'hebrew': hebrew_dict
    }

    # Process Greek dictionary
    try:
        process_dictionary(GREEK_URL, "Greek", enhancement_data, all_dictionaries)
    except Exception as e:
        print(f"\n✗ Error processing Greek dictionary: {e}")

    # Process Hebrew dictionary
    try:
        process_dictionary(HEBREW_URL, "Hebrew", enhancement_data, all_dictionaries)
    except Exception as e:
        print(f"\n✗ Error processing Hebrew dictionary: {e}")

    print("\n" + "="*60)
    print("✓ Strong's Dictionary Fetcher completed!")
    print("="*60)


if __name__ == "__main__":
    main()
