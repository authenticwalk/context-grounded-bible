# Format Standardization - eBible/USFM 3.0 Alignment

---

## Purpose

Align our Bible text organization with established standards from:
- **eBible corpus** (BibleNLP): https://github.com/BibleNLP/ebible
- **USFM 3.0 specification**: Standard book codes
- **ISO-639 language codes**: Standard language identification

---

## Standards Adopted

### 1. Book Codes (USFM 3.0)

**Format:**3-letter uppercase codes per USFM 3.0 specification

**Examples:**
- Matthew: `MAT` (not `mt` or `Matt`)
- Genesis: `GEN`
- Revelation: `REV`

**Source:** https://ubsicap.github.io/usfm/identification/books.html

### 2. Language Codes (ISO-639-3)

**Format:** 3-letter lowercase codes per ISO-639-3 standard

**Rationale:** Biblical scholarship uses ISO-639-3 for ancient languages and better granularity

**Common codes:**
```yaml
eng: English
spa: Spanish
fra: French
deu: German (Deutsch)
por: Portuguese
rus: Russian
zho: Chinese
kor: Korean
ara: Arabic
grc: Ancient Greek
heb: Biblical Hebrew
lat: Latin
```

**Note:** We use ISO-639-3 (3 letters) instead of ISO-639-1 (2 letters) because:
- Ancient languages like `grc` (Ancient Greek) have no ISO-639-1 equivalent
- Consistency across modern and ancient languages
- Standard in biblical text repositories

### 3. Directory Structure

**Commentary:** `/bible/commentary/{BOOK}/{chapter:03d}/{BOOK}.{chapter:03d}.{verse:03d}-{type}.yaml`

**Examples:**

**Commentary:**
```
/bible/commentary/MAT/005/MAT.005.003-translations.yaml
/bible/commentary/MAT/005/MAT.005.003-semantic-clusters.yaml
/bible/commentary/GEN/001/GEN.001.001-translations.yaml
```

**Topics:**
```
/bible/topics/BT109/trinity/trinity.yaml
/bible/topics/BT130/divine-attributes/omniscience/omniscience.yaml
/bible/topics/BT750/salvation/justification/justification.yaml
/bible/topics/BT819/eschatology/second-coming/second-coming.yaml
```

**Words:**
```
/bible/words/{ISO-639-3}/{word-root}/{word-inflected}.yaml
```

**Strong's Concordance:**
```
/bible/words/strongs/{strongs-number}/{strongs-number}.strongs.yaml
```

Strong's numbers use 4-digit zero-padded format:
- Greek: `G0001` through `G5624` (5,523 entries)
- Hebrew: `H0001` through `H8674` (8,674 entries)

Examples:
```
/bible/words/strongs/G0001/G0001.strongs.yaml    # Greek: Α (Alpha)
/bible/words/strongs/G0025/G0025.strongs.yaml    # Greek: ἀγαπάω (agapáō - to love)
/bible/words/strongs/H0157/H0157.strongs.yaml    # Hebrew: אָהַב (ahab - to love)
/bible/words/strongs/G5368/G5368.strongs.yaml    # Greek: φιλέω (philéō - brotherly love)
```

**Rationale (Directory Structure):**
- Book code visible in filename (easier to identify files out of context)
- Period separators for chapter.verse (standard in biblical references)
- Hyphen before type descriptor (translations, semantic-clusters, etc.)

---

### 4. Word Normalization Standards

**Purpose:** Store lexical/semantic data for words, organized by root form for easy lookup

**Path:** `/bible/words/{lang}/{word-root}/{word-inflected}.yaml`

**Components:**
- `{lang}`: ISO-639-3 language code (e.g., `heb`, `grc`, `eng`)
- `{word-root}`: Lemmatized/root form (base word before inflection)
- `{word-inflected}`: Actual word form (may be same as root, or inflected)

**Normalization Rules by Language:**

**Hebrew (`heb`):**
- Use lexical form (dictionary entry)
- No gender, number, or state variations
- Examples: `אָהַב` (ahav) not `אֹהֵב` (ohev), `אָהְבָה` (ahavah)

**Greek (`grc`):**
- Use lexical form (nominative singular for nouns, 1st person singular present for verbs)
- No case, gender, number, tense variations
- Examples: `λόγος` (logos) not `λόγου` (logou), `λόγον` (logon)

**English (`eng`):**
- Use base form (infinitive for verbs, singular for nouns)
- Examples: `love` not `loves`, `loving`, `loved`

**Examples:**

