#!/usr/bin/env python3
"""
Build Strong's dictionary reference files from Macula Greek and Hebrew data.

This script:
1. Fetches XML files from Macula Greek (NT) and Hebrew (OT) repositories
2. Parses words with Strong's numbers, their senses, and grammatical forms
3. Groups by Strong's number and creates reference files showing all uses
4. Outputs YAML files in ./bible/words/strongs/{number}/{number}-references.yaml
"""

import xml.etree.ElementTree as ET
import requests
import yaml
import os
import re
from collections import defaultdict
from typing import Dict, List, Set
import time

# GitHub raw content base URLs
GREEK_BASE_URL = "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/SBLGNT/lowfat"
HEBREW_BASE_URL = "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/WLC/lowfat"

# GitHub API URLs to list files
GREEK_API_URL = "https://api.github.com/repos/Clear-Bible/macula-greek/contents/SBLGNT/lowfat"
HEBREW_API_URL = "https://api.github.com/repos/Clear-Bible/macula-hebrew/contents/WLC/lowfat"


class StrongsReference:
    """Collects all references for a Strong's number"""

    def __init__(self, strongs_num: str):
        self.strongs_num = strongs_num
        # meanings[gloss_or_sense][verse_ref] = grammatical_info
        self.meanings = defaultdict(lambda: defaultdict(list))
        # forms[form_description][verse_ref] = None (for deduplication)
        self.forms = defaultdict(lambda: defaultdict(lambda: None))

    def add_word(self, verse_ref: str, gloss: str, sense: str, morph: str, grammar: Dict[str, str]):
        """Add a word occurrence to this Strong's number"""
        # Determine the meaning key (prefer sense number if available)
        meaning_key = sense if sense else gloss

        # Build form description from grammatical attributes
        form_parts = []

        # For verbs
        if 'tense' in grammar and grammar['tense']:
            form_parts.append(grammar['tense'])
        if 'voice' in grammar and grammar['voice']:
            form_parts.append(grammar['voice'])
        if 'mood' in grammar and grammar['mood']:
            form_parts.append(grammar['mood'])

        # For nouns/adjectives
        if 'gender' in grammar and grammar['gender']:
            form_parts.append(grammar['gender'])
        if 'number' in grammar and grammar['number']:
            form_parts.append(grammar['number'])
        if 'case' in grammar and grammar['case']:
            form_parts.append(grammar['case'])

        # For Hebrew
        if 'stem' in grammar and grammar['stem']:
            form_parts.append(grammar['stem'])
        if 'state' in grammar and grammar['state']:
            form_parts.append(grammar['state'])
        if 'person' in grammar and grammar['person']:
            form_parts.append(grammar['person'])

        form_desc = '/'.join(form_parts) if form_parts else morph

        # Add to meanings
        self.meanings[meaning_key][verse_ref].append({
            'morph': morph,
            'form': form_desc,
            'grammar': grammar
        })

        # Add to forms
        self.forms[form_desc][verse_ref] = None

    def to_dict(self):
        """Convert to dictionary for YAML output"""
        result = {
            'strongs_number': self.strongs_num,
            'meanings': {},
            'forms': {}
        }

        # Convert meanings
        for meaning, verses in sorted(self.meanings.items()):
            result['meanings'][meaning] = sorted(verses.keys())

        # Convert forms
        for form, verses in sorted(self.forms.items()):
            result['forms'][form] = sorted(verses.keys())

        return result


