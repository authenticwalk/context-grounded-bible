"""BibleHub lexicon page parser.

This module fetches and parses BibleHub's lexicon pages to extract
Strong's numbers, morphological parsing, and lexical definitions.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

# Handle both relative imports (when used as module) and direct imports (when run as script)
try:
    from .biblehub_urls import LEXICON_URL_TEMPLATE, REQUEST_TIMEOUT
    from .book_codes import get_biblehub_book_name
    from .parsing_codes import parse_morphology_code
except ImportError:
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from biblehub_urls import LEXICON_URL_TEMPLATE, REQUEST_TIMEOUT
    from book_codes import get_biblehub_book_name
    from parsing_codes import parse_morphology_code


class LexiconFetchError(Exception):
    """Exception raised when lexicon fetching fails."""
    pass


def fetch_lexicon_data(book: str, chapter: int, verse: int, use_cache: bool = True) -> List[Dict]:
    """
    Fetch lexicon data from BibleHub lexicon page (with caching).

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        use_cache: Whether to use cache (default: True)

    Returns:
        List of word dictionaries with lexical data

    Raises:
        LexiconFetchError: If fetching or parsing fails

    Example:
        >>> words = fetch_lexicon_data("MAT", 5, 3)
        >>> words[0]['strongs']
        'G3107'
        >>> words[0]['original']
        'μακάριοι'
    """
    # Try cache first if enabled
    if use_cache:
        try:
            # Import here to avoid circular dependency
            script_dir = Path(__file__).parent
            sys.path.insert(0, str(script_dir))
            from cache_manager import CacheManager

            cache = CacheManager()
            cached_data = cache.get(book, chapter, verse, 'lexicon')
            if cached_data:
                return cached_data
        except ImportError:
            pass  # Cache not available, continue without it

    try:
        book_name = get_biblehub_book_name(book)
    except ValueError as e:
        raise LexiconFetchError(f"Invalid book code '{book}': {e}")

    url = LEXICON_URL_TEMPLATE.format(
        book=book_name,
        chapter=chapter,
        verse=verse
    )

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except requests.Timeout:
        raise LexiconFetchError(f"Request timed out after {REQUEST_TIMEOUT}s: {url}")
    except requests.HTTPError as e:
        raise LexiconFetchError(f"HTTP error {e.response.status_code}: {url}")
    except requests.RequestException as e:
        raise LexiconFetchError(f"Failed to download from BibleHub: {e}")

    try:
        words = parse_lexicon_html(response.text)
    except Exception as e:
        raise LexiconFetchError(f"Failed to parse HTML: {e}")

    if not words:
        raise LexiconFetchError(f"No lexicon data found for {book} {chapter}:{verse}")

    # Cache the result if caching is enabled
    if use_cache:
        try:
            from cache_manager import CacheManager
            cache = CacheManager()
            cache.set(book, chapter, verse, 'lexicon', words)
        except (ImportError, Exception):
            pass  # Continue without caching if it fails

    return words


def parse_lexicon_html(html_content: str) -> List[Dict]:
    """
    Parse BibleHub lexicon HTML to extract word-level lexical data.

    The lexicon page shows each word in a table with:
    - NASB translation
    - Original language text + transliteration
    - Strong's number + gloss
    - Etymology/origin

    And in the KJV Lexicon section:
    - Morphological parsing (case, gender, number, tense, etc.)

    Args:
        html_content: HTML content from lexicon page

    Returns:
        List of dictionaries, one per word

    Example:
        >>> html = '<html>...</html>'
        >>> words = parse_lexicon_html(html)
        >>> len(words) > 0
        True
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    words = []

    # Find the main lexicon table (NASB Lexicon)
    table = soup.find('table', {'class': 'maintext'})

    if not table:
        return words

    # Find all data rows (skip header row)
    rows = table.find_all('tr')

    # First row is usually headers, skip it
    data_rows = [row for row in rows if row.find('td', {'class': 'eng'})]

    # Extract basic data from NASB table
    for idx, row in enumerate(data_rows, 1):
        try:
            word_data = extract_word_from_table_row(row, idx)
            if word_data:
                words.append(word_data)
        except Exception as e:
            # Skip words that fail to parse
            print(f"Warning: Failed to parse word {idx}: {e}", file=sys.stderr)
            continue

    # Now extract morphological parsing from KJV Lexicon section
    # This section has spans with class="grkitspan" or "hebitspan" containing parsing info
    extract_morphology_from_kjv_section(soup, words)

    return words


