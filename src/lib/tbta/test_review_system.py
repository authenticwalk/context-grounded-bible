#!/usr/bin/env python3
"""
Test the TBTA Review Marking System

Tests the review system with real TBTA data from Genesis 1:26.
"""

import sys
from pathlib import Path
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.tbta import (
    calculate_confidence,
    create_review_metadata,
    annotate_field_with_review,
    generate_review_report,
    extract_review_items
)


def test_confidence_scoring():
    """Test confidence scoring with different features."""
    print("=" * 70)
    print("TEST 1: Confidence Scoring")
    print("=" * 70)
    print()

    test_cases = [
        {
            "name": "High Confidence: Dual Number (2 entities clear)",
            "field": "Number",
            "value": "Dual",
            "context": {"entity_count": 2, "antecedent_clear": True},
        },
        {
            "name": "Low Confidence: Trial Number (theological)",
            "field": "Number",
            "value": "Trial",
            "context": {"verse_ref": "GEN.001.026", "theological_content": True},
        },
        {
            "name": "Medium Confidence: Speaker Age (unclear context)",
            "field": "Speaker's Age",
            "value": "Young Adult (18-24)",
            "context": {"speaker_clear": False},
        },
        {
            "name": "High Confidence: Part of Speech",
            "field": "Part",
            "value": "Noun",
            "context": {},
        },
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"  Field: {test['field']} = {test['value']}")

        confidence = calculate_confidence(test['field'], test['value'], test['context'])
        needs_review = confidence < 0.95

        print(f"  Confidence: {confidence:.2f}")
        print(f"  Needs Review: {needs_review}")
        print()


def test_review_metadata():
    """Test review metadata generation."""
    print("=" * 70)
    print("TEST 2: Review Metadata Generation")
    print("=" * 70)
    print()

    # Test: GEN.1.26 Trial Number (should need review)
    context = {
        "verse_ref": "GEN.001.026",
        "theological_content": True,
        "entity_count": 3
    }

    confidence = calculate_confidence("Number", "Trial", context)
    metadata = create_review_metadata("Number", "Trial", confidence, context)

    print("Genesis 1:26 - Trial Number:")
    print(yaml.dump({"Number": "Trial", **metadata}, default_flow_style=False, sort_keys=False))
    print()


def test_field_annotation():
    """Test annotating a field with review metadata."""
    print("=" * 70)
    print("TEST 3: Field Annotation")
    print("=" * 70)
    print()

    context = {
        "verse_ref": "GEN.001.026",
        "theological_content": True
    }

    # Annotate trial number
    annotated = annotate_field_with_review("Number", "Trial", context)
    print("Annotated Trial Number:")
    print(yaml.dump(annotated, default_flow_style=False, sort_keys=False))
    print()

    # Annotate high-confidence field
    annotated2 = annotate_field_with_review("Part", "Noun", context)
    print("Annotated Part of Speech (high confidence):")
    print(yaml.dump(annotated2, default_flow_style=False, sort_keys=False))
    print()


def test_with_real_data():
    """Test with actual TBTA data structure."""
    print("=" * 70)
    print("TEST 4: Real TBTA Data Structure")
    print("=" * 70)
    print()

    # Simplified excerpt from GEN.001.026
    example_word = {
        "Constituent": "God",
        "Part": "Noun",
        "Number": "Trial",
        "Person": "First Inclusive",
        "LexicalSense": "A",
        "SemanticComplexityLevel": "1",
        "NounListIndex": "1",
        "Participant Tracking": "Routine",
        "Polarity": "Affirmative",
        "Surface Realization": "Noun"
    }

    context = {
        "verse_ref": "GEN.001.026",
        "theological_content": True,
        "entity_count": 3,
        "has_dialogue": True
    }

    print("Original Word Structure:")
    print(yaml.dump(example_word, default_flow_style=False))
    print()

    # Calculate confidence for each field
    print("Field-by-Field Confidence Analysis:")
    print("-" * 70)
    for field_name, field_value in example_word.items():
        confidence = calculate_confidence(field_name, field_value, context)
        needs_review = confidence < 0.95

        print(f"{field_name}: {field_value}")
        print(f"  → Confidence: {confidence:.2f} {'✓ High' if not needs_review else '⚠ Needs Review'}")

        if needs_review:
            metadata = create_review_metadata(field_name, field_value, confidence, context)
            print(f"  → Reason: {metadata.get('review_reason')}")
            notes = metadata.get('review_notes', '')
            if notes:
                # Truncate long notes
                notes_short = notes[:120] + "..." if len(notes) > 120 else notes
                print(f"  → Notes: {notes_short}")
        print()


def test_review_summary():
    """Test review summary generation."""
    print("=" * 70)
    print("TEST 5: Review Summary")
    print("=" * 70)
    print()

    # Create a mock annotated structure
    annotated_verse = {
        "verse": "GEN.001.026",
        "source": "tbta",
        "version": "1.0.0",
        "clauses": [
            {
                "Part": "Clause",
                "_confidence": 0.99,
                "Discourse Genre": "Climactic Narrative Story",
                "_confidence": 0.98,
                "children": [
                    {
                        "Constituent": "God",
                        "_confidence": 1.00,
                        "Number": "Trial",
                        "_confidence": 0.75,
                        "_needs_review": True,
                        "_review_reason": "theological_interpretation",
                        "_review_notes": "Trial number assumes Trinity interpretation.",
                        "_review_status": "pending"
                    }
                ]
            }
        ]
    }

    report = generate_review_report(annotated_verse)
    print(report)


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("TBTA REVIEW MARKING SYSTEM - TEST SUITE")
    print("=" * 70)
    print()

    test_confidence_scoring()
    print()

    test_review_metadata()
    print()

    test_field_annotation()
    print()

    test_with_real_data()
    print()

    test_review_summary()
    print()

    print("=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
