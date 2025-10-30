#!/usr/bin/env python3
"""
Test version: Build Strong's dictionary reference files from Matthew 5 only.
"""

import xml.etree.ElementTree as ET
import requests
import yaml
import os
from collections import defaultdict
from typing import Dict


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

    def parse_greek_file_chapter(self, url: str, chapter_filter: int = None):
        """Parse a Greek NT XML file, optionally filtering to one chapter"""
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        current_verses = []
        in_target_chapter = True

        for elem in root.iter():
            if elem.tag == 'milestone' and elem.get('unit') == 'verse':
                verse_id = elem.get('id')
                if verse_id:
                    # Check if we're in the right chapter
                    if chapter_filter is not None:
                        # verse_id format: "MAT 5:1"
                        parts = verse_id.split()
                        if len(parts) == 2:
                            ch_verse = parts[1].split(':')
                            if len(ch_verse) == 2:
                                ch = int(ch_verse[0])
                                if ch != chapter_filter:
                                    in_target_chapter = False
                                    continue
                                else:
                                    in_target_chapter = True

                    current_verses.append(verse_id)
                    if len(current_verses) > 3:
                        current_verses = current_verses[-3:]

            if elem.tag == 'w' and in_target_chapter:
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

        print(f"  Parsed Matthew 5")

    def write_yaml_files(self, output_base_dir: str):
        """Write YAML files for each Strong's number"""
        print(f"\nWriting YAML files to {output_base_dir}...")

        for strongs_num, ref_obj in sorted(self.strongs_data.items()):
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
    print("Testing Strong's Dictionary References Builder - Matthew 5 Only")
    print("=" * 70)

    # Parse Matthew, chapter 5 only
    parser.parse_greek_file_chapter(
        "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/SBLGNT/lowfat/01-matthew.xml",
        chapter_filter=5
    )

    # Write output files
    output_dir = '/home/user/context-grounded-bible/bible/words/strongs'
    parser.write_yaml_files(output_dir)

    print("\n" + "=" * 70)
    print(f"Test Complete! Processed {len(parser.strongs_data)} Strong's numbers from Matthew 5")
    print("=" * 70)


if __name__ == '__main__':
    main()
