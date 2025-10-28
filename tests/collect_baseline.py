"""
Collect baseline Bible quotes using the quote-bible skill.

Note: This script assumes a 'quote-bible' skill is available. If not available,
you can modify this to use a Bible API like api.scripture.api.bible or similar.
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from consts.verses import VERSES, get_verse_references
from consts.languages import BIBLE_VERSIONS, get_version_codes
from database import BibleQuoteDatabase


def parse_verse_reference(reference: str) -> dict:
    """Parse a verse reference into book, chapter, and verse components."""
    # Simple parser - could be enhanced
    parts = reference.split()

    # Handle multi-word book names
    if len(parts) >= 2:
        # Check if first word is a number
        if parts[0].isdigit():
            book = f"{parts[0]} {parts[1]}"
            chapter_verse = parts[2] if len(parts) > 2 else ""
        else:
            # Find where the numbers start
            book_parts = []
            chapter_verse = ""
            for i, part in enumerate(parts):
                if any(char.isdigit() for char in part):
                    chapter_verse = " ".join(parts[i:])
                    break
                book_parts.append(part)
            book = " ".join(book_parts)

    # Parse chapter:verse
    if ':' in chapter_verse:
        chapter, verse = chapter_verse.split(':')
        verse = verse.replace(',', '').strip()  # Remove any commas
    else:
        chapter = chapter_verse
        verse = ""

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "reference": reference
    }


def collect_baseline_quotes_from_skill(db: BibleQuoteDatabase):
    """
    Collect baseline quotes using the quote-bible skill.

    NOTE: This function is a placeholder. The quote-bible skill needs to be
    implemented or this should be replaced with a Bible API integration.
    """
    print("Collecting baseline quotes using quote-bible skill...")
    print("NOTE: quote-bible skill integration needs to be implemented.")
    print("Alternative: Use a Bible API like api.scripture.api.bible")

    # For now, just populate the database structure
    verses = VERSES
    versions = BIBLE_VERSIONS

    print(f"\nPopulating database with {len(verses)} verses and {len(versions)} versions...")

    # Insert verses
    verse_ids = {}
    for ref, category, difficulty in verses:
        verse_id = db.insert_verse(ref, category, difficulty)
        verse_ids[ref] = verse_id

    # Insert Bible versions
    version_ids = {}
    for code, name, language, script, family, rarity in versions:
        version_id = db.insert_bible_version(code, name, language, script, family, rarity)
        version_ids[code] = version_id

    print(f"✓ Inserted {len(verse_ids)} verses")
    print(f"✓ Inserted {len(version_ids)} Bible versions")

    # Placeholder for actual skill calls
    print("\nTo collect baseline quotes, you would:")
    print("1. Call the quote-bible skill for each verse+version combination")
    print("2. Store the results using db.insert_baseline_quote()")
    print(f"\nTotal combinations to collect: {len(verses)} verses × {len(versions)} versions = {len(verses) * len(versions)}")

    return verse_ids, version_ids


def collect_baseline_quotes_from_api(db: BibleQuoteDatabase, api_key: str = None):
    """
    Alternative: Collect baseline quotes using a Bible API.

    This is a more practical approach if quote-bible skill is not available.
    Could use apis like:
    - https://scripture.api.bible
    - https://api.esv.org
    - https://labs.bible.org/api_web_service
    """
    print("Collecting baseline quotes using Bible API...")
    print("NOTE: This requires API integration to be implemented.")
    print("Recommended API: https://scripture.api.bible (requires free API key)")

    # This is a placeholder for API integration
    # You would implement actual API calls here

    pass


def main():
    """Main function to collect baseline quotes."""
    print("=" * 60)
    print("Bible Quote Accuracy Test - Baseline Collection")
    print("=" * 60)

    # Initialize database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"
    print(f"\nDatabase: {db_path}")

    with BibleQuoteDatabase(str(db_path)) as db:
        # Collect baseline quotes
        verse_ids, version_ids = collect_baseline_quotes_from_skill(db)

        # Show statistics
        stats = db.get_statistics()
        print("\n" + "=" * 60)
        print("Database Statistics:")
        print("=" * 60)
        for key, value in stats.items():
            print(f"{key:.<40} {value}")

    print("\n✓ Baseline collection script completed")
    print("\nNext steps:")
    print("1. Implement quote-bible skill integration OR")
    print("2. Integrate with a Bible API like scripture.api.bible")
    print("3. Run the requesty.ai model testing script")


if __name__ == "__main__":
    main()
