"""Simple caching system for lexical data.

This module provides a file-based caching system to avoid repeated
downloads from BibleHub.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


class CacheManager:
    """Manage cached lexical data."""

    def __init__(self, cache_dir: str = ".cache/lexicon"):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache files (relative to current dir)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_path(self, book: str, chapter: int, verse: int, data_type: str) -> Path:
        """
        Get cache file path for a specific verse and data type.

        Args:
            book: USFM book code
            chapter: Chapter number
            verse: Verse number
            data_type: Type of data (e.g., 'lexicon', 'variants')

        Returns:
            Path to cache file
        """
        filename = f"{book}-{chapter}-{verse}-{data_type}.json"
        return self.cache_dir / filename

    def get(self, book: str, chapter: int, verse: int, data_type: str) -> Optional[Any]:
        """
        Get cached data if available.

        Args:
            book: USFM book code
            chapter: Chapter number
            verse: Verse number
            data_type: Type of data

        Returns:
            Cached data or None if not found
        """
        cache_path = self.get_cache_path(book, chapter, verse, data_type)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # If cache is corrupted, remove it
            cache_path.unlink(missing_ok=True)
            return None

    def set(self, book: str, chapter: int, verse: int, data_type: str, data: Any) -> None:
        """
        Store data in cache.

        Args:
            book: USFM book code
            chapter: Chapter number
            verse: Verse number
            data_type: Type of data
            data: Data to cache
        """
        cache_path = self.get_cache_path(book, chapter, verse, data_type)

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except (OSError, TypeError) as e:
            # If caching fails, just continue without cache
            print(f"Warning: Failed to write cache: {e}")

    def clear(self, book: Optional[str] = None, chapter: Optional[int] = None) -> int:
        """
        Clear cache files.

        Args:
            book: Optional book code to clear (if None, clears all)
            chapter: Optional chapter to clear

        Returns:
            Number of files removed
        """
        count = 0

        if book is None:
            # Clear all cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
                count += 1
        elif chapter is None:
            # Clear all for this book
            for cache_file in self.cache_dir.glob(f"{book}-*.json"):
                cache_file.unlink()
                count += 1
        else:
            # Clear specific chapter
            for cache_file in self.cache_dir.glob(f"{book}-{chapter}-*.json"):
                cache_file.unlink()
                count += 1

        return count

    def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            'file_count': len(cache_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir)
        }
