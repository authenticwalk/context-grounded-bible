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
from collections import defaultdict
from typing import Dict
import time

# GitHub API URLs to list files
GREEK_API_URL = "https://api.github.com/repos/Clear-Bible/macula-greek/contents/SBLGNT/lowfat"
HEBREW_API_URL = "https://api.github.com/repos/Clear-Bible/macula-hebrew/contents/WLC/lowfat"


class StrongsReference:
    """Collects all references for a Strong's number"""

    def __init__(self, strongs_num: str):
        self.strongs_num = strongs_num
        self.lemma = None  # Will be set from first occurrence
        # senses[sense_key] = {'gloss': str, 'verses': [verse_refs]}
        self.senses = defaultdict(lambda: {'gloss': '', 'verses': []})
        # forms[form_desc] = {'word': actual_word, 'verses': [refs]}
        self.forms = defaultdict(lambda: {'word': None, 'verses': []})

    def add_word(self, verse_ref: str, word: str, gloss: str, sense: str,
                 domain: str, ln: str, morph: str, grammar: Dict[str, str]):
        """Add a word occurrence to this Strong's number"""

        # Set lemma if not already set
        if self.lemma is None and grammar.get('lemma'):
            self.lemma = grammar['lemma']

        # Determine sense key (prefer domain/ln for Greek, sense number for Hebrew)
        if domain:
            sense_key = domain
        elif ln:
            sense_key = ln
        elif sense:
            sense_key = sense
        else:
            sense_key = gloss if gloss else 'unknown'

        # Add to senses
        if not self.senses[sense_key]['gloss']:
            self.senses[sense_key]['gloss'] = gloss
        if verse_ref not in self.senses[sense_key]['verses']:
            self.senses[sense_key]['verses'].append(verse_ref)

        # Build form description from grammatical attributes
        form_parts = []
        if 'tense' in grammar and grammar['tense']:
            form_parts.append(grammar['tense'])
        if 'voice' in grammar and grammar['voice']:
            form_parts.append(grammar['voice'])
        if 'mood' in grammar and grammar['mood']:
            form_parts.append(grammar['mood'])
        if 'gender' in grammar and grammar['gender']:
            form_parts.append(grammar['gender'])
        if 'number' in grammar and grammar['number']:
            form_parts.append(grammar['number'])
        if 'case' in grammar and grammar['case']:
            form_parts.append(grammar['case'])
        if 'stem' in grammar and grammar['stem']:
            form_parts.append(grammar['stem'])
        if 'state' in grammar and grammar['state']:
            form_parts.append(grammar['state'])
        if 'person' in grammar and grammar['person']:
            form_parts.append(grammar['person'])

        form_desc = '/'.join(form_parts) if form_parts else morph

        # Add to forms - store word once and collect verses
        if self.forms[form_desc]['word'] is None:
            self.forms[form_desc]['word'] = word
        # Add verse if not already present
        if verse_ref not in self.forms[form_desc]['verses']:
            self.forms[form_desc]['verses'].append(verse_ref)

    def to_dict(self):
        """Convert to dictionary for YAML output"""
        result = {
            'strongs_number': self.strongs_num,
        }

        if self.lemma:
            result['lemma'] = self.lemma

        # Convert senses
        senses_dict = {}
        for sense_key, sense_data in sorted(self.senses.items()):
            senses_dict[sense_key] = {
                'gloss': sense_data['gloss'],
                'verses': sorted(sense_data['verses'])
            }
        result['senses'] = senses_dict

        # Convert forms
        forms_dict = {}
        for form, form_data in sorted(self.forms.items()):
            forms_dict[form] = {
                'word': form_data['word'],
                'verses': sorted(form_data['verses'])
            }
        result['forms'] = forms_dict

        return result


