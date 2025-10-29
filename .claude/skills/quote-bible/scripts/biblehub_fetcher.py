"""BibleHub HTML parsing for multi-translation pages.

This module provides functions to fetch and parse BibleHub's multi-translation HTML pages
and extract all available Bible translations with their verse text.
"""
import html
import quopri
import re
import sys
from pathlib import Path
from typing import Dict, Union

import requests

# Handle both relative imports (when used as module) and direct imports (when run as script)
try:
    from .biblehub_urls import BIBLEHUB_MULTI_URL_TEMPLATE, REQUEST_TIMEOUT
    from .book_codes import get_biblehub_book_name
    from .version_codes import ALL_VERSION_MAPPINGS, LANGUAGE_PATTERNS
except ImportError:
    # Running as a script, use direct imports
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from biblehub_urls import BIBLEHUB_MULTI_URL_TEMPLATE, REQUEST_TIMEOUT
    from book_codes import get_biblehub_book_name
    from version_codes import ALL_VERSION_MAPPINGS, LANGUAGE_PATTERNS

# Add project root to path for imports when running as a skill
# Path: biblehub_fetcher.py → scripts/ → quote-bible/ → skills/ → .claude/ → project_root
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.util.cache import fetch_verse_from_cache

CACHE_ROOT = Path('bible/commentary')
# IMPORTANT: you must keep the .cache suffix as this is copyrighted works and .gitignore will skip adding it to source
SUFFIX = "translations-biblehub.cache"

class VerseFetchError(Exception):
    """Exception raised when verse fetching fails."""
    pass


def fetch_verses_from_biblehub(book: str, chapter: int, verse: int,
                use_cache: bool = True) -> Dict[str, str]:
    """
    Fetch verse from cache or BibleHub.

    This is the main entry point for fetching verses. It first checks the cache,
    and if not found (or use_cache=False), fetches from the web and saves to cache.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        use_cache: Whether to use cache (default: True)

    Returns:
        Dictionary mapping version codes to verse text

    Raises:
        VerseFetchError: If fetching fails

    Example:
        >>> # Try cache first, fetch from web if needed
        >>> translations = fetch_verse("MAT", 5, 3)
        >>> print(translations["eng-NIV"])
        Blessed are the poor in spirit...

        >>> # Force web fetch (bypass cache)
        >>> translations = fetch_verse("MAT", 5, 3, use_cache=False)

        >>> # Use different cache suffix
        >>> translations = fetch_verse("MAT", 5, 3, suffix="custom.json")
    """
    if use_cache:   
        return fetch_verse_from_cache(book, chapter, verse, suffix=SUFFIX, onMissing=fetch_verse_from_web, cache_root=CACHE_ROOT) 
    else:
        return fetch_verse_from_web(book, chapter, verse)


def fetch_verse_from_web(book: str, chapter: int, verse: int) -> Dict[str, str]:
    """
    Fetch verse directly from BibleHub (no caching).

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number

    Returns:
        Dictionary mapping version codes to verse text

    Raises:
        VerseFetchError: If download or parsing fails

    Example:
        >>> translations = fetch_verse_from_web("JHN", 3, 16)
        >>> print(translations["eng-NIV"])
        For God so loved the world...
    """
    try:
        # Get the BibleHub book name
        book_name = get_biblehub_book_name(book)
    except ValueError as e:
        raise VerseFetchError(f"Invalid book code '{book}': {e}")

    # Build the URL using template
    url = BIBLEHUB_MULTI_URL_TEMPLATE.format(
        book=book_name,
        chapter=chapter,
        verse=verse
    )

    try:
        # Make HTTP GET request
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        # Force UTF-8 encoding (BibleHub serves UTF-8 but requests may detect wrong encoding)
        response.encoding = 'utf-8'
    except requests.Timeout:
        raise VerseFetchError(f"Request timed out after {REQUEST_TIMEOUT}s: {url}")
    except requests.HTTPError as e:
        raise VerseFetchError(f"HTTP error {e.response.status_code}: {url}")
    except requests.RequestException as e:
        raise VerseFetchError(f"Failed to download from BibleHub: {e}")

    # Parse the HTML (use .text now that encoding is corrected)
    try:
        translations = parse_biblehub_html(response.text)
    except Exception as e:
        raise VerseFetchError(f"Failed to parse HTML: {e}")

    if not translations:
        raise VerseFetchError(f"No translations found for {book} {chapter}:{verse}")

    return translations



