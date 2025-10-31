"""
TBTA Review Marking System

Python package for adding review metadata to TBTA annotations.
"""

from .confidence_scorer import (
    calculate_confidence,
    get_base_confidence,
    get_feature_tier,
    requires_review,
    get_confidence_category,
    FeatureTier,
    ConfidenceAdjustment
)

from .review_metadata import (
    create_review_metadata,
    create_review_summary,
    filter_needs_review,
    determine_review_reason,
    generate_review_notes,
    ReviewReason,
    ReviewStatus
)

from .review_integration import (
    annotate_field_with_review,
    annotate_structure_with_review,
    load_tbta_file,
    save_annotated_tbta,
    generate_review_report,
    extract_review_items
)

__version__ = "1.0.0"
__all__ = [
    # Confidence scoring
    "calculate_confidence",
    "get_base_confidence",
    "get_feature_tier",
    "requires_review",
    "get_confidence_category",
    "FeatureTier",
    "ConfidenceAdjustment",

    # Review metadata
    "create_review_metadata",
    "create_review_summary",
    "filter_needs_review",
    "determine_review_reason",
    "generate_review_notes",
    "ReviewReason",
    "ReviewStatus",

    # Integration
    "annotate_field_with_review",
    "annotate_structure_with_review",
    "load_tbta_file",
    "save_annotated_tbta",
    "generate_review_report",
    "extract_review_items"
]
