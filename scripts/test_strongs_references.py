#!/usr/bin/env python3
"""
Test version: Build Strong's dictionary reference files from a small sample.
"""

import xml.etree.ElementTree as ET
import requests
import yaml
import os
from collections import defaultdict
from typing import Dict

# Test with just a couple of files
TEST_GREEK_FILES = [
    "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/SBLGNT/lowfat/02-mark.xml"
]

TEST_HEBREW_FILES = [
    "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/WLC/lowfat/01-Gen-001-lowfat.xml"
]


class StrongsReference:
    """Collects all references for a Strong's number"""

    def __init__(self, strongs_num: str):
        self.strongs_num = strongs_num
        self.meanings = defaultdict(lambda: defaultdict(list))
        self.forms = defaultdict(lambda: defaultdict(lambda: None))

    def add_word(self, verse_ref: str, gloss: str, sense: str, morph: str, grammar: Dict[str, str]):
        """Add a word occurrence to this Strong's number"""
        meaning_key = sense if sense else gloss

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

        for meaning, verses in sorted(self.meanings.items()):
            result['meanings'][meaning] = sorted(verses.keys())

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
                gloss = elem.get('gloss', elem.get('english', ''))
                lemma = elem.get('lemma', '')
                morph = elem.get('morph', '')

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

                ref = self.get_strongs_ref(f"G{strong}")
                ref.add_word(verse_ref, gloss, '', morph, grammar)

        print(f"  Parsed {len([e for e in root.iter() if e.tag == 'w'])} words")

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
                gloss = elem.get('english', elem.get('mandarin', ''))
                lemma = elem.get('lemma', '')
                morph = elem.get('morph', '')
                sense = elem.get('sensenumber', '')

                grammar = {
                    'lemma': lemma,
                    'gender': elem.get('gender', ''),
                    'number': elem.get('number', ''),
                    'stem': elem.get('stem', ''),
                    'person': elem.get('person', ''),
                    'state': elem.get('state', ''),
                    'pos': elem.get('pos', ''),
                }

                ref = self.get_strongs_ref(f"H{strong}")
                ref.add_word(verse_ref, gloss, sense, morph, grammar)

        print(f"  Parsed {len([e for e in root.iter() if e.tag == 'w'])} words")

    def write_yaml_files(self, output_base_dir: str):
        """Write YAML files for each Strong's number"""
        print(f"\nWriting YAML files to {output_base_dir}...")

        for strongs_num, ref_obj in self.strongs_data.items():
            if ref_obj is None:
                continue

            dir_path = os.path.join(output_base_dir, strongs_num)
            os.makedirs(dir_path, exist_ok=True)

            file_path = os.path.join(dir_path, f"{strongs_num}-references.yaml")
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(ref_obj.to_dict(), f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            print(f"  Written: {file_path}")


def main():
    """Main execution function"""
    parser = MaculaParser()

    print("=" * 70)
    print("Testing Strong's Dictionary References Builder")
    print("=" * 70)

    # Parse test files
    for url in TEST_GREEK_FILES:
        parser.parse_greek_file(url)

    for url in TEST_HEBREW_FILES:
        parser.parse_hebrew_file(url)

    # Write output files
    output_dir = '/home/user/context-grounded-bible/bible/words/strongs'
    parser.write_yaml_files(output_dir)

    print("\n" + "=" * 70)
    print(f"Test Complete! Processed {len(parser.strongs_data)} Strong's numbers")
    print("=" * 70)

    # Show a sample output
    if parser.strongs_data:
        sample_key = list(parser.strongs_data.keys())[0]
        sample_ref = parser.strongs_data[sample_key]
        print(f"\nSample Strong's number: {sample_key}")
        print(f"Meanings: {len(sample_ref.meanings)}")
        print(f"Forms: {len(sample_ref.forms)}")


if __name__ == '__main__':
    main()
