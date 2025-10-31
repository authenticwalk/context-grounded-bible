#!/usr/bin/env python3
"""
Scripture Study - Aggregate and merge commentary data for Bible verses

Retrieves all available commentary files for specified verse(s) and merges them
into a unified output. Supports depth levels, filtering, and verse ranges.
"""

import argparse
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from util.yaml_merger import merge_yaml_files
except ImportError:
    print("Error: Cannot import yaml_merger. Make sure src/util/yaml_merger.py exists", file=sys.stderr)
    sys.exit(1)


# USFM 3.0 book codes mapping (partial list, expand as needed)
BOOK_CODES = {
    'GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA',
    '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO',
    'ECC', 'SNG', 'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO',
    'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL',
    'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH',
    'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS',
    '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'
}


def parse_verse_reference(reference: str) -> List[Tuple[str, int, int]]:
    """
    Parse verse reference(s) into (book, chapter, verse) tuples.

    Supports:
    - Single verse: "JHN 3:16"
    - Verse range: "MAT 5:3-10"
    - Multiple verses: "JHN 3:16 JHN 3:17"
    - Chapter (all verses): "MAT 5"

    Args:
        reference: Verse reference string

    Returns:
        List of (book, chapter, verse) tuples

    Raises:
        ValueError: If reference format is invalid
    """
    verses = []

    # Split on whitespace and process each part
    parts = reference.strip().split()

    i = 0
    while i < len(parts):
        book = parts[i].upper()

        if book not in BOOK_CODES:
            raise ValueError(f"Invalid book code: {book}. Must be USFM 3.0 format (e.g., MAT, JHN, GEN)")

        if i + 1 >= len(parts):
            raise ValueError(f"Missing chapter:verse after book code {book}")

        chapter_verse = parts[i + 1]

        # Handle chapter:verse or chapter:verse-verse
        match = re.match(r'^(\d+):(\d+)(?:-(\d+))?$', chapter_verse)
        if match:
            chapter = int(match.group(1))
            start_verse = int(match.group(2))
            end_verse = int(match.group(3)) if match.group(3) else start_verse

            # Expand range
            for verse in range(start_verse, end_verse + 1):
                verses.append((book, chapter, verse))

        # Handle chapter only (would need to know verse count, skip for now)
        elif re.match(r'^\d+$', chapter_verse):
            raise ValueError(f"Chapter-only references not yet supported: {book} {chapter_verse}")
        else:
            raise ValueError(f"Invalid chapter:verse format: {chapter_verse}")

        i += 2

    return verses


def load_tool_registry(registry_path: Path) -> Dict[str, Any]:
    """
    Load tool registry YAML file.

    Args:
        registry_path: Path to tool-registry.yaml

    Returns:
        Dictionary of tool definitions
    """
    if not registry_path.exists():
        return {}

    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    return registry.get('tools', {}) if registry else {}


def get_commentary_files(
    book: str,
    chapter: int,
    verse: int,
    depth: str,
    base_path: Path,
    tool_registry: Dict[str, Any],
    filters: List[str] = None,
    excludes: List[str] = None
) -> List[Path]:
    """
    Get all commentary files for a verse based on depth level and filters.

    Args:
        book: USFM 3.0 book code
        chapter: Chapter number
        verse: Verse number
        depth: Depth level (light/medium/full)
        base_path: Base path to data/commentary/commentary directory
        tool_registry: Tool registry dictionary
        filters: List of tool suffixes to include (None = all)
        excludes: List of tool suffixes to exclude

    Returns:
        List of Path objects for commentary files
    """
    files = []
    verse_padded = f"{verse:03d}"

    # Verse-level directory (uses non-padded chapter in directory path)
    verse_dir = base_path / book / str(chapter)

    if not verse_dir.exists():
        return files

    # Get all YAML files in verse directory
    # Format: BOOK_chapter_verse.suffix.yaml (underscores, not periods)
    for file_path in verse_dir.glob(f"{book}_{chapter}_{verse_padded}.*.yaml"):
        # Extract tool suffix from filename
        # Format: BOOK_chapter_verse.suffix.yaml
        filename = file_path.name
        match = re.match(rf'{book}_{chapter}_{verse_padded}\.(.+)\.yaml', filename)
        if not match:
            continue

        tool_suffix = match.group(1)

        # Apply filters
        if filters and tool_suffix not in filters:
            continue
        if excludes and tool_suffix in excludes:
            continue

        # Check scope level based on query depth
        if tool_suffix in tool_registry:
            tool_info = tool_registry[tool_suffix]
            tool_scope = tool_info.get('scope', 'standard')

            # Filter by scope based on query depth
            # light queries: core only
            # medium queries: core + standard
            # full queries: core + standard + comprehensive
            if depth == 'light' and tool_scope not in ['core']:
                continue
            if depth == 'medium' and tool_scope not in ['core', 'standard']:
                continue
            # full depth includes all scopes

        files.append(file_path)

    # For full depth, add chapter-level and book-level files
    if depth == 'full':
        # Chapter-level files (format: BOOK_chapter.suffix.yaml)
        for file_path in verse_dir.glob(f"{book}_{chapter}.*.yaml"):
            # Extract suffix
            match = re.match(rf'{book}_{chapter}\.(.+)\.yaml', file_path.name)
            if not match:
                continue
            tool_suffix = match.group(1)
            if filters and tool_suffix not in filters:
                continue
            if excludes and tool_suffix in excludes:
                continue
            files.append(file_path)

        # Book-level files (format: BOOK.suffix.yaml)
        book_dir = base_path / book
        if book_dir.exists():
            for file_path in book_dir.glob(f"{book}.*.yaml"):
                # Extract suffix
                match = re.match(rf'{book}\.(.+)\.yaml', file_path.name)
                if not match:
                    continue
                tool_suffix = match.group(1)
                if filters and tool_suffix not in filters:
                    continue
                if excludes and tool_suffix in excludes:
                    continue
                files.append(file_path)

    return files


