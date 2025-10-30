# TBTA Amplification Tool - Project Request

## Context

In PR #17 (`claude/analyze-tbta-db-export-011CUdx3npbcZbrxN3g6FCMh`), we successfully integrated the TBTA (The Bible Translator's Assistant) database into the Context-Grounded Bible project. TBTA provides cross-linguistic commentary for 11,649 verses across 34 books, encoding grammatical features that differ across the world's languages.

**What was accomplished:**
- Processed all 11,649 TBTA verses into YAML format
- Analyzed TBTA's unique linguistic features (Trial number, inclusive/exclusive pronouns, proximity markers, etc.)
- Stored all data in `./bible/commentaries/{BOOK}/{chapter}/{verse}/{BOOK}-{chapter}-{verse}-tbta.yaml`

**What remains:** Creating a tool that amplifies TBTA's work by:
1. Reproducing all TBTA fields with proper documentation
2. Extending to translation edge cases TBTA didn't explicitly consider
3. Mapping TBTA features to specific languages that need them
4. Leveraging the eBible corpus (1000+ translations) to identify real-world usage patterns

## Comprehensive Research Completed

**NEW:** Extensive linguistic research has been completed and documented in `/plan/tbta-languages/`:

1. **`comprehensive-language-research.md`** (28KB, ~800 lines)
   - Detailed language examples for EVERY TBTA feature
   - Trial number: 7 languages documented (Larike, Marshallese, etc.)
   - Dual number: 6 languages (Slovene, Arabic, Hebrew, Fijian, etc.)
   - Inclusive/Exclusive: 7+ languages with specific examples
   - Demonstratives: 15+ languages with 3-way systems
   - Honorifics: 8 languages with grammatical systems
   - Switch-reference: Comprehensive coverage
   - **PLUS:** Features TBTA doesn't have (evidentiality, classifiers, possession types)

2. **`blind-discovery-test.md`** (794 lines)
   - Independent discovery using ONLY eBible corpus + web research
   - Discovered 10 major feature categories without seeing TBTA
   - Validates that features can be reverse-engineered
   - Provides replication methodology

3. **`blind-test-comparison.md`**
   - Compares blind discovery with actual TBTA data
   - Score: 8.2/10 match rate
   - Identifies what TBTA has, what's missing, what should be added
   - Validates discovery process works

**Key Findings:**
- ✅ Core TBTA features can be discovered through eBible analysis
- ✅ Blind discovery found: clusivity, dual, trial, entity tracking, demonstratives, speaker demographics
- ✅ TBTA has MORE detail: 20+ time categories, 9 participant states, exhaustive pragmatic markup
- ✅ Valid additions identified: evidentiality, classifiers, possession types

**Ready for Implementation:** All research needed to build the tool is complete.

## The Opportunity

We have TWO complementary data sources:

### 1. TBTA Cross-Linguistic Features (11,649 verses)
**Location:** `./bible/commentaries/{BOOK}/{chapter}/{verse}/{BOOK}-{chapter}-{verse}-tbta.yaml`

**Example:** Genesis 1:26 (Trinity as Trial Number)
```yaml
verse: GEN.001.026
clauses:
  - children:
    - Constituent: God
      Number: Trial              # Exactly 3 persons!
      Person: First Inclusive    # "we" includes the Trinity members
      Participant Tracking: Routine
```

### 2. eBible Translation Corpus (1000+ languages)
**Location:** `./bible/commentary/{BOOK}/{chapter}/{BOOK}_{chapter}_{verse}.translations-ebible.yaml`

**Example:** Genesis 1:1 with 1000+ translations
```yaml
verse: GEN.001.001
translations:
  mal-C: ആദിയിൽ ദൈവം ആകാശവും ഭൂമിയും സൃഷ്ടിച്ചു.
  deu-TKW: Im Anfang schuf Gott den Himmel und die Erde.
  swh-ONEN: Hapo mwanzo Mungu aliumba mbingu na dunia.
  tgl-ULB: Noong simula nilikha ng Diyos ang langit at ang lupa.
  ... [1000+ more languages]
```

**The Connection:** By analyzing the eBible translations alongside TBTA features, we can identify which languages use which grammatical patterns, creating a comprehensive cross-linguistic guide for translators.

## Key Files to Reference