def decode_html_content(html_bytes: bytes) -> str:
    """
    Decode HTML content, handling quoted-printable and MHTML formats.

    Args:
        html_bytes: Raw HTML bytes

    Returns:
        Decoded HTML string with unescaped entities

    Example:
        >>> html_bytes = b'=3Chtml=3E...'
        >>> decoded = decode_html_content(html_bytes)
        >>> '<html>' in decoded
        True
    """
    # Try to decode quoted-printable encoding
    try:
        decoded = quopri.decodestring(html_bytes).decode('utf-8')
    except:
        # Fallback to direct UTF-8 decode
        decoded = html_bytes.decode('utf-8', errors='ignore')

    # Extract HTML from MHTML (saved web page format)
    if 'Content-Type: text/html' in decoded and 'MultipartBoundary' in decoded:
        html_start = decoded.find('<!DOCTYPE')
        if html_start == -1:
            html_start = decoded.find('<html')
        if html_start > 0:
            decoded = decoded[html_start:]

    # Unescape HTML entities (&lt; becomes <, etc.)
    return html.unescape(decoded)


def normalize_version_name(version_name: str) -> str:
    """
    Remove verse reference prefix from version name.

    BibleHub includes the verse reference in the version name like:
    "Genesis 1:1 Afrikaans PWL" -> "Afrikaans PWL"

    Args:
        version_name: Raw version name from HTML

    Returns:
        Normalized version name without verse reference

    Example:
        >>> normalize_version_name("Genesis 1:1 Afrikaans PWL")
        'Afrikaans PWL'
        >>> normalize_version_name("New International Version")
        'New International Version'
    """
    # Remove verse reference prefix (e.g., "Genesis 1:1 ")
    version_name = re.sub(r'^[\w\s]+\d+:\d+\s+', '', version_name)
    return version_name.strip()


def map_version_to_code(version_name: str) -> str:
    """
    Map version name to standardized code (incremental lang-version format).

    Uses version mappings from consts.version_codes module.
    Format: {lang}-{VERSION} or {lang}-{VERSION}-{year} (e.g., "eng-NIV", "spa-RV-1909")

    Args:
        version_name: Version name to map (will be normalized first)

    Returns:
        Standardized version code

    Example:
        >>> map_version_to_code("Genesis 1:1 New International Version")
        'eng-NIV'
        >>> map_version_to_code("Afrikaans PWL")
        'afr-PWL'
    """
    normalized = normalize_version_name(version_name)

    # Try exact match first (includes all English and specific non-English versions)
    if normalized in ALL_VERSION_MAPPINGS:
        return ALL_VERSION_MAPPINGS[normalized]

    # Try language pattern matching for non-English
    for lang_name, lang_code in LANGUAGE_PATTERNS.items():
        if lang_name in normalized:
            return lang_code

    # Fallback: create generic code
    # Remove non-alphanumeric, convert to lowercase, take first 10 chars
    clean_name = re.sub(r'[^a-z0-9]', '', normalized.lower())[:10]
    return f'unk-{clean_name}'


def parse_biblehub_html(html_content: Union[str, bytes]) -> Dict[str, str]:
    """
    Parse BibleHub multi-translation HTML and extract all translations.

    Args:
        html_content: HTML content as string or bytes

    Returns:
        Dictionary mapping version codes to verse text

    Example:
        >>> html = '<html>...</html>'
        >>> translations = parse_biblehub_html(html)
        >>> 'eng-niv' in translations
        True
        >>> len(translations) > 40  # Should extract many versions
        True
    """
    # Decode if bytes
    if isinstance(html_content, bytes):
        decoded = decode_html_content(html_content)
    else:
        decoded = html_content

    translations = {}

    # Pattern 1: Find version entries with <span class="versiontext"><a ...>VERSION_NAME</a>
    # The version name is in the link text, and the verse follows after <br> or directly
    # Non-greedy match to avoid capturing too much
    version_pattern = r'<span class="versiontext"><a[^>]*>([^<]+)</a>(?:</span>)?(?:<br\s*/?>)?\s*(.*?)(?=<span class="versiontext">|<p><span class="versiontext">|<div |$)'

    matches = re.finditer(version_pattern, decoded, re.DOTALL | re.IGNORECASE)

    for match in matches:
        version_name = match.group(1).strip()
        # Group 2 contains the verse text (may have some HTML tags mixed in)
        raw_text = match.group(2)

        # Extract text from potential span wrappers
        # Handle language-specific spans like <span class="chi">...</span>, <span class="spa">...</span>, etc.
        span_match = re.search(r'<span class="[a-z]{2,5}">([^<]+)</span>', raw_text)
        if span_match:
            verse_text = span_match.group(1).strip()
        else:
            # Remove any remaining HTML tags and get text
            verse_text = re.sub(r'<[^>]+>', '', raw_text).strip()

        # Clean up extra whitespace
        verse_text = ' '.join(verse_text.split())

        # Skip entries that are empty or start with HTML (invalid parse)
        # Note: No minimum length - shortest verse "Jesus wept" can be very short in some languages
        if not verse_text or verse_text.startswith('<'):
            continue

        # Map to standardized code
        version_code = map_version_to_code(version_name)
        translations[version_code] = verse_text

    return translations


