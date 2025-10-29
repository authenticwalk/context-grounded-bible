# Core Instructions for Semantic Cluster Analysis
**Version:** 1.0 (IMMUTABLE)

## Mission
Extract cross-linguistic semantic clusters (word groupings with unified meaning) from biblical text to serve as grounding context for LLM-powered translation and theological study.

---

## Non-Negotiable Principles

### 1. NO HALLUCINATION
- Only include data you have HIGH CONFIDENCE in from your training data
- If you're uncertain about a translation or fact: **Omit it** 
- Better to have incomplete data than fabricated data
- If you hesitate ("I think..." "probably..." "might be..."): **REJECT that data point**

### 2. GREEK PRIORITY
- Cluster boundaries should honor Greek word divisions from NA28
- EXCEPTION: If 20%+ of translations consistently use different boundaries, document the divergence
- Always cite Greek source: `grc-na28-1993-dbs`

### 3. SOURCE CITATION REQUIRED
- Every translation|fact|theory must cite source inline using format: `{source}` immediately after the content
- Format: `"quoted text" {source}` or `field_name: "content" {source}`
- If from your training data: Use `llm-cs45`
- Translation sources use format: `{lang}-{version}-{revision}-{source}` in arrays only
- See `source-abbreviations.yaml` for lookup table

### 4. VERSE-CENTRIC OUTPUT
- All cluster data for a verse goes in ONE file: `/bible/{book}/{chapter}/{book}-{chapter}-{verse:03d}-semantic-clusters.yaml`
- Follow schema exactly (see examples)
- NO verbose metadata - keep it simple

### 5. NUMBERS FROM CODE, NOT LLMs
- ❌ DO NOT predict: confidence scores, percentages, word counts, statistical metrics
- ✅ DO provide: qualitative notes, rationales, theological insights, cultural observations
- Let validation scripts calculate numbers

---

## What is a Semantic Cluster?

**Definition:** A group of words that function as a unified meaning-bearing unit across translations.

**Examples:**
- ✅ "poor in spirit" (πτωχοὶ τῷ πνεύματι) - unified spiritual poverty concept
- ✅ "kingdom of heaven" (βασιλεία τῶν οὐρανῶν) - theological concept unit
- ✅ "love your neighbor" - command + object + relationship boundary
- ❌ "the poor" - just article + adjective (no unified concept beyond grammar)

**Test:** If splitting the cluster loses translation insight or theological meaning, it's a valid cluster.

---

## Cluster Identification Rules

### MUST identify as cluster IF:
1. **Multi-word Greek concept** that translates as semantic unit
   - Example: τῷ πνεύματι (instrumental dative phrase = "in spirit")

2. **Translation divergence ≥20%** of reviewed translations
   - If 20%+ use different boundaries or cultural substitution
   - Example: "poor in spirit" vs. "humble in heart" (cultural)

