# Project Analysis - Context-Grounded Bible
**Date:** 2025-10-28
**Purpose:** Analysis of existing project structure to inform agent design

---

## Project Overview

**Mission:** Create the largest AI-readable commentary on the entire Bible to empower Bible translators, pastors, and students to use AI effectively and accurately.

**Core Problem:** AI models are "more poet than academic" - they predict plausible-sounding text rather than grounding responses in truth, especially for:
- Lesser-quoted biblical texts
- Rare language translations
- Verses with limited internet training data

**Solution:** Provide extensive contextual data (YAML files) for every verse, structured to ground AI responses in truth.

---

## Repository Structure

### Data Organization

```
./bible/{BOOK}/{chapter}/{verse}/{BOOK}-{chapter}-{verse}-{task}.yaml
```

**Standards:**
- Book codes: USFM 3.0 (3-letter uppercase: MAT, JHN, GEN)
- Language codes: ISO-639-3 (3-letter lowercase: eng, grc, heb)
- Verse format: Zero-padded (e.g., MAT.005.003)

**Example:**
```
./bible/MAT/5/3/MAT-5-3-semantic-clusters.yaml
./bible/JHN/11/35/JHN-11-35-translations.yaml
```

### File Formats

**Primary:** YAML (human and AI readable)
**Philosophy:** Loosely structured, merge-friendly, citation-required

---

## SCHEMA.md Analysis

### Core Required Field

```yaml
verse: MAT.005.003  # Always required, zero-padded
```

### Optional Standard Sections

1. **Source Text**
```yaml
source:
  language: GRC
  text: "Greek text here" {grc-NA28-1993}
```

2. **Word-Level Analysis**
```yaml
words:
  - pos: 1
    word: "ἐδάκρυσεν"
    strongs: G1145
    lemma: "δακρύω"
    morphology:
      part_of_speech: verb
      tense: aorist
      voice: active
```

3. **Translation Files**
```yaml
translations:
  eng-NIV-2011: "Translation text"
  eng-ESV-2016: "Translation text"
```

4. **Semantic Clusters**
```yaml
clusters:
  - id: cluster-name
    positions: [1, 2, 3]
    text: "source text"
    rationale: "Why this matters {llm-cs45}"
    patterns:
      - rendering: "translation pattern"
        examples:
          - "Example translation" {eng-NIV-2011}
```

### Citation System

**Format:** `{source-id}` inline with content
**Incremental specificity:** `{lang}` → `{lang}-VERSION` → `{lang}-VERSION-year}`

**Special sources:**
- `{llm-cs45}` - LLM analysis
- `{grc-NA28-1993}` - Greek manuscript
- `{heb-BHS-1997}` - Hebrew manuscript
- `{manual}` - Human curation

### Key Principles

1. **Citation Required:** All content must cite source
2. **Standardized Fields:** Use established field names when possible
3. **Merge-Friendly:** Designed for filtering and merging
4. **Human Readable:** Clear structure, not just machine-parseable

---

## Existing Bible Study Tools

### Location
```
./bible-study-tools/grouping-semantic-clusters/
```

### Structure

**README.md:**
- Tool name and purpose
- Why it must exist
- How it works
- Examples of insights (7 diverse examples)
- Schema reference

**core-instructions.md:**
- Immutable principles
- No hallucination rules
- Citation requirements
- Quality over quantity focus

### Key Lessons from Existing Tool

**Non-Negotiable Principles:**
1. NO HALLUCINATION - only high-confidence data
2. SOURCE CITATION REQUIRED - every fact cited
3. VERSE-CENTRIC OUTPUT - one file per verse
4. NUMBERS FROM CODE, NOT LLMs - qualitative notes only
5. QUALITY OVER QUANTITY - better incomplete than fabricated

**What NOT to Include:**
- Predicted metadata (confidence scores, percentages)
- Unnecessary fields (redundant glosses)
- Duplicate information
- Verbose content without value

**Focus on Value:**
- What would translators copy to notes?
- What helps understand translation choices?
- What reveals theological significance?

---

## AGENTS.md Analysis

**Note:** File exists but is minimal (only 1 line)
**Implication:** No established agent patterns yet in this project

---

## CLAUDE.md Guidance

**Project Stage:** Early stages
**Development Approach:**
1. Human asks AI a question
2. AI clarifies goals and waits for feedback
3. AI creates sample data file for random Scripture
4. Human and AI agent provide feedback
5. AI refines instructions (self-learning loop)
6. Process entire Bible

**Key Insight:** Iterative refinement is core to project methodology

---

## Proposed Tasks (from todo.md)

