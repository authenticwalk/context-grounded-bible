"""
TBTA Review Metadata Generator

Generates review reasons and notes for TBTA annotations that need human review.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ReviewReason(Enum):
    """Categorical review reasons."""
    LOW_CONFIDENCE = "low_confidence"
    THEOLOGICAL = "theological_interpretation"
    CULTURAL = "cultural_context"
    AMBIGUOUS_REF = "ambiguous_reference"
    TEMPORAL_AMB = "temporal_ambiguity"
    MULTIPLE_VALID = "multiple_valid_interpretations"
    RARE_FEATURE = "rare_feature"
    MISSING_CONTEXT = "missing_context"
    EDGE_CASE = "edge_case"
    CORPUS_MISMATCH = "corpus_mismatch"


class ReviewStatus(Enum):
    """Review status values."""
    PENDING = "pending"
    APPROVED = "approved"
    CORRECTED = "corrected"
    REJECTED = "rejected"
    SKIPPED = "skipped"


def determine_review_reason(
    field_name: str,
    field_value: Any,
    confidence: float,
    context: Optional[Dict[str, Any]] = None
) -> Optional[ReviewReason]:
    """
    Determine the primary reason why a field needs review.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field
        confidence: Confidence score
        context: Optional context dictionary

    Returns:
        ReviewReason or None if no review needed
    """
    context = context or {}

    # If high confidence, no review needed
    if confidence >= 0.95:
        return None

    # Priority order (most specific to least specific)

    # 1. Theological interpretation
    if field_name == "Number" and field_value in ["Trial", "Quadrial"]:
        if "GEN.001.026" in context.get("verse_ref", ""):
            return ReviewReason.THEOLOGICAL
        return ReviewReason.RARE_FEATURE

    if field_name == "Person" and field_value == "First Inclusive":
        if context.get("theological_content"):
            return ReviewReason.THEOLOGICAL

    # 2. Multiple valid interpretations
    if field_name == "Alternative Analysis":
        return ReviewReason.MULTIPLE_VALID

    if field_name == "Vocabulary Alternate":
        return ReviewReason.MULTIPLE_VALID

    # 3. Cultural context required
    if field_name in ["Speaker's Age", "Speaker-Listener Age"]:
        if not context.get("speaker_clear"):
            return ReviewReason.MISSING_CONTEXT
        return ReviewReason.CULTURAL

    if field_name == "Speaker's Attitude":
        return ReviewReason.CULTURAL

    # 4. Ambiguous reference
    if field_name == "Participant Tracking":
        if not context.get("antecedent_clear"):
            return ReviewReason.AMBIGUOUS_REF

    if field_name == "NounListIndex":
        if context.get("multiple_antecedents"):
            return ReviewReason.AMBIGUOUS_REF

    # 5. Temporal ambiguity
    if field_name == "Time":
        if field_value in ["Earlier Today", "Yesterday", "A Week Ago"]:
            if not context.get("chronology_clear"):
                return ReviewReason.TEMPORAL_AMB

    # 6. Proximity ambiguity
    if field_name == "Proximity":
        if not context.get("spatial_context_clear"):
            return ReviewReason.AMBIGUOUS_REF

    # 7. Rhetorical question
    if field_name == "Rhetorical Question":
        return ReviewReason.EDGE_CASE

    if field_name == "Illocutionary Force":
        if context.get("indirect_speech_act"):
            return ReviewReason.EDGE_CASE

    # 8. Lexical sense
    if field_name == "LexicalSense":
        return ReviewReason.LOW_CONFIDENCE  # Requires lexicon

    # 9. Missing context
    if field_name in ["Speaker", "Listener"]:
        if not context.get("has_dialogue"):
            return ReviewReason.MISSING_CONTEXT

    # 10. Corpus mismatch
    if context.get("corpus_mismatch"):
        return ReviewReason.CORPUS_MISMATCH

    # 11. Rare feature
    if field_value in ["Trial", "Quadrial", "Paucal"]:
        return ReviewReason.RARE_FEATURE

    # Default: low confidence
    if confidence < 0.80:
        return ReviewReason.LOW_CONFIDENCE

    # No specific reason, but confidence below threshold
    return ReviewReason.LOW_CONFIDENCE


def generate_review_notes(
    field_name: str,
    field_value: Any,
    review_reason: Optional[ReviewReason],
    context: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """
    Generate human-readable review notes.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field
        review_reason: Why review is needed
        context: Optional context dictionary

    Returns:
        Review notes string or None
    """
    if review_reason is None:
        return None

    context = context or {}
    verse_ref = context.get("verse_ref", "")

    # Generate notes based on reason
    notes_templates = {
        ReviewReason.THEOLOGICAL: {
            "Number-Trial": f"Trial number (exactly 3) in {verse_ref} assumes Trinity interpretation of 'Let us make'. Alternative interpretations: pluralis maiestatis (royal we) or divine council. Verify with theological commentary and original language analysis.",
            "Person-First Inclusive": f"First Inclusive in {verse_ref} assumes Trinity members addressing each other (all included). Depends on Trial number interpretation and theological framework.",
            "default": f"This field requires theological interpretation. Verify with theological commentary for {verse_ref}."
        },
        ReviewReason.CULTURAL: {
            "Speaker's Age": f"Age estimate '{field_value}' is based on narrative context. Cultural and historical context may affect age category assignment. Verify with broader narrative analysis.",
            "Speaker's Attitude": f"Attitude '{field_value}' is based on tone and word choice. Cultural norms for expressing {field_value.lower()} may vary. Verify appropriateness for target languages.",
            "Speaker-Listener Age": f"Relative age '{field_value}' may affect honorific language choice. Verify speaker and listener identities from narrative context.",
            "default": f"This field depends on cultural context. Verify interpretation for {verse_ref}."
        },
        ReviewReason.AMBIGUOUS_REF: {
            "Participant Tracking": f"Participant tracking '{field_value}' assignment unclear. Multiple possible antecedents or unclear discourse flow. Check entity tracking across verse boundaries.",
            "NounListIndex": f"Entity reference unclear. {context.get('ambiguity_note', 'Multiple possible referents')}. Verify discourse entity tracking.",
            "Proximity": f"Proximity '{field_value}' unclear from context. Spatial or temporal reference may be ambiguous. Check narrative perspective and deixis.",
            "default": f"Reference is ambiguous. Verify intended referent from discourse context."
        },
        ReviewReason.TEMPORAL_AMB: {
            "Time": f"Time reference '{field_value}' is on a boundary case. Narrative chronology may need verification. Check for temporal markers in surrounding context.",
            "default": f"Temporal reference is ambiguous. Verify timing from narrative context."
        },
        ReviewReason.MULTIPLE_VALID: {
            "Alternative Analysis": f"Multiple valid linguistic analyses exist for this clause. TBTA provides alternatives: {field_value}. Choose based on target language requirements.",
            "Vocabulary Alternate": f"TBTA provides {field_value} for different complexity levels. Choose based on target audience (simple vocabulary for oral contexts, complex for literate audiences).",
            "default": f"Multiple valid interpretations exist. Choose based on translation goals and target language."
        },
        ReviewReason.RARE_FEATURE: {
            "Number-Trial": f"Trial number is rare (found in <10 languages). Verify count is exactly 3 entities, not generic plural. Languages with trial: Kilivila, Larike, Marshallese, Biak, etc.",
            "Number-Quadrial": f"Quadrial number is very rare. Verify count is exactly 4 entities. Languages with quadrial: Sursurunga, Marshallese.",
            "Number-Paucal": f"Paucal number ('a few', typically 3-5) is rare. Verify count is small but plural. Languages with paucal: Murrinh-patha, Lihir, Sursurunga.",
            "default": f"Rare feature: {field_name} = {field_value}. Verify usage is appropriate and not an error."
        },
        ReviewReason.MISSING_CONTEXT: {
            "Speaker's Age": f"Speaker age '{field_value}' cannot be determined from immediate context. Check broader narrative for speaker identity and life stage.",
            "Speaker-Listener Age": f"Relative age '{field_value}' unclear from context. Verify speaker and listener identities, then determine age relationship.",
            "Speaker": f"Speaker identity '{field_value}' unclear. Verify from dialogue markers and narrative context.",
            "Listener": f"Listener identity '{field_value}' unclear. Verify from dialogue markers and narrative context.",
            "default": f"Insufficient context to determine {field_name}. Verify from broader discourse context."
        },
        ReviewReason.EDGE_CASE: {
            "Rhetorical Question": f"Rhetorical question with value '{field_value}'. Verify pragmatic interpretation and expected answer.",
            "Illocutionary Force": f"Speech act '{field_value}' may be indirect. Verify illocutionary force from context and pragmatic interpretation.",
            "default": f"Edge case detected for {field_name} = {field_value}. Verify interpretation."
        },
        ReviewReason.CORPUS_MISMATCH: {
            "default": f"eBible corpus translations use unexpected form. {context.get('corpus_note', 'Verify expected usage pattern')}."
        },
        ReviewReason.LOW_CONFIDENCE: {
            "LexicalSense": f"Lexical sense '{field_value}' requires sense-distinguished lexicon. Verify sense assignment with lexicographical resources.",
            "default": f"Low confidence ({context.get('confidence', 'N/A')}) for {field_name} = {field_value}. Verify from source data and context."
        }
    }

    # Get template category
    templates = notes_templates.get(review_reason, {})

    # Try specific key
    specific_key = f"{field_name}-{field_value}"
    if specific_key in templates:
        return templates[specific_key]

    # Try field name key
    if field_name in templates:
        return templates[field_name]

    # Use default
    return templates.get("default", f"Review needed for {field_name} = {field_value}.")


def create_review_metadata(
    field_name: str,
    field_value: Any,
    confidence: float,
    context: Optional[Dict[str, Any]] = None,
    review_threshold: float = 0.95
) -> Dict[str, Any]:
    """
    Create complete review metadata for a field.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field
        confidence: Confidence score
        context: Optional context dictionary
        review_threshold: Threshold for requiring review

    Returns:
        Dictionary with review metadata
    """
    needs_review = confidence < review_threshold

    if not needs_review:
        # High confidence, no review needed
        return {
            "confidence": round(confidence, 2)
        }

    # Determine review reason
    review_reason = determine_review_reason(field_name, field_value, confidence, context)

    # Generate review notes
    review_notes = generate_review_notes(field_name, field_value, review_reason, context)

    # Build metadata
    metadata = {
        "confidence": round(confidence, 2),
        "needs_review": True,
        "review_reason": review_reason.value if review_reason else "low_confidence",
        "review_notes": review_notes,
        "review_status": ReviewStatus.PENDING.value,
        "reviewed_by": None,
        "reviewed_at": None
    }

    return metadata


def create_review_summary(annotations: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a summary of review status for a verse.

    Args:
        annotations: TBTA annotations with review metadata

    Returns:
        Dictionary with review summary statistics
    """
    total_fields = 0
    needs_review = 0
    high_confidence = 0
    review_reasons = {}
    status_counts = {}

    def count_fields(node):
        """Recursively count fields with review metadata."""
        nonlocal total_fields, needs_review, high_confidence

        if isinstance(node, dict):
            # Check for confidence field
            if "confidence" in node:
                total_fields += 1
                if node.get("needs_review"):
                    needs_review += 1
                    reason = node.get("review_reason", "unknown")
                    review_reasons[reason] = review_reasons.get(reason, 0) + 1
                    status = node.get("review_status", "pending")
                    status_counts[status] = status_counts.get(status, 0) + 1
                else:
                    high_confidence += 1

            # Recurse into children
            for value in node.values():
                if isinstance(value, (dict, list)):
                    count_fields(value)

        elif isinstance(node, list):
            for item in node:
                count_fields(item)

    count_fields(annotations)

    return {
        "total_fields": total_fields,
        "needs_review": needs_review,
        "high_confidence": high_confidence,
        "pending_reviews": status_counts.get("pending", 0),
        "approved_reviews": status_counts.get("approved", 0),
        "corrected_reviews": status_counts.get("corrected", 0),
        "rejected_reviews": status_counts.get("rejected", 0),
        "review_breakdown": review_reasons
    }