### Analysis & Documentation
1. **`/plan/tbta-analysis.md`** (374 lines)
   - Complete TBTA field analysis
   - Concrete translation edge cases
   - Language examples (Kilivila, Tagalog, Japanese, etc.)
   - Real-world impact scenarios

2. **`/plan/tbta-processing-summary.md`** (125 lines)
   - Processing statistics
   - Book coverage (34 books, 11,649 verses)
   - Data quality notes

### Code & Implementation
3. **`/src/lib/tbta/tbta_processor.py`** (344 lines)
   - TBTA JSON to YAML processor
   - Book name mappings
   - Nullish value filtering logic
   - Field extraction and structuring

4. **`/src/lib/tbta/README.md`**
   - TBTA processor documentation
   - Usage examples

### Data Samples
5. **`/bible/commentaries/GEN/001/026/GEN-001-026-tbta.yaml`** (632 lines)
   - Genesis 1:26 with Trial number and First Inclusive person
   - Shows complete TBTA field structure
   - Multiple clause variants

6. **`/bible/commentaries/GEN/019/031/GEN-019-031-tbta.yaml`** (486 lines)
   - Genesis 19:31 with Speaker Demographics
   - Shows age, relationship, and attitude markers
   - Example of pragmatic information encoding

7. **`/bible/commentary/GEN/1/GEN_1_001.translations-ebible.yaml`**
   - Genesis 1:1 with 1000+ translations
   - Shows eBible corpus structure
   - Language code format (ISO-639-3)

## TBTA Fields That Need Language Mapping

From analysis of 11,649 verses, TBTA encodes these cross-linguistic features:

### 1. Number System (Beyond Singular/Plural)
**TBTA Values:** `Singular`, `Dual` (2), `Trial` (3), `Quadrial` (4), `Paucal` (few), `Plural`

**Research Needed:**
- Which languages have dual number? (Slovene, Arabic, Hebrew, etc.)
- Which languages have trial number? (Kilivila, Larike, some Austronesian)
- Which languages have quadrial number? (Sursurunga, Marshallese)
- Which languages have paucal number? (Many indigenous Australian languages)

**eBible Task:** Examine translations in languages known to have these features and identify patterns

**Example:** GEN 1:26 marks God as "Trial" (3 persons = Trinity)
- Check how Kilivila (kil) translates this
- Check Larike, Marshallese translations
- Document trial number usage patterns

### 2. Person System (Inclusive/Exclusive Distinction)
**TBTA Values:** `First Inclusive`, `First Exclusive`, `First as Third`, `Second as Third`

**Research Needed:**
- Which languages distinguish inclusive/exclusive "we"?
  - Tagalog (tgl): "tayo" (inclusive) vs "kami" (exclusive)
  - Fijian (fij): "keimami" (exclusive) vs "keitou" (inclusive)
  - Malay (zsm/ind): "kita" (inclusive) vs "kami" (exclusive)
  - Guarani, Quechua, many Native American languages
  - Many Southeast Asian languages
  - Many Austronesian languages

**eBible Task:**
- Find all eBible translations in languages with inclusive/exclusive distinction
- Analyze how they handle GEN 1:26 ("Let us create")
- Document translation patterns for First Inclusive vs First Exclusive contexts

**Example:** GEN 1:26 marks "First Inclusive" (Trinity members included)
- Compare Tagalog, Fijian, Malay translations
- Note which form they use
- Extract exceptions and edge cases

### 3. Proximity/Demonstrative Systems (Beyond "this" vs "that")
**TBTA Values:** `Near Speaker`, `Near Listener`, `Near Both`, `Remote Visible`, `Remote Invisible`, `Contextually Near`, `Temporally Near/Remote`

**Research Needed:**
- **2-way systems:** English (this/that), most European languages
- **3-way systems:**
  - Japanese (jpn): これ (kore - near me) / それ (sore - near you) / あれ (are - far)
  - Korean (kor): 이 (i) / 그 (geu) / 저 (jeo)
  - Spanish (spa): este / ese / aquel
  - Turkish (tur): bu / şu / o
- **4-way systems:**
  - Some Native American languages (visible near/far, invisible near/far)
- **5+ way systems:**
  - Malagasy, some Papua New Guinea languages

**eBible Task:**
- Identify all languages with demonstrative distinctions
- Analyze translation patterns for proximity markers
- Document how different systems map to TBTA's proximity codes

