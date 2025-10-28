#!/usr/bin/env python3
"""
Mock test script - simulates API responses to demonstrate the full pipeline.
This generates synthetic data to show how the analysis and reporting works.
"""

import sys
import random
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from consts.verses import VERSES
from consts.languages import BIBLE_VERSIONS, MODELS_TO_TEST
from database import BibleQuoteDatabase
import time


# Sample Bible quotes for demonstration
SAMPLE_QUOTES = {
    "John 3:16": {
        "NIV": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "KJV": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "NLT": "For this is how God loved the world: He gave his one and only Son, so that everyone who believes in him will not perish but have eternal life.",
    },
    "Genesis 1:1": {
        "NIV": "In the beginning God created the heavens and the earth.",
        "KJV": "In the beginning God created the heaven and the earth.",
        "NLT": "In the beginning God created the heavens and the earth.",
    },
    "Psalm 23:1": {
        "NIV": "The LORD is my shepherd, I lack nothing.",
        "KJV": "The LORD is my shepherd; I shall not want.",
        "NLT": "The LORD is my shepherd; I have all that I need.",
    },
}


def generate_mock_quote(verse_ref, version_code, model_name, difficulty):
    """
    Generate a mock Bible quote with some variation to simulate model differences.

    High-tier models get more accurate quotes.
    Easy verses are quoted more accurately than hard ones.
    """
    # Base quote
    if verse_ref in SAMPLE_QUOTES and version_code in SAMPLE_QUOTES[verse_ref]:
        base_quote = SAMPLE_QUOTES[verse_ref][version_code]
    else:
        # Generic placeholder for verses we don't have samples for
        base_quote = f"[Sample quote for {verse_ref} from {version_code} translation]"

    # Simulate accuracy based on model tier and verse difficulty
    is_high_tier = "pro" in model_name.lower() or "max" in model_name.lower() or "sonnet" in model_name.lower() or "exp" in model_name.lower() or "70b" in model_name.lower() or "reasoner" in model_name.lower()

    # Calculate accuracy probability
    base_accuracy = 0.95 if is_high_tier else 0.85
    difficulty_penalty = difficulty * 0.02  # Each difficulty level reduces accuracy by 2%
    accuracy = max(0.5, base_accuracy - difficulty_penalty)

    # Random chance of perfect quote
    if random.random() < accuracy:
        return base_quote

    # Introduce some variations to simulate imperfect recall
    variations = [
        base_quote.replace("the", "a"),  # Article substitution
        base_quote.replace(",", ""),  # Punctuation changes
        base_quote.replace("shall", "will"),  # Word modernization
        base_quote.replace(".", "!"),  # Emphasis changes
        base_quote + " (Approximate)",  # Hedging
        base_quote.replace("LORD", "Lord"),  # Capitalization
    ]

    # For harder verses or lower-tier models, might return paraphrase
    if difficulty > 7 or (not is_high_tier and random.random() < 0.2):
        return f"[Paraphrase of {verse_ref}]"

    return random.choice([base_quote] + variations)


def run_mock_test():
    """Run a mock test with simulated data."""
    print("=" * 70)
    print("Bible Quote Accuracy - MOCK TEST (Simulated Data)")
    print("=" * 70)
    print("\nNOTE: This uses simulated data to demonstrate the analysis pipeline.")
    print("In production, this would query real AI models via requesty.ai API.\n")

    # Initialize database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"

    with BibleQuoteDatabase(str(db_path)) as db:
        # Get test data - use more for a realistic demo
        verses = db.get_verses()[:20]  # 20 verses
        versions = db.get_bible_versions()[:5]  # 5 versions

        # Insert all models
        model_ids = []
        for model_id, provider, model_name, tier in MODELS_TO_TEST:
            mid = db.insert_ai_model(model_id, provider, model_name, tier)
            model_ids.append({
                'id': mid,
                'model_id': model_id,
                'model_name': model_name,
                'provider': provider,
                'tier': tier
            })

        models = model_ids

        total_tests = len(verses) * len(versions) * len(models)

        print(f"Mock Test Configuration:")
        print(f"  Verses: {len(verses)}")
        print(f"  Versions: {len(versions)}")
        for ver in versions:
            print(f"    - {ver['name']} ({ver['code']})")
        print(f"  Models: {len(models)}")
        for m in models:
            print(f"    - {m['model_name']} ({m['provider']}, {m['tier']} tier)")
        print(f"  Total tests: {total_tests:,}")

        completed = 0

        print(f"\n{'='*70}")
        print("Generating Mock Data...")
        print(f"{'='*70}\n")

        for model in models:
            print(f"\nSimulating: {model['model_name']}")

            for verse in verses:
                for version in versions:
                    completed += 1

                    # Generate mock quote
                    mock_quote = generate_mock_quote(
                        verse['reference'],
                        version['code'],
                        model['model_name'],
                        verse['difficulty_score']
                    )

                    # Simulate response time (faster for smaller models)
                    base_time = 800 if model['tier'] == 'low' else 1200
                    response_time = base_time + random.randint(-200, 400)

                    # 98% success rate
                    success = random.random() < 0.98

                    # Store result
                    db.insert_model_quote(
                        model_id=model['id'],
                        verse_id=verse['id'],
                        version_id=version['id'],
                        quote_text=mock_quote if success else None,
                        success=success,
                        response_time_ms=response_time if success else None,
                        error_message=None if success else "Simulated timeout"
                    )

                    if completed % 50 == 0:
                        print(f"  Progress: {completed:,}/{total_tests:,} ({completed/total_tests*100:.1f}%)")

        print(f"\n{'='*70}")
        print("Mock Data Generation Complete!")
        print(f"{'='*70}")
        print(f"Total tests generated: {completed:,}")

        # Show stats
        stats = db.get_statistics()
        print(f"\nDatabase Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value:,}")

    print("\n✓ Mock test completed successfully!")
    print("\nNext steps:")
    print("  1. Run: python analyze_results.py")
    print("  2. Run: python generate_report.py")


if __name__ == "__main__":
    run_mock_test()
