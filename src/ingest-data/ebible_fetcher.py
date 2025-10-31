"""eBible corpus integration for fetching verses from local corpus files.

This module provides access to the eBible corpus (https://github.com/BibleNLP/ebible)
which contains 1,000+ Bible translations in various languages.
"""

import os
from pathlib import Path
from typing import Dict, Optional

from ..constants.bible import get_all_verses, parse_verse_ref
from ..util.cache import fetch_verse_from_cache

CACHE_ROOT = Path('data/commentary/commentary')

class EbibleFetchError(Exception):
    """Exception raised when eBible fetching fails."""
    pass


def _fetch_and_structure_verse(book: str, chapter: int, verse: int) -> Dict:
    """
    Fetch verse from eBible and structure it according to SCHEMA.md.
    
    This is an internal function that adds metadata (verse ref, sources, license)
    to the raw translations data before caching.
    
    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        
    Returns:
        Dictionary with SCHEMA.md structure including verse, translations, sources, license
    """
    # Fetch raw translations
    translations = fetch_verse_from_ebible(book, chapter, verse)
    
    # Detect verse ranges and create appropriate notes
    verse_range_translations = []
    processed_translations = {}
    
    for trans_id, text in translations.items():
        if text == '<range>':
            # This verse is part of a range - text is in previous verse
            verse_range_translations.append(trans_id)
            # Format the note according to cross-referencing standards
            prev_verse = verse - 1
            if prev_verse > 0:
                processed_translations[trans_id] = f"@see-verse:{book}.{chapter:03d}.{prev_verse:03d}"
            else:
                # Edge case: verse 1 marked as range (shouldn't happen but handle it)
                processed_translations[trans_id] = '<range>'
        else:
            processed_translations[trans_id] = text
    
    # Build the YAML structure
    verse_data = {
        'verse': f"{book}.{chapter:03d}.{verse:03d}",
        'translations': processed_translations,
        'sources': [
            {
                'url': 'https://github.com/BibleNLP/ebible/tree/main',
                'description': 'eBible corpus - 1000+ Bible translations'
            }
        ],
        'license': [
            {
                'url': 'https://github.com/BibleNLP/ebible/tree/main/metadata/licenses',
                'note': 'Individual translation licenses vary - see metadata'
            }
        ]
    }
    
    # Add metadata note if verse ranges detected
    if verse_range_translations:
        verse_data['metadata'] = {
            'verse_range_translations': verse_range_translations,
            'note': f"{len(verse_range_translations)} translation(s) use verse ranges - text appears in previous verse"
        }
    
    return verse_data


def fetch_verses_from_ebible(book: str, chapter: int, verse: int,
                use_cache: bool = True) -> Dict:
    """
    Fetch verse from eBible with caching support.

    This is a convenience function that integrates with the existing cache system.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        use_cache: Whether to use cache (default: True)

    Returns:
        Dictionary containing verse data following SCHEMA.md structure

    Example:
        >>> verse_data = fetch_verses_from_ebible("MAT", 5, 3)
        >>> print(f"Found {len(verse_data['translations'])} translations")
        Found 1079 translations
    """

    # Check cache first if enabled
    if use_cache:
        return fetch_verse_from_cache(book, chapter, verse, suffix="translations-ebible", onMissing=_fetch_and_structure_verse, cache_root=CACHE_ROOT) 

    else:
        return _fetch_and_structure_verse(book, chapter, verse)

def get_ebible_dir() -> Optional[Path]:
    """
    Get the eBible directory path from environment or default location.

    Returns:
        Path to eBible directory, or None if not found
    """
    # Try environment variable first
    ebible_dir = os.environ.get('EBIBLE_DIR')
    if ebible_dir:
        path = Path(ebible_dir)
        if path.exists():
            return path

    # Check /tmp/ebible first. If it looks valid, use it.
    tmp_path = Path('/tmp/ebible')
    corpus_dir = tmp_path / 'corpus'
    vref_file = tmp_path / 'metadata' / 'vref.txt'
    if tmp_path.exists() and corpus_dir.exists() and vref_file.exists():
        return tmp_path

    # If not, attempt to clone the repo
    import subprocess

    repo_url = "https://github.com/BibleNLP/ebible.git"
    try:
        # Clone if /tmp/ebible doesn't exist or is invalid
        if not tmp_path.exists() or not corpus_dir.exists() or not vref_file.exists():
            # Remove incomplete clone if necessary
            if tmp_path.exists():
                import shutil
                shutil.rmtree(str(tmp_path))
            subprocess.check_call([
                "git", "clone", "--depth", "1", repo_url, str(tmp_path)
            ])
        # Check again after clone
        if tmp_path.exists() and corpus_dir.exists() and vref_file.exists():
            return tmp_path
    except Exception as e:
        pass  # Let the code fall through to try default locations and error at the end

    raise EbibleFetchError("eBible directory not found. Set EBIBLE_DIR environment variable.")


