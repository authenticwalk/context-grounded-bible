# Experiment: Semantic-Context Approach

**Hypothesis:** The most valuable approach to listing original language words is to focus on **semantic domains and contextual meaning**, showing how each word contributes to the overall meaning of the verse in its specific context.

**Philosophy:** Like a semantic map - each word is understood within its semantic domain and contextual usage. Optimized for understanding meaning and semantic relationships between words.

**Target Use Case:** Translators and exegetes who need to understand not just what words mean in general, but how they function semantically in this specific verse context.

---

## Key Differences from Base README

**Primary Focus:** Semantic domains and contextual meaning of each word

**Data Emphasis:**
1. Semantic domain (Louw-Nida for Greek, semantic categories for Hebrew)
2. Contextual meaning in this specific verse
3. Semantic relationships with other words in the verse
4. Range of meanings and why this specific sense is used here
5. Semantic fields and word families

**De-emphasized:** Strong's numbers (included but tertiary), detailed morphological parsing

---

## Research Methodology

### Phase 1: Data Extraction

**Primary Sources (in order of priority):**
- [ ] Louw-Nida Greek-English Lexicon (semantic domains) - For Greek
- [ ] BDAG - Greek lexicon with semantic ranges
- [ ] BDB - Hebrew lexicon with semantic information
- [ ] BibleHub - Cross-verification and contextual usage
- [ ] Ancient Hebrew Research Center - Hebrew semantic concepts

**Secondary Sources:**
- [ ] Semantic dictionaries and word studies
- [ ] TDNT (Theological Dictionary of the New Testament) - for theological semantic ranges
- [ ] NIDOTTE (New International Dictionary of OT Theology & Exegesis) - for Hebrew

**Extraction Process:**
1. Extract complete original text
2. For each word, identify:
   - Semantic domain (Louw-Nida number for Greek, category for Hebrew)
   - Range of possible meanings
   - Contextual meaning in this verse
   - Related words in same semantic field
   - Collocations and typical usage patterns
3. Analyze how words work together semantically in the verse
4. Identify semantic themes and relationships

**For Greek Words Extract:**
- Louw-Nida domain number (e.g., 33.281)
- Domain name (e.g., "Communication")
- Subdomain (e.g., "Preach")
- Semantic range (all major senses)
- Contextual sense (which sense applies here)

**For Hebrew Words Extract:**
- Semantic category (e.g., "Motion", "Cognition", "Relationship")
- BDB semantic field
- Range of meanings
- Contextual usage
- Ancient Near East conceptual background

### Phase 2: Analysis and Synthesis

**Organization:** Words organized by **semantic contribution** or **thematic relationships**

**Semantic Analysis:**
- How does each word contribute to the verse's overall meaning?
- What semantic relationships exist between words?
- Are there semantic parallels or contrasts?
- What is the semantic structure of the verse?
- How do semantic domains interact?

**Contextual Focus:**
- Why this particular sense of the word (if multiple senses exist)?
- How does context narrow semantic range?
- What other contexts use similar semantic patterns?
- What does the semantic domain tell us about the concept?

### Phase 3: Citation and Verification

**Every semantic claim must be verified:**
- Louw-Nida domain numbers verified
- Semantic ranges checked against lexicons
- Contextual meanings justified from usage
- Cross-references to similar semantic patterns

---

## Output Schema (Experiment-Specific)

