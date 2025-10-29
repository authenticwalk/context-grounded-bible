"""Cache management utilities for Bible verses.

This module provides clean, focused cache operations for storing and retrieving
Bible verse translations in JSON format.
"""

import json
from pathlib import Path
from typing import Callable, Dict, Optional, Union

from .file_helper import get_file_path


def fetch_verse_from_cache(book: str, chapter: int, verse: int,
                           suffix: str = "biblehub",
                           extension: str = "json",
                           cache_root: Optional[Union[str, Path]] = None,
                           onMissing: Callable[[str, int, int], Optional[Dict[str, str]]] = None) -> Optional[Dict[str, str]]:
    """
    Fetch verse from cache if it exists, calling onMissing callback if not found.
    
    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "json")
        cache_root: Root cache directory (default: project cache directory)
        onMissing: Optional callback to fetch data if not in cache
        
    Returns:
        Dictionary mapping version codes to verse text, or None if not found
    """
    result = get_cached_verse(book, chapter, verse, suffix, extension, cache_root)
    if result is None and onMissing is not None:
        result = onMissing(book, chapter, verse)
        if result is not None:
            save_verse_to_cache(book, chapter, verse, result, suffix, extension, cache_root)
    return result

def get_cached_verse(book: str, chapter: int, verse: int,
                     suffix: str = "biblehub",
                     extension: str = "json",
                     cache_root: Optional[Union[str, Path]] = None) -> Optional[Dict[str, str]]:
    """
    Retrieve verse from cache if it exists.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "json")
        cache_root: Root cache directory (default: project cache directory)

    Returns:
        Dictionary mapping version codes to verse text, or None if not cached

    Example:
        >>> translations = get_cached_verse("MAT", 5, 3)
        >>> if translations:
        ...     print(translations["eng-niv"])
        >>> translations = get_cached_verse("MAT", 5, 3, suffix="ebible")
    """
    cache_path = get_file_path(book, chapter, verse, suffix, extension, cache_root=cache_root)

    if not cache_path.exists():
        return None

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If cache is corrupted, treat as missing
        return None


def save_verse_to_cache(book: str, chapter: int, verse: int,
                       translations: Dict[str, str],
                       suffix: str = "biblehub",
                       extension: str = "json",
                       cache_root: Optional[Union[str, Path]] = None) -> Path:
    """
    Save verse translations to cache.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        translations: Dictionary mapping version codes to verse text
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "json")
        cache_root: Root cache directory (default: project cache directory)

    Returns:
        Path to the cached file

    Example:
        >>> translations = {"eng-niv": "Blessed are...", "eng-kjv": "Blessed are..."}
        >>> path = save_verse_to_cache("MAT", 5, 3, translations)
        >>> print(f"Saved to {path}")
        >>> path = save_verse_to_cache("MAT", 5, 3, translations, suffix="ebible")
    """
    cache_path = get_file_path(book, chapter, verse, suffix, extension, cache_root=cache_root)

    # Create parent directories if they don't exist
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON to cache with pretty formatting and UTF-8 support
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)

    return cache_path


def cache_exists(book: str, chapter: int, verse: int,
                suffix: str = "biblehub",
                extension: str = "json",
                cache_root: Optional[Union[str, Path]] = None) -> bool:
    """
    Check if verse is cached.

    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "json")
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
