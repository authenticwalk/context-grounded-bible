# [Tool Name]

**Version:** 1.0.0  
**Status:** [experimental/active/deprecated]  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## Purpose

[2-3 sentences describing what this tool does and why it exists]

**Target Audience:** [Who will use this? E.g., Bible translators, pastors, seminary students, etc.]

**Primary Use Case:** [What specific problem does this solve? E.g., understanding semantic ranges, identifying translation challenges, etc.  Keep this in light of the project goals in the base project README.md by considering if you could get the same results by asking a state of the art model the question without the context (would you get the same depth or accuracy consistently)]

---

## Research Methodology

### Phase 1: Data Extraction

**Required Sources:**

[Sources may be websites or tools and skills we have.  Be sure to look at all the skills we have like
quote-bible and see if that will help.]

- [ ] Source 1 (e.g., BibleHub for translation comparisons)
- [ ] Source 2 (e.g., Strong's Concordance for lexical data)
- [ ] Source 3 (e.g., BDAG for Greek semantic ranges)
- [ ] ... (up to 12 sources)

**Extraction Process:**
1. [Step 1 - What to extract and from where]
2. [Step 2 - How to organize the extracted data]
3. [Step 3 - What to verify or cross-check]

**Critical Rule:** Extract data BEFORE generating any analysis. Never work from memory.

### Phase 2: Analysis and Synthesis


**Analysis Framework:**
1. [What questions to ask of the data]
2. [What patterns to look for]
3. [What connections to identify]

**Synthesis Guidelines:**
[ Choose which of these or similar to include ]
- Focus on insights that provide practical value for the target audience
- Identify convergence and divergence patterns across sources
- Highlight cultural adaptation strategies where applicable
- Note theological significance when relevant

### Phase 3: Citation and Verification

[Carefully look at REVIEW-GUIDELINES.md to pull our criteria that match this task, the following are
examples but you can expand this and it must be made relevant to the task, eg. not all tasks need Strongs or quote verses]

**Citation Requirements:**
- Every fact must have an inline citation: `content {source}`
- Use source codes from `/source-abbreviations.yaml`
- Verify all translations exist in extracted data files
- Mark AI-generated insights with `{llm-cs45}` or appropriate model tag

**Attribution Requirements:**
- [ ] All new sources added to [ATTRIBUTION.md](../../ATTRIBUTION.md) with complete copyright notices
- [ ] Citation format codes match ATTRIBUTION.md entries
- [ ] Public domain/open license/fair use designation specified
- [ ] Purchase or access links included for copyrighted works
- [ ] Update `source-abbreviations.yaml` if new citation codes needed

**Verification Checklist:**
- [ ] All translations verified against data files
- [ ] No fabricated examples
- [ ] Cross-references checked for accuracy
- [ ] Strong's numbers validated (if applicable)
- [ ] All sources exist in ATTRIBUTION.md

---

## Output Schema

### Filename Format

[ Check STANDARDIZATION.md for the latest schema for verses, topics, words, etc and copy this and examples from there in the minimalist way possible]
```
{DATA-DIRECTORY}/commentary/{BOOK}/{chapter:03d}/{BOOK}-{chapter:03d}-{verse:03d}-{tool-name}(?-{prefix-if-any}).yaml
```


**Components:**
- `{DATA-DIRECTORY}`: defaults to the project root/bible but may be overwritten for experiments
- `{BOOK}`: USFM 3.0 three-letter book code (MAT, JHN, GEN, etc.)
- `{chapter:03d}`: Zero-padded chapter number (001, 005, 038)
- `{verse:03d}`: Zero-padded verse number (001, 016, etc.)
- `{tool-name}`: The name of this tool, same as the directory name for the tool
- `{prefix-if-any}`: default: none but may be set for experiments, ex. `check-strongs-rev3`

**Examples:**
- `JHN-001-001.yaml` (John 1:1)
- `MAT-005-003.yaml` (Matthew 5:3)
- `GEN-001-001.yaml` (Genesis 1:1)

### YAML Structure
[ Carefully read SCHEMA.md for how to structure this schema so we have consistent naming and structure allowing us to merge filterable documents together.  The fields are semi-structured where common fields are named the same ]

```yaml
# === METADATA ===
verse:
  reference: "{BOOK} {chapter}:{verse}"
  book: "{BOOK}"
  chapter: {chapter}
  verse: {verse}

tool:
  name: "{tool-name}"
  version: "{version}"
  generated_date: "YYYY-MM-DD"

# === [TOOL-SPECIFIC SECTION 1] ===
# Define your tool's primary data structure here
# Example for semantic clusters:
clusters:
  - id: "cluster-1"
    greek_text: "..." {grc-NA28}  # Notice how we always cite the source after every copied string
    english_gloss: "..."
    semantic_range: "..."
    
# === [TOOL-SPECIFIC SECTION 2] ===
# Define your tool's secondary data structures
# Example for translation patterns:
translation_patterns:
  convergence:
    - pattern: "..."
      languages: [...]
      sources: [...]
  divergence:
    - issue: "..."
      approaches: [...]

# === ANALYSIS ===
key_insights:
  - insight: "[Specific insight discovered]" {llm-cs45}
    rationale: "[Why this matters]" {llm-cs45}
    
  - insight: "[Another insight]" {llm-cs45}
    rationale: "[Significance]" {llm-cs45}

# === CROSS-REFERENCES (if applicable) ===
cross_references:
  - ref: "{BOOK}.{chapter:03d}.{verse:03d}"
    connection: "[How this verse relates]" {llm-cs45}

# Which data did you **use** so future researchers can reproduce it
sources:
  websites:
    # - url: "https://example.com"

  skills:
    # - name: "linguistics"
    #   prompt: "In review, what specific criteria should be checked for this skill domain?"

  mcp:
    # - id: "MCP-001"
    #   prompt: "What is the core question or output a reviewer must confirm is present for this MCP?"

metadata:
  date_time: 2025-11-29 18:32:05
  tokens_used: 10000
  errors_fixed: 0   # How many errors did the review committee or your validation find and then you had to fix
```

### Schema Guidelines

**Tool-Specific Fields:**
- Define your unique data structures clearly
- Use nested structures for complex relationships
- Provide inline citations for all content
- Use arrays for multiple items of the same type

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
- ✅ Copyright and fair use compliance
- ✅ New sources added to ATTRIBUTION.md

**Action if Failed:** REJECT - Regenerate with strict adherence

### Level 2: HIGH PRIORITY Requirements (80%+ to Pass)

**[Define your tool-specific requirements here]:**

#### Structural Requirements
[What structure/format is expected?]

**Examples:**
- "3-5 semantic clusters per verse"
- "5-10 relevant passages for topical research"
- "All major meanings documented for word studies"

#### Content Scope
[What content should/shouldn't be included?]

**Examples:**
- "100% word coverage required - every Greek/Hebrew word must appear in at least one cluster"
- "Both OT and NT passages when applicable"
- "Diachronic development: Classical → Koine → Modern usage"

#### Quality Thresholds
[What minimum standards define acceptance?]

**Examples:**
- "Would a translator copy this to their notes?"
- "Would a pastor use this in sermon preparation?"
- "Would a scholar trust this analysis?"

#### Target Audience Fit
[Does it serve the intended audience effectively?]

**Evaluation Questions:**
- Does it solve the problem stated in the Purpose section?
- Is the level of detail appropriate?
- Are practical applications clear?

### Level 3: MEDIUM PRIORITY Requirements (60%+ to Pass)

These are quality enhancements from [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) Level 3:

- ✅ Cross-references where relevant
- ✅ Grammatical insights where meaningful
- ✅ Practical guidance documented
- ✅ Cultural and historical context

---

## Quality Metrics

### Optimal Ranges

[Define measurable quality indicators for your tool.  Keep in mind that some verses are short like Jesus wept and some really long so allow for those edge cases using percentages like ALL words or edge case exception instructions]:

**Quantitative Metrics:**
- [Metric 1]: [range or target value]
  - Example: "Cluster count: 3-4 for standard verses"
- [Metric 2]: [range or target value]
  - Example: "Token range: 2000-2500 per verse"
- [Metric 3]: [range or target value]
  - Example: "Translation coverage: 10+ languages from diverse families"

**Qualitative Metrics:**
- [Quality indicator 1]
  - Example: "Multiple theological traditions represented (2-3 when relevant)"
- [Quality indicator 2]
  - Example: "Specific language families named (not 'some cultures')"

### Effective Patterns

[What patterns have been proven to work well?]

**Examples:**
- Convergence/divergence framework
- Language family specificity
- Grammar-theology connections
- Critical warnings prominently placed

### Anti-Patterns

[What should be avoided?]

**Examples:**
- Single-word clusters without divergence
- Generic cultural references ("some cultures...")
- Academic verbosity without practical value
- Too sparse (<1500 tokens) or too verbose (>3000 tokens)

---

## Relevant Review Personas

Select personas from [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) that apply to your tool:

### Required Personas

**👤 [Persona 1 Name]** (e.g., Greek/Hebrew Lexicographer)
- **Why Required:** [Specific reason this persona is essential]
- **Focus Areas:** [What they should evaluate]

**👤 [Persona 2 Name]** (e.g., Translation Consultant)
- **Why Required:** [Reason]
- **Focus Areas:** [What to check]

### Recommended Personas

**👤 [Persona 3 Name]** (e.g., Minority Language Translator)
- **When Valuable:** [Situations where this perspective adds value]
- **Focus Areas:** [What they should look for]

### Optional Personas

**👤 [Persona 4 Name]** (e.g., Pastor/Teacher)
- **When Valuable:** [Specific scenarios]
- **Focus Areas:** [Review focus]

---

## Examples of Stellar Outputs

### Example 1: [Verse Reference]

**What Made This Excellent:**

[3-5 lines describing what insight was discovered, what made it valuable, and why it exemplifies tool excellence]

**Key Elements:**
- [Specific element that worked well]
- [Another effective element]
- [What made it actionable/valuable]
- [How to reproduce the results]

**File Location:** `path/to/example/file.yaml`

---

### Example 2: [Verse Reference]

**What Made This Excellent:**

[3-5 lines...]

**Key Elements:**
- [Element 1]
- [Element 2]
- [Element 3]

**File Location:** `path/to/example/file.yaml`

---

### Example 3: [Verse Reference]

[Continue pattern for 3-7 stellar examples]

---

## Common Challenges and Solutions

### Challenge 1: [Common Issue]

**Problem:** [Describe the challenge]

**Solution:** [How to address it]

**Prevention:** [How to avoid it]

---

### Challenge 2: [Another Issue]

**Problem:** [Description]

**Solution:** [Resolution approach]

**Prevention:** [Avoidance strategy]

---

## How to Use This Tool's Outputs

### For Bible Translators

[Specific guidance on how translators can leverage these outputs]

**Workflow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

### For Pastors and Teachers

[How pastoral staff can use these outputs in sermon prep or teaching]

**Workflow:**
1. [Step 1]
2. [Step 2]

---

### For Seminary Students

[How students can use outputs for exegetical studies]

**Workflow:**
1. [Step 1]
2. [Step 2]

---

## Research Guidelines for Bible-Researcher Agent

### Pre-Generation Checklist

Before generating any output, ensure:

- [ ] Tool README fully read and understood
- [ ] Verse reference standardized to USFM 3.0 format
- [ ] All required data sources identified
- [ ] Data extraction strategy planned
- [ ] Schema structure internalized

### During Generation

- [ ] Extract data FIRST, analyze SECOND
- [ ] Cite every fact with inline `{source}` tags
- [ ] Add new sources to ATTRIBUTION.md immediately
- [ ] Stay within defined schema structure
- [ ] Focus on target audience needs
- [ ] Avoid fabrication - only use extracted data

### Post-Generation Quality Control

Review from these perspectives:

**Scholarly Accuracy:**
- [ ] Does it reflect current biblical scholarship?
- [ ] Are all claims properly sourced?

**Translation Sensitivity:**
- [ ] Does it account for translation nuances?
- [ ] Are cross-cultural patterns identified?

**Contextual Completeness:**
- [ ] Is sufficient context provided for AI grounding?
- [ ] Would the target audience find this complete?

**Source Reliability:**
- [ ] Are citations from authoritative sources?
- [ ] Can every claim be traced?
- [ ] Are all sources documented in ATTRIBUTION.md?

**Theological Balance:**
- [ ] Are multiple interpretive traditions represented fairly?
- [ ] Is contested theology labeled as such?

**AI Usability:**
- [ ] Will this effectively ground AI responses in truth?
- [ ] Is the YAML structure machine-readable?

---
---

## Version History

### Version 1.0.0 (YYYY-MM-DD)
- Initial creation
- [Key features or decisions]

### Version 1.1.0 (YYYY-MM-DD)
- [Changes made]
- [Learnings incorporated]

---

## Related Tools

- [Related Tool 1]: [How it relates/complements this tool]
- [Related Tool 2]: [Relationship description]

---

## References

**Biblical Text Resources:**
- [Specific resources used]

**Lexical Resources:**
- [Lexicons and concordances]

**Theological Resources:**
- [Commentaries and references]

**Technical Standards:**
- [STANDARDIZATION.md](../../STANDARDIZATION.md) - Project formatting standards
- [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) - Universal validation framework
- [CLAUDE.md](../../CLAUDE.md) - Core principles and practices

---

**Template Version:** 1.0.0  
**Last Updated:** 2025-10-28  
**Maintained By:** Context-Grounded Bible Project