### 4. Time Granularity (20+ Temporal Distinctions)
**TBTA Values:** `Immediate Past`, `Earlier Today`, `Yesterday`, `A Week Ago`, `A Month Ago`, `Historic Past`, `Immediate Future`, `Tomorrow`, `A Year from Now`, etc.

**Research Needed:**
- Which languages require specific time-distance marking in verbs?
  - Tagalog (tgl): Different forms for immediate vs remote past
  - Swahili (swh): Multiple past tenses by distance
  - Quechua (que): Evidentiality + time marking
  - Many Bantu languages
  - Many indigenous American languages

**eBible Task:**
- Identify verb form patterns in these languages
- Map TBTA time codes to specific language requirements
- Document temporal marking systems across language families

### 5. Speaker Demographics (Age, Relationship, Politeness)
**TBTA Values:**
- Speaker's Age: `Young Adult (18-24)`, `Adult (25-49)`, `Elder (50+)`
- Speaker-Listener Age: `Same Age`, `Older`, `Younger`, `Different Generation`
- Speaker's Attitude: `Neutral`, `Familiar`, `Honorable/Respectful`

**Research Needed:**
- **Honorific systems (required in grammar):**
  - Japanese (jpn): です/ます forms, honorific vocabulary
  - Korean (kor): 7 politeness levels (하십시오체, 해요체, 반말, etc.)
  - Javanese (jav): 3-5 speech levels (ngoko, madya, krama)
  - Balinese (ban): 3 main levels
  - Thai (tha): Particles and pronouns based on social status
  - Vietnamese (vie): Complex pronoun system based on age/relationship

- **Register distinctions:**
  - Hindi/Urdu (hin/urd): तू/तुम/आप (tu/tum/aap)
  - Indonesian (ind): Formal vs informal vocabulary
  - Many others

**eBible Task:**
- Identify which translations use honorifics/register shifts
- Document speaker demographics from TBTA (GEN 19:31 example)
- Map social context to grammatical requirements

**Example:** GEN 19:31 - Older sister speaking to younger sister
```yaml
Speaker's Age: Young Adult (18-24)
Speaker-Listener Age: Essentially the Same Age
Speaker's Attitude: Familiar
```
- Check Japanese translation: Should use casual form (よ)
- Check Korean translation: Should use 반말 (informal speech)
- Check Javanese: Should use ngoko (low, intimate level)

### 6. Participant Tracking (Entity Flow Through Discourse)
**TBTA Values:** `First Mention`, `Routine`, `Exiting`, `Restaging`, `Frame Inferable`, `Generic`

**Research Needed:**
- **Switch-reference languages** (mark when subject changes):
  - Many Papua New Guinea languages
  - Many Native American languages (Navajo, Quechua, etc.)
  - Some Australian Aboriginal languages

**eBible Task:**
- Identify switch-reference languages in eBible corpus
- Analyze how they handle participant tracking
- Document patterns for subject continuity/change

### 7. Noun List Index (Entity Disambiguation)
**TBTA Values:** Uses `1-9, A-Z, a-z` to track which nouns refer to same entity

**Use Case:** Languages with mandatory entity tracking, pronoun dropping, or complex anaphora resolution

**eBible Task:**
- Identify languages with pronoun-dropping (Japanese, Korean, Spanish, Italian, etc.)
- Analyze how they handle entity tracking
- Document disambiguation strategies

## Proposed Tool: `tbta-linguistic-mapping`

### Purpose
Create a tool that generates comprehensive cross-linguistic guidance by:
1. Taking a verse reference
2. Pulling TBTA linguistic features for that verse
3. Identifying which languages need those features
4. Showing relevant translations from eBible corpus
5. Providing translator guidance for edge-case languages

