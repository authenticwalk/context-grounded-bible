# morphhb Repository Analysis - Hebrew Bible Goldmine

**Date:** 2025-10-30
**Purpose:** Comprehensive analysis of the morphhb repository for Strong's enhancement

## Executive Summary

**morphhb is a DIFFERENT type of resource** than STEPBible lexicons:
- **STEPBible TBESH:** Hebrew lexicon/dictionary (definitions of Strong's numbers)
- **morphhb:** Fully tagged Hebrew Bible text (every word with Strong's + morphology)

**Recommendation:** ✅ **HIGHLY VALUABLE - Use for different purposes**

## What is morphhb?

The Open Scriptures Hebrew Bible (OSHB) is a morphologically tagged version of the Westminster Leningrad Codex with linguistic annotation for every single word.

**Repository:** https://github.com/openscriptures/morphhb
**License:** CC BY 4.0 (morphology/lemma data), Public Domain (WLC text)
**Format:** OSIS XML + JSON (via npm package)

## Data Structure

### Files Available

**40 XML files in `/wlc` directory:**
- All 39 OT books (Gen.xml through Mal.xml)
- VerseMap.xml for verse reference mapping

**Each word has three attributes:**

```xml
<w lemma="c/1961" morph="HC/Vqw3ms" id="08xeN">וַ/יְהִ֗י</w>
```

1. **lemma** - Augmented Strong's number
2. **morph** - Morphological parsing code
3. **id** - Unique immutable word ID

### JSON Format (npm package)

Available via: `npm install morphhb`

**Structure:**
```javascript
{
  "Genesis": [  // Book
    [  // Chapter
      [  // Verse
        ["wordString", "lemma", "morphology"],
        ["wordString", "lemma", "morphology"],
        ...
      ]
    ]
  ]
}
```

**Example:**
```javascript
[
  ["וַ/יְהִ֗י", "c/1961", "HC/Vqw3ms"],
  ["בִּ/ימֵי֙", "b/3117", "HR/Ncmpc"],
  ["שְׁפֹ֣ט", "8199", "HVqc"]
]
```

## Augmented Strong's Numbers

### How Prefixes Are Handled

Unlike standard Strong's, morphhb uses **slash notation** for prefixes:

| Augmented | Meaning | Standard Strong's |
|-----------|---------|-------------------|
| `c/1961` | conjunction + #1961 | Splits into prefix + word |
| `b/3117` | preposition "b" + #3117 | Splits into prefix + word |
| `d/8199` | definite article + #8199 | Splits into prefix + word |
| `1961` | No prefix, just #1961 | Same as standard |

**Prefix codes:**
- `c` = conjunction (ו)
- `b` = preposition (ב)
- `d` = definite article (ה)
- `l` = preposition (ל)
- `m` = preposition (מ)
- `k` = preposition (כ)
- `s` = pronoun (ש)
- etc.

### Augmentation Letters

Strong's numbers may have letter suffixes: `6529a`, `6529b`

These distinguish different BDB entries that share a Strong's number.

**Processing option:** `--removeLemmaTypes` strips these letters to match standard dictionaries.

## Morphological Codes

### Code Structure

Format: `<Language><Prefix1><Prefix2>/<POS><Features>`

**Example:** `HC/Vqw3ms`
- `H` = Hebrew
- `C` = Conjunction prefix
- `/` = Separator
- `V` = Verb
- `q` = Qal stem
- `w` = Wayyiqtol (sequential)
- `3` = 3rd person
- `m` = Masculine
- `s` = Singular

**Example:** `HR/Ncmpc`
- `H` = Hebrew
- `R` = Preposition prefix
- `N` = Noun
- `c` = Common (vs. proper)
- `m` = Masculine
- `p` = Plural
- `c` = Construct state

### Full Morphology Code Documentation

Available at: https://hb.openscriptures.org/parsing/HebrewMorphologyCodes.html

**Categories encoded:**
- Part of speech (V=verb, N=noun, A=adjective, etc.)
- Verbal features (stem, conjugation, person, gender, number)
- Nominal features (gender, number, state)
- Prefixes (prepositions, conjunctions, articles)
- Suffixes (pronominal, directional)

## Unique Word IDs

### Format

Each word has a permanent ID like `08xeN`

**Structure:**
- First 2 digits: KJV book number (01-39)
- Last 3 characters: Random identifier

**Example:** `08xeN`
- `08` = Ruth (8th book in KJV ordering)
- `xeN` = Random unique identifier

### Purpose

**Immutability:** IDs never change, even if:
- Versification changes
- Textual variants discovered
- Morphology corrected
- Lemma updated

**Use case:** Associate external data with specific word instances:
- Manuscript variants
- Translation choices
- Commentary notes
- Cross-references

## Comparison: morphhb vs STEPBible

| Feature | morphhb | STEPBible TBESH |
|---------|---------|-----------------|
| **Purpose** | Tagged Bible text | Lexicon/dictionary |
| **Scope** | Every word in Hebrew Bible | Definitions for Strong's numbers |
| **Data type** | Usage instances | Meanings/definitions |
| **Format** | XML, JSON | TSV |
| **Organization** | By verse | By Strong's number |
| **Strong's handling** | Augmented (with prefixes) | Standard numbers |
| **Morphology** | Full parsing codes | Brief POS tags |
| **Word IDs** | Unique immutable IDs | No word IDs |
| **License** | CC BY 4.0 | CC BY 4.0 |

**They complement each other:**
- STEPBible tells you **what a word means**
- morphhb shows you **where and how it's used**

## How morphhb Enhances Our Project

### Use Case 1: Usage Examples

**For each Strong's number, we can extract:**
- All verses where it appears
- Contextual examples
- Frequency count
- Morphological variations

**Example for H1961 (היה - "to be"):**
```yaml
usage:
  total_occurrences: 3562
  example_verses:
    - ref: "Genesis 1:3"
      text: "וַיְהִי אוֹר"
      translation: "And there was light"
      morph: "Vqw3ms"
    - ref: "Ruth 1:1"
      text: "וַיְהִי בִּימֵי"
      translation: "And it was in the days"
      morph: "Vqw3ms"

  morphological_distribution:
    - morph: "Vqw3ms"
      count: 1205
      description: "Qal wayyiqtol 3rd masc singular"
    - morph: "Vqp3ms"
      count: 487
      description: "Qal perfect 3rd masc singular"
```

### Use Case 2: Prefix Analysis

**Identify common prefix patterns:**

For H3117 (יוֹם - "day"):
```yaml
prefix_patterns:
  - lemma: "b/3117"
    prefix: "b"
    meaning: "in/on the day"
    count: 542
  - lemma: "3117"
    prefix: none
    meaning: "day"
    count: 1087
  - lemma: "c/3117"
    prefix: "c"
    meaning: "and day"
    count: 94
```

### Use Case 3: Collocation Discovery

**Find words commonly appearing together:**

For H0430 (אֱלֹהִים - "God"):
```yaml
common_collocations:
  - adjacent_word: H0559 (אמר - "said")
    pattern: "And God said"
    occurrences: 42
  - adjacent_word: H1254 (ברא - "created")
    pattern: "God created"
    occurrences: 11
```

### Use Case 4: Morphological Patterns

**Identify grammatical usage patterns:**

For H8199 (שָׁפַט - "judge"):
```yaml
morphological_usage:
  verb_forms:
    - stem: "Qal"
      count: 105
      common_patterns: ["Vqp", "Vqi", "Vqw"]
    - stem: "Niphal"
      count: 23
      meaning: "to be judged"
  participle_usage:
    - morph: "Vqrmsa"
      count: 67
      meaning: "one who judges (masculine singular active participle)"
      context: "Used as noun for 'judge'"
```

## Implementation Options

### Option 1: Enhanced Strong's Files (Recommended)

**Add usage data to existing Strong's YAML:**

File: `bible/words/strongs/H1961/H1961.strongs.yaml`

```yaml
strongs_number: H1961
language: hebrew
lemma: הָיָה
transliteration: hāyāh
definition: to be, become, come to pass, happen
kjv_usage: was, come to pass, came, has been...

# FROM STEPBIBLE:
extended_definition:
  gloss: to be
  full_definition: "to be, become, exist..."
  source: STEPBible/BDB

# FROM MORPHHB:
usage_statistics:
  total_occurrences: 3562
  with_prefixes: 2234
  without_prefixes: 1328

morphological_distribution:
  - morph: "Vqw3ms"
    description: "Qal wayyiqtol 3rd masc sing"
    count: 1205
    percentage: 33.8
  - morph: "Vqp3ms"
    description: "Qal perfect 3rd masc sing"
    count: 487
    percentage: 13.7

example_verses:
  - ref: "Genesis 1:3"
    text: "וַיְהִי אוֹר"
    word_id: "01abc"
  - ref: "Genesis 1:5"
    text: "וַיְהִי־עֶרֶב"
    word_id: "01def"
  # Limited to 5-10 examples

source: openscriptures/strongs + morphhb
license: CC-BY-SA + CC BY 4.0
```

### Option 2: Separate Usage File

**Create parallel usage files:**

File: `bible/words/strongs/H1961/H1961.usage.yaml`

```yaml
strongs_number: H1961
language: hebrew
source: morphhb
license: CC BY 4.0

statistics:
  total_occurrences: 3562
  books_appearing_in: 39
  most_frequent_book: Genesis (327)

morphology: [...]
examples: [...]
collocations: [...]
```

**Benefits:**
- Keeps base Strong's files clean
- Usage data separate and optional
- Can regenerate independently
- Clearer data provenance

### Option 3: Verse-Level Commentary

**Alternative approach - add to verse commentaries:**

File: `bible/MAT/001/001/MAT-001-001-morphology.yaml`

This would be for Greek (morphgnt), not morphhb, but same concept.

## Processing Scripts

### Proposed Script: `morphhb-usage-processor.py`

**Purpose:** Extract usage statistics from morphhb XML/JSON

**Process:**
1. Load morphhb JSON data (from npm package or convert XML)
2. Build index by Strong's number
3. For each Strong's number:
   - Count total occurrences
   - Count prefix variations
   - Extract morphological patterns
   - Find example verses
   - Calculate statistics
4. Generate usage YAML files

**Output:** `{number}.usage.yaml` or enhanced `{number}.strongs.yaml`

**Libraries needed:**
- `xml.etree.ElementTree` (for XML parsing)
- `yaml` (for output)
- Could use npm morphhb package directly

### Integration with Existing Scripts

**Update `strongs-fetcher.py`:**
- Add morphhb processing alongside STEPBible
- OR keep separate for cleaner separation

## Data Volume Considerations

### Full morphhb Dataset

**Size:**
- 39 XML files (~30-500 KB each)
- Total XML: ~10-15 MB
- JSON package: ~5-7 MB

**Processing:**
- Parse ~23,000 verses
- Tag ~305,000 words
- Group by ~8,674 Hebrew Strong's numbers
- Average 35 occurrences per Strong's number

### Storage Impact

**Per Strong's entry (if adding usage data):**
- Current YAML: ~300-500 bytes
- With usage stats: ~1-2 KB
- With examples (5): ~2-3 KB

**Total for 8,674 Hebrew entries:**
- Current: ~2.6 MB
- With usage: ~17-26 MB

**Reasonable:** Modern storage can easily handle this.

## Recommendations

### Immediate Actions (High Priority)

1. ✅ **Use morphhb for Hebrew usage statistics**
   - Extract occurrence counts
   - Add to Strong's YAML files
   - OR create separate `.usage.yaml` files

2. ✅ **Download morphhb npm package**
   - Run: `npm install morphhb`
   - Use JSON format (easier than XML parsing)
   - More lightweight than cloning full repo

3. ✅ **Create morphhb processor script**
   - Script: `src/lib/morphhb/morphhb_usage_processor.py`
   - Follow pattern from macula processors
   - Output: Enhanced Strong's files OR separate usage files

### Future Enhancements (Medium Priority)

4. ⚠️ **Prefix pattern analysis**
   - Track b/3117 vs 3117 patterns
   - Show common prepositional uses
   - Valuable for translators

5. ⚠️ **Morphological distribution**
   - Show verb stem usage
   - Show noun state patterns
   - Grammar learning tool

6. ⚠️ **Collocation discovery**
   - Words appearing together
   - Common phrases
   - Idiomatic expressions

### Optional (Lower Priority)

7. ⚠️ **Unique word IDs**
   - Store for future manuscript variant tracking
   - Not immediately needed for lexicon project
   - Bookmark for textual criticism features

8. ⚠️ **morphgnt for Greek**
   - Same concept for Greek NT
   - Available at: https://github.com/morphgnt
   - Would complement morphhb

## Comparison with Other Sources

### morphhb vs Clear-Bible Proximity

**Clear-Bible Proximity:** Word similarity scores (synonyms)
**morphhb:** Word usage instances and patterns

**Both valuable, different purposes:**
- Proximity → Related words (semantic)
- morphhb → Usage patterns (syntactic)

### morphhb vs STEPBible TBESH

**STEPBible TBESH:** Definitions and meanings
**morphhb:** Usage and occurrences

**Complementary:**
- TBESH → What it means
- morphhb → How it's used

### morphhb vs unfoldingWord UHAL

**unfoldingWord UHAL:** Lexicon entries in Markdown
**morphhb:** Tagged Bible text

**Different formats, similar source:**
- Both use Westminster Leningrad Codex
- UHAL focused on definitions
- morphhb focused on tagging

## Licensing & Attribution

**morphhb License:** CC BY 4.0

**Attribution required:**
- "Lemma and morphology data: CC BY 4.0 Open Scriptures Hebrew Bible Project"
- WLC text: Public Domain

**Compatible with our project:** ✅ Yes (MIT + CC licenses compatible)

## Conclusion

**morphhb is EXTREMELY valuable for our project:**

✅ **What it gives us:**
1. Usage statistics for every Hebrew Strong's number
2. Real verse examples with context
3. Morphological pattern analysis
4. Prefix/suffix usage patterns
5. Frequency data
6. Collocation discovery

✅ **How it complements existing sources:**
- STEPBible: Definitions
- Clear-Bible: Synonyms
- morphhb: Usage & Examples

✅ **Implementation priority:** HIGH
- Enhances Strong's data significantly
- Easy to process (JSON available)
- Clean license (CC BY 4.0)
- Well-maintained project

**Recommendation:** Create `morphhb-usage-processor.py` to extract usage statistics and add to Strong's YAML files (or create parallel `.usage.yaml` files).

This is a **genuine goldmine** for Hebrew word study!