### Word Analysis
- Analyze every lexicon, concordance for each word
- Find all verses using each word, reverse-engineer to source language

### Bible Translation
- Look up source words in word files
- Identify definitions matching context

### Theology
- Different interpretations and arguments

### Context
- Cultural context impact
- Parallel passages and related scriptures

### Outline
- Break books/chapters into potential outlines

---

## Implications for Agent Design

### Must-Haves

1. **Adherence to SCHEMA.md**
   - Generate valid YAML structure
   - Include required `verse` field
   - Use proper citation format
   - Follow standardization rules

2. **Quality Controls**
   - No hallucination
   - Citation required
   - Qualitative over quantitative
   - Value focus over completeness

3. **Iterative Refinement**
   - Test with sample verses
   - Get feedback (human + AI reviewers)
   - Refine approach
   - Repeat until quality threshold

4. **File Organization**
   - Create proper directory structure
   - Use standardized naming
   - One file per verse per task type

### Design Patterns to Follow

1. **Semantic Cluster Pattern**
   - Start with research phase
   - Generate sample output
   - Multi-perspective review
   - Synthesis and refinement
   - Iteration with max loop limit

2. **Documentation Pattern**
   - README.md with examples
   - LEARNINGS.md with experiments
   - Clear rationale (WHY, not just HOW)
   - Linked to evidence

3. **Citation Pattern**
   - Inline `{source-id}` format
   - Web search for factual verification
   - `{llm-cs45}` for AI analysis
   - Human review flags when uncertain

---

## Gaps and Opportunities

### Current Gaps

1. **No Agent Framework**
   - AGENTS.md is minimal
   - No established agent patterns
   - Opportunity to set standards

2. **Limited Tool Examples**
   - Only one example tool (semantic-clusters)
   - Need more tool patterns
   - Opportunity to create templates

3. **No Experiment Tracking**
   - No standardized LEARNINGS.md format
   - No revision tracking pattern
   - Opportunity to establish conventions

### Opportunities

1. **Create Agent Standards**
   - Document agent patterns in AGENTS.md
   - Establish subagent conventions
   - Create reusable templates

2. **Build Tool Creation Pipeline**
   - Automated tool scaffolding
   - Experiment runner framework
   - Reviewer system

3. **Establish Learning Loop**
   - Structured experiment format
   - Revision tracking
   - Synthesis methodology

---

## Recommendations

### For Bible Study Tool Creator Agent

1. **Follow Semantic Cluster Pattern**
   - Proven successful in project
   - Aligns with project methodology
   - Clear quality standards

2. **Extend with Automation**
   - Automate directory creation
   - Automate README generation
   - Automate reviewer spawning

3. **Add Learning Capture**
   - Structured LEARNINGS.md format
   - Revision directories with README
   - Clear experiment documentation

4. **Build on Existing Standards**
   - Use SCHEMA.md as foundation
   - Follow STANDARDIZATION.md rules
   - Respect core-instructions.md principles

5. **Create Reusable Components**
   - Reviewer subagent template
   - Experiment runner pattern
   - Synthesis methodology

---

## File Structure for New Tools

Based on requirements and existing patterns:

```
./bible-study-tools/{tool-name}/
├── README.md
│   ├── Human-readable title
│   ├── Overview (Why + How)
│   ├── 7 diverse examples of insights
│   └── Schema reference
├── LEARNINGS.md
│   └── Experiment logs with analysis
└── learnings-{experiment-name}-log/
    ├── rev1/
    │   ├── README.md (schema for this revision)
    │   └── {BOOK}-{CH}-{VS}.yaml (verse outputs)
    ├── rev2/
    │   ├── README.md (refined schema)
    │   └── {BOOK}-{CH}-{VS}.yaml (refined outputs)
    └── {persona}-{round}.md (reviewer feedback)
```

---

## Success Criteria

### For Agent System

1. **Generates valid structure**
   - All required directories
   - All required files
   - Proper naming conventions

2. **Produces quality content**
   - Valid YAML against SCHEMA.md
   - All citations present
   - No hallucinated data
   - High value-to-noise ratio

3. **Iterates effectively**
   - Incorporates reviewer feedback
   - Refines schema between revisions
   - Converges on quality output
   - Stops at quality threshold or max iterations

4. **Documents learnings**
   - Clear experiment goals
   - Structured analysis
   - Actionable insights
   - Examples of stellar findings

---

## Next Steps

1. Design agent architecture
2. Create agent instruction files
3. Test with simple experiment
4. Refine based on learnings
5. Document patterns in AGENTS.md
