# TBTA Review Marking System

## Purpose

Before implementing the TBTA amplification tool, establish a system to mark generated annotations that need human review. This ensures 100% accuracy on items marked as "approved" while flagging uncertain items for expert validation.

## Design Principles

1. **Conservative Marking**: When in doubt, mark for review
2. **Transparent Confidence**: Show confidence scores for all annotations
3. **Actionable Guidance**: Explain WHY review is needed
4. **Batch Operations**: Support reviewing many items at once
5. **Audit Trail**: Track who reviewed what and when

---

## Review Metadata Schema

### Core Fields

Every generated annotation can include these optional review fields:

```yaml
# Example: Generated annotation with review metadata
- Constituent: God
  Part: Noun
  Number: Trial
  confidence: 0.75
  needs_review: true
  review_reason: "theological_interpretation"
  review_notes: "Trial number assumes Trinity interpretation of Genesis 1:26"
  review_status: pending
  reviewed_by: null
  reviewed_at: null
```

### Field Definitions

#### `confidence`
- **Type**: Float (0.0 - 1.0)
- **Required**: Yes (for all generated fields)
- **Purpose**: System's confidence in this annotation
- **Thresholds**:
  - `>= 0.95`: High confidence (Tier 1 features)
  - `0.80 - 0.94`: Medium confidence (Tier 2 features)
  - `< 0.80`: Low confidence (Tier 3 features, ambiguous cases)

#### `needs_review`
- **Type**: Boolean
- **Required**: Yes (if confidence < 0.95)
- **Purpose**: Flag for human review
- **Auto-set when**:
  - `confidence < 0.95`
  - Feature requires human expertise
  - Multiple valid interpretations exist
  - Edge case or exception detected

#### `review_reason`
- **Type**: String (categorical)
- **Required**: Yes (if needs_review = true)
- **Purpose**: Explain why review is needed

**Possible Values**:

| Reason Code | Description | Examples |
|-------------|-------------|----------|
| `low_confidence` | AI confidence below threshold | Ambiguous participant tracking |
| `theological_interpretation` | Requires theological expertise | Trial = Trinity, prophecy interpretation |
| `cultural_context` | Requires cultural knowledge | Speaker age/relationship unclear |
| `ambiguous_reference` | Referent unclear from context | Pronoun with multiple possible antecedents |
| `temporal_ambiguity` | Time reference unclear | "Earlier Today" vs "Yesterday" boundary |
| `multiple_valid_interpretations` | More than one correct answer | Alternative analyses in TBTA |
| `rare_feature` | Rarely used feature | Trial, Quadrial number |
| `missing_context` | Insufficient context to decide | Speaker demographics outside dialogue |
| `edge_case` | Exception to general patterns | Unusual grammatical construction |
| `corpus_mismatch` | eBible data contradicts expected pattern | Translation uses unexpected form |

#### `review_notes`
- **Type**: String (free text)
- **Required**: No
- **Purpose**: Additional context for reviewers
- **Content**:
  - Explanation of the issue
  - Alternative interpretations considered
  - References to source data
  - Suggestions for resolution

#### `review_status`
- **Type**: String (categorical)
- **Required**: Yes (if needs_review = true)
- **Default**: `pending`

**Possible Values**:
- `pending`: Awaiting review
- `approved`: Human verified as correct
- `corrected`: Human made changes
- `rejected`: Marked as incorrect
- `skipped`: Review deferred

#### `reviewed_by`
- **Type**: String
- **Required**: No
- **Purpose**: Track who reviewed
- **Values**:
  - `null` (not yet reviewed)
  - User identifier
  - `system_auto_approved` (for high-confidence items)

#### `reviewed_at`
- **Type**: ISO 8601 timestamp
- **Required**: No
- **Purpose**: Track when reviewed
- **Format**: `2025-10-30T14:30:00Z`

---

## Confidence Scoring Rules

### Tier 1 Features (95-100% Confidence)

**Auto-approve** (no review needed):

