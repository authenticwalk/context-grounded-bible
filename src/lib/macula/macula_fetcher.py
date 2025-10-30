#!/usr/bin/env python3
"""
Macula Source Language Fetcher
===============================

Downloads and caches the Macula Hebrew and Greek datasets from Clear Bible.

This script:
1. Clones the macula-hebrew and macula-greek repositories
2. Extracts the lowfat XML files
3. Caches them in /tmp/macula for fast access

Data sources:
- Hebrew: https://github.com/Clear-Bible/macula-hebrew (WLC/lowfat)
- Greek: https://github.com/Clear-Bible/macula-greek (Nestle1904/lowfat)

License: CC BY 4.0
Copyright: Biblica, Inc (2022-2024)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import json

# Configuration
CACHE_DIR = Path("/tmp/macula")
HEBREW_REPO = "https://github.com/Clear-Bible/macula-hebrew.git"
GREEK_REPO = "https://github.com/Clear-Bible/macula-greek.git"

# Directory structure
HEBREW_CACHE = CACHE_DIR / "hebrew"
GREEK_CACHE = CACHE_DIR / "greek"
HEBREW_LOWFAT = HEBREW_CACHE / "WLC" / "lowfat"
GREEK_LOWFAT = GREEK_CACHE / "Nestle1904" / "lowfat"

# Metadata
METADATA_FILE = CACHE_DIR / "metadata.json"


def log(message):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def check_git():
    """Check if git is installed."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log("ERROR: git is not installed. Please install git first.")
        return False


def clone_or_update_repo(repo_url, target_dir, name):
    """Clone repository or update if it already exists."""
    if target_dir.exists():
        log(f"Updating {name} repository...")
        try:
            subprocess.run(
                ["git", "-C", str(target_dir), "pull"],
                capture_output=True,
                check=True,
                text=True
            )
            log(f"✓ {name} repository updated")
            return True
        except subprocess.CalledProcessError as e:
            log(f"ERROR updating {name}: {e.stderr}")
            log("Removing and re-cloning...")
            shutil.rmtree(target_dir)

    log(f"Cloning {name} repository...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(target_dir)],
            capture_output=True,
            check=True,
            text=True
        )
        log(f"✓ {name} repository cloned")
        return True
    except subprocess.CalledProcessError as e:
        log(f"ERROR cloning {name}: {e.stderr}")
        return False


def count_files(directory, pattern="*.xml"):
    """Count files matching pattern in directory."""
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def save_metadata():
    """Save metadata about the cached data."""
    metadata = {
        "last_updated": datetime.now().isoformat(),
        "hebrew": {
            "repo": HEBREW_REPO,
            "path": str(HEBREW_LOWFAT),
            "file_count": count_files(HEBREW_LOWFAT),
            "license": "CC BY 4.0",
            "copyright": "Biblica, Inc (2022-2024)",
            "citation": "MACULA Hebrew Linguistic Datasets, available at https://github.com/Clear-Bible/macula-hebrew/"
        },
        "greek": {
            "repo": GREEK_REPO,
            "path": str(GREEK_LOWFAT),
            "file_count": count_files(GREEK_LOWFAT),
            "license": "CC BY 4.0",
            "copyright": "Biblica, Inc (2022-2024)",
            "citation": "MACULA Greek Linguistic Datasets, available at https://github.com/Clear-Bible/macula-greek/"
        }
    }

    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

    log(f"Metadata saved to {METADATA_FILE}")


def fetch_hebrew():
    """Fetch Macula Hebrew dataset."""
    log("=" * 60)
    log("Fetching Macula Hebrew Dataset")
    log("=" * 60)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not clone_or_update_repo(HEBREW_REPO, HEBREW_CACHE, "Hebrew"):
        return False

    if not HEBREW_LOWFAT.exists():
        log(f"ERROR: Lowfat directory not found at {HEBREW_LOWFAT}")
        return False

    file_count = count_files(HEBREW_LOWFAT)
    log(f"✓ Found {file_count} Hebrew XML files")

    return True


def fetch_greek():
    """Fetch Macula Greek dataset."""
    log("=" * 60)
    log("Fetching Macula Greek Dataset")
    log("=" * 60)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not clone_or_update_repo(GREEK_REPO, GREEK_CACHE, "Greek"):
        return False

    if not GREEK_LOWFAT.exists():
        log(f"ERROR: Lowfat directory not found at {GREEK_LOWFAT}")
        return False

    file_count = count_files(GREEK_LOWFAT)
    log(f"✓ Found {file_count} Greek XML files")

    return True


def get_metadata():
    """Load and return metadata."""
    if METADATA_FILE.exists():
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return None


def print_status():
    """Print status of cached data."""
    metadata = get_metadata()

    if not metadata:
        log("No cached data found. Run fetch_all() first.")
        return

    log("=" * 60)
    log("Macula Dataset Status")
    log("=" * 60)
    log(f"Last updated: {metadata['last_updated']}")
    log("")
    log("Hebrew (Westminster Leningrad Codex):")
    log(f"  Files: {metadata['hebrew']['file_count']}")
    log(f"  Path: {metadata['hebrew']['path']}")
    log(f"  License: {metadata['hebrew']['license']}")
    log("")
    log("Greek (Nestle1904):")
    log(f"  Files: {metadata['greek']['file_count']}")
    log(f"  Path: {metadata['greek']['path']}")
    log(f"  License: {metadata['greek']['license']}")
    log("=" * 60)


def fetch_all():
    """Fetch both Hebrew and Greek datasets."""
    log("Starting Macula dataset fetch...")

    if not check_git():
        sys.exit(1)

    hebrew_success = fetch_hebrew()
    greek_success = fetch_greek()

    if hebrew_success and greek_success:
        save_metadata()
        log("")
        log("=" * 60)
        log("✓ All datasets fetched successfully!")
        log("=" * 60)
        print_status()
        return True
    else:
        log("")
        log("=" * 60)
        log("✗ Some datasets failed to fetch")
        log("=" * 60)
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch Macula Hebrew and Greek datasets"
    )
    parser.add_argument(
        "--hebrew-only",
        action="store_true",
        help="Fetch only Hebrew dataset"
    )
    parser.add_argument(
        "--greek-only",
        action="store_true",
        help="Fetch only Greek dataset"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status of cached datasets"
    )

    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.hebrew_only:
        if fetch_hebrew():
            save_metadata()
            print_status()
    elif args.greek_only:
        if fetch_greek():
            save_metadata()
            print_status()
    else:
        fetch_all()


if __name__ == "__main__":
    main()
