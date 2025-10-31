"""
TBTA Confidence Scorer

Assigns confidence scores to generated TBTA annotations based on:
- Feature type (Tier 1/2/3)
- Context analysis
- Edge case detection
"""

from typing import Dict, Any, Optional
from enum import Enum


class FeatureTier(Enum):
    """Feature confidence tiers based on reproduction accuracy."""
    TIER_1 = "tier_1"  # 95-100% accuracy: Auto-approve
    TIER_2 = "tier_2"  # 80-95% accuracy: May need review
    TIER_3 = "tier_3"  # <80% accuracy: Always review


# Base confidence scores for each TBTA field
BASE_CONFIDENCE = {
    # Tier 1: High confidence (95-100%)
    "Constituent": 1.00,
    "Part": 0.99,
    "NounListIndex": 0.99,
    "SemanticComplexityLevel": 1.00,  # Always '1' in TBTA
    "Clusivity": 0.98,
    "Number": 0.97,  # Singular/Plural/Dual
    "Sequence": 0.98,
    "Implicit": 0.98,  # When value is 'No'
    "Relativized": 0.99,  # When value is 'No'
    "Aspect": 0.98,  # Almost always 'Unmarked'
    "Discourse Genre": 0.98,  # Almost always 'Climactic Narrative Story'

    # Tier 2: Medium confidence (80-95%)
    "Participant Tracking": 0.85,
    "Speaker Demographics": 0.88,
    "Speaker": 0.88,
    "Listener": 0.88,
    "Speaker's Attitude": 0.85,
    "Speaker's Age": 0.82,
    "Speaker-Listener Age": 0.83,
    "Proximity": 0.82,
    "Time": 0.80,
    "Illocutionary Force": 0.90,
    "Semantic Role": 0.87,
    "Topic NP": 0.86,
    "Polarity": 0.95,
    "Mood": 0.88,
    "Surface Realization": 0.90,
    "Type": 0.89,  # Clause type
    "Usage": 0.90,  # Adjective usage
    "Degree": 0.92,  # Adjective/Adverb degree
    "Adjective Degree": 0.98,  # On verbs, always 'No Degree'

    # Tier 3: Low confidence (<80%)
    "Number-Trial": 0.75,  # Special case: Trial number
    "Number-Quadrial": 0.70,  # Special case: Quadrial number
    "LexicalSense": 0.65,
    "Vocabulary Alternate": 0.70,
    "Alternative Analysis": 0.60,
    "Rhetorical Question": 0.75,
    "Salience Band": 0.78,
    "Location": 0.80,
    "Implicit Information": 0.72,
}

# Field tier classification
FIELD_TIERS = {
    FeatureTier.TIER_1: [
        "Constituent", "Part", "NounListIndex", "SemanticComplexityLevel",
        "Clusivity", "Number", "Sequence", "Relativized", "Aspect",
        "Discourse Genre", "Adjective Degree", "Implicit", "Polarity"
    ],
    FeatureTier.TIER_2: [
        "Participant Tracking", "Speaker", "Listener", "Speaker's Attitude",
        "Speaker's Age", "Speaker-Listener Age", "Proximity", "Time",
        "Illocutionary Force", "Semantic Role", "Topic NP", "Mood",
        "Surface Realization", "Type", "Usage", "Degree"
    ],
    FeatureTier.TIER_3: [
        "LexicalSense", "Vocabulary Alternate", "Alternative Analysis",
        "Rhetorical Question", "Salience Band", "Location", "Implicit Information"
    ]
}


class ConfidenceAdjustment:
    """Context-based confidence adjustments."""

    # Adjustment amounts
    THEOLOGICAL = -0.20
    CULTURAL = -0.15
    AMBIGUOUS = -0.15
    MISSING_CONTEXT = -0.10
    RARE_FEATURE = -0.10
    EDGE_CASE = -0.12

    # Boost for clear cases
    CLEAR_CONTEXT = +0.05
    CORPUS_VALIDATED = +0.05


def get_base_confidence(field_name: str, field_value: Any = None) -> float:
    """
    Get base confidence score for a field.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field (for special cases)

    Returns:
        Base confidence score (0.0 - 1.0)
    """
    # Special case: Trial/Quadrial number
    if field_name == "Number" and field_value in ["Trial", "Quadrial", "Paucal"]:
        return BASE_CONFIDENCE.get(f"Number-{field_value}", 0.75)

    # Default lookup
    return BASE_CONFIDENCE.get(field_name, 0.75)


def get_feature_tier(field_name: str, field_value: Any = None) -> FeatureTier:
    """
    Get the tier classification for a field.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field (for special cases)

    Returns:
        Feature tier
    """
    # Special case: rare number values
    if field_name == "Number" and field_value in ["Trial", "Quadrial", "Paucal"]:
        return FeatureTier.TIER_3

    # Check tier assignments
    for tier, fields in FIELD_TIERS.items():
        if field_name in fields:
            return tier

    # Default to Tier 2
    return FeatureTier.TIER_2