| Feature | Confidence | Reasoning |
|---------|------------|-----------|
| **Clusivity** | 0.98 | Discourse analysis is reliable |
| **Dual Number** | 0.97 | Two named entities = clear |
| **Entity Tracking** | 0.99 | Noun counting is mechanical |
| **Part of Speech** | 0.99 | NLP tagging is highly accurate |
| **Constituent** | 1.00 | Word extraction is trivial |
| **Implicit: No** | 0.98 | Default value for explicit text |
| **Sequence** | 0.98 | Syntactic coordination is clear |
| **SemanticComplexityLevel: 1** | 1.00 | TBTA uses '1' for 100% of cases |

### Tier 2 Features (80-95% Confidence)

**Mark for review** when confidence drops:

| Feature | Base Confidence | Review Triggers |
|---------|-----------------|-----------------|
| **Participant Tracking** | 0.85 | Drop to 0.70 if: ambiguous antecedent, unclear narrative flow |
| **Speaker Demographics** | 0.88 | Drop to 0.65 if: age/relationship unclear from context, speaker identity ambiguous |
| **Proximity** | 0.82 | Drop to 0.70 if: spatial context unclear, temporal vs spatial ambiguous |
| **Time Granularity** | 0.80 | Drop to 0.60 if: narrative chronology unclear, time markers absent |
| **Illocutionary Force** | 0.90 | Drop to 0.75 if: indirect speech act, rhetorical question edge cases |

### Tier 3 Features (< 80% Confidence)

**Always mark for review**:

| Feature | Base Confidence | Reasoning |
|---------|-----------------|-----------|
| **Trial Number** | 0.75 | Requires theological interpretation (Trinity) |
| **Vocabulary Alternate** | 0.70 | Requires translation expertise, not always present |
| **LexicalSense** | 0.65 | Requires lexicon with sense distinctions |
| **Alternative Analysis** | 0.60 | Multiple valid interpretations by design |
| **Rhetorical Question** | 0.75 | Pragmatic interpretation required |

---

## Review Reason Assignment Logic

### Algorithm

```python
def assign_review_metadata(field_name, field_value, context):
    """Assign confidence, needs_review, and review_reason for a field."""

    # Step 1: Get base confidence for this field type
    confidence = get_base_confidence(field_name)

    # Step 2: Apply context-specific adjustments
    if is_ambiguous_context(field_name, context):
        confidence -= 0.15
        reason = "ambiguous_reference"

    if requires_expertise(field_name):
        confidence -= 0.20
        reason = "theological_interpretation" if is_theological(context) else "cultural_context"

    if has_missing_context(field_name, context):
        confidence -= 0.10
        reason = "missing_context"

    # Step 3: Determine if review is needed
    needs_review = confidence < 0.95

    # Step 4: Generate review notes
    notes = generate_review_notes(field_name, field_value, context, reason)

    return {
        "confidence": confidence,
        "needs_review": needs_review,
        "review_reason": reason if needs_review else None,
        "review_notes": notes if needs_review else None,
        "review_status": "pending" if needs_review else None
    }
```

### Specific Rules

#### Rule 1: Theological Interpretation Required

**Trigger**:
- `Number: Trial` in Genesis 1:26
- Prophecy interpretation
- Typological references

**Action**:
```yaml
confidence: 0.75
needs_review: true
review_reason: theological_interpretation
review_notes: "Trial number assumes Trinity interpretation. Verify with theological commentary."
```

#### Rule 2: Missing Speaker Demographics

**Trigger**:
- Dialogue detected but speaker age/relationship unclear
- Speaker identity ambiguous

**Action**:
```yaml
confidence: 0.65
needs_review: true
review_reason: missing_context
review_notes: "Speaker age cannot be determined from immediate context. Check broader narrative."
```

#### Rule 3: Ambiguous Participant Tracking

**Trigger**:
- Multiple possible antecedents for pronoun
- Entity tracking unclear

**Action**:
```yaml
confidence: 0.70
needs_review: true
review_reason: ambiguous_reference
review_notes: "Pronoun 'his' could refer to entity 1 (Cain) or entity 2 (Abel). Check discourse flow."
```