def parse_biblehub_file(html_file_path: str) -> Dict[str, str]:
    """
    Parse BibleHub HTML from a file path.

    Args:
        html_file_path: Path to HTML file

    Returns:
        Dictionary mapping version codes to verse text

    Raises:
        FileNotFoundError: If file doesn't exist

    Example:
        >>> translations = parse_biblehub_file("data/genesis-1-1.html")
        >>> len(translations) > 40
        True
    """
    file_path = Path(html_file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file_path}")

    with open(file_path, 'rb') as f:
        html_bytes = f.read()

    return parse_biblehub_html(html_bytes)


def main():
    """Test the BibleHub fetcher with sample verses."""
    print("BibleHub Fetcher Test - FULL VERSION ANALYSIS")
    print("=" * 80)
    print()
    
    # Test verses: famous passages across different books
    test_verses = [
        ("GEN", 1, 1, "Genesis 1:1 - The Creation"),
        ("JHN", 3, 16, "John 3:16 - For God So Loved"),
        ("MAT", 5, 3, "Matthew 5:3 - Blessed are the Poor in Spirit"),
        ("PSA", 23, 1, "Psalm 23:1 - The Lord is My Shepherd"),
    ]
    
    all_results = {}
    
    for book, chapter, verse, description in test_verses:
        print(f"\n{description}")
        print(f"Reference: {book} {chapter}:{verse}")
        print("-" * 80)
        
        try:
            # Fetch translations (will use cache if available)
            translations = fetch_verses_from_biblehub(book, chapter, verse, use_cache=True)
            all_results[f"{book}.{chapter}.{verse}"] = translations
            
            # Analyze translations
            unknown_codes = [k for k in translations.keys() if k.startswith('unk-')]
            english_codes = [k for k in translations.keys() if k.startswith('eng-')]
            other_codes = [k for k in translations.keys() if not k.startswith('eng-') and not k.startswith('unk-')]
            
            # Show summary
            print(f"✓ Total translations: {len(translations)}")
            print(f"  - English: {len(english_codes)}")
            print(f"  - Non-English: {len(other_codes)}")
            print(f"  - Unknown (UNK): {len(unknown_codes)}")
            
            # Show all English translations
            if english_codes:
                print(f"\n📖 All English translations ({len(english_codes)}):")
                for key in sorted(english_codes):
                    text = translations[key]
                    display_text = text if len(text) <= 70 else text[:67] + "..."
                    print(f"  {key:20} {display_text}")
            
            # Show all non-English translations
            if other_codes:
                print(f"\n🌍 All non-English translations ({len(other_codes)}):")
                for key in sorted(other_codes):
                    text = translations[key]
                    display_text = text if len(text) <= 70 else text[:67] + "..."
                    print(f"  {key:20} {display_text}")
            
            # HIGHLIGHT UNKNOWN CODES
            if unknown_codes:
                print(f"\n⚠️  UNKNOWN VERSION CODES ({len(unknown_codes)}) - NEED TO ADD TO MAPPINGS:")
                for key in sorted(unknown_codes):
                    text = translations[key]
                    display_text = text if len(text) <= 70 else text[:67] + "..."
                    print(f"  {key:20} {display_text}")
                    
        except VerseFetchError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    # Compare translation counts across verses
    print("\n" + "=" * 80)
    print("TRANSLATION COUNT ANALYSIS")
    print("-" * 80)
    
    if all_results:
        for ref, translations in all_results.items():
            unknown = len([k for k in translations.keys() if k.startswith('unk-')])
            english = len([k for k in translations.keys() if k.startswith('eng-')])
            other = len([k for k in translations.keys() if not k.startswith('eng-') and not k.startswith('unk-')])
            total = len(translations)
            
            print(f"{ref:15} Total: {total:3}  English: {english:2}  Non-Eng: {other:2}  Unknown: {unknown:2}")
    
    print("\n📝 Notes on translation count variations:")
    print("  - Different verses may have different translations available on BibleHub")
    print("  - Old Testament vs New Testament typically have different translation sets")
    print("  - Some modern translations may not include Psalms or may be NT-only")
    print("  - This is NORMAL and expected behavior, not a bug")
    
    print("\n" + "=" * 80)
    print("Test complete!")
    print(f"Cache location: {CACHE_ROOT}")
    print(f"Cache suffix: {SUFFIX}")


if __name__ == "__main__":
    main()