class MaculaParser:
    """Parses Macula XML files and extracts Strong's references"""

    def __init__(self):
        self.strongs_data = defaultdict(lambda: None)

    def get_strongs_ref(self, strongs_num: str) -> StrongsReference:
        """Get or create a StrongsReference object"""
        # Ensure 4-digit zero-padding (G0025 format)
        if strongs_num.startswith('G') or strongs_num.startswith('H'):
            prefix = strongs_num[0]
            number = strongs_num[1:]
            strongs_num = f"{prefix}{int(number):04d}"

        if self.strongs_data[strongs_num] is None:
            self.strongs_data[strongs_num] = StrongsReference(strongs_num)
        return self.strongs_data[strongs_num]

    def parse_greek_file(self, url: str):
        """Parse a Greek NT XML file"""
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        current_verses = []

        for elem in root.iter():
            if elem.tag == 'milestone' and elem.get('unit') == 'verse':
                verse_id = elem.get('id')
                if verse_id:
                    current_verses.append(verse_id)
                    if len(current_verses) > 3:
                        current_verses = current_verses[-3:]

            if elem.tag == 'w':
                strong = elem.get('strong')
                if not strong:
                    continue

                verse_ref = current_verses[-1] if current_verses else 'UNKNOWN'

                # Get the actual Greek word
                word = elem.text if elem.text else ''

                gloss = elem.get('gloss', elem.get('english', ''))
                lemma = elem.get('lemma', '')
                morph = elem.get('morph', '')
                domain = elem.get('domain', '')
                ln = elem.get('ln', '')

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

                # Handle compound Strong's numbers (e.g., "1537+4053")
                strongs_numbers = strong.split('+')
                for snum in strongs_numbers:
                    ref = self.get_strongs_ref(f"G{snum}")
                    ref.add_word(verse_ref, word, gloss, '', domain, ln, morph, grammar)

        print(f"  Parsed Greek file")

    def parse_hebrew_file(self, url: str):
        """Parse a Hebrew OT XML file"""
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        current_verse = None

        for elem in root.iter():
            if elem.tag == 'milestone' and elem.get('unit') == 'verse':
                verse_id = elem.get('id')
                if verse_id:
                    current_verse = verse_id

            if elem.tag == 'w':
                strong = elem.get('strongnumberx')
                if not strong:
                    continue

                verse_ref = current_verse if current_verse else 'UNKNOWN'

                # Get the actual Hebrew word
                word = elem.get('unicode', elem.text if elem.text else '')

                gloss = elem.get('english', elem.get('mandarin', ''))
                lemma = elem.get('lemma', '')
                morph = elem.get('morph', '')
                sense = elem.get('sensenumber', '')
                domain = elem.get('lexdomain', '')

                grammar = {
                    'lemma': lemma,
                    'gender': elem.get('gender', ''),
                    'number': elem.get('number', ''),
                    'stem': elem.get('stem', ''),
                    'person': elem.get('person', ''),
                    'state': elem.get('state', ''),
                    'pos': elem.get('pos', ''),
                }

                # Handle compound Strong's numbers (e.g., "1254+4053")
                strongs_numbers = strong.split('+')
                for snum in strongs_numbers:
                    ref = self.get_strongs_ref(f"H{snum}")
                    ref.add_word(verse_ref, word, gloss, sense, domain, '', morph, grammar)

        print(f"  Parsed Hebrew file")

    def fetch_and_parse_all(self):
        """Fetch and parse all files from both repositories"""
        # Fetch Greek files
        print("\n" + "=" * 70)
        print("GREEK NEW TESTAMENT")
        print("=" * 70)
        response = requests.get(GREEK_API_URL)
        response.raise_for_status()
        greek_files = response.json()

        for file_info in greek_files:
            if file_info['name'].endswith('.xml') and not file_info['name'].startswith('sblgnt'):
                try:
                    self.parse_greek_file(file_info['download_url'])
                    time.sleep(0.5)  # Be nice to GitHub
                except Exception as e:
                    print(f"  Error parsing {file_info['name']}: {e}")

        # Fetch Hebrew files
        print("\n" + "=" * 70)
        print("HEBREW OLD TESTAMENT")
        print("=" * 70)
        response = requests.get(HEBREW_API_URL)
        response.raise_for_status()
        hebrew_files = response.json()

        for file_info in hebrew_files:
            if file_info['name'].endswith('.xml'):
                try:
                    self.parse_hebrew_file(file_info['download_url'])
                    time.sleep(0.5)  # Be nice to GitHub
                except Exception as e:
                    print(f"  Error parsing {file_info['name']}: {e}")

    def write_yaml_files(self, output_base_dir: str):
        """Write YAML files for each Strong's number"""
        print("\n" + "=" * 70)
        print(f"Writing YAML files to {output_base_dir}...")
        print("=" * 70)

        count = 0
        for strongs_num, ref_obj in sorted(self.strongs_data.items()):
            if ref_obj is None:
                continue

            dir_path = os.path.join(output_base_dir, strongs_num)
            os.makedirs(dir_path, exist_ok=True)

            file_path = os.path.join(dir_path, f"{strongs_num}.references.yaml")
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(ref_obj.to_dict(), f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            count += 1
            if count % 100 == 0:
                print(f"  Written {count} files...")

        print(f"  Complete! Written {count} files total.")


def main():
    """Main execution function"""
    parser = MaculaParser()

    print("=" * 70)
    print("Building Strong's Dictionary References - Full Bible")
    print("=" * 70)

    # Fetch and parse all files
    parser.fetch_and_parse_all()

    # Write output files
    output_dir = '/home/user/context-grounded-bible/bible/words/strongs'
    parser.write_yaml_files(output_dir)

    print("\n" + "=" * 70)
    print(f"COMPLETE! Processed {len(parser.strongs_data)} Strong's numbers")
    print("=" * 70)


if __name__ == '__main__':
    main()
