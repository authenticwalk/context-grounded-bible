#!/usr/bin/env python3
"""
Demo test script - runs a small subset to demonstrate functionality.
Tests 3 verses × 2 versions × 2 models = 12 API calls
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from consts.verses import VERSES
from consts.languages import BIBLE_VERSIONS, MODELS_TO_TEST
from database import BibleQuoteDatabase
from test_models import RequestyAIClient, create_verse_quote_prompt
import time


def run_demo_test():
    """Run a small demo test."""
    print("=" * 60)
    print("Bible Quote Accuracy - DEMO TEST")
    print("=" * 60)

    # Get API key
    api_key = os.environ.get('REQUESTY_API_KEY')
    if not api_key:
        print("\n❌ Error: REQUESTY_API_KEY environment variable not set")
        sys.exit(1)

    print(f"\n✓ API key found (length: {len(api_key)})")

    # Initialize database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"

    with BibleQuoteDatabase(str(db_path)) as db:
        # Get limited test data
        verses = db.get_verses()[:3]  # Just 3 verses
        versions = db.get_bible_versions()[:2]  # Just 2 versions (NIV, NLT)

        # Get or create models - just test 2 models
        models_to_test = MODELS_TO_TEST[:2]  # First 2 models

        model_ids = []
        for model_id, provider, model_name, tier in models_to_test:
            mid = db.insert_ai_model(model_id, provider, model_name, tier)
            model_ids.append({
                'id': mid,
                'model_id': model_id,
                'model_name': model_name,
                'provider': provider
            })

        models = model_ids

        total_tests = len(verses) * len(versions) * len(models)

        print(f"\nDemo Test Configuration:")
        print(f"  Verses: {len(verses)}")
        for v in verses:
            print(f"    - {v['reference']}")
        print(f"  Versions: {len(versions)}")
        for ver in versions:
            print(f"    - {ver['name']} ({ver['code']})")
        print(f"  Models: {len(models)}")
        for m in models:
            print(f"    - {m['model_name']}")
        print(f"  Total API calls: {total_tests}")

        # Initialize client
        client = RequestyAIClient(api_key)

        completed = 0
        failed = 0

        print(f"\n{'='*60}")
        print("Running Tests...")
        print(f"{'='*60}\n")

        for model in models:
            print(f"\nTesting: {model['model_name']}")

            for verse in verses:
                for version in versions:
                    completed += 1

                    # Create prompt
                    prompt = create_verse_quote_prompt(
                        verse['reference'],
                        version['code'],
                        version['name'],
                        version['language']
                    )

                    # Query model
                    print(f"  [{completed}/{total_tests}] {verse['reference']} ({version['code']})...", end=" ", flush=True)

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
                        if result['text']:
                            preview = result['text'][:60].replace('\n', ' ')
                            print(f"      Quote: {preview}...")
                    else:
                        print(f"✗ Error: {result['error']}")
                        failed += 1

                    # Small delay to be nice to the API
                    time.sleep(0.5)

        print(f"\n{'='*60}")
        print("Demo Test Complete!")
        print(f"{'='*60}")
        print(f"Total tests: {completed}")
        print(f"Successful: {completed - failed}")
        print(f"Failed: {failed}")

        # Show stats
        stats = db.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"  Model quotes stored: {stats['total_model_quotes']}")

    print("\n✓ Demo test completed successfully!")
    print("\nNext step: Run analyze_results.py")


if __name__ == "__main__":
    run_demo_test()