```
# Root form (same as directory)
/bible/words/heb/אהב/אהב.yaml          # Root: love (ahav)
/bible/words/grc/λογος/λογος.yaml      # Root: word/logos

# Inflected forms grouped under root
/bible/words/heb/אהב/אהבה.yaml         # Inflected: ahavah (she loved)
/bible/words/grc/λογος/λογου.yaml      # Inflected: logou (genitive)
/bible/words/grc/λογος/λογον.yaml      # Inflected: logon (accusative)

# English (minimal inflection, but still grouped)
/bible/words/eng/love/love.yaml        # Base form
/bible/words/eng/love/loves.yaml       # 3rd person singular
/bible/words/eng/love/loved.yaml       # Past tense
```

**YAML Format:**

```yaml
# Root form example
language: heb
word: אָהַב
root: אָהַב
transliteration: ahav
strongs: H157
meaning: to love, have affection
related_words:
  - grc/αγαπη/αγαπη
  - eng/love/love
verses: [JHN.3.16, 1JN.4.8]

# Inflected form example
language: grc
word: λόγου
root: λόγος
transliteration: logou
grammatical_form: genitive singular
meaning: of a word
verses: [JHN.1.1]
```

**Benefits:**
- **Discoverable**: Can look up any inflected form and find its root
- **Organized**: All forms of a word grouped together
- **Root explicit**: Root is visible in directory path
- **Cross-referencing**: Easy to link related words across languages

**References for Lemmatization:**

- **Hebrew:** Brown-Driver-Briggs (BDB) Lexicon, Strong's Concordance
- **Greek:** BDAG Lexicon, Strong's Concordance, Thayer's Greek Lexicon
- **Strong's Numbers:** Use as cross-reference (e.g., H0157 for אָהַב, G0026 for ἀγάπη)

### 4a. Strong's Concordance Format

**Purpose:** Standardized reference database for every Hebrew and Greek word in the Bible

**Path:** `/bible/words/strongs/{strongs-number}/{strongs-number}.strongs.yaml`

**Number Format:** 4-digit zero-padded with language prefix
- Greek: `G0001` through `G5624` (prefix `G`)
- Hebrew: `H0001` through `H8674` (prefix `H`)

**YAML Structure:**
```yaml
strongs_number: G0025
language: greek
lemma: ἀγαπάω
transliteration: agapáō
pronunciation: ag-ap-ah'-o         # Hebrew only
definition: to love (in a social or moral sense)
kjv_usage: (be-)love(-ed)
derivation: perhaps from (much) (or compare G5689);
source: openscriptures/strongs
license: CC-BY-SA
```

**Field Descriptions:**
- `strongs_number`: Zero-padded identifier (G0001-G5624 or H0001-H8674)
- `language`: Either `greek` or `hebrew`
- `lemma`: Original language word in native script
- `transliteration`: Romanized version of the word
- `pronunciation`: Phonetic pronunciation guide (Hebrew entries only)
- `definition`: Strong's original definition
- `kjv_usage`: How the word appears in King James Version
- `derivation`: Etymological origin and related Strong's numbers
- `source`: Data source (openscriptures/strongs)
- `license`: CC-BY-SA (Creative Commons Attribution-ShareAlike)

**Examples:**
```
/bible/words/strongs/G0001/G0001.strongs.yaml    # Α (Alpha) - first letter
/bible/words/strongs/G0025/G0025.strongs.yaml    # ἀγαπάω (agapáō) - divine love
/bible/words/strongs/G0026/G0026.strongs.yaml    # ἀγάπη (agápē) - love (noun)
/bible/words/strongs/G5368/G5368.strongs.yaml    # φιλέω (philéō) - brotherly love
/bible/words/strongs/H0001/H0001.strongs.yaml    # אָב (ab) - father
/bible/words/strongs/H0157/H0157.strongs.yaml    # אָהַב (ahab) - to love
```

**Cross-referencing with Word Files:**
```yaml
# In /bible/words/grc/αγαπη/αγαπη.yaml
strongs: G0026                      # Reference to Strong's entry

# In /bible/words/heb/אהב/אהב.yaml
strongs: H0157                      # Reference to Strong's entry
```

**Data Source:** https://github.com/openscriptures/strongs (CC-BY-SA license)

**Why Zero-Padding:**
- Consistent string length for sorting and display
- Aligns with digital Bible tools and reference software
- Prevents ambiguity (G1 vs G0001 both valid, but G0001 is standard)
- Easier programmatic handling and file system organization

### 5. Theological Topic Taxonomy

**Standard:** Library of Congress Classification (LCC) codes + human-readable slugs

**Format:** `/bible/topics/{lcc-code}/{slug}/{slug}.yaml`

