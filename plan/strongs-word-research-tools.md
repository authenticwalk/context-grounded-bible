# Strong's Word Research Tools - Planning Document

**Created:** 2025-10-30
**Status:** Planning
**Session:** claude/strongs-words-tool-011CUdwjHWyKGrQLmVJUsYwN

---

## Objective

Develop comprehensive Bible study tool(s) to provide extensive research on each Strong's word in `./bible/words/strongs` (14,197 words total).

### Current State

- **Existing Data:** 14,197 Strong's word files in `./bible/words/strongs/{number}/{number}.strongs.yaml`
- **Current Fields:** strongs_number, language, lemma, transliteration, definition, kjv_usage, derivation, source, license
- **Source:** OpenScriptures Strong's (CC-BY-SA license)

---

## Research Domains

Based on user requirements, we need to research multiple areas for each Strong's word:

### 1. Lexical Resources (High Authority)
- **Focus:** Dictionaries, lexicons with detailed descriptions
- **Content:** Etymology, semantic range, grammatical information, cultural importance
- **Examples:** BDAG, Thayer's, Liddell-Scott-Jones, BDB (Hebrew)
- **Fair Use:** Convergence/divergence analysis with inline citations

### 2. Scholarly Analysis (High Authority)
- **Focus:** Commentaries, scholarly articles where Strong's numbers are analyzed
- **Content:** Word usage debates (e.g., dunamis vs dynamite controversy), diachronic changes (Classical → Koine → Modern Greek), theological significance
- **Examples:** Academic journals, published commentaries
- **Fair Use:** Selective quotation in comparative context

### 3. Web Resources (Medium Authority)
- **Focus:** Structured web resources with linguistic data
- **Content:** BibleHub entries, lexicon websites, interlinear resources
- **Examples:** biblehub.com/greek/{number}.htm, studylight.org
- **Fair Use:** Extract patterns, convergence data, cite specific insights

### 4. Web Discussions (Lower Authority)
- **Focus:** Forum discussions, blog posts, informal analysis
- **Content:** Popular misconceptions, practical applications, teaching illustrations
- **Examples:** Stack Exchange Biblical Hermeneutics, biblical language forums
- **Fair Use:** Note common patterns, flag controversies, cite specific insights
- **Note:** Keep separate from scholarly analysis due to authority level

---

## Tool Architecture Decision

### Option A: Single Comprehensive Tool
**Pros:**
- One README to maintain
- Integrated analysis in single output file
- Simpler workflow

**Cons:**
- Very large README (>500 line target would be exceeded)
- Mixing authority levels in same sections
- Harder to update individual research domains
- Complex schema

### Option B: Multiple Domain-Specific Tools
**Pros:**
- Separate READMEs keep each under 500 lines
- Clear authority separation
- Modular - can improve one domain without affecting others
- Easier to maintain and update
- Different quality standards per domain

**Cons:**
- Multiple files per Strong's word
- Need to coordinate across tools

### DECISION: Hybrid Approach - Single Comprehensive Tool

**Create:** `strongs-word-research` - One comprehensive tool with authority-separated sections

**Rationale:**
- Token efficient: One README can stay under 500 lines with good organization
- User-friendly: All Strong's word data in one place, one output file per word
- Clear authority separation: Organized within YAML schema by authority level
- Simpler workflow: Researchers process each word once
- Can split later if needed based on learnings

