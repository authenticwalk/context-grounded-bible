"""BibleHub Strong's Concordance page parser.

This module fetches and parses Strong's concordance pages from BibleHub
to extract:
- Usage frequency and occurrence counts
- Extended definitions
- Semantic domain categories
- All biblical references where the word appears
- Cognate information

Usage:
    from biblehub_strongs import fetch_strongs_data

    data = fetch_strongs_data("H7225")  # Hebrew word
    data = fetch_strongs_data("G26")    # Greek word
"""

import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import requests

from cache_manager import CacheManager


class StrongsFetchError(Exception):
    """Exception raised when fetching Strong's data fails."""
    pass


def fetch_strongs_html(strongs_number: str) -> str:
    """Fetch HTML content for a Strong's number.

    Args:
        strongs_number: Strong's number (e.g., "H7225", "G26")

    Returns:
        HTML content as string

    Raises:
        StrongsFetchError: If fetching fails
    """
    # Determine language (Hebrew or Greek)
    if strongs_number.startswith('H'):
        lang = 'hebrew'
        number = strongs_number[1:]  # Remove 'H' prefix
    elif strongs_number.startswith('G'):
        lang = 'greek'
        number = strongs_number[1:]  # Remove 'G' prefix
    else:
        raise StrongsFetchError(f"Invalid Strong's number format: {strongs_number}")

    # Remove letter suffixes (e.g., H1254a -> 1254)
    number = number.rstrip('abcdefghijklmnopqrstuvwxyz')

    url = f"https://biblehub.com/{lang}/{number}.htm"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise StrongsFetchError(f"Failed to fetch {url}: {e}")


def parse_usage_frequency(soup: BeautifulSoup) -> Optional[Dict]:
    """Extract usage frequency data from Strong's page.

    Args:
        soup: BeautifulSoup object of the page

    Returns:
        Dictionary with frequency data or None if not found
    """
    # Look for occurrence count in the page
    # Pattern: "XX Occurrences" or "X Occurrence"
    text = soup.get_text()

    # Find total occurrence count
    occurrence_match = re.search(r'(\d+)\s+Occurrence[s]?', text)
    if not occurrence_match:
        return None

    total_count = int(occurrence_match.group(1))

    result = {
        'total_occurrences': total_count,
        'forms': {}
    }

    # Try to find form breakdown
    # Pattern: "word_form (XX times)" or "word_form — XX"
    form_pattern = re.compile(r'([א-ת\u0590-\u05FF\w\u0370-\u03FF·]+)\s*[—\(]\s*(\d+)\s*(?:times?|\))')

    for match in form_pattern.finditer(text):
        form = match.group(1).strip()
        count = int(match.group(2))
        result['forms'][form] = count

    return result


def parse_extended_definition(soup: BeautifulSoup) -> Optional[str]:
    """Extract full definition from Strong's page.

    Args:
        soup: BeautifulSoup object of the page

    Returns:
        Extended definition string or None
    """
    # Look for definition in common locations

    # Try the main definition paragraph
    # Usually in a div with class containing 'definition' or under specific heading

    # Pattern 1: Look for "Englishman's Concordance" section or "Strong's Exhaustive Concordance"
    headings = soup.find_all(['h2', 'h3', 'h4'])

    for heading in headings:
        heading_text = heading.get_text(strip=True)

        if "Strong's Exhaustive Concordance" in heading_text or "Definition" in heading_text:
            # Get the next paragraph or div
            next_elem = heading.find_next_sibling()
            if next_elem:
                definition = next_elem.get_text(strip=True)
                # Clean up the definition
                if definition and len(definition) > 10:  # Reasonable definition length
                    return definition

    # Pattern 2: Look for specific div classes
    for div_class in ['strongs', 'lexicon', 'definition']:
        divs = soup.find_all('div', class_=re.compile(div_class, re.I))
        for div in divs:
            text = div.get_text(strip=True)
            if text and len(text) > 20 and len(text) < 1000:
                return text

    # Pattern 3: Search for definition after "Definition:" label in full page text
    page_text = soup.get_text()
    def_match = re.search(r'Definition:\s*(.+?)(?:\n|$|Strong\'s)', page_text, re.DOTALL)
    if def_match:
        return def_match.group(1).strip()

    return None


def parse_semantic_categories(soup: BeautifulSoup) -> List[str]:
    """Extract semantic domain categories from occurrence groupings.

    Args:
        soup: BeautifulSoup object of the page

    Returns:
        List of semantic category names
    """
    categories = []

    # Look for section headings that group occurrences thematically
    # These are often in h3 or h4 tags with specific patterns

    headings = soup.find_all(['h3', 'h4'])

    for heading in headings:
        heading_text = heading.get_text(strip=True)

        # Skip navigation/structural headings
        skip_patterns = [
            'Concordance',
            'Lexicon',
            'Strong',
            'Interlinear',
            'Parallel',
            'Commentary',
            'Treasury',
            'Topical',
            'Library',
            'Resources'
        ]

        if any(pattern in heading_text for pattern in skip_patterns):
            continue

        # Look for thematic headings (usually contain colon or are title-cased phrases)
        if ':' in heading_text or (len(heading_text.split()) >= 2 and heading_text[0].isupper()):
            # Clean up the category name
            category = heading_text.replace(':', '').strip()
            if category and len(category) < 100:  # Reasonable category length
                categories.append(category)

    return list(set(categories))  # Remove duplicates