#### Rule 4: Time Granularity Uncertainty

**Trigger**:
- Boundary cases ("Earlier Today" vs "Yesterday")
- Narrative chronology unclear

**Action**:
```yaml
confidence: 0.60
needs_review: true
review_reason: temporal_ambiguity
review_notes: "Event timing unclear. Could be 'Earlier Today' or 'Yesterday' depending on narrative flow."
```

#### Rule 5: Rare Feature Usage

**Trigger**:
- Trial, Quadrial, Paucal number
- First appearance of rare value

**Action**:
```yaml
confidence: 0.75
needs_review: true
review_reason: rare_feature
review_notes: "Trial number is rare. Verify count is exactly 3 entities, not generic plural."
```

---

## Output Format Examples

### Example 1: High Confidence (No Review)

```yaml
verse: GEN.004.008
clauses:
  - Part: Clause
    Discourse Genre: Climactic Narrative Story
    confidence: 0.98
    Illocutionary Force: Suggestive 'let's'
    confidence: 0.92
    children:
      - Part: NP
        Semantic Role: Most Agent-like
        confidence: 0.97
        children:
          - Constituent: Cain
            Part: Noun
            Number: Dual
            confidence: 0.97
            NounListIndex: '1'
            confidence: 0.99
            Participant Tracking: Routine
            confidence: 0.95
```

**Notes**: All confidence >= 0.95 except Illocutionary Force (0.92), but since it's close and clear from context, auto-approve.

### Example 2: Medium Confidence (Needs Review)

```yaml
verse: GEN.019.031
clauses:
  - Part: Clause
    Speaker: Woman
    confidence: 0.90
    Listener: Woman
    confidence: 0.90
    Speaker's Age: Young Adult (18-24)
    confidence: 0.70
    needs_review: true
    review_reason: cultural_context
    review_notes: "Age estimate based on 'older daughter' being unmarried. Cultural context may vary."
    review_status: pending
    Speaker-Listener Age: Essentially the Same Age
    confidence: 0.85
    needs_review: true
    review_reason: missing_context
    review_notes: "Age difference between sisters unclear. 'Older' could mean different generation or same cohort."
    review_status: pending
```

### Example 3: Low Confidence (Requires Expert Review)

```yaml
verse: GEN.001.026
clauses:
  - children:
      - Constituent: God
        Part: Noun
        Number: Trial
        confidence: 0.75
        needs_review: true
        review_reason: theological_interpretation
        review_notes: "Trial number (exactly 3) assumes Trinity interpretation of 'Let us make'. Alternative: pluralis maiestatis (royal we) or divine council. Verify with theological commentary and original language analysis."
        review_status: pending
        Person: First Inclusive
        confidence: 0.80
        needs_review: true
        review_reason: theological_interpretation
        review_notes: "First Inclusive assumes Trinity members addressing each other (all included). Depends on Trial number interpretation."
        review_status: pending
```

---

## Filtering and Queries

### Command-Line Filters

```bash
# Show only items needing review
python tbta_tool.py --verse GEN.1.26 --filter needs_review

# Show only low confidence items
python tbta_tool.py --verse GEN.1.26 --filter "confidence < 0.80"

# Show by review reason
python tbta_tool.py --verse GEN.1.26 --filter "review_reason == theological_interpretation"

# Show pending reviews
python tbta_tool.py --verse GEN.1.26 --filter "review_status == pending"
```

### YAML Output with Review Summary

```yaml
verse: GEN.001.026
review_summary:
  total_fields: 147
  needs_review: 12
  high_confidence: 135
  pending_reviews: 12
  approved_reviews: 0
  review_breakdown:
    theological_interpretation: 4
    cultural_context: 2
    temporal_ambiguity: 3
    ambiguous_reference: 2
    rare_feature: 1
clauses:
  [... full data ...]
```

---

## Review Workflow

### Phase 1: Generation

1. Tool generates TBTA annotations for a verse
2. Each field receives confidence score
3. Items below threshold auto-flagged for review
4. Output includes review metadata

### Phase 2: Review