### Output Structure
```yaml
verse: GEN.001.026
tbta_features:
  number_system:
    value: Trial
    description: "Exactly 3 persons (Trinity)"
    relevant_languages:
      - code: kil
        name: Kilivila
        feature: "Has trial number (singular/dual/trial/plural)"
        translation: "[fetch from eBible if available]"
        guidance: "MUST use trial form, not generic plural"
      - code: lar
        name: Larike
        feature: "Has trial number"
        guidance: "Choose trial form for theological precision"

  person_system:
    value: First Inclusive
    description: "We (including the Trinity members addressed)"
    relevant_languages:
      - code: tgl
        name: Tagalog
        feature: "Distinguishes inclusive (tayo) vs exclusive (kami)"
        translation: "[from eBible]"
        guidance: "Use 'tayo' (inclusive) - Trinity includes all members"
      - code: fij
        name: Fijian
        feature: "Inclusive/exclusive distinction required"
        translation: "[from eBible]"
        guidance: "Use inclusive form (keitou)"

  proximity_markers:
    value: Contextually Near with Focus
    description: "Demonstrative indicating near+focused entity"
    relevant_languages:
      - code: jpn
        name: Japanese
        feature: "3-way demonstrative (kore/sore/are)"
        guidance: "Likely use それ (sore - near listener) or これ (kore - near speaker)"
      - code: kor
        name: Korean
        feature: "3-way demonstrative (i/geu/jeo)"
        guidance: "Choose based on narrative perspective"

translator_notes:
  - "This verse (GEN 1:26) is theologically significant for Trinity doctrine"
  - "Trial number languages can express 3-person precision that English cannot"
  - "Inclusive 'we' clarifies intra-Trinity dialogue"
```

### Implementation Phases

#### Phase 1: Research & Documentation
**Goal:** Build comprehensive language feature database

**Tasks:**
1. **Web research:** For each TBTA feature, identify which world languages have it
   - Use linguistic resources (WALS, Glottolog, academic papers)
   - Create markdown files documenting findings
   - Example: `/plan/tbta-languages/trial-number-languages.md`

2. **eBible corpus analysis:**
   - Count total translations available
   - Map ISO-639-3 codes to language names
   - Identify which linguistic features each language has

3. **Language feature matrix:**
   - Create a database mapping languages to features
   - Format: `language_code → [features]`
   - Example: `tgl → [inclusive_exclusive, time_granularity, demonstrative_3way]`

**Deliverable:**
- `/plan/tbta-languages/` directory with research files
- `/src/lib/tbta/language_features.yaml` - Master feature mapping

#### Phase 2: Tool Implementation
**Goal:** Create the linguistic mapping tool

**Tasks:**
1. **Build language feature database**
   - Load language feature mappings
   - Create lookup functions

2. **TBTA feature extractor**
   - Read TBTA YAML files
   - Extract key linguistic features
   - Identify which features are present in each verse

3. **eBible corpus integration**
   - Load translation files
   - Filter by languages with relevant features
   - Extract translations for comparison

4. **Guidance generator**
   - Match TBTA features to language requirements
   - Generate translator-friendly guidance
   - Produce cross-linguistic comparison output

**Deliverable:**
- `/src/lib/tbta/linguistic_mapper.py` - Main tool
- Usage: `python linguistic_mapper.py --verse "GEN 1:26"`

#### Phase 3: Tool Integration & Testing
**Goal:** Make the tool accessible and useful

**Tasks:**
1. **Create Bible study tool wrapper**
   - Follow existing tool patterns in `/bible-study-tools/`
   - Add to tool registry
   - Write comprehensive README

2. **Test with key verses**
   - Genesis 1:26 (Trial number, First Inclusive)
   - Genesis 19:31 (Speaker demographics)
   - Acts 15:25 (Inclusive vs Exclusive)
   - John 1:29 (Proximity markers)

3. **Document exceptions and edge cases**
   - What TBTA marks that languages don't distinguish
   - What languages distinguish that TBTA doesn't mark
   - Translation strategies for mismatches

**Deliverable:**
- `/bible-study-tools/tbta-linguistic-mapping/` tool directory
- README with examples
- Integration with scripture-study skill

## Research Tasks Breakdown

### Immediate Web Research Needed

For each TBTA feature, research and document:

1. **Trial Number Languages**
   - Search: "languages with trial number grammar"
   - Document: Kilivila, Larike, Marshallese, etc.
   - Note: Austronesian families most common

2. **Inclusive/Exclusive Languages**
   - Search: "clusivity languages", "inclusive exclusive we"
   - Document: ~40% of world's languages have this
   - Major families: Austronesian, many Native American, some Asian

3. **Demonstrative Systems**
   - Search: "demonstrative systems cross-linguistic", "spatial deixis"
   - Document: 2-way, 3-way, 4-way, 5-way systems
   - Map to TBTA proximity codes