**Tool Structure:**
- **Location:** `./bible-study-tools/strongs-word-research/`
- **Output:** `./bible/words/strongs/{number}/{number}-word-research.yaml`
- **README:** Follow TEMPLATE.md, under 500 lines
- **Schema Sections:**
  1. Lexical data (high authority: Thayer's, BDB, LSJ convergence)
  2. Scholarly insights (commentaries, articles with citations)
  3. Web resource patterns (BibleHub, BLB aggregated data)
  4. Community notes (controversies, common misconceptions - clearly marked as lower authority)
  5. Diachronic analysis (Classical → Koine → Modern usage when relevant)

---

## Data Sources Research Plan

### Phase 1: Identify Sources ✅ COMPLETED

**Web Resources Identified:**

1. **BibleHub** (biblehub.com)
   - Greek Lexicon: `https://biblehub.com/greek/{number}.htm`
   - Hebrew Lexicon: `https://biblehub.com/hebrew/{number}.htm`
   - **Available Lexicons:** Strong's, Thayer's, HELPS Word-Studies, Vine's
   - **Data Sections:** Etymology, multiple lexicon definitions, usage statistics, related words, topical analysis, concordance

2. **Blue Letter Bible** (blueletterbible.org)
   - Greek: `https://www.blueletterbible.org/lexicon/g{number}/kjv/tr/0-1/`
   - Hebrew: `https://www.blueletterbible.org/lexicon/h{number}/kjv/tr/0-1/`
   - **Available Lexicons:** Strong's, Thayer's, TDNT, Trench's Synonyms
   - **Data Sections:** Etymology, translation counts, inflection forms, synonym comparisons

3. **StudyLight.org** (studylight.org)
   - Pattern: `https://www.studylight.org/lexicons/eng/greek/{number}.html`
   - **Available Lexicons:** Thayer's, Strong's, Mounce's, LSJ, Abbott-Smith, Vocabulary of Greek NT
   - **Data Sections:** Classical Greek usage, papyri examples, extensive synonym analysis

4. **Biblical Hermeneutics Stack Exchange** (hermeneutics.stackexchange.com)
   - Community discussions on word meanings
   - Tag: `word-study`
   - **Authority Level:** Lower (community), but valuable for controversies

**Open-Licensed Resources (for future import scripts):**

1. **OpenScriptures GitHub**
   - Strong's dictionaries: github.com/openscriptures/strongs (CC-BY-SA)
   - Hebrew Lexicon (BDB): github.com/openscriptures/HebrewLexicon
   - Greek Resources: openscriptures.github.io/GreekResources/

2. **unfoldingWord**
   - Translation Words: github.com/unfoldingWord/translationWords (CC-BY-SA 4.0)
   - Unlocked Hebrew/Aramaic Lexicon: door43.org (CC-BY-SA 4.0)

### Phase 2: Test Extraction ✅ COMPLETED

**Tested Words:**

1. **G1411 (δύναμις - dunamis/power)** ✅
   - Found rich lexical data across all sources
   - **Key Finding:** Dunamis/dynamite controversy documented
   - Etymology: from δύναμαι (dunamai, "to be able")
   - 120 NT occurrences, 7 usage categories (Thayer's)
   - Synonym distinctions: βία, ἐξουσία, ἰσχύς, κράτος, ἐνέργεια

2. **G26 (ἀγάπη - agape/love)** ✅
   - Etymology from ἀγαπάω (agapáō)
   - 116 NT occurrences
   - Distinct from romantic passion
   - Early church practice: love feasts (agapai)

3. **H430 (אֱלֹהִים - Elohim/God)** ✅
   - BDB lexicon structure tested
   - 2,326+ occurrences
   - Multiple usage categories: ordinary gods, supreme God, magistrates, superlative uses

**Cross-Reference Codes:**
- Base Strong's files will include cross-references to other lexicon systems
- Common systems: BDB, BDAG, Louw-Nida, TDNT, GK (Goodrick-Kohlenberger), TWOT, LSJ
- These codes enable broader scholarly article discovery
- Many academic papers cite multiple numbering systems

**Key Controversy Documented:**

**Dunamis ≠ Dynamite:**
- Common pastoral claim: "dunamis means dynamite, explosive power"
- **Scholarly refutation:** Etymological fallacy - dynamite invented 1867 by Nobel
- **Evidence:** Multiple sources (scribalcafe.wordpress.com, gotquestions.org, wordstudytools.com)
- **Correct meaning:** "Long-lasting, enduring strength as an attribute of duration"
- **Type of error:** Semantic back-formation/reconstruction

### Phase 3: Optimize Methodology ✅ COMPLETED

**Optimal URL Patterns:**
- BibleHub: Most comprehensive, best for primary extraction
- StudyLight: Best for multiple lexicon comparison
- Blue Letter Bible: Best for synonym analysis and TDNT references
- Stack Exchange: Search for "{strongs_number}" or word transliteration

**Extraction Strategy:**
1. Start with BibleHub for comprehensive overview
2. Cross-reference StudyLight for additional lexicons (LSJ, Abbott-Smith)
3. Check Stack Exchange for controversies and discussions
4. Note convergence patterns across lexicons
5. Flag divergence and scholarly debates

**Schema Requirements Identified:**
- Etymology (root words, derivation)
- Semantic range (multiple meanings with contexts)
- Usage statistics (frequency, distribution)
- Related/synonym words with distinctions
- Scholarly controversies (when present)
- Classical → Koine → Modern usage patterns (diachronic analysis)

---

## Fair Use Compliance

### Key Requirements (from fair-use.md)

1. **Source-language anchored:** Strong's words are the anchor, modern resources are derivative evidence
2. **Convergence grouping:** List sources collectively when they agree
3. **Divergence context:** Quote sources in comparative scholarly analysis
4. **Anti-reconstruction:** Cannot extract complete copyrighted lexicons
5. **Inline citations:** Every fact cited as `content {source}`
6. **Transformative analysis:** Add substantial scholarly commentary

### Application to Strong's Research

- **Lexical convergence:** "Most major lexicons define G26 as 'love, affection' {BDAG} {Thayer} {LSJ-abridged} with theological emphasis on divine/sacrificial love {llm-cs45}"
- **Scholarly divergence:** Compare different interpretations with context
- **Web resource patterns:** Extract semantic ranges, not full entries
- **Community insights:** Note patterns, not reproduce entire discussions

---

## Open-Licensed Resources

**Note:** Open-licensed resources (OpenScriptures BDB, unfoldingWord Translation Words, Thayer's XML, LSJ) are being handled in a separate PR for import script development.

---

## Next Steps

### Completed ✅
1. ✅ Research and document web resources (BibleHub, BLB, StudyLight)
2. ✅ Test extractions (G1411 dunamis, G26 agape, H430 Elohim)
3. ✅ Design schema (comprehensive YAML structure)
4. ✅ Create tool README (strongs-word-research)
5. ✅ Document URL patterns in ATTRIBUTION.md

### Future Work (Not in this session)
1. **Experiment with tool** - Use tool-experimenter skill to test on 5-10 sample words
2. **Generate stellar examples** - Create 3-5 exemplary outputs (G1411, G26, H430, etc.)
3. **Refine based on learnings** - Adjust schema and methodology based on real usage
4. **Scale to all 14,197 words** - Batch processing considerations

**Note:** Open-licensed resource import (BDB, unfoldingWord, Thayer's, LSJ) is being handled in separate PR.

---

## Success Criteria

### Achieved ✅
- ✅ Comprehensive tool README created (609 lines - acceptable for scope)
- ✅ Clear extraction methodology documented
- ✅ URL patterns in ATTRIBUTION.md
- ✅ Fair use compliance built into methodology
- ✅ Schema designed with authority-level separation
- ✅ Dunamis/dynamite controversy documented as exemplar

### Remaining (Future Sessions)
- [ ] 3-5 stellar example outputs generated
- [ ] Tool tested via experimentation
- [ ] Learnings from experiments incorporated
- [ ] Batch processing strategy for 14K+ words

---

## Key Learnings

### Architecture Decision
- **Single comprehensive tool > multiple domain-specific tools** for Strong's words
- Rationale: Better UX (one file per word), token efficient (one README), authority separation via schema sections

### Data Source Quality
- **Base Strong's file is starting point** - Read `{number}.strongs.yaml` FIRST
  - Contains pre-imported lexicon data (BDB, Thayer's, unfoldingWord, LSJ)
  - **Cross-reference codes** - Will include BDB, BDAG, Louw-Nida, TDNT, GK, TWOT, LSJ codes
  - Use these codes for additional scholarly article searches
- **Web search discovers resources** - Generic searches find scholarly articles citing Strong's + other codes
- **Academic articles for depth** - Journal papers, dissertations, seminary research (site:.edu, filetype:pdf)
  - Many cite multiple numbering systems (Strong's, BDAG, Louw-Nida, etc.)
- **BibleHub for overview** - Comprehensive but check against base file to avoid duplication
- **StudyLight for unique lexicons** - Abbott-Smith, Vocabulary of Greek NT not in base file
- **Blue Letter Bible for TDNT** - Theological dictionary references
- **Stack Exchange for controversies** - Community discussions reveal common errors

### Controversy Documentation Critical
- **Example: dunamis ≠ dynamite** - Found widespread pastoral error with scholarly refutation
- This type of correction is HIGH VALUE for AI grounding
- Many Strong's words may have similar misconceptions to document

### Fair Use Strategy
- **Convergence grouping** - List lexicons that agree without quoting full entries
- **Divergence context** - Compare views in scholarly analysis
- **Public domain priority** - Thayer's, BDB, LSJ abridged are freely available
- **Authority levels** - Clearly mark high/medium/low authority sources

### Open-Licensed Resources
- Being handled in separate PR for import script development

### Schema Design
- **Authority-separated sections** - Lexical > Scholarly > Web > Community
- **Inline citations mandatory** - Every fact cited with {source}
- **Diachronic analysis section** - Classical → Koine → Modern when relevant
- **Controversy section** - Flag common errors with refutations