1. Reviewer filters for `needs_review: true`
2. Reviews each item:
   - Approves: Set `review_status: approved`, `reviewed_by: [name]`, `reviewed_at: [timestamp]`
   - Corrects: Update field value, set `review_status: corrected`
   - Rejects: Set `review_status: rejected`, add notes
   - Skips: Set `review_status: skipped` for later

3. System removes `needs_review` flag for approved/corrected items

### Phase 3: Tracking

1. Tool tracks review statistics:
   - Total items generated
   - Items needing review
   - Items reviewed
   - Accuracy rate (approved vs corrected vs rejected)

2. Learning loop:
   - If feature consistently needs correction, lower base confidence
   - If feature consistently approved, can raise confidence threshold
   - Track common review reasons to improve generation

---

## Implementation Strategy

### Step 1: Add Confidence Scoring Module

**File**: `/src/lib/tbta/confidence_scorer.py`

**Responsibilities**:
- Define base confidence scores for each TBTA field
- Implement context-aware adjustments
- Return confidence + review metadata

### Step 2: Add Review Metadata Generator

**File**: `/src/lib/tbta/review_metadata.py`

**Responsibilities**:
- Assign review reasons based on rules
- Generate review notes
- Format review metadata for YAML output

### Step 3: Integrate into TBTA Tool

**File**: `/src/lib/tbta/tbta_annotator.py` (or similar)

**Changes**:
- For each generated field, call confidence_scorer
- Attach review metadata to field
- Include review summary in output

### Step 4: Add Filtering Support

**File**: `/src/lib/tbta/review_filter.py`

**Responsibilities**:
- Parse filter expressions
- Filter annotations by review metadata
- Generate review-only output

### Step 5: Create Review UI/Tool

**File**: `/bible-study-tools/tbta-reviewer/README.md`

**Capabilities**:
- Display items needing review
- Allow batch approval/correction
- Track review history
- Generate review statistics

---

## Testing Plan

### Test Cases

1. **High Confidence Item** (GEN.4.8 - Dual Number)
   - Expected: `confidence: 0.97`, `needs_review: false`

2. **Medium Confidence Item** (GEN.19.31 - Speaker Age)
   - Expected: `confidence: 0.70`, `needs_review: true`, `review_reason: cultural_context`

3. **Low Confidence Item** (GEN.1.26 - Trial Number)
   - Expected: `confidence: 0.75`, `needs_review: true`, `review_reason: theological_interpretation`

4. **Ambiguous Reference** (Pronoun with multiple antecedents)
   - Expected: `confidence: 0.70`, `review_reason: ambiguous_reference`

5. **Missing Context** (Speaker demographics outside dialogue)
   - Expected: `confidence: 0.60`, `review_reason: missing_context`

### Success Metrics

- **100% accuracy** on items marked `approved` (verified by human review)
- **< 10% false positives** (items marked for review that don't need it)
- **< 1% false negatives** (items that need review but aren't flagged)

---

## Future Enhancements

1. **Machine Learning Integration**
   - Train model on reviewed data
   - Improve confidence scoring over time
   - Predict review reasons automatically

2. **Collaborative Review**
   - Multiple reviewers
   - Vote on disputed items
   - Track inter-annotator agreement

3. **Review Difficulty Rating**
   - Easy: Clear-cut corrections
   - Medium: Requires context research
   - Hard: Requires expert knowledge

4. **Batch Review Tools**
   - Review all instances of a pattern
   - Apply corrections across multiple verses
   - Propagate approved patterns

---

## Summary

This review marking system ensures:
- **Transparency**: Every annotation has a confidence score
- **Quality**: Low-confidence items flagged for human review
- **Efficiency**: High-confidence items auto-approved
- **Learning**: System improves through review feedback
- **Trust**: 100% accuracy goal for approved items

**Key Principle**: Better to mark too many items for review than to miss one that needs it.

**End Goal**: AI generates TBTA annotations at 95%+ accuracy, with remaining 5% explicitly flagged for expert validation, achieving 100% accuracy on all approved items.
