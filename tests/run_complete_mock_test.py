#!/usr/bin/env python3
"""
Complete mock test - simulates both baseline and model quotes.
This generates synthetic data to demonstrate the full analysis pipeline.
"""

import sys
import random
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from consts.verses import VERSES
from consts.languages import BIBLE_VERSIONS, MODELS_TO_TEST
from database import BibleQuoteDatabase


# Realistic Bible quotes for demonstration
BIBLE_QUOTES = {
    "John 3:16": {
        "NIV": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "KJV": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "NLT": "For this is how God loved the world: He gave his one and only Son, so that everyone who believes in him will not perish but have eternal life.",
        "ESV": "For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.",
        "NASB": "For God so loved the world, that He gave His only begotten Son, that whoever believes in Him shall not perish, but have eternal life.",
    },
    "Genesis 1:1": {
        "NIV": "In the beginning God created the heavens and the earth.",
        "KJV": "In the beginning God created the heaven and the earth.",
        "NLT": "In the beginning God created the heavens and the earth.",
        "ESV": "In the beginning, God created the heavens and the earth.",
        "NASB": "In the beginning God created the heavens and the earth.",
    },
    "Psalm 23:1": {
        "NIV": "The LORD is my shepherd, I lack nothing.",
        "KJV": "The LORD is my shepherd; I shall not want.",
        "NLT": "The LORD is my shepherd; I have all that I need.",
        "ESV": "The LORD is my shepherd; I shall not want.",
        "NASB": "The LORD is my shepherd, I shall not want.",
    },
    "John 14:6": {
        "NIV": "Jesus answered, \"I am the way and the truth and the life. No one comes to the Father except through me.\"",
        "KJV": "Jesus saith unto him, I am the way, the truth, and the life: no man cometh unto the Father, but by me.",
        "NLT": "Jesus told him, \"I am the way, the truth, and the life. No one can come to the Father except through me.\"",
        "ESV": "Jesus said to him, \"I am the way, and the truth, and the life. No one comes to the Father except through me.\"",
        "NASB": "Jesus said to him, \"I am the way, and the truth, and the life; no one comes to the Father but through Me.\"",
    },
    "Romans 3:23": {
        "NIV": "for all have sinned and fall short of the glory of God,",
        "KJV": "For all have sinned, and come short of the glory of God;",
        "NLT": "For everyone has sinned; we all fall short of God's glorious standard.",
        "ESV": "for all have sinned and fall short of the glory of God,",
        "NASB": "for all have sinned and fall short of the glory of God,",
    },
}


def get_baseline_quote(verse_ref, version_code):
    """Get the authoritative baseline quote."""
    if verse_ref in BIBLE_QUOTES and version_code in BIBLE_QUOTES[verse_ref]:
        return BIBLE_QUOTES[verse_ref][version_code]
    else:
        # Generate a placeholder for verses we don't have samples for
        return f"Sample authoritative quote for {verse_ref} from {version_code} translation."


def generate_model_quote(baseline_quote, model_name, tier, difficulty):
    """
    Generate a model quote based on baseline with realistic variations.

    High-tier models are more accurate.
    Easy verses are quoted more accurately than hard ones.
    """
    # Calculate accuracy probability
    is_high_tier = tier == "high"
    base_accuracy = 0.92 if is_high_tier else 0.78
    difficulty_penalty = difficulty * 0.03  # Each difficulty level reduces accuracy by 3%
    accuracy = max(0.4, base_accuracy - difficulty_penalty)

    # Perfect quote
    if random.random() < accuracy:
        return baseline_quote

    # Near-perfect (small variations)
    if random.random() < 0.7:
        variations = [
            baseline_quote.replace("the", "a", 1),  # Single article change
            baseline_quote.replace(",", "", 1),  # Remove one comma
            baseline_quote.replace(".", "!"),  # Emphasis change
            baseline_quote.replace("  ", " "),  # Spacing
            baseline_quote.lower(),  # Case change
            baseline_quote.replace("LORD", "Lord"),  # Capitalization
            baseline_quote.replace(" and ", " & "),  # Symbol substitution
            baseline_quote + " ",  # Extra space
        ]
        return random.choice(variations)

    # Moderate differences
    if random.random() < 0.5:
        return baseline_quote[:int(len(baseline_quote) * 0.9)]  # Truncated

    # Significant differences (paraphrase or wrong quote)
    paraphrases = [
        f"This verse says that {baseline_quote[:50]}...",
        f"According to this passage: {baseline_quote}",
        f"The Bible states: {baseline_quote}",
        baseline_quote.replace("God", "the Lord").replace("Lord", "God"),
    ]
    return random.choice(paraphrases)


