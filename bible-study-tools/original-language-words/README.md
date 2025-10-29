# Original Language Words

**Version:** 1.0.0
**Status:** experimental
**Created:** 2025-10-28
**Last Updated:** 2025-10-28

---

## Purpose

Creates a comprehensive inventory of all original language words (Hebrew/Aramaic for Old Testament, Greek for New Testament) in each verse, providing lexical and linguistic data to enable accurate exegesis and translation work.

**Target Audience:** Bible translators, pastors, seminary students, biblical scholars

**Primary Use Case:** Quick reference to see every word in the original languages with lexical information, enabling AI systems to ground their understanding of the original biblical text. Unlike semantic cluster tools that group words thematically, this tool provides a complete word-by-word inventory with individual lexical data for each term.

---

## Research Methodology

### Phase 1: Data Extraction

**Required Sources:**

- [ ] BibleHub Interlinear (https://biblehub.com/interlinear/) - Primary source for original text with Strong's numbers
- [ ] Strong's Concordance - Lexical definitions and catalog numbers
- [ ] Blue Letter Bible (https://www.blueletterbible.org/) - Cross-verification and morphological data
- [ ] Perseus Digital Library - Greek morphological parsing
- [ ] Ancient Hebrew Research Center - Hebrew linguistic data
- [ ] Louw-Nida Greek Lexicon - Semantic domains (for Greek)
- [ ] BDB Lexicon - Hebrew lexical data
- [ ] BDAG Lexicon - Greek lexical data

**Extraction Process:**
1. Extract the complete original language text for the verse (Hebrew/Aramaic for OT, Greek for NT)
2. Identify each individual word in the original text with its position in the verse
3. For each word, extract:
   - Original script (Hebrew/Aramaic/Greek characters)
   - Transliteration (using scholarly standards)
   - Strong's number (if available)
   - Basic gloss/meaning
   - Root/lexical form
   - Any additional linguistic data (morphology, semantic domain, etc.)
4. Cross-verify data across multiple sources

**Critical Rule:** Extract data BEFORE generating any analysis. Never work from memory.

### Phase 2: Analysis and Synthesis

**Analysis Framework:**
1. Verify completeness: Is every word in the verse accounted for?
2. Check for proper word boundaries (especially in Hebrew where word boundaries can be complex)
3. Identify any textual variants that affect word choices
4. Note any words with multiple possible meanings in context
5. Verify that linguistic data is consistent across sources

**Synthesis Guidelines:**
- Organize words in a clear, logical structure (order will vary by experiment)
- Provide sufficient lexical context for each word
- Include inline citations for all data
- Focus on accuracy and completeness over interpretation
- Flag any uncertainties or ambiguities

### Phase 3: Citation and Verification

**Citation Requirements:**
- Every fact must have an inline citation: `content {source}`
- Use source codes from `/source-abbreviations.yaml`
- Verify all original language text against authoritative sources
- Mark AI-generated insights with `{llm-cs45}` or appropriate model tag

**Verification Checklist:**
- [ ] All words in verse accounted for (100% coverage)
- [ ] No fabricated lexical data
- [ ] Strong's numbers validated (if used)
- [ ] Original language text verified against NA28 (Greek) or BHS (Hebrew)
- [ ] Transliterations follow scholarly standards

---

## Output Schema

### Filename Format

```
{DATA-DIRECTORY}/commentary/{BOOK}/{chapter:03d}/{BOOK}.{chapter:03d}.{verse:03d}-original-language-words.yaml
```

**Components:**
- `{DATA-DIRECTORY}`: defaults to the project root/bible but may be overwritten for experiments
- `{BOOK}`: USFM 3.0 three-letter book code (MAT, JHN, GEN, etc.)
- `{chapter:03d}`: Zero-padded chapter number (001, 005, 038)
- `{verse:03d}`: Zero-padded verse number (001, 016, etc.)

**Examples:**
- `JHN-001-001-original-language-words.yaml` (John 1:1)
- `MAT-005-003-original-language-words.yaml` (Matthew 5:3)
- `GEN-001-001-original-language-words.yaml` (Genesis 1:1)

### YAML Structure

```yaml
# === METADATA ===
verse:
  reference: "{BOOK} {chapter}:{verse}"
  book: "{BOOK}"
  chapter: {chapter}
  verse: {verse}

tool:
  name: "original-language-words"
  version: "{version}"
  generated_date: "YYYY-MM-DD"

# === SOURCE TEXT ===
source_text:
  language: "{ISO-639-3}"  # grc for Greek, heb for Hebrew, arc for Aramaic
  text: "[Original language text]" {source}
  transliteration: "[Transliteration]" {source}

# === WORDS ===
# Note: The structure of this section will vary by experimental approach
# This is a placeholder that will be refined through experiments

words:
  - position: 1
    original: "[Original script]" {source}
    transliteration: "[Transliteration]" {source}
    strongs: "[Strong's number]" {source}
    lexical_form: "[Root/dictionary form]" {source}
    gloss: "[Basic meaning]" {source}
    # Additional fields will be defined per experiment

# === ANALYSIS (if applicable) ===
notes:
  - note: "[Any noteworthy observations about the words in this verse]" {llm-cs45}

# === CROSS-REFERENCES (if applicable) ===
cross_references:
  - ref: "{BOOK}.{chapter:03d}.{verse:03d}"
    connection: "[How this verse relates]" {llm-cs45}
```

### Schema Guidelines

**Tool-Specific Fields:**
- Must capture every word in the original language verse (100% coverage)
- Position field indicates word order in the original text
- All original language text must use proper Unicode characters
- Transliterations must follow scholarly standards (SBL for Greek, academic standards for Hebrew)
- Strong's numbers when available (format: H#### for Hebrew, G#### for Greek)

**Citation Format:**
- Inline: `"content {source}"`
- Multiple sources: `sources: [source1, source2, source3]`
- Never use separate `source:` fields

---

## Output Validation

### Level 1: CRITICAL Requirements (Must Pass 100%)

All outputs must pass universal validation from [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) Level 1:

- ✅ No fabricated data
- ✅ Inline citations present
- ✅ No number predictions
- ✅ Data file grounding
- ✅ Follows core principles from CLAUDE.md

**Action if Failed:** REJECT - Regenerate with strict adherence

### Level 2: HIGH PRIORITY Requirements (80%+ to Pass)

#### Structural Requirements
**100% Word Coverage Required**
- Every word in the original language verse must be accounted for
- No words skipped or missing
- Proper word boundaries maintained
- Edge cases: Very short verses (e.g., "Jesus wept") should have 2 words, not be oversimplified
- Edge cases: Very long verses should have all words, regardless of length

#### Content Scope
**Lexical Completeness**
- Original script present for all words (Hebrew/Greek characters)
- Transliteration present for all words
- Strong's numbers present when available (or note if not available)
- Basic gloss/meaning for each word
- Root/lexical form for each word

#### Quality Thresholds
**Accuracy and Consistency**
- Would a translator trust this as a reliable word inventory?
- Would a pastor use this for word study preparation?
- Would a scholar verify this against original texts?
- Are Strong's numbers correctly matched to words?
- Is original language text properly encoded (Unicode)?

#### Target Audience Fit
**Practical Usability**
- Clear organization of word data
- Easy to look up specific words
- Sufficient detail for translation work
- Not overwhelming with unnecessary technical detail
- Actionable for exegesis

### Level 3: MEDIUM PRIORITY Requirements (60%+ to Pass)

These are quality enhancements from [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) Level 3:

- ✅ Morphological data where available (parsing, case, tense, etc.)
- ✅ Semantic domains where applicable
- ✅ Notes on textual variants affecting word choices
- ✅ Cross-references to related word studies

---

## Quality Metrics

### Optimal Ranges

**Quantitative Metrics:**
- Word count: Must match actual word count in original verse
  - Short verses: 2-5 words (e.g., John 11:35 "Jesus wept" = 2 Greek words)
  - Standard verses: 10-25 words
  - Long verses: 26-50+ words (some verses have 50+ words in original)
- Completeness: 100% of words accounted for (no exceptions)
- Data fields per word: Minimum 5 (original, transliteration, strongs, lexical_form, gloss)

**Qualitative Metrics:**
- Accuracy: Strong's numbers correctly matched
- Consistency: Data consistent across verification sources
- Usability: Clear organization enables quick lookup

### Effective Patterns

**What Works Well:**
- Clear word-by-word structure
- Consistent data fields for each word
- Proper Unicode encoding for original scripts
- Cross-verification across multiple sources
- Notes flagging ambiguities or variants

### Anti-Patterns

**What to Avoid:**
- Incomplete word lists (missing words)
- Fabricated Strong's numbers
- Incorrect transliterations
- Working from memory instead of data extraction
- Oversimplified glosses that lose meaning
- Too much interpretation (this tool is for inventory, not interpretation)

---

## Relevant Review Personas

Select personas from [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) that apply to your tool:

### Required Personas

**👤 Greek/Hebrew Lexicographer**
- **Why Required:** Essential for verifying accuracy of lexical data, Strong's numbers, and original language text
- **Focus Areas:** Strong's accuracy, transliteration standards, lexical form correctness, textual variants

**👤 Senior Bible Translation Consultant**
- **Why Required:** Ensures the tool provides practical value for translators
- **Focus Areas:** Completeness, usability, accuracy, practical application

### Recommended Personas

**👤 Pastor/Teacher**
- **When Valuable:** For assessing usability in sermon preparation and teaching contexts
- **Focus Areas:** Clarity of presentation, accessibility of data, practical insights

### Optional Personas

**👤 Ancient Near East Scholar** (for OT passages)
- **When Valuable:** When Hebrew linguistic or cultural context needs verification
- **Focus Areas:** Hebrew word boundaries, semantic nuances, cultural context

---

## Examples of Stellar Outputs

### Example 1: [To be added after experiments]

**What Made This Excellent:**

[Will be populated after experiments with actual examples]

**Key Elements:**
- [Element 1]
- [Element 2]
- [Element 3]

**File Location:** `path/to/example/file.yaml`

---

### Example 2: [To be added after experiments]

**What Made This Excellent:**

[Will be populated after experiments]

**Key Elements:**
- [Element 1]
- [Element 2]

**File Location:** `path/to/example/file.yaml`

---

## Common Challenges and Solutions

### Challenge 1: Word Boundary Ambiguities in Hebrew

**Problem:** Hebrew words can include prefixes and suffixes that might be separate words or part of the word

**Solution:** Use authoritative sources (BibleHub, Blue Letter Bible) that show standard word divisions. When ambiguous, note in the data.

**Prevention:** Always cross-verify word boundaries across multiple sources

---

### Challenge 2: Multiple Strong's Numbers for Same Word

**Problem:** Some words have variant Strong's numbers or multiple entries

**Solution:** Use the most commonly accepted Strong's number and note variants if significant

**Prevention:** Verify against multiple concordances

---

### Challenge 3: Textual Variants Affecting Word Choice

**Problem:** Different manuscript traditions may have different words

**Solution:** Use the critical text (NA28 for Greek, BHS for Hebrew) as primary source and note significant variants

**Prevention:** Check critical apparatus for variants affecting word inventory

---

## How to Use This Tool's Outputs

### For Bible Translators

Use this tool to get a complete inventory of original language words before beginning translation work. Each word's lexical data provides a foundation for making informed translation choices.

**Workflow:**
1. Look up the verse to see all original language words
2. Review lexical data for each word (Strong's, gloss, root form)
3. Use this as a foundation for more detailed word studies
4. Cross-reference with semantic cluster tools for thematic groupings

---

### For Pastors and Teachers

Use this tool in sermon preparation to understand the original language behind English translations. Quick reference to see what words the biblical authors actually used.

**Workflow:**
1. Look up your sermon text
2. Identify key words in the original language
3. Use Strong's numbers to do deeper word studies
4. Compare English translations to original word meanings

---

### For Seminary Students

Use this tool as a starting point for exegetical work, providing a complete word inventory with lexical data.

**Workflow:**
1. Begin exegesis by reviewing all original words
2. Identify words requiring deeper study
3. Use lexical data as a foundation for detailed analysis
4. Verify your own translations against the word inventory

---

## Research Guidelines for Bible-Researcher Agent

### Pre-Generation Checklist

Before generating any output, ensure:

- [ ] Tool README fully read and understood
- [ ] Verse reference standardized to USFM 3.0 format
- [ ] Testament identified (OT = Hebrew/Aramaic, NT = Greek)
- [ ] Data sources accessible (BibleHub, Strong's, etc.)
- [ ] Schema structure internalized

### During Generation

- [ ] Extract complete original language text FIRST
- [ ] Identify every word in the verse (100% coverage)
- [ ] Look up lexical data for each word individually
- [ ] Cite every piece of data with inline `{source}` tags
- [ ] Cross-verify Strong's numbers and transliterations
- [ ] Never work from memory - always extract from sources

### Post-Generation Quality Control

Review from these perspectives:

**Completeness:**
- [ ] Every word in the verse is accounted for
- [ ] No words skipped or missing
- [ ] Word count matches actual original text

**Accuracy:**
- [ ] Strong's numbers correctly matched
- [ ] Original script properly encoded (Unicode)
- [ ] Transliterations follow standards
- [ ] Lexical forms are correct dictionary entries

**Citation Quality:**
- [ ] Every field has inline citation
- [ ] Sources are authoritative (BibleHub, Strong's, etc.)
- [ ] No fabricated data
- [ ] LLM insights marked with {llm-cs45}

**Usability:**
- [ ] Clear organization
- [ ] Easy to look up specific words
- [ ] Sufficient detail without overwhelming
- [ ] Practical for target audience

---

## Version History

### Version 1.0.0 (2025-10-28)
- Initial creation
- Base structure defined
- Awaiting experimental results to refine approach

---

## Related Tools

- **semantic-clusters**: Groups words thematically rather than listing individually
- **test-word-meanings**: Analyzes meanings of key words in context (this tool provides the word inventory for that analysis)

---

## References

**Biblical Text Resources:**
- BibleHub Interlinear: https://biblehub.com/interlinear/
- Blue Letter Bible: https://www.blueletterbible.org/
- Perseus Digital Library: http://www.perseus.tufts.edu/

**Lexical Resources:**
- Strong's Concordance: Standard lexical catalog
- BDB (Brown-Driver-Briggs): Hebrew lexicon
- BDAG: Greek lexicon
- Louw-Nida: Greek semantic domains

**Technical Standards:**
- [STANDARDIZATION.md](../../STANDARDIZATION.md) - Project formatting standards
- [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) - Universal validation framework
- [CLAUDE.md](../../CLAUDE.md) - Core principles and practices

---

**Template Version:** 1.0.0
**Last Updated:** 2025-10-28
**Maintained By:** Context-Grounded Bible Project