def merge_commentary_for_verses(
    verses: List[Tuple[str, int, int]],
    depth: str,
    base_path: Path,
    tool_registry: Dict[str, Any],
    filters: List[str] = None,
    excludes: List[str] = None
) -> Dict[str, Any]:
    """
    Merge commentary data for multiple verses.

    Args:
        verses: List of (book, chapter, verse) tuples
        depth: Depth level
        base_path: Base path to commentary
        tool_registry: Tool registry
        filters: Tool filters
        excludes: Tool exclusions

    Returns:
        Merged dictionary organized by verse
    """
    result = {
        'verses': [],
        'metadata': {
            'verse_count': len(verses),
            'depth': depth,
            'filters': filters or [],
            'excludes': excludes or []
        }
    }

    for book, chapter, verse in verses:
        verse_ref = f"{book}.{chapter:03d}.{verse:03d}"

        files = get_commentary_files(
            book, chapter, verse, depth, base_path, tool_registry, filters, excludes
        )

        if not files:
            result['verses'].append({
                'reference': verse_ref,
                'display_reference': f"{book} {chapter}:{verse}",
                'commentary': None,
                'note': 'No commentary data found for this verse'
            })
            continue

        # Merge all files for this verse
        try:
            merged = merge_yaml_files(files)
            result['verses'].append({
                'reference': verse_ref,
                'display_reference': f"{book} {chapter}:{verse}",
                'commentary': merged,
                'sources': [str(f.relative_to(base_path.parent)) for f in files],
                'source_count': len(files)
            })
        except Exception as e:
            result['verses'].append({
                'reference': verse_ref,
                'display_reference': f"{book} {chapter}:{verse}",
                'commentary': None,
                'error': str(e)
            })

    return result


def list_available_tools(
    verses: List[Tuple[str, int, int]],
    base_path: Path
) -> Dict[str, Any]:
    """
    List all available tools for the given verses.

    Args:
        verses: List of (book, chapter, verse) tuples
        base_path: Base path to commentary

    Returns:
        Dictionary of available tools by verse
    """
    result = {}

    for book, chapter, verse in verses:
        verse_ref = f"{book}.{chapter:03d}.{verse:03d}"
        verse_padded = f"{verse:03d}"

        # Directory uses non-padded chapter
        verse_dir = base_path / book / str(chapter)

        if not verse_dir.exists():
            result[verse_ref] = []
            continue

        tools = []
        # Filename format: BOOK_chapter_verse.suffix.yaml
        for file_path in verse_dir.glob(f"{book}_{chapter}_{verse_padded}.*.yaml"):
            filename = file_path.name
            match = re.match(rf'{book}_{chapter}_{verse_padded}\.(.+)\.yaml', filename)
            if match:
                tools.append(match.group(1))

        result[verse_ref] = sorted(tools)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate and merge Bible commentary data for verse study'
    )
    parser.add_argument(
        'reference',
        help='Verse reference (e.g., "JHN 3:16", "MAT 5:3-10")'
    )
    parser.add_argument(
        '--depth',
        choices=['light', 'medium', 'full'],
        default='medium',
        help='Depth level (default: medium)'
    )
    parser.add_argument(
        '--filter',
        action='append',
        dest='filters',
        help='Include only specified tool types (can use multiple times)'
    )
    parser.add_argument(
        '--exclude',
        action='append',
        dest='excludes',
        help='Exclude specified tool types (can use multiple times)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Save output to file instead of stdout'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON instead of YAML'
    )
    parser.add_argument(
        '--list-tools',
        action='store_true',
        help='List available tools for the verse(s)'
    )

    args = parser.parse_args()

    # Determine base paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    commentary_base = project_root / 'bible' / 'commentary'
    tool_registry_path = project_root / 'bible-study-tools' / 'tool-registry.yaml'

    # Parse verse reference
    try:
        verses = parse_verse_reference(args.reference)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # List tools mode
    if args.list_tools:
        tools = list_available_tools(verses, commentary_base)
        if args.json:
            import json
            output = json.dumps(tools, indent=2)
        else:
            output = yaml.dump(tools, default_flow_style=False, allow_unicode=True)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding='utf-8')
        else:
            print(output)
        return

    # Load tool registry
    tool_registry = load_tool_registry(tool_registry_path)

    # Merge commentary
    result = merge_commentary_for_verses(
        verses,
        args.depth,
        commentary_base,
        tool_registry,
        args.filters,
        args.excludes
    )

    # Output
    if args.json:
        import json
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = yaml.dump(result, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding='utf-8')
        print(f"Output saved to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