def calculate_confidence(
    field_name: str,
    field_value: Any,
    context: Optional[Dict[str, Any]] = None
) -> float:
    """
    Calculate confidence score for a field with context adjustments.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field
        context: Optional context dictionary with:
            - verse_ref: Verse reference (e.g., "GEN.001.026")
            - discourse_type: Type of discourse
            - has_dialogue: Boolean
            - speaker_clear: Boolean
            - temporal_markers: Boolean
            - entity_count: Number of entities
            - antecedent_clear: Boolean
            - theological_content: Boolean
            - etc.

    Returns:
        Adjusted confidence score (0.0 - 1.0)
    """
    context = context or {}

    # Get base confidence
    confidence = get_base_confidence(field_name, field_value)

    # Apply context-specific adjustments

    # 1. Theological interpretation required
    if context.get("theological_content") and field_name in ["Number", "Person"]:
        if field_value in ["Trial", "First Inclusive"] and "GEN.001.026" in context.get("verse_ref", ""):
            confidence += ConfidenceAdjustment.THEOLOGICAL

    # 2. Speaker demographics unclear
    if field_name in ["Speaker's Age", "Speaker-Listener Age", "Speaker's Attitude"]:
        if not context.get("speaker_clear"):
            confidence += ConfidenceAdjustment.MISSING_CONTEXT
        if not context.get("has_dialogue"):
            confidence += ConfidenceAdjustment.CULTURAL

    # 3. Ambiguous reference
    if field_name in ["Participant Tracking", "NounListIndex"]:
        if not context.get("antecedent_clear"):
            confidence += ConfidenceAdjustment.AMBIGUOUS

    # 4. Time granularity unclear
    if field_name == "Time":
        if not context.get("temporal_markers"):
            confidence += ConfidenceAdjustment.AMBIGUOUS
        # Boundary cases
        if field_value in ["Earlier Today", "A Week Ago", "A Month Ago"]:
            if not context.get("chronology_clear"):
                confidence += ConfidenceAdjustment.AMBIGUOUS

    # 5. Rare feature usage
    if field_value in ["Trial", "Quadrial", "Paucal"]:
        confidence += ConfidenceAdjustment.RARE_FEATURE

    # 6. Proximity unclear
    if field_name == "Proximity":
        if not context.get("spatial_context_clear"):
            confidence += ConfidenceAdjustment.AMBIGUOUS

    # 7. Illocutionary force edge cases
    if field_name == "Illocutionary Force":
        if field_value == "Rhetorical Question":
            confidence += ConfidenceAdjustment.EDGE_CASE
        if context.get("indirect_speech_act"):
            confidence += ConfidenceAdjustment.AMBIGUOUS

    # Boost for clear cases
    if context.get("corpus_validated"):
        confidence += ConfidenceAdjustment.CORPUS_VALIDATED
    if context.get("clear_context"):
        confidence += ConfidenceAdjustment.CLEAR_CONTEXT

    # Clamp to [0.0, 1.0]
    return max(0.0, min(1.0, confidence))


def requires_review(confidence: float, threshold: float = 0.95) -> bool:
    """
    Determine if a field needs human review based on confidence.

    Args:
        confidence: Confidence score
        threshold: Review threshold (default 0.95)

    Returns:
        True if review needed
    """
    return confidence < threshold


def get_confidence_category(confidence: float) -> str:
    """
    Get human-readable confidence category.

    Args:
        confidence: Confidence score

    Returns:
        Category string
    """
    if confidence >= 0.95:
        return "high"
    elif confidence >= 0.80:
        return "medium"
    elif confidence >= 0.60:
        return "low"
    else:
        return "very_low"


# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        {
            "field": "Number",
            "value": "Dual",
            "context": {"entity_count": 2, "antecedent_clear": True},
            "expected": "high"
        },
        {
            "field": "Number",
            "value": "Trial",
            "context": {"verse_ref": "GEN.001.026", "theological_content": True},
            "expected": "low"
        },
        {
            "field": "Speaker's Age",
            "value": "Young Adult (18-24)",
            "context": {"speaker_clear": False},
            "expected": "medium"
        },
        {
            "field": "Participant Tracking",
            "value": "Routine",
            "context": {"antecedent_clear": False},
            "expected": "medium"
        }
    ]

    print("Confidence Scorer Test Cases:\n")
    for i, test in enumerate(test_cases, 1):
        conf = calculate_confidence(test["field"], test["value"], test["context"])
        cat = get_confidence_category(conf)
        review = requires_review(conf)

        print(f"Test {i}: {test['field']} = {test['value']}")
        print(f"  Confidence: {conf:.2f} ({cat})")
        print(f"  Needs Review: {review}")
        print(f"  Expected: {test['expected']}")
        print()