def parse_occurrence_list(soup: BeautifulSoup, strongs_number: str) -> List[str]:
    """Extract list of all biblical references where word occurs.

    Args:
        soup: BeautifulSoup object of the page
        strongs_number: Strong's number for context

    Returns:
        List of verse references (e.g., ["GEN 1:1", "GEN 10:10", ...])
    """
    occurrences = []

    # Look for links to biblical references
    # Pattern: links to /.../{book}/{chapter}-{verse}.htm

    links = soup.find_all('a', href=re.compile(r'/(hebrew|greek)/\d+(-\d+)?\.htm'))

    for link in links:
        href = link.get('href')
        # Extract reference from href like /hebrew/7225-1.htm or from link text

        # Better approach: look for actual verse references in text
        verse_ref = link.get_text(strip=True)

        # Match patterns like "Genesis 1:1", "Exo 12:3", etc.
        ref_pattern = re.compile(r'([A-Z][a-z]+(?:\s+\d)?)\s+(\d+):(\d+)')
        match = ref_pattern.match(verse_ref)

        if match:
            book_name = match.group(1)
            chapter = match.group(2)
            verse = match.group(3)

            # Convert book name to USFM code (would need book_codes.py)
            # For now, store as-is
            occurrences.append(f"{book_name} {chapter}:{verse}")

    return list(set(occurrences))  # Remove duplicates


def parse_cognates(soup: BeautifulSoup) -> List[Dict]:
    """Extract cognate information.

    Args:
        soup: BeautifulSoup object of the page

    Returns:
        List of cognate dictionaries
    """
    cognates = []

    text = soup.get_text()

    # Look for Aramaic cognates (common pattern: "from the same as HXXXX")
    aramaic_match = re.search(r'from the same as (H\d+)', text)
    if aramaic_match:
        cognates.append({
            'type': 'root',
            'strongs': aramaic_match.group(1),
            'relationship': 'derived from'
        })

    # Look for other language references
    # Patterns: "Syriac: ...", "Aramaic: ...", etc.
    lang_patterns = {
        'Syriac': r'Syriac:\s*([^\n,.]+)',
        'Aramaic': r'Aramaic:\s*([^\n,.]+)',
        'Chaldean': r'Chaldean:\s*([^\n,.]+)',
    }

    for lang, pattern in lang_patterns.items():
        match = re.search(pattern, text)
        if match:
            cognates.append({
                'type': 'cognate',
                'language': lang,
                'word': match.group(1).strip()
            })

    return cognates


def fetch_strongs_data(strongs_number: str, use_cache: bool = True) -> Dict:
    """Fetch complete Strong's concordance data for a word.

    Args:
        strongs_number: Strong's number (e.g., "H7225", "G26")
        use_cache: Whether to use cached data (default: True)

    Returns:
        Dictionary with all extracted data

    Raises:
        StrongsFetchError: If fetching or parsing fails
    """
    # Check cache first
    cache = CacheManager()

    if use_cache:
        cached = cache.get('strongs', 0, 0, strongs_number)
        if cached:
            return cached

    # Fetch HTML
    html = fetch_strongs_html(strongs_number)
    soup = BeautifulSoup(html, 'html.parser')

    # Parse all data
    result = {
        'strongs': strongs_number,
    }

    # Usage frequency
    frequency = parse_usage_frequency(soup)
    if frequency:
        result['usage_frequency'] = frequency

    # Extended definition
    definition = parse_extended_definition(soup)
    if definition:
        result['extended_definition'] = definition

    # Semantic categories
    categories = parse_semantic_categories(soup)
    if categories:
        result['semantic_categories'] = categories

    # Occurrence list (may be large, make optional)
    # occurrences = parse_occurrence_list(soup, strongs_number)
    # if occurrences:
    #     result['occurrences'] = occurrences

    # Cognates
    cognates = parse_cognates(soup)
    if cognates:
        result['cognates'] = cognates

    # Cache the result
    if use_cache:
        cache.set('strongs', 0, 0, strongs_number, result)

    return result


if __name__ == '__main__':
    # Test with Genesis 1:1 words
    test_numbers = ['H7225', 'H430', 'H1254', 'G26', 'G2316']

    for number in test_numbers:
        print(f"\n{'='*80}")
        print(f"Strong's {number}")
        print('='*80)

        try:
            data = fetch_strongs_data(number, use_cache=False)

            if 'usage_frequency' in data:
                print(f"\nUsage Frequency:")
                freq = data['usage_frequency']
                print(f"  Total: {freq['total_occurrences']} occurrences")
                if freq['forms']:
                    print(f"  Forms: {freq['forms']}")

            if 'extended_definition' in data:
                print(f"\nExtended Definition:")
                print(f"  {data['extended_definition'][:200]}...")

            if 'semantic_categories' in data:
                print(f"\nSemantic Categories:")
                for cat in data['semantic_categories'][:5]:
                    print(f"  - {cat}")

            if 'cognates' in data:
                print(f"\nCognates:")
                for cog in data['cognates']:
                    print(f"  {cog}")

        except StrongsFetchError as e:
            print(f"Error: {e}")