3. **Theological concept** with unified meaning
   - Example: "kingdom of heaven" (Matthew's Jewish circumlocution for "kingdom of God")

4. **Cultural adaptation** required in some language families
   - Example: "white as snow" → "white as wool" in desert cultures

### MUST NOT identify as cluster IF:
- ❌ Pure grammatical units with no semantic unity (article + noun, unless theologically loaded)
- ❌ Mechanical word combinations (every 2-word window)
- ❌ Same translation pattern across ALL reviewed languages (no divergence = no insight)
- ❌ Differs by one word with no semantic/theological shift

---

## Single Word Rules

**Critical Rule:** ALL words in the verse MUST be covered by at least one cluster

**Default:** Include single words in multi-word clusters when possible

**Create single-word cluster IF:**
- Word not covered by any multi-word cluster
- Significant theological or translation divergence exists

**Rationale:** Each cluster must be translatable in isolation to reconstruct the verse in any language. Skipped words cannot be reconstructed.

## Overlap Rules

**Default:** Each Greek word appears in ONE cluster

**Allow SECOND cluster IF:**
- ≥20% translation divergence from primary cluster, **OR**
- Theological debate boundary (different traditions cluster differently)

**Allow THIRD cluster IF:**
- ≥20% translation divergence **AND** theological significance

**Maximum:** 3 overlapping clusters per word (hard limit)

**Why allow overlap?**
Different languages and theological traditions may cluster boundaries differently. Overlap reveals these translation challenges.

---

## Greek Analysis Requirements

For each verse:

1. **Word-by-word breakdown:**
   - Position (1, 2, 3, ...)
   - Greek word from `grc-na28-1993-dbs`
   - Strong's number (no separate citation needed)

2. **Textual variants** (if any):
   - Include as separate cluster with `variant_info` section
   - Cite manuscripts supporting/opposing
   - Note theological impact of variant

3. **Grammar notes** (when relevant to clustering):
   - Instrumental dative, genitive constructions, etc.
   - Only note if it affects cluster boundaries

---

## Translation Pattern Analysis

For each cluster, identify **rendering patterns**:

1. **Standard pattern** (most common)
   - Example rendering
   - Example sources (3-5 translations)

2. **Dynamic equivalence** (if present)
   - Example rendering
   - Example sources
   - Note: `reason: dynamic_equivalence`

3. **Cultural adaptations** (if present)
   - Example rendering
   - Example sources
   - Note: `reason: cultural_{explanation}`
   - Cultural note with inline citation: `cultural_note: "explanation" {llm-cs45}`

4. **Paraphrases** (if relevant)
   - Example: Message Bible
   - Note limitations

### Critical Rule: NO NUMBER PREDICTIONS
- ❌ Don't say "85% of translations use..."
- ✅ Say "Most major translations use... Examples: [list 5-10]" (or better European translations use... Asian translations use - or whatever shared pattern)
- ✅ Say "Some cultures substitute... Examples: [list 2-3]"

---

## Theological Analysis

### Required for theologically significant clusters:

1. **Debate** (if exists):
   - Name the debate (e.g., "spiritual vs. material poverty")
   - List 2-3 major traditions with their views
   - Representative theologian for each view
   - NO favoritism - present all views fairly

2. **Cross-references:**
   - List 3-5 key related passages
   - Brief note on relationship

3. **Pregnant words** (if any):
   - Language-specific terms that capture depth beyond components
   - ONLY include if theologically/exegetically significant
   - Format: `{lang: code, word: "term", note: "why significant"}`

---


## What NOT to Include

### ❌ Predicted Metadata
- Word arrays
- Confidence scores
- Convergence percentages
- Statistical metrics
- **Reason:** LLMs predict next tokens, not accurate numbers. Let code calculate.

### ❌ Unnecessary Fields
- `gloss` field (redundant with example patterns)
- `validation_status` field (implied by llm-cs45 citations)
- Long `sources` lists at cluster end
- Separate `source` field for each subfield

### ❌ Duplicate Information
- Don't repeat translation text in multiple places
- Don't create separate "verse manifestation" or "translation rendering" sections
- Keep it in ONE verse-centric file

### ❌ Verbose Content
- Redundant rationale conclusions ("This makes it important...")
- Exhaustive translation lists (3-5 diverse examples sufficient)
- Separate source citations (use inline `{source}` format)

---

## Output Format

**File:** `/bible/{book}/{chapter}/{book}-{chapter}-{verse:03d}-semantic-clusters.yaml`

**Structure:**
```yaml
verse: {ref}

greek:
  text: "..." {grc-na28-1993-dbs}
  words:
    - {pos: 1, word: "word", strongs: G1234}
    # strongs citation implied, no separate source field

clusters:
  - id: {cluster-id}
    positions: [...]
    greek: "..."
    rationale: |
      Why this is a cluster (focus on WHY important, not redundant conclusions). {llm-cs45}
    patterns:
      - id: pattern-type
        example: "translation"
        sources: [lang-ver-year-llm-cs45, ...]
        pattern_note: "brief explanation" {llm-cs45}
        cultural_note: "if applicable" {llm-cs45}  # implies needs review
    theological:  # if significant
      debate: "debate name" {llm-cs45}
      traditions:
        - tradition: "name"
          view: "brief view" {llm-cs45}
      cross_refs:
        - ref: "reference"
          note: "why relevant (concise)" {llm-cs45}
    pregnant_words:  # only if noteworthy
      - word: "word"
        significance: "why significant" {llm-cs45}
    # NO long source lists
    # NO validation_status field (implied by llm-cs45 citations)

metadata:
  analysis_date: "{iso8601}"
  experiment: "semantic-clusters"
  variant: "{variant-name}"
  instructions_version: "{version}"
```

**See example:** `/bible/mt/5/MAT.5.003-semantic-clusters.yaml`

---

## Conflict Resolution

**If core-instructions.md conflicts with additional-instructions.md:**
- **Core instructions ALWAYS WIN**
- Additional instructions can add details, but cannot override core rules

**If you're unsure:**
- Mark `validation_status: requires_human_review`
- Explain your uncertainty in `rationale` field
- Provide multiple interpretations if helpful

---

## Quality Over Quantity

- Better to identify 5 high-quality clusters than 15 questionable ones
- Better to omit uncertain data than fabricate
- Better to flag for human review than guess

**Remember:** This data will ground other LLMs. Bad data compounds errors. Good data compounds insights.

---

## Value Over Noise

Focus on **practical value** for translators, pastors, theologians, and students:
- What insights would they copy to their notes?
- What helps understanding translation choices?
- What reveals theological significance?

**Quality metrics:**
- Rationale explains WHY important (not just describes pattern)
- Patterns show meaningful divergence (not exhaustive lists)
- Theological notes reveal practical implications
- All words in verse covered (reconstructable)

**Avoid:**
- Redundant conclusions ("This makes it important for...")
- Exhaustive pattern lists (show diversity, not completeness)
- Academic completeness over practical insight
- Token limits without value assessment

You will be called many times. Efficiency matters, but value matters more.
