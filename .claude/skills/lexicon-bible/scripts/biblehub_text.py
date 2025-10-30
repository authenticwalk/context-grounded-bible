"""BibleHub text/manuscript page parser.

This module fetches and parses BibleHub's text pages to extract
textual variants across multiple Greek and Hebrew manuscript traditions.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

# Handle both relative imports (when used as module) and direct imports (when run as script)
try:
    from .biblehub_urls import TEXT_URL_TEMPLATE, REQUEST_TIMEOUT
    from .book_codes import get_biblehub_book_name
except ImportError:
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from biblehub_urls import TEXT_URL_TEMPLATE, REQUEST_TIMEOUT
    from book_codes import get_biblehub_book_name


class TextFetchError(Exception):
    """Exception raised when text fetching fails."""
    pass


def fetch_text_variants(book: str, chapter: int, verse: int) -> List[Dict]:
    """
    Fetch textual variants from BibleHub text page.

    The text page shows the same verse across multiple manuscript traditions:
    - Nestle 1904
    - Westcott and Hort 1881
    - Westcott and Hort with NA27/UBS4 variants
    - RP Byzantine Majority Text 2005
    - Greek Orthodox Church
    - Tischendorf 8th Edition
    - Scrivener's Textus Receptus 1894
    - Stephanus Textus Receptus 1550

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number

    Returns:
        List of manuscript dictionaries with text and variants

    Raises:
        TextFetchError: If fetching or parsing fails

    Example:
        >>> variants = fetch_text_variants("MAT", 5, 3)
        >>> variants[0]['name']
        'Nestle 1904'
        >>> len(variants) > 5
        True
    """
    try:
        book_name = get_biblehub_book_name(book)
    except ValueError as e:
        raise TextFetchError(f"Invalid book code '{book}': {e}")

    url = TEXT_URL_TEMPLATE.format(
        book=book_name,
        chapter=chapter,
        verse=verse
    )

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except requests.Timeout:
        raise TextFetchError(f"Request timed out after {REQUEST_TIMEOUT}s: {url}")
    except requests.HTTPError as e:
        raise TextFetchError(f"HTTP error {e.response.status_code}: {url}")
    except requests.RequestException as e:
        raise TextFetchError(f"Failed to download from BibleHub: {e}")

    try:
        variants = parse_text_html(response.text)
    except Exception as e:
        raise TextFetchError(f"Failed to parse HTML: {e}")

    if not variants:
        raise TextFetchError(f"No text variants found for {book} {chapter}:{verse}")

    return variants


def parse_text_html(html_content: str) -> List[Dict]:
    """
    Parse BibleHub text HTML to extract manuscript variants.

    The text page displays multiple manuscript traditions in this structure:
    <span class="versiontext"><a href="...">MANUSCRIPT NAME</a></span>
    <span class="greek">Greek text...</span>

    Args:
        html_content: HTML content from text page

    Returns:
        List of manuscript dictionaries

    Example:
        >>> html = '<html>...</html>'
        >>> variants = parse_text_html(html)
        >>> len(variants) > 0
        True
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    variants = []

    # Find all version text spans that contain manuscript names
    version_spans = soup.find_all('span', class_='versiontext')

    for version_span in version_spans:
        # Extract manuscript name from the link
        link = version_span.find('a')
        if not link:
            continue

        manuscript_name = link.get_text(strip=True)

        # Filter to just manuscript names (not other Bible versions)
        # Look for Greek/Hebrew manuscript indicators
        if not any(keyword in manuscript_name.lower() for keyword in [
            'nestle', 'westcott', 'hort', 'byzantine', 'majority',
            'tischendorf', 'scrivener', 'stephanus', 'textus receptus',
            'greek orthodox', 'hebrew bible', 'masoretic', 'aramaic', 'peshitta'
        ]):
            continue

        # Clean up manuscript name (remove book/verse prefix)
        # E.g., "ΚΑΤΑ ΜΑΤΘΑΙΟΝ 5:3 Greek NT: Nestle 1904" -> "Nestle 1904"
        if ':' in manuscript_name and 'Greek NT:' in manuscript_name:
            manuscript_name = manuscript_name.split('Greek NT:')[-1].strip()
        elif ':' in manuscript_name and 'Hebrew Bible' in manuscript_name:
            manuscript_name = 'Hebrew Bible'
        elif 'Aramaic NT' in manuscript_name:
            manuscript_name = manuscript_name.split('Aramaic NT:')[-1].strip()

        # Find the next span with Greek/Hebrew/Aramaic text
        # It's usually a sibling or close following span
        current = version_span

        # Try to find the text span (could be next sibling or in next <p>)
        text_span = None
        for _ in range(5):  # Look ahead max 5 elements
            current = current.find_next(['span', 'p'])
            if not current:
                break

            # Check if this span contains the text we want
            if current.name == 'span' and current.get('class'):
                classes = current.get('class', [])
                if any(cls in ['greek', 'hebrew', 'heb', 'aramaic'] for cls in classes):
                    text_span = current
                    break

            # Or if it's a <p> containing such a span
            if current.name == 'p':
                inner_span = current.find('span', class_=['greek', 'hebrew', 'heb', 'aramaic'])
                if inner_span:
                    text_span = inner_span
                    break

        if not text_span:
            continue

        text = text_span.get_text(strip=True)

        # Clean up the text
        text = ' '.join(text.split())

        # Skip if text is too short (probably not the actual verse)
        if len(text) < 5:
            continue

        variant = {
            'name': manuscript_name,
            'text': text
        }

        variants.append(variant)

    return variants


def extract_variant_notes(element) -> Optional[str]:
    """
    Extract variant notes from a manuscript text element.

    Variant notes might be in:
    - Parentheses
    - Square brackets
    - Special span elements

    Args:
        element: BeautifulSoup element containing the text

    Returns:
        Variant notes string or None
    """
    text = element.get_text()

    # Look for common variant notation patterns
    notes = []

    # Parenthetical notes
    paren_matches = re.findall(r'\([^)]+\)', text)
    notes.extend(paren_matches)

    # Bracketed notes
    bracket_matches = re.findall(r'\[[^\]]+\]', text)
    notes.extend(bracket_matches)

    # Look for specific variant spans or notes
    variant_spans = element.find_all('span', class_=['variant', 'note'])
    for span in variant_spans:
        note_text = span.get_text(strip=True)
        if note_text:
            notes.append(note_text)

    return '; '.join(notes) if notes else None


def main():
    """Test the text variants fetcher with sample verses."""
    print("BibleHub Text Variants Fetcher Test")
    print("=" * 80)
    print()

    test_verses = [
        ("MAT", 5, 3, "Matthew 5:3 - Blessed are the poor in spirit"),
        ("JHN", 3, 16, "John 3:16 - For God so loved the world"),
        ("JHN", 1, 1, "John 1:1 - In the beginning was the Word"),
    ]

    for book, chapter, verse, description in test_verses:
        print(f"\n{description}")
        print(f"Reference: {book} {chapter}:{verse}")
        print("-" * 80)

        try:
            variants = fetch_text_variants(book, chapter, verse)

            print(f"✓ Found {len(variants)} manuscript traditions\n")

            for variant in variants:
                print(f"{variant['name']}:")
                text = variant['text']
                # Truncate long text for display
                display_text = text if len(text) <= 100 else text[:97] + "..."
                print(f"  {display_text}")

                if 'notes' in variant:
                    print(f"  Notes: {variant['notes']}")

                print()

        except TextFetchError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    print("=" * 80)
    print("Test complete!")


if __name__ == "__main__":
    main()
