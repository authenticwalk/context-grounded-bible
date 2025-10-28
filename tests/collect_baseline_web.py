#!/usr/bin/env python3
"""
Collect baseline Bible quotes using bible-api.com (free API).

This is a simpler approach than using a skill, directly calling the API.
"""

import sys
import os
import requests
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from consts.verses import VERSES
from consts.languages import BIBLE_VERSIONS
from database import BibleQuoteDatabase


# Mapping of our version codes to bible-api.com translation codes
# bible-api.com supports: kjv (default), web, bbe, clementine, almeida, rccv
VERSION_MAP = {
    "KJV": "kjv",
    "WEB": "web",
    # Other versions we'll skip for baseline (will compare models to each other)
}


def fetch_verse_from_api(reference: str, translation: str = "kjv") -> dict:
    """
    Fetch a verse from bible-api.com.

    Args:
        reference: Verse reference (e.g., "John 3:16")
        translation: Translation code (kjv, web, etc.)

    Returns:
        Dictionary with verse data or error
    """
    try:
        url = f"https://bible-api.com/{reference}?translation={translation}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "text": data.get("text", "").strip(),
                "reference": data.get("reference", reference),
                "translation": data.get("translation_id", translation),
                "error": None
            }
        else:
            return {
                "success": False,
                "text": None,
                "reference": reference,
                "translation": translation,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "text": None,
            "reference": reference,
            "translation": translation,
            "error": str(e)
        }


def collect_baselines(num_verses=10):
    """Collect baseline quotes for a limited set of verses and versions."""
    print("=" * 70)
    print("Bible Quote Baseline Collection - Using bible-api.com")
    print("=" * 70)

    db_path = Path(__file__).parent / "bible_quote_accuracy.db"

    with BibleQuoteDatabase(str(db_path)) as db:
        # Get verses and versions
        verses = db.get_verses()[:num_verses]
        versions = db.get_bible_versions()

        print(f"\nCollecting baselines for {len(verses)} verses...")
        print("Supported versions: KJV, WEB")

        collected = 0
        skipped = 0

        for verse in verses:
            print(f"\n{verse['reference']}:")

            for version in versions:
                # Only collect for supported versions
                if version['code'] not in VERSION_MAP:
                    skipped += 1
                    continue

                api_translation = VERSION_MAP[version['code']]

                print(f"  {version['code']:.<10} ", end="", flush=True)

                # Fetch from API
                result = fetch_verse_from_api(verse['reference'], api_translation)

                if result['success']:
                    # Store in database
                    db.insert_baseline_quote(
                        verse_id=verse['id'],
                        version_id=version['id'],
                        quote_text=result['text'],
                        success=True
                    )
                    collected += 1
                    preview = result['text'][:50].replace('\n', ' ')
                    print(f"✓ {preview}...")
                else:
                    db.insert_baseline_quote(
                        verse_id=verse['id'],
                        version_id=version['id'],
                        quote_text=None,
                        success=False,
                        error_message=result['error']
                    )
                    print(f"✗ {result['error']}")

                # Be nice to the API
                time.sleep(0.2)

        print(f"\n{'='*70}")
        print(f"Baseline Collection Complete")
        print(f"{'='*70}")
        print(f"Collected: {collected}")
        print(f"Skipped (unsupported versions): {skipped}")

        # Show stats
        stats = db.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"  Total baseline quotes: {stats['total_baseline_quotes']}")


if __name__ == "__main__":
    num_verses = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    collect_baselines(num_verses)