class MaculaParser:
    """Parses Macula XML files and extracts Strong's references"""

    def __init__(self):
        self.strongs_data = defaultdict(lambda: None)

    def get_strongs_ref(self, strongs_num: str) -> StrongsReference:
        """Get or create a StrongsReference object"""
        if self.strongs_data[strongs_num] is None:
            self.strongs_data[strongs_num] = StrongsReference(strongs_num)
        return self.strongs_data[strongs_num]

    def parse_greek_file(self, url: str):
        """Parse a Greek NT XML file"""
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        # Track current verse(s) - sentences can span multiple verses
        current_verses = []

        # Iterate through all elements
        for elem in root.iter():
            # Check for milestone markers
            if elem.tag == 'milestone' and elem.get('unit') == 'verse':
                verse_id = elem.get('id')
                if verse_id:
                    current_verses.append(verse_id)
                    # Keep only last few verses (in case of long sentences)
                    if len(current_verses) > 3:
                        current_verses = current_verses[-3:]

            # Check for word elements
            if elem.tag == 'w':
                strong = elem.get('strong')
                if not strong:
                    continue

                # Get verse reference (use the most recent verse)
                verse_ref = current_verses[-1] if current_verses else 'UNKNOWN'

                # Extract word information
                gloss = elem.get('gloss', elem.get('english', ''))
                lemma = elem.get('lemma', '')
                morph = elem.get('morph', '')

                # Extract grammatical attributes
                grammar = {
                    'lemma': lemma,
                    'case': elem.get('case', ''),
                    'number': elem.get('number', ''),
                    'gender': elem.get('gender', ''),
                    'tense': elem.get('tense', ''),
                    'voice': elem.get('voice', ''),
                    'mood': elem.get('mood', ''),
                    'person': elem.get('person', ''),
                }

                # Add to Strong's reference
                ref = self.get_strongs_ref(f"G{strong}")
                ref.add_word(verse_ref, gloss, '', morph, grammar)

    def parse_hebrew_file(self, url: str):
        """Parse a Hebrew OT XML file"""
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        # Track current verse
        current_verse = None

        # Iterate through all elements
        for elem in root.iter():
            # Check for milestone markers
            if elem.tag == 'milestone' and elem.get('unit') == 'verse':
                verse_id = elem.get('id')
                if verse_id:
                    current_verse = verse_id

            # Check for word elements
            if elem.tag == 'w':
                strong = elem.get('strongnumberx')
                if not strong:
                    continue

                verse_ref = current_verse if current_verse else 'UNKNOWN'

                # Extract word information
                gloss = elem.get('english', elem.get('mandarin', ''))
                lemma = elem.get('lemma', '')
                morph = elem.get('morph', '')
                sense = elem.get('sensenumber', '')

                # Extract grammatical attributes
                grammar = {
                    'lemma': lemma,
                    'gender': elem.get('gender', ''),
                    'number': elem.get('number', ''),
                    'stem': elem.get('stem', ''),
                    'person': elem.get('person', ''),
                    'state': elem.get('state', ''),
                    'pos': elem.get('pos', ''),
                }

                # Add to Strong's reference
                ref = self.get_strongs_ref(f"H{strong}")
                ref.add_word(verse_ref, gloss, sense, morph, grammar)

    def fetch_and_parse_all(self):
        """Fetch and parse all files from both repositories"""
        # Fetch Greek files
        print("Fetching Greek (NT) file list...")
        response = requests.get(GREEK_API_URL)
        response.raise_for_status()
        greek_files = response.json()

        for file_info in greek_files:
            if file_info['name'].endswith('.xml') and not file_info['name'].startswith('sblgnt'):
                try:
                    self.parse_greek_file(file_info['download_url'])
                    time.sleep(0.5)  # Be nice to GitHub
                except Exception as e:
                    print(f"Error parsing {file_info['name']}: {e}")

        # Fetch Hebrew files
        print("Fetching Hebrew (OT) file list...")
        response = requests.get(HEBREW_API_URL)
        response.raise_for_status()
        hebrew_files = response.json()

        for file_info in hebrew_files:
            if file_info['name'].endswith('.xml'):
                try:
                    self.parse_hebrew_file(file_info['download_url'])
                    time.sleep(0.5)  # Be nice to GitHub
                except Exception as e:
                    print(f"Error parsing {file_info['name']}: {e}")

    def write_yaml_files(self, output_base_dir: str):
        """Write YAML files for each Strong's number"""
        print(f"\nWriting YAML files to {output_base_dir}...")

        for strongs_num, ref_obj in self.strongs_data.items():
            if ref_obj is None:
                continue

            # Create directory structure
            dir_path = os.path.join(output_base_dir, strongs_num)
            os.makedirs(dir_path, exist_ok=True)

            # Write YAML file
            file_path = os.path.join(dir_path, f"{strongs_num}-references.yaml")
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(ref_obj.to_dict(), f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            print(f"  Written: {file_path}")


def main():
    """Main execution function"""
    parser = MaculaParser()

    print("=" * 70)
    print("Building Strong's Dictionary References")
    print("=" * 70)

    # Fetch and parse all files
    parser.fetch_and_parse_all()

    # Write output files
    output_dir = '/home/user/context-grounded-bible/bible/words/strongs'
    parser.write_yaml_files(output_dir)

    print("\n" + "=" * 70)
    print(f"Complete! Processed {len(parser.strongs_data)} Strong's numbers")
    print("=" * 70)


if __name__ == '__main__':
    main()