```yaml
# === METADATA ===
verse:
  reference: "{BOOK} {chapter}:{verse}"
  book: "{BOOK}"
  chapter: {chapter}
  verse: {verse}

tool:
  name: "original-language-words"
  version: "1.0.0"
  experiment: "semantic"
  revision: 1
  generated_date: "YYYY-MM-DD"

# === SOURCE TEXT ===
source_text:
  language: "{grc/heb/arc}"
  text: "[Complete verse in original]" {source}
  transliteration: "[Complete transliteration]" {source}

# === WORDS (SEMANTIC FORMAT) ===
# Organized by semantic contribution to the verse

words:
  - position: 1
    original: "[Original script]" {source}
    transliteration: "[Transliteration]" {source}
    lemma: "[Lexical form]" {source}
    strongs: "[H#### or G####]" {source}  # Tertiary priority

    semantic_data:
      # For Greek:
      louw_nida_domain: "[Domain number]" {source}
      domain_name: "[Domain name]" {source}
      subdomain: "[Subdomain]" {source}
      # For Hebrew:
      semantic_category: "[Category]" {source}

      semantic_range:
        - sense: "[Meaning 1]" {source}
        - sense: "[Meaning 2]" {source}
        - sense: "[Meaning 3]" {source}

      contextual_meaning: "[What it means in THIS verse]" {source}
      why_this_sense: "[Why this particular sense applies here]" {llm-cs45}

      semantic_field: "[Related concept family]" {source}
      related_words: [list of related words in same domain] {source}

    gloss: "[Contextual gloss]" {source}

  # Continue for all words...

# === SEMANTIC ANALYSIS ===
semantic_structure:
  - theme: "[Semantic theme in verse]" {llm-cs45}
    words_involved: [list of positions] {llm-cs45}
    significance: "[Why this semantic pattern matters]" {llm-cs45}

semantic_relationships:
  - relationship_type: "[parallel/contrast/cause-effect/etc]" {llm-cs45}
    word_1: "[Position and lemma]" {llm-cs45}
    word_2: "[Position and lemma]" {llm-cs45}
    explanation: "[How they relate semantically]" {llm-cs45}

# === CONTEXTUAL INSIGHTS ===
contextual_notes:
  - word: "[Lemma]" {llm-cs45}
    observation: "[Why this word choice is significant]" {llm-cs45}
    cross_references: [verses with similar semantic usage] {llm-cs45}

# === STATISTICS ===
word_count: [integer]
semantic_domains: [list of all domains present]
dominant_themes: [list] {llm-cs45}
```

---

## Quality Metrics for This Experiment

**Success Criteria:**
- 100% of words have semantic domain identified
- Contextual meaning clearly stated for each word
- Semantic relationships between words mapped
- Louw-Nida (or equivalent) domains verified
- Why this particular sense is explained

**Optimal Format:**
- Semantic domains clearly identified
- Contextual meaning distinguished from general meaning
- Semantic relationships shown
- Organized by semantic contribution
- Insights about word choice and usage

**What Makes This Experiment Succeed:**
- Depth: Does it show semantic nuance?
- Context: Is the meaning contextually appropriate?
- Relationships: Are semantic connections identified?
- Insight: Does it illuminate why these words were chosen?
- Usability: Can a translator understand semantic ranges?

---

## Research Guidelines for This Experiment

**Top Priority:** Understand contextual meaning. Don't just list definitions - show how words function semantically in THIS verse.

**Workflow:**
1. Extract complete text
2. For each word, look up semantic domain
3. Identify range of meanings
4. Determine which sense applies in this context
5. Explain why this sense (not others)
6. Map semantic relationships between words
7. Identify semantic themes in the verse

**Focus:**
- Semantic domains and families
- Contextual meaning (not just dictionary definitions)
- Semantic relationships
- Why this word choice
- How words work together semantically

**Avoid:**
- Generic definitions without context
- Ignoring semantic nuance
- Missing semantic relationships
- Listing all senses without identifying which applies
- Superficial glosses

---

## Test Verses for This Experiment

We will test on:
1. **John 1:1** (high-context, rich semantic domains for "word", "God", "beginning")
2. **Matthew 5:3** (medium-context, semantic richness in "poor in spirit", "blessed")
3. **Job 38:36** (low-context, Hebrew semantic concepts)

---

**Experiment Version:** Rev 1
**Created:** 2025-10-28
**Thesis:** Semantic domain analysis provides the most exegetically valuable word inventory
