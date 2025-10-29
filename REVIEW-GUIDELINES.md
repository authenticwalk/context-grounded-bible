# Output Review Guidelines

**Purpose**: Universal validation framework for all Bible study tool outputs

**Version**: 2.2  
**Scope**: All Bible study tools (semantic clusters, word studies, topical research, commentary, etc.)

---

## Review Process Overview

All tool outputs must pass through **THREE LEVELS** of validation:

1. **CRITICAL** - Universal requirements (must pass 100% or REJECT)
2. **HIGH PRIORITY** - Tool-specific requirements (defined in tool's README, typically 80%+ to pass)
3. **MEDIUM PRIORITY** - Quality enhancements (60%+ suggested)

---

## How Tools Should Use These Guidelines

### In Your Tool's README

1. **Reference this document** for CRITICAL (Level 1) requirements - no need to repeat them
2. **Define your HIGH PRIORITY requirements** (Level 2) specific to your tool type
3. **Select relevant personas** for review from the persona list
4. **Adapt the validation checklist** template with your tool-specific checks

### Example README Section

```markdown
## Output Validation

### Critical Requirements
All outputs must pass universal validation from [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) Level 1.

### Tool-Specific Requirements (High Priority)

**Structural**: 3-5 semantic clusters per verse
- Simple verses: 2-3 clusters
- Standard verses: 3-4 clusters  
- Complex verses: 4-5 clusters

**Content Scope**: 100% word coverage required
- Every Greek/Hebrew word must appear in at least one cluster
- Word-by-word breakdown with Strong's numbers
- No single-word clusters unless significant divergence

**Quality Threshold**: Translation utility
- Critical warnings for translators
- Proven solutions by language family
- Grammar-theology connections where relevant

### Relevant Review Personas
- Greek/Hebrew Lexicographer (required)
- Translation Consultant (required)
- Minority Language Translator (recommended)
- Theological Tradition Representative (when relevant)

See [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) for persona details.
```

---

## LEVEL 1: CRITICAL Validation (Must Pass 100%)

These are **universal requirements** for all Bible study tools, regardless of type.

---

### ✅ 1. No Fabricated Data

**Question**: Are all cited sources verified to exist in the source data files?

**Applies To**: All tools

**How to Check**:
- Cross-reference translations with `*-translations.yaml` files
- Verify commentary sources exist if cited
- Confirm lexical data matches Strong's/BDAG if referenced
- Check that cross-references are valid Bible references

**Red Flags**:
- Translation too specific/dramatic without data file evidence
- Citations to sources not in extracted data
- "I recall that..." without verifiable source
- Too-perfect alignment across unrelated languages (likely fabricated)

**Action if Failed**: **REJECT** - Regenerate with strict data grounding

---

### ✅ 2. Inline Citations Present

**Question**: Does every fact, insight, and citation have `{source}` immediately after it?

**Applies To**: All tools

**How to Check**:
- Scan for any factual claims without `{source}` tag
- Verify format: `content {source}` not `content\n{source}`
- Check Greek/Hebrew text has `{grc-na28-1993-dbs}` or equivalent
- Verify LLM-generated insights have `{llm-cs45}` or appropriate model tag

**Red Flags**:
- Missing `{source}` after translations or quotes
- Missing `{llm-*}` after AI-generated insights
- Provenance in separate field instead of inline
- Citations at end of paragraph instead of inline

**Action if Failed**: **REJECT** - Add inline citations throughout

---

### ✅ 3. No Number Predictions

**Question**: Are percentages, confidence scores, or counts avoided in main content?

**Applies To**: All tools

**How to Check**:
- Search for: `%`, `percent`, confidence scores, "X out of Y translations"
- Verify qualitative terms used instead: "most major translations", "many scholars", "some traditions"

**Allowed Exceptions**:
- Confidence scores in validation metadata (not main content)
- Strong's numbers (not predictions)
- Actual verse counts when verifiable (e.g., "appears 3 times in John's Gospel")

**Red Flags**:
- "85% of translations say..."
- "Confidence: 0.92 that this means..."
- "Most scholars (73%) agree..."

**Action if Failed**: **REJECT** - Replace with qualitative descriptions

---

### ✅ 4. Data File Grounding

**Question**: Are all examples from actual data extraction, not LLM memory?

**Applies To**: All tools

**How to Check**:
- Verify tool extracted data BEFORE generating content
- Confirm all citations traceable to data files
- Check that language codes match ISO 639-3 standards

**Red Flags**:
- Content generated before data extraction
- No data files in tool output directory
- Citations to sources not in data files

**Action if Failed**: **REJECT** - Extract data first, then generate content

---

### ✅ 5. Follows Core Principles from CLAUDE.md

**Question**: Are the universal principles from CLAUDE.md followed?

**Applies To**: All tools

**Core Principles**:
1. Extract real data FIRST (don't work from memory)
2. Cite ONLY sources that exist in data files
3. Inline citation format: `content {source}`
4. No number predictions in main content
5. Value over noise focus
6. Practical utility over academic completeness

**Action if Failed**: **REJECT** - Fix violations

---

### ✅ 6. Copyright and Fair Use Compliance

**Question**: Does the output comply with fair use principles for copyrighted Bible translations?

**Applies To**: All tools that reference copyrighted translations (NIV, ESV, NASB, etc.)

**Fair Use Methodology**:
1. **Source-language anchored**: Greek/Hebrew text is primary; translations are derivative evidence
2. **Convergence grouping**: When translations agree, list them collectively without individual quotation
3. **Divergence analysis**: Quote copyrighted translations only in comparative scholarly context
4. **Transformative purpose**: Focus is translation pattern analysis, not text distribution

**How to Check**:
- Verify Greek/Hebrew source text is present and primary
- Confirm copyrighted translations appear in convergence groups or comparative analysis, not standalone
- Check that data structure prevents programmatic reconstruction of any single translation
- Ensure work is complementary to Bible ownership (requires Bibles for full utility)

**Red Flags**:
- Copyrighted translation text in simple key-value format (e.g., `niv: "verse text"`)
- Standalone translation fields without comparative analysis context
- Structure allows easy `forEach/map/reduce` extraction of single translation
- Work could substitute for purchasing Bible translations

**Action if Failed**: **REJECT** - Restructure to ensure source-language primary, comparative analysis focus

**See Also**: [Fair Use Policy](../../plan/policy/fair-use.md) for detailed methodology

---

### ✅ 7. New Sources Added to ATTRIBUTION.md

**Question**: Have all new sources been added to ATTRIBUTION.md with proper copyright notices?

**Applies To**: All tools that introduce sources not already documented

**How to Check**:
- Review all `{source}` citations in the output
- Verify each source exists in [ATTRIBUTION.md](../../ATTRIBUTION.md)
- Confirm new sources have complete copyright notices
- Check that citation format codes match ATTRIBUTION.md entries

**Required Information for New Sources**:
1. **Full copyright notice** with year and copyright holder
2. **Citation format code** used in inline citations
3. **Public domain/open license/fair use designation**
4. **Purchase or access link** when available
5. **Source type category** (translation, commentary, lexicon, etc.)

**Red Flags**:
- Citations using sources not in ATTRIBUTION.md
- New translations without copyright notices
- Missing purchase links for copyrighted works
- Incomplete attribution information

**Action if Failed**: **REJECT** - Add complete attribution to ATTRIBUTION.md before accepting output

**Process for Adding New Sources**:
1. Identify all unique sources used in output
2. Add to appropriate section in ATTRIBUTION.md
3. Include all required attribution information
4. Update source-abbreviations.yaml if new citation code needed
5. Verify citation format consistency

---

## LEVEL 2: HIGH PRIORITY Validation (80%+ to Pass)

**These requirements are tool-specific.** Each tool's README defines what constitutes high-priority validation for its outputs. Below are examples from various tool types.

---

### Tool-Specific Requirements Framework

Each tool should define in its README:

1. **Structural Requirements** - Expected format, sections, granularity
2. **Content Scope** - What should/shouldn't be included
3. **Quality Thresholds** - Minimum standards for acceptance
4. **Target Audience Fit** - Who will use this and for what purpose

---

### Example: Semantic Cluster Tools

**Structural Requirement**: 3-5 focused clusters
- Simple verses (e.g., "Jesus wept"): 2-3 clusters
- Standard verses (e.g., beatitudes): 3-4 clusters
- Complex verses: 4-5 clusters

**Content Scope**: 100% word coverage required
- All Greek/Hebrew words must appear in at least one cluster
- Word-by-word breakdown with Strong's numbers
- No single-word clusters unless significant divergence

**Quality Threshold**: Practical translation value
- Would a translator copy this to their notes?
- Critical warnings highlighted
- Proven solutions by language family

---

### Example: Topical Research Tools

**Structural Requirement**: 5-10 relevant passages
- Cover multiple biblical authors/genres
- Include both OT and NT where applicable
- Organized thematically or chronologically

**Content Scope**: Context over isolated verses
- Surrounding verses for context
- Original audience considerations
- Cultural/historical background

**Quality Threshold**: Sermon/teaching utility
- Would a pastor use this in preparation?
- Multiple angles on topic
- Practical application insights

---

### Example: Word Study Tools

**Structural Requirement**: Semantic range analysis
- All major meanings documented
- Usage patterns across corpus
- Collocations and typical contexts

**Content Scope**: Diachronic development
- Classical → Koine → Modern usage
- Meaning shifts over time
- Testament-specific usage patterns

**Quality Threshold**: Exegetical precision
- Would a scholar trust this analysis?
- Distinguishes homonyms/polysemy
- Cites authoritative lexicons

---

### Universal High-Priority Checks (All Tools)

### ✅ Practical Value ("Would You Copy This to Notes?")

**Question**: Would the target audience copy this to their study materials?

**Applies To**: All tools

**High-Value Indicators**:
- Critical warnings ("NEVER...")
- Cultural insights (specific language families)
- Grammatical-theological connections
- Proven solutions with examples
- Non-obvious patterns

**Low-Value Indicators**:
- Obvious patterns everyone knows
- Academic verbosity without insight
- Repetition without added value
- Generic statements ("This is important")

**Action if Failed**: **RECOMMISSION** - Focus on unique, actionable insights

---

### ✅ Theological Balance

**Question**: Are multiple theological traditions represented fairly when relevant?

**Applies To**: All tools (especially commentary, topical research)

**How to Check**:
- Look for 2-3 traditions mentioned when topic is contested
- Verify no single tradition dominates interpretation
- Check that tradition-specific views are labeled as such

**Good Examples**:
- Reformed tradition emphasizes... {llm-cs45}
- Liberation theology reads this as... {llm-cs45}
- Orthodox tradition connects to... {llm-cs45}

**Red Flags**:
- Only Western/Reformed perspective
- Claims universal agreement on contested doctrines
- Presents one tradition's view as "correct"
- Ignores non-Western interpretive traditions

**Action if Failed**: **RECOMMISSION** - Add balanced perspectives

---

### ✅ Specific Cultural References (Not Generic)

**Question**: Are cultural patterns specific to identifiable groups?

**Applies To**: Tools citing cross-cultural patterns

**Good Examples**:
- Niger-Congo family (Swahili, Yoruba)
- Sino-Tibetan family (Mandarin, Burmese)
- Second Temple Judaism
- Ancient Near East honor-shame cultures

**Bad Examples**:
- "Some cultures..."
- "Eastern languages..."
- "Non-Western translations..."
- "Asian Bibles..."

**Action if Failed**: **RECOMMISSION** - Specify or remove generic claims

---

## LEVEL 3: MEDIUM PRIORITY Validation (60%+ to Pass)

**These are quality enhancements** that add value but aren't essential for acceptance. Each tool may prioritize different enhancements based on its purpose.

---

### ✅ Cross-References Where Relevant

**Question**: Are parallel passages and intertextual connections noted when they add insight?

**Applies To**: Most tools (especially commentary, semantic clusters, topical research)

**When Valuable**:
- OT quotations in NT
- Repeated phrases showing thematic connections
- Typological connections (e.g., Psalm 23 → John 10)
- Theological parallels across corpus

**Example Format**:
```yaml
cross_references:
  - ref: "MAT 5:5"
    connection: "Same beatitude structure" {llm-cs45}
  - ref: "PSA 37:11"
    connection: "OT source for 'inherit the earth'" {llm-cs45}
```

**Not Expected**:
- Exhaustive cross-reference lists
- Tangential connections without clear relevance
- Cross-references without explanation of connection

**Action if Failed**: **ACCEPT WITH NOTES** - Suggest valuable additions

---

### ✅ Grammatical Insights Where Meaningful

**Question**: Is grammar discussed when it affects interpretation or theology?

**Applies To**: Tools focused on exegesis (semantic clusters, word studies, commentary)

**When Valuable**:
- Tense/aspect encoding eschatology
- Voice (passive) indicating divine action
- Case distinctions affecting meaning
- Mood indicating contingency/certainty
- Discourse markers showing structure

**Not Valuable**:
- Grammar for grammar's sake
- Obvious structures everyone knows
- Technical jargon without explanation
- Parsing details without interpretive impact

**Action if Failed**: **ACCEPT WITH NOTES** - Note missed opportunities

---

### ✅ Practical Guidance Documented

**Question**: Are actionable "do this" and "avoid this" guidelines included when appropriate?

**Applies To**: Tools for practitioners (semantic clusters, translation tools)

**Good Format**:
```yaml
translation_guidance:
  preserve: "Future tense in promise - eschatological significance" {llm-cs45}
  avoid: "Specifying mourning cause - limits pastoral breadth" {llm-cs45}
  proven_solutions:
    niger_congo: "Use humility/lowliness metaphor" {llm-cs45}
    sino_tibetan: "Preserve with 'empty heart' idiom" {llm-cs45}
```

**Quality Indicators**:
- Specific, actionable advice
- Proven solutions cited (not theoretical)
- Clear warnings about common errors
- Cultural adaptation strategies

**Action if Failed**: **ACCEPT WITH NOTES** - Suggest additions

---

### ✅ Cultural and Historical Context

**Question**: Is relevant ANE/Second Temple/cultural background provided?

**Applies To**: Commentary, topical research, semantic clusters

**When Valuable**:
- Explains cultural distance from modern readers
- Provides honor-shame framework for understanding
- Notes original audience assumptions
- Connects to ANE parallels
- Clarifies Second Temple Judaism context for NT

**Not Valuable**:
- Generic historical background everyone knows
- Tangential cultural information
- Anachronistic modern concepts imposed on ancient text

**Action if Failed**: **ACCEPT WITH NOTES** - Note missed contextual opportunities

---

## Persona-Based Review Questions

Use these personas to evaluate outputs from different expert perspectives. **Not all personas apply to all tools** - select the relevant ones based on your tool's purpose and audience.

### 👤 **Persona 1: Greek/Hebrew Lexicographer**

**Expertise**: BDAG, Strong's, NA28, semantic ranges, textual criticism

**Questions to Ask**:
1. Are Strongs numbers accurate?
2. Do cluster boundaries respect Greek grammar?
3. Are semantic range distinctions noted (e.g., δακρύω ≠ κλαίω)?
4. Are manuscript variants mentioned if significant?
5. Does the parsing match standard lexicons?

**Red Flags**:
- Cluster breaks mid-phrase against Greek grammar
- Strongs number mismatched to word
- Semantic distinction claimed but not in BDAG

**Use For**: Cluster boundary decisions, word-level accuracy

---

### 👤 **Persona 2: Ancient Near East (ANE) Scholar**

**Expertise**: Cultural context, ANE literature, archaeology, original audience

**Questions to Ask**:
1. Is cultural distance from modern context explained?
2. Are ANE background parallels noted (e.g., honor-shame)?
3. Does interpretation account for original audience worldview?
4. Are anachronisms avoided (modern concepts in ancient text)?
5. Are Second Temple Judaism contexts noted for NT?

**Red Flags**:
- Modern Western individualism imposed on collectivist text
- Ignoring honor-shame dimensions
- Missing ANE parallel texts (e.g., beatitudes in ancient wisdom lit)

**Use For**: Cultural context, avoiding Western bias

---

### 👤 **Persona 3: Minority Language Translator (Specify Culture)**

**Examples**: Quechua translator, Hmong translator, Swahili translator, Arabic translator

**Expertise**: Cross-cultural translation, non-Western perspectives, cultural adaptation

**Questions to Ask**:
1. Are Western assumptions exposed?
2. Are proven cultural adaptations documented?
3. Is honor-shame vs guilt-innocence considered?
4. Are animistic worldview bridges noted?
5. Are specific adaptations actionable (not generic)?

**Red Flags**:
- Only Indo-European examples
- Generic "some cultures" without specifics
- Cultural adaptation suggested without proven example
- Ignoring non-Western theological traditions

**Use For**: Exposing Western bias, cultural solutions

---

### 👤 **Persona 4: Theological Tradition Representative**

**Examples**: 
- Reformed (John Calvin perspective)
- Liberation Theology (Gustavo Gutiérrez perspective)
- Eastern Orthodox (John Chrysostom perspective)
- Catholic (Thomas Aquinas perspective)
- Pentecostal (contemporary charismatic perspective)

**Expertise**: Interpretive traditions, theological debates, doctrinal significance

**Questions to Ask**:
1. Are contested interpretations noted?
2. Is my tradition's view represented fairly?
3. Are other traditions mentioned without bias?
4. Does cluster impact foundational doctrines?
5. Are tradition-specific emphases labeled as such?

**Red Flags**:
- Single tradition assumed universal
- Contested doctrine presented as consensus
- Missing tradition-specific insights
- Heretical interpretation presented neutrally

**Use For**: Theological significance, multi-tradition balance

---

### 👤 **Persona 5: Senior Bible Translation Consultant (Wycliffe/SIL)**

**Expertise**: Translation theory, field experience, quality control, cross-linguistic patterns

**Questions to Ask**:
1. Is this actionable for a translator?
2. Would this prevent common errors?
3. Are proven solutions transferable?
4. Is the advice grounded in actual translation practice?
5. Would I recommend this to my teams?

**Red Flags**:
- Theoretical without practical application
- Advice contradicts field experience
- Missing critical warnings
- Proven solutions not cited

**Use For**: Overall quality, practical viability

---

### 👤 **Persona 6: Pastor/Teacher**

**Expertise**: Sermon preparation, pastoral application, congregational teaching

**Questions to Ask**:
1. Does this enrich my sermon prep?
2. Are pastoral implications noted?
3. Can I explain this to my congregation?
4. Are misinterpretations flagged?
5. Is this spiritually edifying, not just academic?

**Red Flags**:
- Too technical for pastoral use
- Missing pastoral application
- Theological insight without life impact
- Academic completeness over value

**Use For**: Practical value, pastoral relevance

---

### 👤 **Persona 7: Translation Philosophy Expert**

**Examples**:
- Formal Equivalence advocate (NASB, ESV approach)
- Dynamic Equivalence advocate (NIV, NLT approach)
- Paraphrase advocate (MSG, TLB approach)

**Expertise**: Translation unit boundaries, equivalence theory, receptor language primacy

**Questions to Ask**:
1. Does cluster granularity match my philosophy?
2. Are translation unit boundaries defensible?
3. Is receptor language prioritized appropriately?
4. Would my approach preserve this cluster?
5. Are alternative philosophies acknowledged?

**Red Flags**:
- Assumes one translation philosophy is "correct"
- Cluster boundaries that only work for one approach
- Missing discussion of translation unit options

**Use For**: Cluster granularity decisions

---

## Hallucination Detection

### Common LLM Hallucination Markers

**Pattern 1: Too-Perfect Alignment**
- **Red Flag**: Unrelated language families converge suspiciously
- **Example**: "All translations from Indo-European, Sino-Tibetan, Niger-Congo, and Austronesian use exact metaphor"
- **Action**: Verify in data file - likely fabricated

**Pattern 2: High Confidence on Obscure Language**
- **Red Flag**: Rare language cited with specific rendering but no confidence caveat
- **Example**: "Hmong uses 'heart-humble' (moob-daw)" without `requires_human_review`
- **Action**: Flag as `uncertain` or omit if confidence <90%

**Pattern 3: Violates Greek Grammar Without Explanation**
- **Red Flag**: Cluster boundary splits prepositional phrase or breaks case agreement
- **Example**: Cluster "poor" separate from "in spirit" when τῷ πνεύματι is dative modifier
- **Action**: Consult lexicographer persona - likely error

**Pattern 4: Rendering Contradicts Lexicon**
- **Red Flag**: Translation given that contradicts BDAG semantic range
- **Example**: πτωχός translated "spiritually bankrupt" when BDAG says "poor, destitute"
- **Action**: Check BDAG - if contradicts, likely hallucination

**Pattern 5: Anachronistic Language**
- **Red Flag**: Modern slang or concepts in ancient text
- **Example**: "emotional intelligence" for καρδία
- **Action**: Consult ANE scholar persona - remove anachronism

**Pattern 6: Textual Variant Not in NA28**
- **Red Flag**: Manuscript variant claimed but not in standard apparatus
- **Example**: "Some manuscripts add 'greatly' after 'mourn'"
- **Action**: Verify in NA28 apparatus - if absent, remove

---

## Confidence Levels & Human Review Triggers

### Confidence Scoring (When Present)

```yaml
certain: 0.95-1.0        # Include in main dataset
high: 0.80-0.94          # Include with confidence score
medium: 0.60-0.79        # Mark as "needs validation"
low: 0.40-0.59           # Omit or flag as "uncertain"
very_low: 0.0-0.39       # Do not include (hallucination risk)
```

### Automatic Human Review Triggers

**Flag `requires_human_review: true` IF**:

1. **Theological Significance**
   - Foundational doctrine (Trinity, atonement, resurrection)
   - Contested interpretation across traditions
   - Impacts divine name/title translation

2. **Textual Criticism**
   - Manuscript variants change meaning significantly
   - NA28 vs Textus Receptus diverge
   - Variant affects cluster boundary

3. **Low Confidence**
   - LLM confidence <0.80 on any component
   - Sparse training data for language
   - Suspected hallucination (see markers above)

4. **Cultural Sensitivity**
   - Cultural adaptation might cause offense
   - Honor-shame implications
   - Potential for syncretism
   - Translation impacts interfaith relations

---

## Quality Metrics

**Note**: Each tool should define quality metrics in its README. Below are universal principles and tool-specific examples.

---

### Universal Quality Principles (All Tools)

**Balance**:
- **Not too sparse**: Enough detail to be useful
- **Not too verbose**: Concise, no redundancy
- **Value density**: High ratio of insights to word count

**Specificity**:
- Named sources, not "scholars say"
- Specific language families, not "some cultures"
- Concrete examples, not abstract generalizations

**Actionability**:
- Clear next steps for target audience
- Warnings about common errors
- Proven solutions with context

---

### Example: Semantic Cluster Tool Metrics

**Optimal Ranges** (from experiments):
- Cluster count: 3-4 for standard verses
- Token range: 2000-2500 per verse
- Translation coverage: 10+ languages from diverse families
- Theological traditions: 2-3 when relevant

**Effective Patterns**:
- Convergence/divergence framework
- Language family specificity
- Grammar-theology connections
- Critical warnings prominently placed

**Anti-Patterns**:
- Single-word clusters without divergence
- Under 1500 tokens (too sparse)
- Over 3000 tokens (diminishing returns)
- Generic cultural references

---

### Example: Topical Research Tool Metrics

**Optimal Ranges**:
- Passage count: 5-10 primary passages
- Coverage: Both OT and NT when applicable
- Perspective count: 2-3 theological traditions

**Effective Patterns**:
- Thematic organization
- Context included (surrounding verses)
- Multiple genres represented
- Practical application insights

**Anti-Patterns**:
- Isolated verses without context
- Single-tradition dominance
- Exhaustive lists without curation
- Academic without practical value

---

### Example: Word Study Tool Metrics

**Optimal Ranges**:
- Semantic senses: 3-7 major meanings
- Example count: 2-3 per sense
- Testament coverage: Both OT and NT usage

**Effective Patterns**:
- Semantic range clearly mapped
- Diachronic development shown
- Collocations documented
- Lexicon citations

**Anti-Patterns**:
- Conflating homonyms
- Missing key semantic distinctions
- Memory-based definitions (not data)
- Ignoring usage patterns

---

## Decision Framework

### ACCEPT

**Criteria**:
- All CRITICAL (Level 1) checks pass ✅
- 80%+ of HIGH PRIORITY (Level 2) checks pass ✅
- Practical value evident
- No fabricated data
- No hallucination markers

**Action**: Present to user with highlights of key insights

---

### RECOMMISSION (Max 2 Attempts)

**Criteria**:
- All CRITICAL (Level 1) checks pass ✅
- 50-79% of HIGH PRIORITY (Level 2) checks pass ⚠️
- Issues are correctable

**Correctable Issues**:
- Incomplete word coverage (need 100%)
- Too verbose without value
- Generic cultural patterns
- Minor citation gaps
- Theological imbalance

**Action**: Provide specific corrections, regenerate

---

### REJECT

**Criteria**:
- Any CRITICAL (Level 1) check fails ❌
- Fabricated translations present
- No data extraction performed
- Missing word breakdown
- No inline citations
- Violated non-negotiables

**Action**: Start over with strict adherence to core instructions

---

## Validation Checklist Template

**Note**: Adapt this template for your specific tool. Add tool-specific checks under `high_priority_checks` based on your README requirements. Include only relevant persona reviews.

```yaml
validation:
  tool_name: "[Tool name]"
  tool_version: "[Version]"
  reviewer_id: "[Your Name/ID]"
  reviewer_type: "[community/scholar/translator/pastor/authority]"
  date: "YYYY-MM-DD"
  target: "[BOOK CHAPTER:VERSE or topic or word being studied]"
  
  critical_checks:
    no_fabrication: [PASS/FAIL]
    inline_citations: [PASS/FAIL]
    no_numbers: [PASS/FAIL]
    data_file_only: [PASS/FAIL]
    follows_core_principles: [PASS/FAIL]
    copyright_compliance: [PASS/FAIL/NA]
    new_sources_attributed: [PASS/FAIL/NA]
  
  high_priority_checks:
    # Add tool-specific checks from tool's README
    # Examples:
    # word_coverage_100: [PASS/FAIL/NA]  # For semantic clusters
    # cluster_count_appropriate: [PASS/FAIL/NA]  # For semantic clusters
    # passage_count_appropriate: [PASS/FAIL/NA]  # For topical research
    # semantic_range_complete: [PASS/FAIL/NA]  # For word studies
    
    # Universal checks:
    practical_value: [PASS/FAIL]
    theological_balance: [PASS/FAIL/NA]
    specific_not_generic: [PASS/FAIL/NA]
  
  medium_priority_checks:
    cross_references: [PASS/FAIL/NA]
    grammatical_insights: [PASS/FAIL/NA]
    practical_guidance: [PASS/FAIL/NA]
    cultural_context: [PASS/FAIL/NA]
  
  persona_reviews:
    # Include only personas relevant to your tool type
    # Rate 1-5 where applicable, NA if persona doesn't apply
    lexicographer:
      rating: [1-5/NA]
      notes: ""
    ane_scholar:
      rating: [1-5/NA]
      notes: ""
    minority_translator:
      rating: [1-5/NA]
      notes: ""
    theologian:
      rating: [1-5/NA]
      notes: ""
    translation_consultant:
      rating: [1-5/NA]
      notes: ""
    pastor:
      rating: [1-5/NA]
      notes: ""
    translation_philosophy_expert:
      rating: [1-5/NA]
      notes: ""
  
  hallucination_check:
    markers_found: [NONE/list if found]
    confidence_flags: [NONE/list if needed]
    
  decision: [ACCEPT/RECOMMISSION/REJECT]
  overall_rating: [1-5]
  notes: ""
  recommended_human_review: [true/false]
  human_review_reason: ""
```

---

## Quick Reference: Common Issues & Fixes

| Issue | Severity | Fix |
|-------|----------|-----|
| Missing `{source}` tags | CRITICAL | Add inline citations throughout |
| Fabricated data | CRITICAL | Remove, cite only from data files |
| No data extraction performed | CRITICAL | Extract data BEFORE generating content |
| Used percentages/predictions | CRITICAL | Replace with qualitative terms |
| Copyright violation (standalone translations) | CRITICAL | Restructure: source-language primary, convergence grouping |
| New source not in ATTRIBUTION.md | CRITICAL | Add complete attribution to ATTRIBUTION.md |
| Generic "some cultures" | HIGH | Specify language family/tradition or remove |
| Single tradition dominance | HIGH | Add 1-2 other perspectives when relevant |
| No practical value | HIGH | Focus on actionable insights for target audience |
| Too verbose | HIGH | Trim redundancy, maintain value density |
| Missing cross-refs (when relevant) | MEDIUM | Add where they provide insight |
| No grammar insights (when relevant) | MEDIUM | Add if affects interpretation |
| Missing cultural context | MEDIUM | Add ANE/Second Temple background when helpful |
| Tool-specific structure issues | Varies | See tool's README for specific requirements |

---

**Version**: 2.2  
**Status**: Production-ready (Universal framework)  
**Last Updated**: 2025-10-29  
**Scope**: All Bible study tools (semantic clusters, topical research, word studies, commentary, etc.)  
**Originally Based On**: Semantic cluster experiments Phase 1 & 2, generalized for all tool types

