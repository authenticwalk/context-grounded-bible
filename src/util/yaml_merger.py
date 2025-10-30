"""
YAML Merger Utility

Provides nested merging of YAML data structures with special handling for strings.
"""

from typing import Any, Dict, List, Union
import yaml
from pathlib import Path


def merge_yaml_data(base: Any, update: Any) -> Any:
    """
    Recursively merges two YAML data structures.

    Rules:
    - Dicts are merged recursively
    - Lists are combined (update extends base)
    - Strings are concatenated if different (with newline separator)
    - Other types: update overwrites base

    Args:
        base: The base data structure
        update: The data to merge into base

    Returns:
        Merged data structure
    """
    # If types don't match, return update
    if type(base) != type(update):
        return update

    # Handle dictionaries - recursive merge
    if isinstance(base, dict):
        result = base.copy()
        for key, value in update.items():
            if key in result:
                result[key] = merge_yaml_data(result[key], value)
            else:
                result[key] = value
        return result

    # Handle lists - extend
    elif isinstance(base, list):
        result = base.copy()
        result.extend(update)
        return result

    # Handle strings - concatenate if different
    elif isinstance(base, str):
        if base.strip() == update.strip():
            return update  # Same content, use latest
        else:
            # Different content, concatenate
            return f"{base}\n\n{update}"

    # For other types (int, float, bool, None), use update
    else:
        return update


def merge_yaml_files(file_paths: List[Union[str, Path]]) -> Dict[str, Any]:
    """
    Merges multiple YAML files into a single data structure.

    Files are merged in order, with later files taking precedence.
    Uses merge_yaml_data rules for combining values.

    Args:
        file_paths: List of paths to YAML files

    Returns:
        Merged data dictionary

    Raises:
        FileNotFoundError: If a file doesn't exist
        yaml.YAMLError: If a file is invalid YAML
    """
    result = {}

    for file_path in file_paths:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data is not None:
            result = merge_yaml_data(result, data)

    return result


def merge_directory_yaml_files(directory: Union[str, Path], pattern: str = "*.yaml") -> Dict[str, Any]:
    """
    Merges all YAML files in a directory matching a pattern.

    Files are sorted alphabetically before merging to ensure deterministic results.

    Args:
        directory: Path to directory containing YAML files
        pattern: Glob pattern for matching files (default: "*.yaml")

    Returns:
        Merged data dictionary

    Raises:
        NotADirectoryError: If directory doesn't exist
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        raise NotADirectoryError(f"Directory not found: {directory}")

    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    # Get all matching files, sorted for deterministic merging
    yaml_files = sorted(dir_path.glob(pattern))

    if not yaml_files:
        return {}

    return merge_yaml_files(yaml_files)


def save_merged_yaml(data: Dict[str, Any], output_path: Union[str, Path]) -> None:
    """
    Saves merged YAML data to a file.

    Args:
        data: Data dictionary to save
        output_path: Path where YAML should be saved
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 3:
        print("Usage: python yaml_merger.py <output_file> <input_file1> [input_file2] ...")
        print("   or: python yaml_merger.py <output_file> --dir <directory> [--pattern <pattern>]")
        sys.exit(1)

    output_file = sys.argv[1]

    if sys.argv[2] == "--dir":
        if len(sys.argv) < 4:
            print("Error: --dir requires a directory path")
            sys.exit(1)

        directory = sys.argv[3]
        pattern = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "--pattern" else "*.yaml"
        if len(sys.argv) > 5 and sys.argv[4] == "--pattern":
            pattern = sys.argv[5]

        print(f"Merging YAML files from directory: {directory}")
        print(f"Pattern: {pattern}")
        merged = merge_directory_yaml_files(directory, pattern)
    else:
        input_files = sys.argv[2:]
        print(f"Merging {len(input_files)} YAML files...")
        merged = merge_yaml_files(input_files)

    save_merged_yaml(merged, output_file)
    print(f"Merged YAML saved to: {output_file}")