def ebible_available() -> bool:
    """
    Check if eBible corpus is available.

    Returns:
        True if eBible corpus can be accessed, False otherwise
    """
    ebible_dir = get_ebible_dir()
    if not ebible_dir:
        return False

    corpus_dir = ebible_dir / 'corpus'
    vref_file = ebible_dir / 'metadata' / 'vref.txt'

    return corpus_dir.exists() and vref_file.exists()


def normalize_ebible_code(translation_id: str) -> str:
    """
    Normalize eBible corpus translation IDs to our standard format.
    
    eBible corpus uses redundant language prefixes in filenames:
    - eng-engBBE → eng-BBE
    - spa-spaRV1909 → spa-RV-1909  
    - deu-deuELB → deu-ELB
    
    Args:
        translation_id: Raw translation ID from corpus filename
        
    Returns:
        Normalized translation code
        
    Example:
        >>> normalize_ebible_code("eng-engBBE")
        'eng-BBE'
        >>> normalize_ebible_code("spa-spaRV1909")
        'spa-RV-1909'
    """
    parts = translation_id.split('-', 1)
    if len(parts) != 2:
        return translation_id
    
    lang, version = parts
    
    # Remove redundant language prefix from version
    # e.g., "engBBE" → "BBE", "spaRV1909" → "RV1909"
    if version.lower().startswith(lang.lower()):
        version = version[len(lang):]
    
    # If version is empty after removing prefix, keep original
    if not version:
        return translation_id
    
    # Uppercase the version code
    version = version.upper()
    
    # Separate year if present (e.g., "RV1909" → "RV-1909")
    # Look for 4-digit year at the end
    import re
    match = re.search(r'^([A-Z]+)(\d{4})$', version)
    if match:
        version_part, year = match.groups()
        version = f"{version_part}-{year}"
    
    return f"{lang}-{version}"


def get_verse_line_number(book: str, chapter: int, verse: int, vref_file: Path) -> int:
    """
    Get the line number for a verse from vref.txt.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        vref_file: Path to vref.txt

    Returns:
        Line number (1-based) in corpus files

    Raises:
        EbibleFetchError: If verse not found in vref.txt
    """
    verse_ref = f"{book} {chapter}:{verse}"

    try:
        with open(vref_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                if line.strip() == verse_ref:
                    return line_num
    except IOError as e:
        raise EbibleFetchError(f"Failed to read vref.txt: {e}")

    raise EbibleFetchError(f"Verse not found in vref.txt: {verse_ref}")


def fetch_verse_from_ebible(book: str, chapter: int, verse: int) -> Dict[str, str]:
    """
    Fetch verse from eBible corpus.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number

    Returns:
        Dictionary mapping translation codes to verse text

    Raises:
        EbibleFetchError: If eBible not available or verse fetch fails

    Example:
        >>> translations = fetch_verse_from_ebible("JHN", 3, 16)
        >>> len(translations) > 1000  # Should get 1000+ translations
        True
    """
    # Check if eBible is available
    ebible_dir = get_ebible_dir()
    if ebible_dir is None:
        raise EbibleFetchError("eBible directory not found or not configured")
    
    corpus_dir = ebible_dir / 'corpus'
    vref_file = ebible_dir / 'metadata' / 'vref.txt'

    if not corpus_dir.exists():
        raise EbibleFetchError(f"Corpus directory not found: {corpus_dir}")

    if not vref_file.exists():
        raise EbibleFetchError(f"vref.txt not found: {vref_file}")

    # Get line number for this verse
    line_num = get_verse_line_number(book, chapter, verse, vref_file)

    # Extract verse from all corpus files
    translations = {}

    for corpus_file in corpus_dir.glob('*.txt'):
        # Get translation ID from filename (e.g., eng-engBBE from eng-engBBE.txt)
        raw_translation_id = corpus_file.stem
        
        # Normalize to our standard format (eng-engBBE → eng-BBE)
        translation_id = normalize_ebible_code(raw_translation_id)

        try:
            # Read the specific line (line_num is 1-based, but we need 0-based index)
            with open(corpus_file, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, start=1):
                    if i == line_num:
                        verse_text = line.strip()
                        # Only add non-empty verses
                        if verse_text:
                            translations[translation_id] = verse_text
                        break
        except IOError:
            # Skip files that can't be read
            continue

    if not translations:
        raise EbibleFetchError(f"No translations found for {book} {chapter}:{verse}")

    return translations

def main():
    bible_verses = get_all_verses()
    print(f"Total verses to fetch: {len(bible_verses)}")
    for verse in bible_verses:
        book, chapter, verse_num = parse_verse_ref(verse)
        if not (book and chapter and verse_num):
            print(f"Skipping invalid verse entry: {verse}")
            continue
        print(f"Fetching {book} {chapter}:{verse_num} from eBible...")
        try:
            verse_data = fetch_verses_from_ebible(book, chapter, verse_num)
            translations_count = len(verse_data.get('translations', {}))
            print(f"  Found {translations_count} translations.")
        except EbibleFetchError as e:
            print(f"  Error fetching {book} {chapter}:{verse_num}: {e}")


if __name__ == "__main__":
    main()

