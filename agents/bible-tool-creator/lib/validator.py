#!/usr/bin/env python3
"""
Validation Gates for Bible Tool Creator Agent

Provides validation functions to catch errors early and prevent
cascading failures between phases.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Validator:
    """Validates files and state at phase boundaries."""

    @staticmethod
    def validate_directory(path: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate directory exists and is writable.

        Args:
            path: Directory path to validate

        Returns:
            (success, error_message)
        """
        if not path.exists():
            return False, f"Directory does not exist: {path}"

        if not path.is_dir():
            return False, f"Path is not a directory: {path}"

        # Check writability by trying to create a temp file
        test_file = path / ".write_test"
        try:
            test_file.touch()
            test_file.unlink()
            return True, None
        except Exception as e:
            return False, f"Directory not writable: {e}"

    @staticmethod
    def validate_yaml_syntax(yaml_file: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate YAML file has valid syntax.

        Args:
            yaml_file: Path to YAML file

        Returns:
            (success, error_message)
        """
        if not yaml_file.exists():
            return False, f"File does not exist: {yaml_file}"

        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
            return True, None
        except yaml.YAMLError as e:
            return False, f"Invalid YAML syntax: {e}"
        except Exception as e:
            return False, f"Error reading file: {e}"

    @staticmethod
    def validate_verse_field(yaml_file: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate YAML has required 'verse' field.

        Args:
            yaml_file: Path to YAML file

        Returns:
            (success, error_message)
        """
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)

            if not isinstance(data, dict):
                return False, "YAML root must be a dictionary"

            if 'verse' not in data:
                return False, "Missing required 'verse' field"

            verse = data['verse']
            if not isinstance(verse, str):
                return False, "'verse' field must be a string"

            # Validate verse format: BOOK.chapter.verse (e.g., JHN.001.001)
            pattern = r'^[A-Z]{3}\.\d{3}\.\d{3}$'
            if not re.match(pattern, verse):
                return False, f"Invalid verse format: {verse} (expected BOOK.CCC.VVV)"

            return True, None

        except Exception as e:
            return False, f"Error validating verse field: {e}"

    @staticmethod
    def validate_file_size(file_path: Path, min_bytes: int = 100,
                          max_bytes: int = 51200) -> Tuple[bool, Optional[str]]:
        """
        Validate file size is within reasonable bounds.

        Args:
            file_path: Path to file
            min_bytes: Minimum file size (default 100 bytes)
            max_bytes: Maximum file size (default 50KB)

        Returns:
            (success, error_message)
        """
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"

        size = file_path.stat().st_size

        if size < min_bytes:
            return False, f"File too small: {size} bytes (min {min_bytes})"

        if size > max_bytes:
            return False, f"File too large: {size} bytes (max {max_bytes})"

        return True, None

    @staticmethod
    def validate_citations(yaml_file: Path, min_citations: int = 1) -> Tuple[bool, Optional[str]]:
        """
        Validate YAML contains citations.

        Args:
            yaml_file: Path to YAML file
            min_citations: Minimum number of citations required

        Returns:
            (success, error_message)
        """
        try:
            content = yaml_file.read_text()

            # Count citations in format {source-id}
            citation_pattern = r'\{[a-z0-9\-]+\}'
            citations = re.findall(citation_pattern, content)

            if len(citations) < min_citations:
                return False, f"Insufficient citations: {len(citations)} (min {min_citations})"

            return True, None

        except Exception as e:
            return False, f"Error checking citations: {e}"

    @staticmethod
    def validate_markdown(md_file: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate markdown file is readable and non-empty.

        Args:
            md_file: Path to markdown file

        Returns:
            (success, error_message)
        """
        if not md_file.exists():
            return False, f"File does not exist: {md_file}"

        try:
            content = md_file.read_text()

            if len(content.strip()) < 50:
                return False, "Markdown file too short (< 50 characters)"

            # Check for basic markdown structure (at least one header)
            if not re.search(r'^#+\s+.+', content, re.MULTILINE):
                return False, "No markdown headers found"

            return True, None

        except Exception as e:
            return False, f"Error reading markdown: {e}"

    @staticmethod
    def validate_verses_complete(state: Dict, expected_count: int) -> Tuple[bool, Optional[str]]:
        """
        Validate all expected verses are complete.

        Args:
            state: State dictionary
            expected_count: Number of verses expected

        Returns:
            (success, error_message)
        """
        verses = state.get('verses', [])

        if len(verses) != expected_count:
            return False, f"Expected {expected_count} verses, found {len(verses)}"

        completed = sum(1 for v in verses if v.get('status') == 'complete')

        if completed != expected_count:
            return False, f"Only {completed}/{expected_count} verses complete"

        return True, None

    @staticmethod
    def run_all_verse_validations(yaml_file: Path) -> List[Tuple[str, bool, Optional[str]]]:
        """
        Run all validations on a verse YAML file.

        Args:
            yaml_file: Path to YAML file

        Returns:
            List of (check_name, passed, error_message) tuples
        """
        results = []

        # YAML syntax
        passed, error = Validator.validate_yaml_syntax(yaml_file)
        results.append(("YAML Syntax", passed, error))

        if not passed:
            # If syntax invalid, skip other checks
            return results

        # Required verse field
        passed, error = Validator.validate_verse_field(yaml_file)
        results.append(("Verse Field", passed, error))

        # File size
        passed, error = Validator.validate_file_size(yaml_file)
        results.append(("File Size", passed, error))

        # Citations
        passed, error = Validator.validate_citations(yaml_file)
        results.append(("Citations", passed, error))

        return results