**Major LCC Sections for Biblical Topics:**
```
BS: Biblical Studies (texts, interpretation, geography, biblical topics)
BT: Doctrinal Theology (God, Christ, salvation, eschatology)
BV: Practical Theology (prayer, Christian life, worship, ethics)
BX: Denominations and Church History
```

**Example Topics with LCC Codes:**
```
/bible/topics/BS1199/land-of-canaan/land-of-canaan.yaml    # Biblical geography
/bible/topics/BT109/trinity/trinity.yaml                   # Doctrinal theology
/bible/topics/BT750/salvation/justification/justification.yaml  # Soteriology
/bible/topics/BV210/prayer/prayer.yaml                     # Practical theology
/bible/topics/BV4909/suffering/suffering.yaml              # Christian life topics
```

**YAML Format:**
```yaml
lcc_code: BT109
topic: Trinity
slug: trinity
related_topics: [BT117/holy-spirit, BT130/divine-attributes]
verses: [MAT.28.19, JHN.1.1]
```

**How to Find LCC Codes:**
- Search Westminster Seminary LibGuide: https://wts.libguides.com/c.php?g=1414259
- Use Library of Congress Online Catalog: https://catalog.loc.gov
- Check BISAC codes for cross-reference: https://www.bisg.org/religion

---

### 6. Cross-Referencing Standards

**Purpose:** Consistent format for linking between files (words, topics, verses)

#### Word References

**Format:** `{lang}/{word-root}/{word-inflected}`

Use full directory path when referencing words in any YAML field:

```yaml
# In word files
related_words:
  - grc/αγαπη/αγαπη      # Greek agape (root)
  - heb/אהב/אהב          # Hebrew ahav (root)
  - eng/love/love        # English love
  - grc/λογος/λογου      # Greek logos (genitive)

# In topic or verse analysis files
key_words:
  - grc/πιστις/πιστις    # faith
  - grc/ελπις/ελπις      # hope
  - grc/αγαπη/αγαπη      # love
```

**Benefits:**
- Unambiguous file location
- Language explicit
- Can reference specific inflections
- Easy to programmatically resolve

#### Topic References and Aliases

**Format:** `{lcc-code}/{slug}` - LCC code provides category, slug provides readability

**Standard reference** (no `@`):
```yaml
related_topics:
  - BT750/justification           # Soteriology section
  - BT198/atonement               # Christology section  
  - BV210/prayer                  # Practical theology
```

**Alias reference** (with `@` prefix) - indicates primary definition is elsewhere:
```yaml
# In /bible/topics/BV4627/sin/sin.yaml (Practical: Sins & Virtues)
primary_topic: "@BT695/fall-of-man"   # See doctrinal treatment

# In /bible/topics/BT750/atonement/atonement.yaml (Soteriology)
see_also:
  - "@BV210/prayer"                    # Practical application
  - "@BS1199/day-of-atonement"         # Biblical reference
```

**Understanding LCC Codes** (for human reference):
```
BS1199: Biblical Topics (geography, people, events)
BT109:  Trinity
BT130:  Divine Attributes  
BT198:  Christology
BT695:  Creation & Fall
BT750:  Soteriology (Salvation)
BT819:  Eschatology
BV210:  Worship & Prayer
BV4627: Sins & Virtues
BV4909: Suffering & Consolation
```

**Use Cases:**
- `@prefix`: Topic aliased/defined elsewhere
- No prefix: Standard cross-reference
- `primary_topic`: This file redirects to another
- `see_also`: Related topics for further study

**Note:** While LCC codes aren't immediately readable, they're necessary for:
- Precise categorization
- Avoiding slug conflicts
- Standard library compatibility
- The slug makes the actual topic clear

#### Verse References

**Format:** `{BOOK}.{chapter:03d}.{verse:03d}` (zero-padded per Section 1)

```yaml
cross_refs:
  - JHN.3.16
  - ROM.8.28
  - PSA.23.1

related_verses:
  - ref: MAT.5.3
    note: "First beatitude"
  - ref: JHN.11.35
    note: "Jesus wept"
```

### 7. Translation Version Keys (Incremental Format)

**Format:** Incremental specificity as needed: `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

**Principles:**
1. Use minimum specificity needed to uniquely identify the translation
2. Add components only when disambiguation is required
3. Maintain consistency within language families

**Examples:**
```yaml
# Single translation in language (language code only)
ara: "Standard Arabic translation"
heb: "Standard Hebrew text"

# Multiple translations, no version conflict (language + version)
eng-niv: "New International Version"
eng-kjv: "King James Version"
eng-esv: "English Standard Version"

