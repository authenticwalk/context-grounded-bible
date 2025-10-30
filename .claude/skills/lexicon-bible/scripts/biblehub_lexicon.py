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


def fetch_lexicon_data(book: str, chapter: int, verse: int) -> List[Dict]:
    """
    Fetch lexicon data from BibleHub lexicon page.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number

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

    return words


def parse_lexicon_html(html_content: str) -> List[Dict]:
    """
    Parse BibleHub lexicon HTML to extract word-level lexical data.

    The lexicon page shows each word in a table with:
    - NASB translation
    - Original language text + transliteration
    - Strong's number + gloss
    - Etymology/origin

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

    # Find the main lexicon table
    # Look for table with class="maintext"
    table = soup.find('table', {'class': 'maintext'})

    if not table:
        return words

    # Find all data rows (skip header row)
    rows = table.find_all('tr')

    # First row is usually headers, skip it
    data_rows = [row for row in rows if row.find('td', {'class': 'eng'})]

    for idx, row in enumerate(data_rows, 1):
        try:
            word_data = extract_word_from_table_row(row, idx)
            if word_data:
                words.append(word_data)
        except Exception as e:
            # Skip words that fail to parse
            print(f"Warning: Failed to parse word {idx}: {e}", file=sys.stderr)
            continue

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

                if 'parsing_code' in word:
                    print(f"  Parsing: {word['parsing_code']}")

                if 'parsing' in word and word['parsing']:
                    from parsing_codes import format_parsing_display
                    print(f"  Grammar: {format_parsing_display(word['parsing'])}")

                if 'gloss' in word:
                    print(f"  Gloss: {word['gloss']}")

                if 'definition' in word:
                    print(f"  Definition: {word['definition']}")

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