def extract_word_from_table_row(row, position: int) -> Optional[Dict]:
    """
    Extract lexical data from a table row in BibleHub's lexicon table.

    Table structure:
    <tr>
      <td class="eng">NASB translation</td>
      <td class="greek2">
        <span="greek3">Original text</span>
        <br />
        <span class="translit">(transliteration)</span>
      </td>
      <td class="strongsnt">
        <a href="...">Strong's number:</a>
        <span class="eng2">gloss</span>
      </td>
      <td class="eng3">etymology/origin</td>
    </tr>

    Args:
        row: BeautifulSoup <tr> element
        position: Word position in verse (1-indexed)

    Returns:
        Dictionary with word data or None if extraction fails
    """
    word_data = {'position': position}

    # Get all cells
    cells = row.find_all('td')

    if len(cells) < 3:
        return None

    # Cell 0: NASB translation
    nasb_cell = cells[0]
    nasb_text = nasb_cell.get_text(strip=True)
    if nasb_text:
        word_data['nasb'] = nasb_text

    # Cell 1: Original language + transliteration
    original_cell = cells[1]

    # Extract original text (Greek or Hebrew)
    # Look for span with class greek3 or similar
    original_text = None
    for attr in ['greek3', 'hebrew3', 'greek2', 'hebrew2']:
        span = original_cell.find('span', attrs=lambda x: x and attr in str(x))
        if span:
            original_text = span.get_text(strip=True)
            break

    # Alternative: just get first text before <br>
    if not original_text:
        text_parts = original_cell.stripped_strings
        first_part = next(text_parts, None)
        if first_part and not first_part.startswith('('):
            original_text = first_part

    if original_text:
        word_data['original'] = original_text

    # Extract transliteration from span with class="translit"
    translit_span = original_cell.find('span', {'class': 'translit'})
    if translit_span:
        translit = translit_span.get_text(strip=True)
        # Remove parentheses if present
        translit = translit.strip('()')
        word_data['transliteration'] = translit

    # Cell 2: Strong's number + gloss
    strongs_cell = cells[2]

    # Extract Strong's number from link
    strongs_link = strongs_cell.find('a', href=re.compile(r'strongsnumbers\.com|/greek/|/hebrew/'))
    if strongs_link:
        strongs_text = strongs_link.get_text(strip=True)
        # Remove colon if present (e.g., "3107:" -> "G3107")
        strongs_num = strongs_text.strip(':')

        # Determine if Greek (NT) or Hebrew (OT) and add prefix
        if not strongs_num.startswith('G') and not strongs_num.startswith('H'):
            # Check URL to determine G or H
            href = strongs_link.get('href', '')
            if '/greek/' in href or 'greek' in href.lower():
                strongs_num = 'G' + strongs_num
            elif '/hebrew/' in href or 'hebrew' in href.lower():
                strongs_num = 'H' + strongs_num

        word_data['strongs'] = strongs_num

    # Extract gloss from span with class="eng2"
    gloss_span = strongs_cell.find('span', {'class': 'eng2'})
    if gloss_span:
        word_data['gloss'] = gloss_span.get_text(strip=True)

    # Cell 3 (if exists): Etymology/origin
    if len(cells) > 3:
        origin_cell = cells[3]
        origin_text = origin_cell.get_text(strip=True)
        if origin_text:
            word_data['origin'] = origin_text

            # Try to extract root from origin (e.g., "from makar" or "from pneō")
            root_match = re.search(r'from\s+([^\s,;.()]+)', origin_text, re.IGNORECASE)
            if root_match:
                word_data['root'] = root_match.group(1).strip()

    return word_data if 'strongs' in word_data else None


def extract_morphology_from_kjv_section(soup, words: List[Dict]) -> None:
    """
    Extract morphological parsing from the KJV Lexicon section.

    The KJV section shows parsing like:
    - "adjective - nominative plural masculine"
    - "verb - present indicative - third person singular"
    - "noun - dative singular neuter"

    This function matches these to the words list by original text.

    Args:
        soup: BeautifulSoup object
        words: List of word dictionaries to enhance with parsing
    """
    # Find the KJV Lexicon section
    kjv_section = soup.find('div', {'id': 'combox'})

    if not kjv_section:
        return

    # Find all bold Greek/Hebrew text spans followed by italic parsing spans
    bold_spans = kjv_section.find_all('span', {'class': ['grkboldspan', 'hebboldspan']})

    for bold_span in bold_spans:
        # Get the original text
        original_text = bold_span.get_text(strip=True)
        if not original_text:
            continue

        # Find the next italic span with parsing info
        next_span = bold_span.find_next_sibling('span', {'class': ['grkitspan', 'hebitspan']})
        if not next_span:
            continue

        parsing_text = next_span.get_text(strip=True)

        # Check if this is a morphological description (not a pronunciation)
        # Morphology contains words like: noun, verb, adjective, article, pronoun, conjunction
        # And grammatical features: nominative, genitive, dative, accusative, singular, plural, etc.
        if not any(keyword in parsing_text.lower() for keyword in [
            'noun', 'verb', 'adjective', 'article', 'pronoun', 'conjunction',
            'preposition', 'particle', 'interjection'
        ]):
            continue

        # Parse the morphology string
        morphology = parse_morphology_description(parsing_text)

        # Find matching word in words list by comparing original text
        for word in words:
            if 'original' in word:
                # Normalize for comparison (remove diacritics/accents might differ)
                word_orig = word['original'].replace('ὶ', 'ι').replace('ὶ', 'ι').replace('̀', '').replace('́', '')
                check_orig = original_text.replace('ὶ', 'ι').replace('ὶ', 'ι').replace('̀', '').replace('́', '')

                if word_orig.lower() == check_orig.lower():
                    word['morphology'] = parsing_text
                    if morphology:
                        word['parsing'] = morphology
                    break