4. **Time Granularity Systems**
   - Search: "tense systems languages", "temporal deixis"
   - Document: Languages with obligatory time-distance marking
   - Focus: Bantu languages, Austronesian, some Native American

5. **Honorific/Register Systems**
   - Search: "honorific languages", "politeness grammar"
   - Document: Japanese, Korean, Javanese, Thai, Vietnamese, etc.
   - Note: Required vs optional distinctions

6. **Switch-Reference Languages**
   - Search: "switch reference grammar", "same subject different subject"
   - Document: Papua New Guinea, Native American families
   - Map to TBTA participant tracking

### eBible Corpus Analysis Tasks

1. **Language inventory**
   - Count unique language codes
   - Map to full language names
   - Identify language families

2. **Coverage analysis**
   - Which books have most translations?
   - Which verses have most translations?
   - Which languages have complete vs partial translations?

3. **Feature detection**
   - For known feature languages (e.g., Tagalog), examine translations
   - Identify patterns indicating feature usage
   - Document exceptions and interesting cases

## Success Metrics

1. **Completeness:** All TBTA fields mapped to relevant languages
2. **Accuracy:** Language feature database verified against linguistic literature
3. **Utility:** Tool provides actionable guidance for Bible translators
4. **Coverage:** Identifies edge cases TBTA didn't explicitly consider
5. **Integration:** Works seamlessly with existing scripture-study skill

## Expected Output

By the end of this work, we should have:

1. **Research documentation:**
   - `/plan/tbta-languages/` with 8-10 markdown files documenting language features
   - Language feature database with 100+ languages mapped to TBTA features

2. **Working tool:**
   - `/src/lib/tbta/linguistic_mapper.py` - Core implementation
   - `/bible-study-tools/tbta-linguistic-mapping/` - Tool wrapper
   - README with comprehensive examples

3. **Test cases:**
   - 5-10 key verses fully analyzed
   - Documentation of translation strategies for each TBTA feature
   - Cross-linguistic comparison showing real-world usage

4. **Integration:**
   - Tool callable from scripture-study skill
   - Depth level: "comprehensive" (large dataset)
   - Scope: Cross-linguistic translation guidance

## References

### Linguistic Resources
- **WALS (World Atlas of Language Structures):** https://wals.info/
- **Glottolog:** https://glottolog.org/
- **SIL International Ethnologue:** https://www.ethnologue.com/
- **Wikipedia linguistic articles:** Search "[feature] languages" for each TBTA feature

### Existing Project Files
- Previous PR: #17 (`claude/analyze-tbta-db-export-011CUdx3npbcZbrxN3g6FCMh`)
- TBTA GitHub: https://github.com/AllTheWord/tbta_db_export
- eBible corpus: Already integrated in `./bible/commentary/`

## Starting Point for Next Session

1. **First read these files:**
   - `/plan/tbta-analysis.md` - Understand TBTA features deeply
   - `/bible/commentaries/GEN/001/026/GEN-001-026-tbta.yaml` - See real TBTA data
   - `/bible/commentary/GEN/1/GEN_1_001.translations-ebible.yaml` - See eBible format

2. **Start research with:**
   - Trial number languages (most specific, easiest to document)
   - Inclusive/exclusive distinction (most common, well-documented)

3. **Create initial files:**
   - `/plan/tbta-languages/trial-number.md`
   - `/plan/tbta-languages/inclusive-exclusive.md`
   - `/src/lib/tbta/language_features.yaml` (start building database)

4. **First implementation task:**
   - Simple script to extract TBTA features from a verse
   - Print which features are present
   - This validates understanding before building full tool

## Key Insight

TBTA encodes features relevant to 1000+ languages, but doesn't explicitly say WHICH languages need WHICH features. By combining TBTA's linguistic annotations with the eBible corpus (actual translations in those languages), we can create the world's most comprehensive cross-linguistic Bible translation guide.

This amplifies TBTA's manual work by:
- Making it searchable and queryable
- Connecting it to real translation data
- Extending it with patterns they didn't explicitly document
- Providing concrete guidance for translators in edge-case languages

**End Goal:** When a translator working in Kilivila asks an AI about Genesis 1:26, the AI can say: "TBTA marks this as Trial number (3 persons). Kilivila has trial number. You MUST use the trial form here, not generic plural, to maintain theological precision about the Trinity."

That's the power we're building.
