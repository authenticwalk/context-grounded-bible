"""File path utilities for Bible verse cache management."""

from pathlib import Path
from typing import Optional, Union

# Project root is the parent of the util directory
PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_CACHE_ROOT = PROJECT_ROOT / "cache"


def format_filename(book: str, chapter: int, verse: int, suffix: str, extension: str = "json") -> str:
    """
    Format a cache filename according to the standard pattern.
    
    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub.json", "ebible.tsv")
    
    Returns:
        Formatted filename (e.g., "MAT_5_003.biblehub.json")
    
    Example:
        >>> format_cache_filename("MAT", 5, 3, "biblehub.json")
        'MAT_5_003.biblehub.json'
    """
    return f"{book}_{chapter}_{verse:03d}.{suffix}.{extension}"


def get_file_path(book: str, chapter: int, verse: int, suffix: str, extension: str = "json",
                   cache_root: Optional[Union[str, Path]] = None) -> Path:
    """
    Build the full file path.
    
    Args:
        book: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
        suffix: File suffix (e.g., "biblehub", "ebible")
        extension: File extension (default: "json")
        cache_root: Root cache directory (default: project cache directory)
    
    Returns:
        Full path to file
    
    Example:
        >>> get_file_path("MAT", 5, 3, "biblehub.json")
        PosixPath('/path/to/project/cache/MAT/5/MAT_5_003.biblehub.json')
    """
    if cache_root is None:
        cache_root = DEFAULT_CACHE_ROOT
    
    filename = format_filename(book, chapter, verse, suffix, extension)
    return Path(cache_root) / book / str(chapter) / filename




