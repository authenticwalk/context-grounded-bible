# Strong's Words - Available Sources Summary

**Date:** 2025-10-30
**Purpose:** Summary of all available open-license sources for enhancing Strong's concordance data

## Current Implementation Status

### ✅ What We Have
- **Script:** `strongs-fetcher.py` (root directory)
- **Source:** openscriptures/strongs (GitHub)
- **Format:** JavaScript dictionaries → YAML
- **License:** CC-BY-SA
- **Data Fields:**
  - strongs_number, language, lemma, transliteration
  - pronunciation (Hebrew only)
  - definition (strongs_def)
  - kjv_usage (kjv_def)
  - derivation
- **Total Entries:** 14,197 (8,674 Hebrew + 5,523 Greek)

### ✅ Confirmed: Strong's Exhaustive Concordance
Yes, we already have Strong's data. The openscriptures/strongs repository contains:
- Strong's Hebrew Dictionary (H0001-H8674)
- Strong's Greek Dictionary (G0001-G5624)
- Public domain content with corrections and deduplication

## Available Enhancement Sources

### 1. Extended Definitions - HIGH PRIORITY

#### STEPBible Extended Strong's ⭐ RECOMMENDED
- **Source:** https://github.com/STEPBible/STEPBible-Data
- **License:** CC BY 4.0
- **Credit:** Tyndale House Cambridge / STEPBible.org
- **Format:** Tab-delimited UTF-8 text

**Greek (TBESG):**
- File: `Lexicons/TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt`
- Based on Abbott-Smith + LSJ
- Covers: NT, LXX, Apocrypha, variants
- Fields: eStrong, dStrong, uStrong, Greek, Transliteration, Morph, Gloss, Meaning

**Hebrew (TBESH):**
- File: `Lexicons/TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt`
- Based on Abridged BDB
- Includes affix support
- Fields: eStrong#, dStrong#, uStrong#, Hebrew, Transliteration, Morph, Gloss, Meaning

**Benefits:**
- Enhanced definitions beyond basic Strong's
- Morphological information
- Disambiguated entries for multiple senses
- Backward compatible with original Strong's numbers
- Well-maintained and actively corrected

#### UBS Semantic Dictionaries ⭐ RECOMMENDED
- **Source:** https://github.com/ubsicap/ubs-open-license
- **License:** CC-BY-SA 4.0
- **Format:** XML and JSON

**SDBH (Semantic Dictionary of Biblical Hebrew):**
- Location: `/dictionaries` folder
- Coverage: ~90% of OT words
- Languages: English, French, Spanish, Chinese
- Contains: Definitions, glosses, Scripture references, semantic domains

**SDGNT (Semantic Dictionary of Greek New Testament):**
- Location: `/dictionaries` folder
- Based on Louw-Nida lexicon (revised edition)
- Contains: Definitions, glosses, Scripture references, semantic domains
- Includes exhaustive list of Scripture references per meaning

**Benefits:**
- Semantic domain organization
- Comprehensive Scripture references
- Multiple language support
- Professional scholarly resource

#### Brown-Driver-Briggs (BDB) Hebrew Lexicon
- **Source:** https://github.com/eliranwong/unabridged-BDB-Hebrew-lexicon
- **License:** Public domain
- **Format:** JSON and CSV

**Fields:**
- Hebrew/Aramaic headword
- Strong's number mapping
- Definitions and etymologies
- Scripture references (SBL abbreviations)
- Cross-references

**Note:** OpenScriptures Hebrew Lexicon also has BDB in XML format

#### Dodson Greek Lexicon
- **Source:** https://github.com/biblicalhumanities/Dodson-Greek-Lexicon
- **License:** Public domain
- **Format:** XML and CSV

**Benefits:**
- Public domain
- Strong's mapping
- Structured format

### 2. Synonym/Related Words Sources

#### Clear-Bible Proximity Data ⭐ PRIMARY SOURCE
- **Source:**
  - https://github.com/Clear-Bible/macula-hebrew/blob/main/sources/Clear/synonyms/Proximity.tsv
  - https://github.com/Clear-Bible/macula-greek/blob/main/sources/Clear/synonyms/Proximity.tsv
- **License:** CC BY 4.0
- **Format:** TSV (3 columns)

**Structure:**
```
StrongNumberX1  StrongNumberX2  Distance
G1236          G2225           0.77626025290499
H2518          H2507           0.799513172966781
```

**Benefits:**
- Quantified similarity scores (0-1 range)
- Cross-language relationships (Hebrew ↔ Greek via LXX)
- Pairwise comparisons enable finding closest synonyms
- **Most comprehensive synonym source found**

#### Ancient Greek WordNet
- **Source:** https://github.com/jcuenod/greekwordnet
- **License:** GPL-3.0
- **Format:** SQLite databases (Python library)

**Features:**
- Synsets (synonym sets)
- Antonyms
- Semantic relations
- Cross-linguistic (English, Italian)

**Limitations:**
- GPL license (not as permissive as CC)
- Automated assignment (prone to false positives)
- Python library (not raw data files)
- Unclear if it covers Biblical Greek specifically

#### UBS Semantic Dictionaries (Semantic Domains)
- Same as above in Extended Definitions
- Semantic domain groupings can identify related words
- Not direct synonyms but conceptually related terms

### 3. Cross-References & Etymologies

#### OpenScriptures Hebrew Lexicon
- **Source:** https://github.com/openscriptures/HebrewLexicon
- **License:** CC BY 4.0
- **Format:** XML