def run_complete_mock_test():
    """Run a complete mock test with baseline and model quotes."""
    print("=" * 70)
    print("Bible Quote Accuracy - COMPLETE MOCK TEST")
    print("=" * 70)
    print("\nGenerating baseline + model data for full pipeline demonstration\n")

    # Clear existing database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"
    if db_path.exists():
        print(f"Removing existing database: {db_path}")
        db_path.unlink()

    with BibleQuoteDatabase(str(db_path)) as db:
        # Get test data
        num_verses = 30  # 30 verses for a good sample
        num_versions = 5  # 5 versions

        # Insert verses
        print("Populating database...")
        verse_ids = []
        for ref, category, difficulty in VERSES[:num_verses]:
            vid = db.insert_verse(ref, category, difficulty)
            verse_ids.append({'id': vid, 'ref': ref, 'category': category, 'difficulty': difficulty})

        # Insert versions
        version_ids = []
        for code, name, language, script, family, rarity in BIBLE_VERSIONS[:num_versions]:
            vid = db.insert_bible_version(code, name, language, script, family, rarity)
            version_ids.append({'id': vid, 'code': code, 'name': name, 'language': language})

        # Insert models
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

        verses = verse_ids
        versions = version_ids
        models = model_ids

        print(f"✓ Inserted {len(verses)} verses")
        print(f"✓ Inserted {len(versions)} versions")
        print(f"✓ Inserted {len(models)} models")

        # Generate baseline quotes
        print(f"\n{'='*70}")
        print("Generating Baseline Quotes...")
        print(f"{'='*70}\n")

        baseline_count = 0
        for verse in verses:
            for version in versions:
                baseline_quote = get_baseline_quote(verse['ref'], version['code'])
                db.insert_baseline_quote(
                    verse_id=verse['id'],
                    version_id=version['id'],
                    quote_text=baseline_quote,
                    success=True
                )
                baseline_count += 1

        print(f"✓ Generated {baseline_count} baseline quotes")

        # Generate model quotes
        total_tests = len(verses) * len(versions) * len(models)

        print(f"\n{'='*70}")
        print("Generating Model Quotes...")
        print(f"{'='*70}")
        print(f"Total tests: {total_tests:,}\n")

        completed = 0

        for model in models:
            print(f"\nSimulating: {model['model_name']} ({model['tier']} tier)")

            for verse in verses:
                # Get baseline for this verse
                for version in versions:
                    completed += 1

                    baseline_quote = get_baseline_quote(verse['ref'], version['code'])

                    # Generate model quote
                    model_quote = generate_model_quote(
                        baseline_quote,
                        model['model_name'],
                        model['tier'],
                        verse['difficulty']
                    )

                    # Simulate response time
                    base_time = 700 if model['tier'] == 'low' else 1100
                    response_time = base_time + random.randint(-150, 350)

                    # 99% success rate
                    success = random.random() < 0.99

                    # Store result
                    db.insert_model_quote(
                        model_id=model['id'],
                        verse_id=verse['id'],
                        version_id=version['id'],
                        quote_text=model_quote if success else None,
                        success=success,
                        response_time_ms=response_time if success else None,
                        error_message=None if success else "Timeout"
                    )

                    if completed % 100 == 0:
                        print(f"  Progress: {completed:,}/{total_tests:,} ({completed/total_tests*100:.1f}%)")

        print(f"\n{'='*70}")
        print("Data Generation Complete!")
        print(f"{'='*70}")

        # Show stats
        stats = db.get_statistics()
        print(f"\nDatabase Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value:,}")

    print("\n✓ Complete mock test finished!")
    print("\nNext steps:")
    print("  1. Run: python analyze_results.py")
    print("  2. Run: python generate_report.py")


if __name__ == "__main__":
    run_complete_mock_test()
