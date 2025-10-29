"""Cache management utilities for Bible verses.

This module provides clean, focused cache operations for storing and retrieving
Bible verse translations in YAML format following SCHEMA.md standards.
"""

from pathlib import Path
from typing import Callable, Dict, Optional, Union

import yaml

from .file_helper import get_file_path


def fetch_verse_from_cache(book: str, chapter: int, verse: int,
                           suffix: str = "biblehub",
                           extension: str = "yaml",
                           cache_root: Optional[Union[str, Path]] = None,
                           onMissing: Callable[[str, int, int], Optional[Dict]] = None) -> Optional[Dict]:
    """
    Fetch verse from cache if it exists, calling onMissing callback if not found.
    
    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "yaml")
        cache_root: Root cache directory (default: project cache directory)
        onMissing: Optional callback to fetch data if not in cache
        
    Returns:
        Dictionary containing verse data structure, or None if not found
    """
    result = get_cached_verse(book, chapter, verse, suffix, extension, cache_root)
    if result is None and onMissing is not None:
        result = onMissing(book, chapter, verse)
        if result is not None:
            save_verse_to_cache(book, chapter, verse, result, suffix, extension, cache_root)
    return result

def get_cached_verse(book: str, chapter: int, verse: int,
                     suffix: str = "biblehub",
                     extension: str = "yaml",
                     cache_root: Optional[Union[str, Path]] = None) -> Optional[Dict]:
    """
    Retrieve verse from cache if it exists.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "yaml")
        cache_root: Root cache directory (default: project cache directory)

    Returns:
        Dictionary containing verse data structure, or None if not cached

    Example:
        >>> verse_data = get_cached_verse("MAT", 5, 3)
        >>> if verse_data:
        ...     print(verse_data.get("translations", {}).get("eng-niv"))
        >>> verse_data = get_cached_verse("MAT", 5, 3, suffix="ebible")
    """
    cache_path = get_file_path(book, chapter, verse, suffix, extension, cache_root=cache_root)

    if not cache_path.exists():
        return None

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # Return the full data structure as-is
            return data
    except (yaml.YAMLError, IOError):
        # If cache is corrupted, treat as missing
        return None


def save_verse_to_cache(book: str, chapter: int, verse: int,
                       verse_data: Dict,
                       suffix: str = "biblehub",
                       extension: str = "yaml",
                       cache_root: Optional[Union[str, Path]] = None) -> Path:
    """
    Save verse data to cache in YAML format (generic storage - caller is responsible for structure).

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        verse_data: Dictionary containing verse data structure (as-is from caller)
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "yaml")
        cache_root: Root cache directory (default: project cache directory)

    Returns:
        Path to the cached file

    Example:
        >>> verse_data = {
        ...     "verse": "MAT.005.003",
        ...     "translations": {"eng-niv": "Blessed are...", "eng-kjv": "Blessed are..."},
        ...     "sources": [{"url": "https://example.com"}]
        ... }
        >>> path = save_verse_to_cache("MAT", 5, 3, verse_data, suffix="ebible")
        >>> print(f"Saved to {path}")
    """
    cache_path = get_file_path(book, chapter, verse, suffix, extension, cache_root=cache_root)

    # Create parent directories if they don't exist
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    # Write YAML to cache with pretty formatting and UTF-8 support
    # Cache stores data as-is (garbage in, garbage out)
    with open(cache_path, 'w', encoding='utf-8') as f:
        yaml.dump(verse_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return cache_path


def cache_exists(book: str, chapter: int, verse: int,
                suffix: str = "biblehub",
                extension: str = "yaml",
                cache_root: Optional[Union[str, Path]] = None) -> bool:
    """
    Check if verse is cached.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "yaml")
        cache_root: Root cache directory (default: project cache directory)

    Returns:
        True if verse is cached, False otherwise

    Example:
        >>> if cache_exists("MAT", 5, 3):
        ...     print("Verse is cached")
        >>> if cache_exists("MAT", 5, 3, suffix="ebible"):
        ...     print("eBible verse is cached")
    """
    cache_path = get_file_path(book, chapter, verse, suffix, extension, cache_root=cache_root)
    return cache_path.exists()
