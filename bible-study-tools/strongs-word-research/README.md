# Strong's Word Research

**Version:** 1.0.0
**Status:** experimental
**Created:** 2025-10-30
**Last Updated:** 2025-10-30

**Token Efficiency:** Main README target ≤500 lines. Inline only what's relevant to THIS tool.

---

## Purpose

This tool provides comprehensive research on each Strong's Concordance word (14,197 Greek and Hebrew words), extracting etymology, semantic ranges, scholarly insights, and usage patterns from multiple authoritative sources. It goes beyond the basic Strong's definition to provide "a book's worth of information" for AI grounding.

**Target Audience:** Bible translators, pastors, seminary students, lexicographers, and AI systems requiring deep contextual understanding of biblical language.

**Primary Use Case:** When translating or studying a biblical word, users need more than a gloss - they need cultural context, scholarly consensus/divergence, etymology, diachronic development, and awareness of common misconceptions. This tool provides that depth, enabling AI to give accurate, nuanced answers about biblical language that go beyond compressed training data.

---

## Research Methodology

### Phase 1: Data Extraction

**Required Sources:**

**ALWAYS start with:**
- [x] Base Strong's file: `./bible/words/strongs/{number}/{number}.strongs.yaml`
  - Contains pre-imported open-licensed data (BDB, Thayer's, unfoldingWord, LSJ)
  - Foundation for all research - read this FIRST

**Web search for scholarly resources:**
- [ ] Generic web search: `"Strong's {number}"`, `"{transliteration} Greek etymology"`
- [ ] Academic search: `"{transliteration} {gloss} biblical" site:.edu`
- [ ] PDF search: `"{transliteration} New Testament" filetype:pdf`
- [ ] Commentary search: `"Strong's {number}" commentary analysis`

**Established lexicon sites** (check ATTRIBUTION.md for URL patterns):
- [x] BibleHub: `https://biblehub.com/greek/{number}.htm`
- [x] Blue Letter Bible: `https://www.blueletterbible.org/lexicon/g{number}/kjv/tr/0-1/`
- [x] StudyLight.org: `https://www.studylight.org/lexicons/eng/greek/{number}.html`

**Controversy and discussion sources:**
- [ ] Biblical Hermeneutics Stack Exchange: search `{number}` or transliteration
- [ ] Theological blogs: search `"{transliteration} misconception"` or `"{transliteration} controversy"`
- [ ] Academic discussions: journals, seminary websites

**Note:** Many additional resources will be discovered through web searches. Document all sources used in the output file.

**Extraction Process:**

1. **Read base Strong's file FIRST** - Always start here
   - File: `./bible/words/strongs/{number}/{number}.strongs.yaml`
   - Contains: strongs_number, language, lemma, transliteration, definition, kjv_usage, derivation
   - This includes imported open-licensed data (BDB, Thayer's, unfoldingWord, LSJ)
   - **Cross-reference codes:** May include references to other lexicon systems (see below)
   - Use this as foundation - do NOT re-extract what's already there

   **Cross-Reference Codes (will grow over time):**
   - When present in base file, use these for additional searches
   - Common systems that may be added: BDB, BDAG, Louw-Nida, TDNT, GK, TWOT, LSJ
   - Example searches: `"BDAG {code}"`, `"Louw-Nida {domain}"`, `"TDNT {reference}"`

2. **Generic web search** - Discover additional scholarly resources
   - Search: `"Strong's {number}"` or `"Strong's G{number}"` or `"Strong's H{number}"`
   - Search: `"{transliteration} Greek etymology"` or `"{transliteration} Hebrew etymology"`
   - **If cross-reference codes present:** Search by those too
     - `"BDAG {code}"` (Greek lexicon)
     - `"BDB {code}"` (Hebrew lexicon)
     - `"Louw-Nida {domain}"` (semantic domains)
     - `"TDNT {reference}"` (theological dictionary)
     - `"GK {number}"` or `"Goodrick-Kohlenberger {number}"`
     - `"TWOT {code}"` (Hebrew theology)
   - Look for: Academic articles, theological journals, biblical language blogs
   - Note: Many scholarly articles cite multiple numbering systems

3. **Scholarly article search** - Find academic analysis
   - Search: `"{transliteration} {gloss} biblical Greek" site:.edu`
   - Search: `"{transliteration} New Testament usage" filetype:pdf`
   - Search: `"Strong's {number}" commentary analysis`
   - Target: Journal articles, seminary papers, linguistic dissertations
   - Note any analysis that uses this Strong's number in context

4. **BibleHub extraction** - Comprehensive lexicon overview
   - URL: `https://biblehub.com/greek/{number}.htm` or `https://biblehub.com/hebrew/{number}.htm`
   - Extract: Etymology, usage statistics, related words, topical analysis
   - Cross-reference with base file to avoid duplication

5. **StudyLight cross-reference** - Additional lexicon perspectives
   - URL: `https://www.studylight.org/lexicons/eng/greek/{number}.html`
   - Look for: Abbott-Smith, Vocabulary of Greek NT, Mounce's (not in base file)
   - Focus on: Papyri examples, non-biblical usage patterns

6. **Blue Letter Bible** - Synonym analysis and TDNT
   - URL: `https://www.blueletterbible.org/lexicon/g{number}/kjv/tr/0-1/`
   - Extract: TDNT references, Trench's synonym distinctions
   - Comparative analysis with related words

7. **Search for controversies and discussions**
   - Biblical Hermeneutics Stack Exchange: search by number or transliteration
   - Theological blogs: search `"{transliteration} misconception"` or `"{transliteration} controversy"`
   - Common teaching errors (like dunamis/dynamite)
   - Scholarly debates about meaning or usage

**Critical Rules:**
- Extract data BEFORE generating any analysis. Never work from memory.
- Read base Strong's file FIRST - avoid re-extracting imported data
- **Check for cross-reference codes** - Search by BDB, BDAG, Louw-Nida, etc. when present
- Cast wide net with web searches - many resources cite multiple numbering systems
- Document ALL sources used, even if not explicitly listed above

### Phase 2: Analysis and Synthesis

**Analysis Framework:**

1. **Identify convergence patterns** - Where do lexicons agree?
   - Document consensus definitions
   - Note which lexicons converge (list collectively per fair use)

2. **Highlight divergence** - Where do scholars disagree?
   - Semantic range debates
   - Theological interpretation differences
   - Classical vs. Koine usage distinctions

3. **Flag controversies** - Common errors and misconceptions
   - Popular but incorrect etymologies
   - Anachronistic interpretations
   - Scholarly refutations

4. **Trace diachronic development** - How did meaning evolve?
   - Classical Greek → Koine Greek → Modern Greek
   - Classical Hebrew → Biblical Hebrew → Modern Hebrew
   - Septuagint influence on NT Greek words

**Synthesis Guidelines:**

- Focus on insights that provide practical value for translators and students
- Identify convergence and divergence patterns across lexicons
- Highlight cultural and historical context that aids understanding
- Note theological significance when relevant
- Document synonym distinctions that aid precise translation

### Phase 3: Citation and Verification

**Critical validation** (from REVIEW-GUIDELINES.md Level 1 - must pass 100%):

- [ ] No fabricated data - all sources verified
- [ ] Inline citations: `content {source}` (not separate fields)
- [ ] No percentages or predictions (use "most", "many", "some")
- [ ] Data extracted BEFORE analysis (not from memory)
- [ ] All new sources in ATTRIBUTION.md

**Tool-specific validation:**

- [ ] Etymology verified from multiple lexicons (not invented)
- [ ] Usage statistics match source data exactly
- [ ] Synonym distinctions cite authoritative sources (TDNT, Trench, etc.)
- [ ] Controversies documented with scholarly references
- [ ] Authority levels clearly marked (lexicons > web resources > community discussions)

See REVIEW-GUIDELINES.md for full details if needed.

---

## Output Schema

### Filename Format

```
./bible/words/strongs/{STRONG_NUM}/{STRONG_NUM}-word-research.yaml
```

**Components:**
- `{STRONG_NUM}`: Strong's number with prefix (G0001-G5624 for Greek, H0001-H8674 for Hebrew)

**Examples:**
- `./bible/words/strongs/G1411/G1411-word-research.yaml` (dunamis - power)
- `./bible/words/strongs/G0026/G0026-word-research.yaml` (agape - love)
- `./bible/words/strongs/H0430/H0430-word-research.yaml` (Elohim - God)

### YAML Structure

**Required fields** (from SCHEMA.md):
- `strongs_number`: The Strong's number (G#### or H####)
- Inline citations: `"content {source}"` immediately after every fact
- `metadata.tokens_used`: populate from API response

**Optional standard fields** (use only if relevant):
- `language`: "greek" or "hebrew"
- `lemma`: The lexical form
- `transliteration`: Romanized form
- `etymology`: Root words and derivation
- `semantic_range`: Multiple meanings with contexts
- `synonyms`: Related words with distinctions

```yaml
# === METADATA ===
strongs_number: "{STRONG_NUM}"
language: "{greek|hebrew}"
lemma: "{lexical_form}"
transliteration: "{romanized}"

tool:
  name: "strongs-word-research"
  version: "1.0.0"
  generated_date: "YYYY-MM-DD"

# === BASE DATA (from ./bible/words/strongs/{number}/{number}.strongs.yaml) ===
# This section copied from pre-imported base file
base_data:
  strongs_number: "{number}"
  language: "{greek|hebrew}"
  lemma: "{lexical_form}"
  transliteration: "{romanized}"
  definition: "{base definition}" {strongs}
  kjv_usage: "{KJV usage}" {strongs}
  derivation: "{derivation}" {strongs}

  # Cross-reference codes to other lexicon systems (when present in base file)
  cross_references:
    bdb: "{code}"           # Brown-Driver-Briggs (Hebrew)
    bdag: "{code}"          # Bauer-Danker-Arndt-Gingrich (Greek)
    louw_nida: "{domain}"   # Louw-Nida semantic domain
    tdnt: "{reference}"     # Theological Dictionary of NT
    gk: "{number}"          # Goodrick-Kohlenberger
    twot: "{code}"          # Theological Wordbook of OT (Hebrew)
    lsj: "{code}"           # Liddell-Scott-Jones (Classical Greek)

  # Additional fields from base file (imported lexicon data)
  imported_lexicon_data: |
    {Any additional data from open-licensed imports in base file}

# === ETYMOLOGY ===
etymology:
  root_words:
    - word: "{root_word_1}"
      strongs: "{number}"
      meaning: "{root meaning}" {biblehub-lexicon}
  derivation_notes: "{detailed etymology}" {thayer} {biblehub-lexicon}
  diachronic_development: |
    {Classical/Biblical/Modern usage patterns if significantly different}
    {llm-cs45}

# === LEXICAL CONVERGENCE ===
# Where multiple authoritative lexicons agree
lexical_convergence:
  primary_meaning: "{core agreed definition}"
  lexicons_agreeing: [thayer, bdag, helps, lsj-abridged, bdb]
  usage_notes: "{consensus notes on usage}" {lexicon-citations}

# === LEXICAL DIVERGENCE ===
# Where scholars/lexicons disagree
lexical_divergence:
  - semantic_area: "{area of disagreement}"
    approach_1:
      definition: "{first interpretation}"
      sources: [lexicon1, lexicon2]
      rationale: "{why this view}" {llm-cs45}
    approach_2:
      definition: "{second interpretation}"
      sources: [lexicon3, lexicon4]
      rationale: "{why this view}" {llm-cs45}

# === SEMANTIC RANGE ===
semantic_range:
  - category: "{meaning category 1}"
    definition: "{specific meaning}" {thayer} {biblehub-lexicon}
    biblical_examples:
      - ref: "{BOOK.chapter.verse}"
        context: "{how it's used here}" {biblehub-interlinear}
  - category: "{meaning category 2}"
    definition: "{specific meaning}" {thayer} {biblehub-lexicon}
    biblical_examples:
      - ref: "{BOOK.chapter.verse}"
        context: "{how it's used here}" {biblehub-interlinear}

# === USAGE STATISTICS ===
usage_statistics:
  total_occurrences: {count} {biblehub-lexicon}
  grammatical_forms: {count} {biblehub-lexicon}
  testament_distribution:
    old_testament: {count if applicable}
    new_testament: {count if applicable}
  kjv_translation_frequency:
    - translation: "{English word}"
      count: {number} {biblehub-lexicon}

# === SYNONYM ANALYSIS ===
# Distinctions from related words
synonyms:
  - word: "{related_word}"
    strongs: "{number}"
    distinction: "{how meanings differ}" {tdnt} {trench} {biblehub-lexicon}
    usage_contrast: "{when to use each}" {llm-cs45}

# === SCHOLARLY INSIGHTS ===
# From commentaries, TDNT, academic articles
scholarly_insights:
  - insight: "{specific scholarly observation}"
    source: {tdnt} {commentary-reference}
    significance: "{why this matters for interpretation}" {llm-cs45}

# === THEOLOGICAL SIGNIFICANCE ===
# Only when theologically important words
theological_significance:
  key_themes:
    - theme: "{theological concept}"
      explanation: "{how word relates to theme}" {helps} {tdnt}
      biblical_foundation: "{key verses}" {llm-cs45}

# === CONTROVERSIES & MISCONCEPTIONS ===
# Common errors, scholarly debates (clearly marked as lower authority for web discussions)
controversies:
  - type: "{misconception|scholarly_debate|popular_error}"
    claim: "{the controversial claim}"
    refutation: "{scholarly correction}" {source}
    evidence: "{why the correction is accurate}" {source}
    authority_level: "{high|medium|low}"

# === CULTURAL & HISTORICAL CONTEXT ===
cultural_context:
  classical_usage: "{how word used in classical Greek/Hebrew}" {lsj} {bdb}
  biblical_era_context: "{cultural significance in biblical times}" {llm-cs45 citing sources}
  septuagint_influence: "{LXX usage patterns if relevant for NT Greek}" {llm-cs45}

# === PRACTICAL TRANSLATION GUIDANCE ===
translation_guidance:
  formal_equivalence:
    suggestions: ["{word1}", "{word2}"]
    rationale: "{why these preserve meaning}" {llm-cs45}
  dynamic_equivalence:
    suggestions: ["{word1}", "{word2}"]
    rationale: "{how these communicate intent}" {llm-cs45}
  cultural_adaptation_notes: "{when cultural context requires explanation}" {llm-cs45}

# === KEY INSIGHTS ===
key_insights:
  - insight: "{Specific valuable discovery from research}" {llm-cs45}
    rationale: "{Why this matters for translators/students}" {llm-cs45}

# === CROSS-REFERENCES ===
cross_references:
  related_strongs:
    - strongs: "{number}"
      relationship: "{synonym|antonym|root|derived}" {llm-cs45}

# === SOURCES USED ===
sources:
  websites:
    - url: "https://biblehub.com/{greek|hebrew}/{number}.htm"
    - url: "https://www.blueletterbible.org/lexicon/{g|h}{number}/kjv/tr/0-1/"
    - url: "https://www.studylight.org/lexicons/eng/greek/{number}.html"
    # Add any additional sources used

metadata:
  date_time: "YYYY-MM-DD HH:MM:SS"
  tool_version: "strongs-word-research-v1.0"
  tokens_used: {count}
  errors_fixed: {count}
```

### Schema Guidelines

**Authority Levels:**

Mark each section clearly by source authority:
- **High Authority:** Published lexicons (Thayer's, BDB, BDAG, LSJ, TDNT)
- **Medium Authority:** Structured web resources (BibleHub aggregations)
- **Low Authority:** Community discussions (Stack Exchange, blogs)

Use inline citations to show authority level.

**Citation Format:**
- Inline: `"content {source}"`
- Multiple sources for convergence: `{thayer} {bdag} {helps}`
- Never use separate `source:` fields

---

## Output Validation

### Level 1: CRITICAL Requirements (Must Pass 100%)

From REVIEW-GUIDELINES.md Level 1:
- ✅ No fabricated data
- ✅ Inline citations: `content {source}`
- ✅ No percentages (use qualitative: "most", "many", "some")
- ✅ Extract data FIRST
- ✅ New sources in ATTRIBUTION.md

**Action if Failed:** REJECT

### Level 2: HIGH PRIORITY Requirements (80%+ to Pass)

#### Structural Requirements
- Etymology verified from multiple lexicons (not invented)
- At least 3 semantic range categories for words with 20+ occurrences
- Usage statistics match source data exactly
- Synonym distinctions cite authoritative sources when included

#### Content Scope
- All major meanings documented (Thayer's categories covered)
- Diachronic development when word has significant Classical vs. Koine shift
- Controversies documented when they exist (e.g., dunamis/dynamite)
- Cultural context when culturally-bound concept

#### Quality Thresholds
- Would a translator copy this to their notes?
- Would a seminary student trust this for exegesis?
- Are common pitfalls clearly flagged?

#### Target Audience Fit
- Practical translation guidance provided
- Theological significance explained when relevant
- Technical terms explained accessibly

### Level 3: MEDIUM PRIORITY Requirements (60%+ to Pass)

These are quality enhancements from REVIEW-GUIDELINES.md Level 3:

- ✅ Cross-references to related Strong's numbers
- ✅ Grammatical insights (from TDNT, technical lexicons)
- ✅ Practical translation guidance documented
- ✅ Cultural and historical context provided

---

## Quality Metrics

### Optimal Ranges

**Quantitative Metrics:**
- Etymology section: Always present, citing 2+ lexicons
- Semantic range: 2-7 categories (varies by word complexity)
- Token range: 1,500-3,500 per word (simple words lower, complex theological terms higher)
- Usage statistics: Always include total occurrences and top 3-5 KJV translations

**Qualitative Metrics:**
- Multiple lexicon sources represented (3+ for Greek, 2+ for Hebrew)
- Authority levels clearly distinguished
- Controversies flagged when present

### Effective Patterns

- **Convergence/divergence framework** for lexicon comparison
- **Controversy flagging** with scholarly refutation (dunamis/dynamite example)
- **Diachronic analysis** when Classical → Koine shift is significant
- **Synonym distinctions** from TDNT/Trench with usage guidance
- **Translation guidance** balancing formal and dynamic approaches

### Anti-Patterns

- Generic definitions without lexicon sources
- Etymology invented from modern languages (anachronism)
- Missing controversies that exist (e.g., not noting dunamis/dynamite error)
- Single-source data without cross-verification
- Overly technical without practical application

---

## Examples of Stellar Outputs

### Example 1: G1411 (δύναμις - dunamis)

**What Made This Excellent:**

This word demonstrates the tool's value by documenting the dunamis/dynamite controversy - a common pastoral error. The research shows: (1) Etymology from δύναμαι "to be able" {thayer} {biblehub-lexicon}, (2) Seven usage categories from Thayer's (universal strength, miraculous power, moral excellence, wealth, numerical strength, military forces, word meaning), (3) 120 NT occurrences with distribution data, (4) Critical controversy section refuting "dunamis = dynamite" claim with evidence that dynamite was invented 1867 {scribalcafe} {gotquestions}, and (5) Synonym distinctions from five related power words (βία, ἐξουσία, ἰσχύς, κράτος, ἐνέργεια) {trench}.

**Key Elements:**
- Comprehensive 7-category semantic range from authoritative source
- Controversy flagged with scholarly refutation and evidence
- Synonym analysis prevents confusion with related terms
- Practical value: prevents common preaching error

**File Location:** `./bible/words/strongs/G1411/G1411-word-research.yaml`

---

### Example 2: G0026 (ἀγάπη - agape)

**What Made This Excellent:**

This theologically critical word benefits from: (1) Etymology from ἀγαπάω with LXX influence noted {biblehub-lexicon}, (2) Clear distinction from romantic/natural affection {helps}, (3) Cultural context of early church love feasts (agapai) {thayer}, (4) 116 NT occurrences documented, (5) Theological significance section on divine love and Spirit-produced virtue, (6) Translation guidance warning against generic "love" that misses theological weight.

**Key Elements:**
- Theological significance clearly explained
- Cultural practice (love feasts) documented
- Etymology traces LXX → NT usage
- Translation guidance prevents over-simplification

**File Location:** `./bible/words/strongs/G0026/G0026-word-research.yaml`

---

## Common Challenges and Solutions

### Challenge 1: Limited Data for Rare Words

**Problem:** Some Strong's words appear only 1-2 times in Scripture, limiting available research.

**Solution:**
- Focus on etymology and root word analysis
- Document what lexicons do say, even if brief
- Note rarity explicitly: "Appears only in {verse} {biblehub-lexicon}"
- Cross-reference related Strong's numbers with more data

**Prevention:** Don't fabricate elaborate semantic ranges for rare words - be honest about limited data.

---

### Challenge 2: Lexicon Access Limitations

**Problem:** Premium lexicons (BDAG, TDNT) not fully accessible via web scraping.

**Solution:**
- Use freely available lexicons (Thayer's, Strong's, LSJ-abridged, BDB)
- Note TDNT references when shown on BLB but don't fabricate content
- Focus on convergence patterns from available sources
- Future: Import open-licensed lexicons (see plan document)

**Prevention:** Never fabricate BDAG/TDNT content - only cite what's actually accessible.

---

### Challenge 3: Separating Classical from Koine Usage

**Problem:** LSJ shows Classical Greek usage; may differ significantly from NT Koine.

**Solution:**
- Document both when divergent: "Classical usage: {meaning} {lsj}; NT usage: {meaning} {thayer}"
- Note the shift explicitly in diachronic_development section
- Use Thayer's and NT-focused lexicons as primary for meaning
- LSJ as supporting evidence for etymology and semantic development

**Prevention:** Don't assume Classical meaning = NT meaning without verification.

---

## How to Use This Tool's Outputs

### For Bible Translators

Use Strong's word research to make informed translation decisions with full semantic range, cultural context, and scholarly consensus/divergence.

**Workflow:**
1. Look up the Strong's number for the word in your source text
2. Review semantic range to identify which category fits the context
3. Check translation guidance for formal vs. dynamic options
4. Note cultural context that may require footnotes
5. Review controversies to avoid common errors

---

### For Pastors and Teachers

Use this research for sermon preparation, especially for key theological terms, to avoid common misconceptions and provide accurate linguistic background.

**Workflow:**
1. Identify key words in your passage via Strong's numbers
2. Review controversy section first - avoid common errors
3. Read theological significance for sermon applications
4. Use synonym distinctions to clarify precise meaning
5. Note cultural context for illustrations

---

### For Seminary Students

Use this research for exegetical papers and word studies, with proper citation of original lexical sources.

**Workflow:**
1. Extract semantic range and usage statistics
2. Trace etymology for diachronic analysis
3. Review scholarly insights and TDNT references
4. Cite original lexicons (Thayer's, BDB, etc.) not this tool
5. Use as starting point, verify claims in primary sources

---

## Research Guidelines for Bible-Researcher Agent

### Pre-Generation Checklist

Before generating any output, ensure:

- [ ] Tool README fully read and understood
- [ ] Strong's number verified (G#### or H####)
- [ ] **Base Strong's file read FIRST**: `./bible/words/strongs/{number}/{number}.strongs.yaml`
- [ ] Cross-reference codes noted (BDB, BDAG, Louw-Nida, etc.) for additional searches
- [ ] Generic web searches planned (Strong's + any cross-reference codes)
- [ ] Data extraction strategy planned (base file → web search → lexicons → discussions)
- [ ] Schema structure internalized

### During Generation

- [ ] **Read base Strong's file FIRST** - Start with pre-imported data
- [ ] **Note cross-reference codes** - Use for additional searches (BDB, BDAG, Louw-Nida, etc.)
- [ ] Cast wide net with web searches - use Strong's number AND cross-reference codes
- [ ] Extract data from sources, analyze SECOND
- [ ] Cite every fact with inline `{source}` tags
- [ ] Add new sources to ATTRIBUTION.md immediately
- [ ] Mark authority levels clearly (lexicon > scholarly article > web > community)
- [ ] Stay within defined schema structure
- [ ] Focus on translator/student needs

### Post-Generation Quality Control

Review from these perspectives:

**Scholarly Accuracy:**
- [ ] Etymology verified from multiple lexicons (not invented)
- [ ] Usage statistics match source data exactly
- [ ] All claims properly sourced

**Lexicographic Completeness:**
- [ ] All major semantic categories documented
- [ ] Synonym distinctions cited from authoritative sources
- [ ] Diachronic development noted when significant

**Controversy Awareness:**
- [ ] Common misconceptions flagged
- [ ] Scholarly refutations documented
- [ ] Authority level marked (high/medium/low)

**Translation Utility:**
- [ ] Practical translation guidance provided
- [ ] Cultural context aids understanding
- [ ] Theological significance explained when relevant

**Source Reliability:**
- [ ] Citations from authoritative lexicons
- [ ] Can every claim be traced?
- [ ] All sources documented in ATTRIBUTION.md?

**Fair Use Compliance:**
- [ ] Convergence patterns documented (not full lexicon entries)
- [ ] Divergence in comparative context
- [ ] Inline citations present
- [ ] Cannot reconstruct any single lexicon

---

## Version History

### Version 1.0.0 (2025-10-30)
- Initial creation based on comprehensive research
- URL patterns documented for BibleHub, BLB, StudyLight
- Dunamis/dynamite controversy documented as exemplar
- Schema designed for authority-level separation
- Fair use compliance built into methodology

---

## Related Tools

- **original-language-words**: Analyzes words in context of specific verses; this tool provides comprehensive word data independent of verse context
- **grouping-semantic-clusters**: Uses Strong's numbers; this tool provides the deep word research that informs cluster analysis

---

## References

**Lexical Resources:**
- BibleHub Lexicons: https://biblehub.com
- Blue Letter Bible: https://www.blueletterbible.org
- StudyLight.org: https://www.studylight.org

**Open-Licensed Resources (for future import):**
- OpenScriptures Strong's: github.com/openscriptures/strongs
- OpenScriptures BDB: github.com/openscriptures/HebrewLexicon
- unfoldingWord Translation Words: github.com/unfoldingWord/translationWords

**Technical Standards:**
- [STANDARDIZATION.md](../../STANDARDIZATION.md) - Project formatting standards
- [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) - Universal validation framework
- [CLAUDE.md](../../CLAUDE.md) - Core principles and practices
- [plan/policy/fair-use.md](../../plan/policy/fair-use.md) - Fair use compliance

---

**Template Version:** 1.0.0
**Last Updated:** 2025-10-30
**Maintained By:** Context-Grounded Bible Project