def parse_morphology_description(description: str) -> Optional[Dict]:
    """
    Parse a morphological description string into structured components.

    Input examples:
    - "adjective - nominative plural masculine"
    - "verb - present indicative - third person singular"
    - "noun - dative singular neuter"
    - "definite article - nominative singular feminine"

    Args:
        description: Morphological description string

    Returns:
        Dictionary with parsed components

    Example:
        >>> parse_morphology_description("adjective - nominative plural masculine")
        {'pos': 'adjective', 'case': 'nominative', 'number': 'plural', 'gender': 'masculine'}

        >>> parse_morphology_description("verb - present indicative - third person singular")
        {'pos': 'verb', 'tense': 'present', 'mood': 'indicative', 'person': 'third', 'number': 'singular'}
    """
    if not description:
        return None

    result = {}
    desc_lower = description.lower()

    # Extract part of speech (first word before dash or full description if no dash)
    parts = [p.strip() for p in description.split('-')]

    # Part of speech
    pos_match = re.search(r'\b(noun|verb|adjective|article|pronoun|conjunction|preposition|particle|interjection)\b',
                         desc_lower)
    if pos_match:
        result['pos'] = pos_match.group(1)

    # Case (for nouns, adjectives, pronouns, articles)
    case_match = re.search(r'\b(nominative|genitive|dative|accusative|vocative)\b', desc_lower)
    if case_match:
        result['case'] = case_match.group(1)

    # Gender
    gender_match = re.search(r'\b(masculine|feminine|neuter)\b', desc_lower)
    if gender_match:
        result['gender'] = gender_match.group(1)

    # Number
    number_match = re.search(r'\b(singular|plural)\b', desc_lower)
    if number_match:
        result['number'] = number_match.group(1)

    # Tense (for verbs)
    tense_match = re.search(r'\b(present|imperfect|future|aorist|perfect|pluperfect)\b', desc_lower)
    if tense_match:
        result['tense'] = tense_match.group(1)

    # Voice (for verbs)
    voice_match = re.search(r'\b(active|passive|middle)\b', desc_lower)
    if voice_match:
        result['voice'] = voice_match.group(1)

    # Mood (for verbs)
    mood_match = re.search(r'\b(indicative|subjunctive|optative|imperative|infinitive|participle)\b', desc_lower)
    if mood_match:
        result['mood'] = mood_match.group(1)

    # Person (for verbs)
    person_match = re.search(r'\b(first|second|third)\s+person\b', desc_lower)
    if person_match:
        result['person'] = person_match.group(1)

    return result if result else None


def main():
    """Test the lexicon fetcher with sample verses."""
    print("BibleHub Lexicon Fetcher Test")
    print("=" * 80)
    print()

    test_verses = [
        ("MAT", 5, 3, "Matthew 5:3 - Blessed are the poor in spirit"),
        ("JHN", 3, 16, "John 3:16 - For God so loved the world"),
        ("GEN", 1, 1, "Genesis 1:1 - In the beginning"),
    ]

    for book, chapter, verse, description in test_verses:
        print(f"\n{description}")
        print(f"Reference: {book} {chapter}:{verse}")
        print("-" * 80)

        try:
            words = fetch_lexicon_data(book, chapter, verse)

            print(f"✓ Found {len(words)} words\n")

            for word in words:
                print(f"Word {word['position']}:")
                print(f"  Original: {word.get('original', 'N/A')}")
                print(f"  Transliteration: {word.get('transliteration', 'N/A')}")
                print(f"  Strong's: {word.get('strongs', 'N/A')}")

                if 'morphology' in word:
                    print(f"  Morphology: {word['morphology']}")

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
                        print(f"  Parsing: {', '.join(parsed_parts)}")

                if 'gloss' in word:
                    print(f"  Gloss: {word['gloss']}")

                if 'root' in word:
                    print(f"  Root: {word['root']}")

                print()

        except LexiconFetchError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    print("=" * 80)
    print("Test complete!")


if __name__ == "__main__":
    main()
