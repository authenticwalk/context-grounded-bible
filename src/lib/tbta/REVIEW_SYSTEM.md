# TBTA Review Marking System

A Python library for adding confidence scores and review metadata to TBTA (The Bible Translator's Assistant) annotations.

## Purpose

The TBTA amplification tool will generate linguistic annotations for Bible verses. This review marking system ensures quality by:

1. **Confidence Scoring**: Assigns 0-100% confidence to each annotation
2. **Review Flagging**: Marks low-confidence items for human review
3. **Review Guidance**: Explains WHY review is needed
4. **Quality Assurance**: Achieves 100% accuracy on approved items

## Key Features

- **Three-Tier Confidence System**:
  - Tier 1 (95-100%): Auto-approve (clusivity, number, entity tracking)
  - Tier 2 (80-95%): May need review (participant tracking, speaker demographics)
  - Tier 3 (<80%): Always review (trial number, vocabulary alternates)

- **10 Review Reason Categories**:
  - `theological_interpretation`: Requires theological expertise
  - `cultural_context`: Requires cultural knowledge
  - `ambiguous_reference`: Unclear referent
  - `temporal_ambiguity`: Time reference unclear
  - `rare_feature`: Rarely-used grammatical feature
  - And 5 more...

- **Detailed Review Notes**: Context-specific guidance for reviewers

## Quick Start

### 1. Basic Confidence Scoring

```python
from lib.tbta import calculate_confidence

# High confidence example
confidence = calculate_confidence("Part", "Noun", {})
# → 0.99 (auto-approve)

# Low confidence example
context = {
    "verse_ref": "GEN.001.026",
    "theological_content": True
}
confidence = calculate_confidence("Number", "Trial", context)
# → 0.45 (needs review)
```

### 2. Generate Review Metadata

```python
from lib.tbta import create_review_metadata, calculate_confidence

context = {
    "verse_ref": "GEN.001.026",
    "theological_content": True
}

confidence = calculate_confidence("Number", "Trial", context)
metadata = create_review_metadata("Number", "Trial", confidence, context)

print(metadata)
# {
#   "confidence": 0.45,
#   "needs_review": True,
#   "review_reason": "theological_interpretation",
#   "review_notes": "Trial number (exactly 3) assumes Trinity...",
#   "review_status": "pending",
#   "reviewed_by": None,
#   "reviewed_at": None
# }
```

### 3. Annotate a Field

```python
from lib.tbta import annotate_field_with_review

context = {"verse_ref": "GEN.001.026", "theological_content": True}
annotated = annotate_field_with_review("Number", "Trial", context)

# Returns:
# {
#   "Number": "Trial",
#   "confidence": 0.45,
#   "needs_review": True,
#   "review_reason": "theological_interpretation",
#   "review_notes": "Trial number (exactly 3) assumes Trinity interpretation...",
#   "review_status": "pending"
# }
```

### 4. Generate Review Report

```python
from lib.tbta import generate_review_report

# Annotated verse structure
annotated_verse = {
    "verse": "GEN.001.026",
    "clauses": [...]  # With review metadata
}

report = generate_review_report(annotated_verse)
print(report)

# Outputs:
# ======================================================================
# TBTA REVIEW REPORT
# ======================================================================
# Verse: GEN.001.026
# Total Fields: 147
# Needs Review: 12 (8.2%)
# High Confidence: 135 (91.8%)
# ...
```

## Module Reference

### `confidence_scorer.py`

**Core Functions:**

- `calculate_confidence(field_name, field_value, context) -> float`
  - Returns confidence score (0.0 - 1.0)
  - Applies context-based adjustments

- `get_base_confidence(field_name, field_value) -> float`
  - Returns base confidence for a field type

- `get_feature_tier(field_name, field_value) -> FeatureTier`
  - Returns tier classification (TIER_1/2/3)

- `requires_review(confidence, threshold=0.95) -> bool`
  - Determines if review is needed

**Constants:**

- `BASE_CONFIDENCE`: Dictionary of base confidence scores
- `FIELD_TIERS`: Field tier classifications
- `ConfidenceAdjustment`: Adjustment amounts

### `review_metadata.py`

**Core Functions:**

- `create_review_metadata(field_name, field_value, confidence, context) -> dict`
  - Creates complete review metadata

- `determine_review_reason(field_name, field_value, confidence, context) -> ReviewReason`
  - Determines why review is needed

- `generate_review_notes(field_name, field_value, review_reason, context) -> str`
  - Generates human-readable review notes

- `create_review_summary(annotations) -> dict`
  - Summarizes review status for a verse

- `filter_needs_review(annotations) -> dict`
  - Filters to show only items needing review

**Enums:**

- `ReviewReason`: 10 categorical review reasons
- `ReviewStatus`: pending/approved/corrected/rejected/skipped

### `review_integration.py`

**Core Functions:**

- `annotate_field_with_review(field_name, field_value, context) -> dict`
  - Annotates a single field

- `annotate_structure_with_review(structure, context) -> dict`
  - Recursively annotates a TBTA structure

- `generate_review_report(annotations) -> str`
  - Generates formatted review report

- `extract_review_items(annotations) -> list`
  - Extracts flat list of review items

- `load_tbta_file(filepath) -> dict`
  - Loads TBTA YAML file

- `save_annotated_tbta(annotations, output_path)`
  - Saves annotated TBTA to file

## Context Dictionary

The `context` dictionary provides additional information for confidence scoring:

```python
context = {
    # Verse information
    "verse_ref": "GEN.001.026",           # Verse reference
    "discourse_type": "narrative",        # Type of discourse

    # Dialogue context
    "has_dialogue": True,                 # Has quoted speech
    "speaker_clear": True,                # Speaker identity clear

    # Temporal context
    "temporal_markers": True,             # Has time markers
    "chronology_clear": False,            # Chronology is clear

    # Entity tracking
    "entity_count": 3,                    # Number of entities
    "antecedent_clear": True,             # Antecedent is clear
    "multiple_antecedents": False,        # Multiple possible antecedents

    # Spatial context
    "spatial_context_clear": True,        # Spatial relations clear

    # Special cases
    "theological_content": True,          # Requires theological interpretation
    "indirect_speech_act": False,         # Indirect speech act
    "corpus_validated": False,            # Validated against eBible corpus
    "corpus_mismatch": False,             # Corpus contradicts expectation
    "clear_context": True,                # Context is very clear

    # Notes
    "ambiguity_note": "...",              # Note about ambiguity
    "corpus_note": "..."                  # Note about corpus
}
```

## Confidence Adjustments

Adjustments applied based on context:

| Trigger | Adjustment | Example |
|---------|------------|---------|
| Theological interpretation | -0.20 | Trial number = Trinity |
| Cultural context required | -0.15 | Speaker age/relationship |
| Ambiguous reference | -0.15 | Multiple antecedents |
| Missing context | -0.10 | Speaker unclear |
| Rare feature | -0.10 | Trial/Quadrial number |
| Edge case | -0.12 | Rhetorical questions |
| Clear context | +0.05 | All markers present |
| Corpus validated | +0.05 | eBible confirms pattern |

## Output Format

### YAML with Review Metadata

```yaml
verse: GEN.001.026
source: tbta
version: 1.0.0
clauses:
  - Part: Clause
    confidence: 0.99
    Discourse Genre: Climactic Narrative Story
    confidence: 0.98
    children:
      - Constituent: God
        confidence: 1.00
        Number: Trial
        confidence: 0.45
        needs_review: true
        review_reason: theological_interpretation
        review_notes: "Trial number (exactly 3) assumes Trinity interpretation..."
        review_status: pending
        reviewed_by: null
        reviewed_at: null
```

## Testing

Run the test suite:

```bash
cd src/lib/tbta
python3 test_review_system.py
```

Tests include:
1. Confidence scoring with various features
2. Review metadata generation
3. Field annotation
4. Real TBTA data structures
5. Review summary generation

## Example: Genesis 1:26 Analysis

```python
from lib.tbta import calculate_confidence, create_review_metadata

# Context for GEN.1.26 (Trinity dialogue)
context = {
    "verse_ref": "GEN.001.026",
    "theological_content": True,
    "entity_count": 3,
    "has_dialogue": True
}

# Analyze Trial number
field = "Number"
value = "Trial"
confidence = calculate_confidence(field, value, context)
# → 0.45 (low, due to theological interpretation)

metadata = create_review_metadata(field, value, confidence, context)
# → {
#     "confidence": 0.45,
#     "needs_review": True,
#     "review_reason": "theological_interpretation",
#     "review_notes": "Trial number (exactly 3) in GEN.001.026 assumes
#                      Trinity interpretation of 'Let us make'.
#                      Alternative interpretations: pluralis maiestatis
#                      (royal we) or divine council. Verify with theological
#                      commentary and original language analysis.",
#     "review_status": "pending"
# }
```

## Integration with TBTA Tool

When building the TBTA amplification tool, integrate this system as follows:

```python
from lib.tbta import annotate_structure_with_review, generate_review_report

# 1. Generate TBTA annotations (your tool logic)
annotations = generate_tbta_annotations(verse_ref)

# 2. Add review metadata
context = build_context_from_verse(verse_ref)
annotated = annotate_structure_with_review(annotations, context)

# 3. Generate review report
report = generate_review_report(annotated)
print(report)

# 4. Save annotated data
save_annotated_tbta(annotated, output_path)

# 5. Extract items for review UI
review_items = extract_review_items(annotated)
# → List of items needing review
```

## Review Workflow

### Phase 1: Generation
1. Tool generates annotations
2. System assigns confidence scores
3. Low-confidence items flagged for review

### Phase 2: Review
1. Reviewer examines flagged items
2. Approves, corrects, or rejects each
3. System updates metadata

### Phase 3: Learning
1. Track correction patterns
2. Adjust base confidence scores
3. Improve future generations

## Design Principles

1. **Conservative**: Better to flag for review than miss an error
2. **Transparent**: Show confidence for all fields
3. **Actionable**: Explain why review is needed
4. **Iterative**: Learn from reviews to improve

## Success Metrics

- **100% accuracy** on approved items (verified by human review)
- **< 10% false positives** (items flagged unnecessarily)
- **< 1% false negatives** (errors missed)
- **95%+ overall accuracy** (correct on first generation)

## References

- Design document: `/plan/tbta-review-marking-system.md`
- TBTA field taxonomy: `/plan/tbta-languages/complete-field-taxonomy.md`
- Reproduction guide: `/plan/tbta-languages/reproduction-guide-95-percent.md`
- TBTA processor: `src/lib/tbta/README.md`

## License

MIT License - Part of the Context-Grounded Bible project

---

**Status**: Ready for integration with TBTA amplification tool

**Version**: 1.0.0

**Last Updated**: 2025-10-30