# Same version, different years (language + version + year)
eng-niv-1984: "NIV 1984 edition"
eng-niv-2011: "NIV 2011 edition"
spa-rv-1909: "Reina Valera 1909"
spa-rv-1960: "Reina Valera 1960"
```

**Components (add incrementally as needed):**
1. `lang`: ISO-639-3 language code (3 letters, lowercase) - **REQUIRED**
2. `version`: Translation abbreviation (UPPERCASE: NIV, ESV, KJV, etc.) - add when multiple translations exist
3. `year`: Publication year (4 digits) - add only when same version has multiple editions

**Version Code Standards:**
- Version abbreviations: UPPERCASE (NIV, KJV, ESV, RV, NA28)
- Language codes: lowercase (eng, spa, grc, heb)
- Separator: hyphen (`-`)
- No redundancy: Don't repeat language in version (❌ `eng-engNIV`, ✅ `eng-NIV`)

**Rationale:**
- Minimal format reduces verbosity for unique translations
- Year precision only when needed (NIV 1984 vs 2011 has significant differences)
- Matches eBible corpus naming conventions
- Easy to extend when disambiguation needed

---

### 5. Citation Standards (Inline Source Format)

**Format:** Inline citations immediately after content: `content {source}`

**Principles:**
1. Every translation, fact, or analysis must cite its source
2. Citations appear inline, not as separate fields or lists
3. No fabricated examples - only cite what exists in data files
4. Use standardized source codes from `source-abbreviations.yaml`

**Citation Format by Content Type:**

```yaml
# AI-generated analysis or insights
rationale: "This demonstrates theological emphasis" {llm-cs45}

# Translation citations in examples
- example: "Blessed are the poor in spirit"
  sources: [eng-NIV-2011, eng-ESV]

# Cultural or linguistic notes
cultural_note: "Sino-Tibetan languages use emptiness concept" {llm-cs45}

# Greek/Hebrew source text
source_text: "μακάριοι οἱ πτωχοὶ τῷ πνεύματι" {grc-NA28}
```

**Source Code Structure:**

Incremental format: `{lang}-{version}` → `{lang}-{version}-{year}`

Components:
- `lang`: ISO-639-3 code (3 letters, lowercase) - **REQUIRED**
- `version`: Translation abbreviation (UPPERCASE: NIV, ESV, NA28, etc.)
- `year`: Publication/revision year (4 digits) - **only when multiple editions exist**

**Common Examples:**
```yaml
grc-NA28                   # Greek: Nestle-Aland 28th edition (single edition)
eng-NIV-1984               # English: NIV 1984 (multiple editions exist)
eng-NIV-2011               # English: NIV 2011
eng-ESV                    # English: ESV (single primary edition)
spa-RV-1960                # Spanish: Reina Valera 1960 (multiple editions exist)
llm-cs45                   # AI analysis: Claude Sonnet 4.5
```

**Rules:**
- ✅ Inline format: `content {source}` (curly braces)
- ✅ Immediate placement: Citation directly after the content it supports
- ✅ Array format for multiple sources: `sources: [source1, source2, source3]`
- ❌ NO separate `source:` fields
- ❌ NO newline citations
- ❌ NO fabricated translations
- ❌ NO citations without actual data verification

**Source Authority Levels:**

Per `source-abbreviations.yaml`:
- **High authority**: Biblical text editions (NA28, UBS5, Biblia Hebraica), established translations (NIV, ESV, NASB)
- **Medium authority**: Digital platforms (BibleHub, eBible, Bible Gateway)
- **Low authority**: LLM-generated content (llm-cs45, llm-gpt4) - ALWAYS requires human review

**Rationale:**
- Enables full traceability of all claims
- Prevents fabrication or hallucination
- Maintains academic rigor in analysis
- Clear distinction between authoritative sources and AI-generated content
- Inline format keeps content and citations together
- Incremental specificity (only add year when needed for disambiguation)

**Reference:** See `/source-abbreviations.yaml` for complete version lookup table.

---


## References

**Bible Text Standards:**
- **eBible corpus:** https://github.com/BibleNLP/ebible
- **USFM 3.0 book codes:** https://ubsicap.github.io/usfm/identification/books.html
- **ISO-639-3 codes:** https://iso639-3.sil.org/code_tables/639/data
- **BibleHub:** https://biblehub.com (translation source)

**Theological Topic Standards:**
- **Library of Congress Classification (LCC):** https://wts.libguides.com/c.php?g=1414259
- **BISAC Subject Headings (Religion):** https://www.bisg.org/religion
- **Index Theologicus (IxTheo):** https://ixtheo.de/Content/IxTheoClassification