def filter_needs_review(annotations: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter annotations to show only items needing review.

    Args:
        annotations: Full TBTA annotations

    Returns:
        Filtered annotations with only review items
    """
    def filter_node(node):
        """Recursively filter nodes."""
        if isinstance(node, dict):
            filtered = {}
            has_review = False

            for key, value in node.items():
                if key == "needs_review" and value:
                    has_review = True
                if isinstance(value, (dict, list)):
                    filtered_value = filter_node(value)
                    if filtered_value is not None:
                        filtered[key] = filtered_value
                        has_review = True
                else:
                    filtered[key] = value

            return filtered if has_review else None

        elif isinstance(node, list):
            filtered = [filter_node(item) for item in node]
            filtered = [item for item in filtered if item is not None]
            return filtered if filtered else None

        return node

    return filter_node(annotations) or {}


# Example usage
if __name__ == "__main__":
    # Test case: GEN.1.26 Trial number
    context = {
        "verse_ref": "GEN.001.026",
        "theological_content": True,
        "entity_count": 3
    }

    metadata = create_review_metadata(
        field_name="Number",
        field_value="Trial",
        confidence=0.75,
        context=context
    )

    print("Review Metadata Example (GEN.1.26 - Trial Number):")
    print("-" * 60)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print()

    # Test case: High confidence - no review
    metadata2 = create_review_metadata(
        field_name="Part",
        field_value="Noun",
        confidence=0.99,
        context={}
    )

    print("Review Metadata Example (High Confidence):")
    print("-" * 60)
    for key, value in metadata2.items():
        print(f"{key}: {value}")
