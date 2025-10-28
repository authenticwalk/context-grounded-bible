"""
Test AI models using requesty.ai API to quote Bible verses.

This script tests multiple AI models' ability to quote scripture accurately
across different languages and translations.
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from consts.verses import VERSES, get_verse_references
from consts.languages import BIBLE_VERSIONS, MODELS_TO_TEST
from database import BibleQuoteDatabase


class RequestyAIClient:
    """Client for interacting with requesty.ai API using OpenAI SDK."""

    def __init__(self, api_key: str):
        """Initialize the client with API key."""
        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://router.requesty.ai/v1"
        )

    def query_model(self, model_id: str, prompt: str,
                   max_tokens: int = 500) -> Dict[str, Any]:
        """
        Query a specific model with a prompt.

        Args:
            model_id: The model identifier with provider prefix (e.g., 'openai/gpt-4o')
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in response

        Returns:
            Dictionary with response and metadata
        """
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.1  # Low temperature for accuracy
            )

            response_time_ms = (time.time() - start_time) * 1000

            if response.choices and len(response.choices) > 0:
                return {
                    "success": True,
                    "text": response.choices[0].message.content,
                    "response_time_ms": response_time_ms,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "text": None,
                    "response_time_ms": response_time_ms,
                    "error": "No response choices found"
                }

        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return {
                "success": False,
                "text": None,
                "response_time_ms": response_time_ms,
                "error": str(e)
            }


def create_verse_quote_prompt(verse_reference: str, version_code: str,
                              version_name: str, language: str) -> str:
    """
    Create a prompt asking the model to quote a specific Bible verse.

    Args:
        verse_reference: E.g., "John 3:16"
        version_code: E.g., "NIV"
        version_name: E.g., "New International Version"
        language: E.g., "English"

    Returns:
        Formatted prompt string
    """
    prompt = f"""Please quote {verse_reference} from the {version_name} ({version_code}) Bible translation.

Language: {language}

Provide ONLY the verse text itself, without any additional commentary, explanation, or verse reference. Do not include the verse number at the beginning."""

    return prompt


def test_all_models(db: BibleQuoteDatabase, api_key: str,
                   limit_verses: Optional[int] = None,
                   limit_versions: Optional[int] = None):
    """
    Test all models across all verses and versions.

    Args:
        db: Database instance
        api_key: requesty.ai API key
        limit_verses: Limit number of verses to test (for testing)
        limit_versions: Limit number of versions to test (for testing)
    """
    client = RequestyAIClient(api_key)

    # Get verses and versions from database
    verses = db.get_verses()
    versions = db.get_bible_versions()
    models = db.get_ai_models()

    if limit_verses:
        verses = verses[:limit_verses]
    if limit_versions:
        versions = versions[:limit_versions]

    total_tests = len(models) * len(verses) * len(versions)

    print(f"\n{'='*60}")
    print(f"Testing Configuration:")
    print(f"{'='*60}")
    print(f"Models: {len(models)}")
    print(f"Verses: {len(verses)}")
    print(f"Versions: {len(versions)}")
    print(f"Total tests: {total_tests:,}")
    print(f"{'='*60}\n")

    completed = 0
    failed = 0

    for model_idx, model in enumerate(models, 1):
        print(f"\n[{model_idx}/{len(models)}] Testing model: {model['model_name']} ({model['model_id']})")

        for verse_idx, verse in enumerate(verses, 1):
            for version_idx, version in enumerate(versions, 1):
                completed += 1

                # Create prompt
                prompt = create_verse_quote_prompt(
                    verse['reference'],
                    version['code'],
                    version['name'],
                    version['language']
                )

                # Query model
                print(f"  [{completed}/{total_tests}] {verse['reference']} in {version['code']}...", end=" ")

                result = client.query_model(model['model_id'], prompt)

                # Store result
                db.insert_model_quote(
                    model_id=model['id'],
                    verse_id=verse['id'],
                    version_id=version['id'],
                    quote_text=result['text'],
                    success=result['success'],
                    response_time_ms=result['response_time_ms'],
                    error_message=result['error']
                )

                if result['success']:
                    print(f"✓ ({result['response_time_ms']:.0f}ms)")
                else:
                    print(f"✗ Error: {result['error']}")
                    failed += 1

                # Rate limiting - adjust as needed
                time.sleep(0.1)

            # Progress update
            print(f"  Progress: {verse_idx}/{len(verses)} verses completed for this model")

    print(f"\n{'='*60}")
    print(f"Testing Complete!")
    print(f"{'='*60}")
    print(f"Total tests: {completed:,}")
    print(f"Successful: {completed - failed:,}")
    print(f"Failed: {failed:,}")
    print(f"{'='*60}\n")


def populate_database(db: BibleQuoteDatabase):
    """Populate database with verses, versions, and models."""
    print("Populating database...")

    # Insert verses
    verse_ids = {}
    for ref, category, difficulty in VERSES:
        verse_id = db.insert_verse(ref, category, difficulty)
        verse_ids[ref] = verse_id

    # Insert Bible versions
    version_ids = {}
    for code, name, language, script, family, rarity in BIBLE_VERSIONS:
        version_id = db.insert_bible_version(code, name, language, script, family, rarity)
        version_ids[code] = version_id

    # Insert models
    model_ids = {}
    for model_id, provider, model_name, tier in MODELS_TO_TEST:
        mid = db.insert_ai_model(model_id, provider, model_name, tier)
        model_ids[model_id] = mid

    print(f"✓ Populated {len(verse_ids)} verses")
    print(f"✓ Populated {len(version_ids)} versions")
    print(f"✓ Populated {len(model_ids)} models")

    return verse_ids, version_ids, model_ids


def main():
    """Main function to test all models."""
    print("=" * 60)
    print("Bible Quote Accuracy Test - Model Testing")
    print("=" * 60)

    # Get API key from environment
    api_key = os.environ.get('REQUESTY_API_KEY')
    if not api_key:
        print("\n❌ Error: REQUESTY_API_KEY environment variable not set")
        print("Please set it with: export REQUESTY_API_KEY='your-api-key'")
        sys.exit(1)

    # Initialize database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"
    print(f"\nDatabase: {db_path}")

    with BibleQuoteDatabase(str(db_path)) as db:
        # Populate database
        populate_database(db)

        # Ask user if they want to limit testing (for development)
        print("\nDo you want to run a limited test first? (recommended)")
        print("This will test just a few verses and versions to verify everything works.")
        response = input("Run limited test? (y/n): ").strip().lower()

        if response == 'y':
            limit_verses = 5
            limit_versions = 3
            print(f"\nRunning limited test: {limit_verses} verses × {limit_versions} versions")
        else:
            limit_verses = None
            limit_versions = None
            print("\nRunning FULL test - this may take a long time and incur API costs!")
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Test cancelled.")
                sys.exit(0)

        # Run tests
        test_all_models(db, api_key, limit_verses, limit_versions)

        # Show statistics
        stats = db.get_statistics()
        print("\n" + "=" * 60)
        print("Database Statistics:")
        print("=" * 60)
        for key, value in stats.items():
            print(f"{key:.<40} {value:,}")

    print("\n✓ Model testing completed")
    print("\nNext step: Run the analysis script to compare results")


if __name__ == "__main__":
    main()