**Files:**
- `BrownDriverBriggs.xml` - Full BDB
- `HebrewStrong.xml` - Strong's with corrections
- `LexicalIndex.xml` - Cross-reference hub

**Features:**
- Links between BDB, Strong's, and TWOT numbers
- Derivative information (etymology)
- Part of speech
- Glosses

### 4. Other Notable Sources (Lower Priority)

#### Cognate Words (Semitic Languages)
- No single GitHub dataset found
- Available in academic papers and HALOT lexicon
- Mostly commercial resources
- Could be valuable for etymology but not immediately available

#### Young's Analytical Concordance
- Public domain (1882 edition)
- Available on Internet Archive
- **No structured GitHub repository found**
- Would require OCR/digitization work

#### Nave's Topical Bible
- Public domain
- Focused on topical organization, not lexical definitions
- Less relevant for word-level enhancements

#### Thayer's Greek Lexicon
- Public domain (1889)
- Available on Internet Archive
- **No clean GitHub structured data found** (only Dodson as alternative)
- Abbott-Smith (in STEPBible) is comparable

## Recommended Implementation Plan

### Phase 1: Extended Definitions (Integrate into strongs-fetcher.py)

**Update `strongs-fetcher.py` to add:**

1. **STEPBible Data**
   - Download TBESG and TBESH from STEPBible repository
   - Parse TSV format
   - Map by Strong's number
   - Add fields:
     - `extended_definition.gloss`
     - `extended_definition.full_definition`
     - `extended_definition.morphology`
     - `extended_definition.source` = "STEPBible/Abbott-Smith" or "STEPBible/BDB"

2. **UBS Semantic Dictionary** (Optional - depends on file size/complexity)
   - Could add semantic domain information
   - Add field: `semantic_domain`
   - Would require downloading ubs-open-license repo

**Example Enhanced YAML:**
```yaml
strongs_number: G0026
language: greek
lemma: ἀγάπη
transliteration: agápē
definition: love, i.e. affection or benevolence...
kjv_usage: (feast of) charity(-ably), dear, love
derivation: from G25 (ἀγαπάω)

# NEW FIELDS:
extended_definition:
  gloss: love
  full_definition: "affection or benevolence; specially a love-feast..."
  morphology: N-F
  source: STEPBible/Abbott-Smith

semantic_domain: "25.43 Love, Affection, Compassion"

source: openscriptures/strongs
license: CC-BY-SA
```

### Phase 2: Synonyms (Separate Script: strongs-synonyms-fetcher.py)

**Create new script:** `strongs-synonyms-fetcher.py`
**Output location:** `bible/words/strongs/{number}/{number}.synonyms.yaml`

**Data Source:** Clear-Bible Proximity.tsv (both Hebrew and Greek)

**Process:**
1. Download Proximity.tsv files
2. For each Strong's number:
   - Find all pairs where it appears as StrongNumberX1 or StrongNumberX2
   - Filter by minimum proximity threshold (e.g., > 0.70)
   - Sort by proximity score (highest first)
   - Group by language (same-language vs cross-language)

**Output Format:**
```yaml
strongs_number: G0026
language: greek

synonyms:
  same_language:
    - strongs: G0025
      lemma: ἀγαπάω
      proximity: 0.95
      type: verbal_form
    - strongs: G5368
      lemma: φιλέω
      proximity: 0.82
      type: related_love_word

  cross_language:
    - strongs: H0160
      lemma: אַהֲבָה
      proximity: 0.78
      language: hebrew
      note: via_lxx

source: Clear-Bible/macula-proximity
license: CC BY 4.0
```

**Benefits of Separate File:**
- Keep base Strong's data clean
- Easy to filter/exclude synonym data
- Simpler to regenerate independently
- Clearer data provenance
- Users can choose to load or ignore synonyms

### Phase 3: Additional Enhancements (Future)

Could create additional separate files:
- `{number}.etymology.yaml` - Derivations, cognates
- `{number}.cross-refs.yaml` - BDB, TWOT, HALOT references
- `{number}.usage.yaml` - Scripture reference lists

## Summary of Recommendations

### For Extended Definitions (Integrate into base script):
✅ **STEPBible TBESG/TBESH** - Best combination of quality, coverage, and ease of use
✅ **UBS SDBH/SDGNT** - Optional addition for semantic domains

### For Synonyms (Separate script):
✅ **Clear-Bible Proximity Data** - Most comprehensive, quantified relationships
⚠️ **Ancient Greek WordNet** - Consider as supplemental Greek source (GPL license concern)

### Not Immediately Recommended:
❌ Young's Analytical Concordance - No structured data available
❌ Thayer's Lexicon - No clean structured data (use Abbott-Smith from STEPBible instead)
❌ Nave's Topical - Different purpose (topical, not lexical)
❌ Cognate databases - No single comprehensive source found

## Next Steps

1. **✅ Research completed** - This document + strongs-enhancement-research.md
2. **Update strongs-fetcher.py** - Add STEPBible extended definitions
3. **Create strongs-synonyms-fetcher.py** - Process Clear-Bible proximity data
4. **Test on sample** - Verify output format with 10-20 entries
5. **Run full generation** - Process all 14,197 Strong's entries
6. **Commit:**
   - Commit 1: Code changes (fetcher scripts)
   - Commit 2: Data changes (enhanced YAML files)

## License Compatibility

All recommended sources are compatible:
- Strong's base: CC-BY-SA
- STEPBible: CC BY 4.0
- UBS: CC-BY-SA 4.0
- Clear-Bible: CC BY 4.0
- OpenScriptures: CC BY 4.0

All require attribution and allow commercial use.
