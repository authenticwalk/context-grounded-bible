# Strong's Words Enhancement Research

**Date:** 2025-10-30
**Purpose:** Research available resources to enhance Strong's concordance data with synonyms, related words, corrections, and cross-references.

## Current State

### Data Structure
- **Location:** `./bible/words/strongs/{number}/{number}.strongs.yaml`
- **Total entries:** 14,197 (8,674 Hebrew + 5,523 Greek)
- **Source:** openscriptures/strongs
- **License:** CC-BY-SA

### Current Fields
```yaml
strongs_number: G0026
language: greek
lemma: ἀγάπη
transliteration: agápē
definition: love, i.e. affection or benevolence...
kjv_usage: (feast of) charity(-ably), dear, love
derivation: from G25 (ἀγαπάω)
source: openscriptures/strongs
license: CC-BY-SA
```

## Available Enhancement Resources

### 1. Clear-Bible Synonym Proximity Data

**Source:** https://github.com/Clear-Bible/macula-hebrew & macula-greek
**License:** CC BY 4.0
**Format:** TSV (Tab-Separated Values)

#### Structure
- **File:** `sources/Clear/synonyms/Proximity.tsv`
- **Columns:** StrongNumberX1, StrongNumberX2, Distance
- **Description:** Pairwise similarity scores between Strong's numbers

#### Example Data
```
StrongNumberX1  StrongNumberX2  Distance
G1236          G2225           0.77626025290499
G1236          H2416d          0.729886027859856
H2518          H2507           0.799513172966781
```

#### Use Case
- Find synonyms by proximity score (higher = more similar)
- Cross-language relationships (Hebrew ↔ Greek via LXX)
- Related word suggestions

### 2. STEPBible Extended Strong's Data

**Source:** https://github.com/STEPBible/STEPBible-Data
**Credit:** Tyndale House Cambridge / STEPBible.org
**License:** CC BY 4.0
**Format:** Tab-delimited UTF-8 text files

#### TBESG (Greek) - Translators Brief Lexicon
**File:** `Lexicons/TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt`

**Columns:**
- eStrong (Extended Strong's)
- dStrong (Disambiguated Strong's)
- uStrong (Unified Strong's)
- Greek (Unicode form)
- Transliteration
- Morph (Grammatical classification)
- Gloss (Brief meaning)
- Meaning (Full definition from Abbott-Smith/LSJ)

**Enhancements:**
- Disambiguated entries for words with multiple senses
- Corrected Abbott-Smith definitions
- Covers NT, LXX, Apocrypha, and variants
- Morphological classifications

#### TBESH (Hebrew) - Translators Brief Lexicon
**File:** `Lexicons/TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt`

**Columns:**
- eStrong# (Extended)
- dStrong# (Disambiguated)
- uStrong# (Unified)
- Hebrew (Unicode form)
- Transliteration
- Morph (Grammatical classification)
- Gloss (Brief meaning)
- Meaning (Abridged BDB definition)

**Enhancements:**
- Abridged BDB (Brown-Driver-Briggs) definitions
- Affix support (prefixes/suffixes)
- Compatible with OpenScriptures
- Backward compatible with original Strong's

### 3. OpenScriptures Hebrew Lexicon

**Source:** https://github.com/openscriptures/HebrewLexicon
**License:** CC BY 4.0 (text is public domain)
**Format:** XML

#### Files
- `BrownDriverBriggs.xml` - Full BDB content
- `HebrewStrong.xml` - Strong's Hebrew with corrections
- `LexicalIndex.xml` - Cross-reference hub

#### Features
- **Cross-references:** Links between BDB, Strong's, and TWOT numbers
- **Derivative information:** Etymology and word relationships
- **Corrections:** Numerous fixes to original Strong's
- **Deduplicated entries**

### 4. Additional Semantic Resources

#### Louw-Nida Semantic Domains (Greek NT)
- Organizes 5,594 words into 25,000+ meanings
- 93 semantic domains
- Available in commercial Bible software (not free dataset found)

#### Clear-Bible Speaker Quotations
**Source:** https://github.com/Clear-Bible/speaker-quotations
**Contains:** Louw-Nida identifiers for semantic relationships

## Proposed Enhancements

### 1. Synonym/Related Words (High Priority)
**Source:** Clear-Bible Proximity.tsv
**Implementation:**
- Add `related_words` field with proximity scores
- Include both same-language and cross-language relationships
- Filter by minimum proximity threshold (e.g., > 0.70)

```yaml
related_words:
  synonyms:
    - strongs: G2225
      proximity: 0.776
      lemma: ψυχή
    - strongs: H2416d
      proximity: 0.729
      lemma: חַי
```

### 2. Enhanced Definitions (High Priority)
**Source:** STEPBible TBESG/TBESH
**Implementation:**
- Add extended definitions from Abbott-Smith (Greek) or BDB (Hebrew)
- Include morphological information
- Add glosses for quick reference

```yaml
extended_definition:
  gloss: love
  full_definition: "affection or benevolence; specially a love-feast..."
  morphology: N-F  # Noun-Feminine
  source: STEPBible/Abbott-Smith
```

### 3. Disambiguation (Medium Priority)
**Source:** STEPBible disambiguated numbers
**Implementation:**
- Track when a Strong's number has multiple distinct senses
- Link to specific contextual meanings

```yaml
disambiguation:
  extended_number: G0026
  disambiguated: G0026
  senses:
    - context: "general affection"
    - context: "Christian love feast"
```

### 4. Cross-References (Medium Priority)
**Source:** OpenScriptures LexicalIndex.xml
**Implementation:**
- Link to other lexicon systems (BDB, TWOT, HALOT)
- Include etymological derivations

```yaml
cross_references:
  bdb: "BDB entry 12"
  twot: "TWOT 4"
  derivation:
    from: G0025
    type: verb_to_noun
```

### 5. Corrections/Updates (Low Priority - Document Only)
**Approach:** Document known corrections rather than modify original data
**Implementation:**
- Add `corrections` field noting updates from STEPBible
- Preserve original for backward compatibility

```yaml
corrections:
  - field: transliteration
    original: agape
    corrected: agápē
    source: STEPBible
    note: "Added diacritical marks for pronunciation"
```

## Implementation Plan

### Phase 1: Infrastructure Setup

#### 1.1 Create Shared Fetcher Library
**Pattern:** Follow `src/lib/macula/macula_fetcher.py`

Create `src/lib/strongs/strongs_fetcher.py`:
- Fetch Clear-Bible proximity data
- Fetch STEPBible lexicons
- Fetch OpenScriptures lexicon XMLs
- Cache in `/tmp/strongs_enhancement/`

```python
# Example structure
CACHE_DIR = Path("/tmp/strongs_enhancement")
PROXIMITY_DIR = CACHE_DIR / "proximity"
STEPBIBLE_DIR = CACHE_DIR / "stepbible"
OPENSCRIPTURES_DIR = CACHE_DIR / "openscriptures"
```

#### 1.2 Create Processing Library
**Pattern:** Follow `src/lib/macula/macula_processor.py`

Create `src/lib/strongs/strongs_processor.py`:
- Parse TSV proximity data
- Parse STEPBible lexicon TSV
- Parse OpenScriptures XML
- Generate enhanced YAML files

### Phase 2: Data Integration

#### 2.1 Proximity/Synonym Processor
```python
def process_proximity_data():
    """Process Clear-Bible proximity data into synonyms"""
    proximity_data = load_proximity_tsv()

    for strongs_num, entry in strongs_entries():
        related = find_related_words(strongs_num, proximity_data, min_score=0.70)
        entry['related_words'] = {
            'synonyms': related
        }
```

#### 2.2 Extended Definition Processor
```python
def enhance_with_stepbible():
    """Add extended definitions from STEPBible"""
    stepbible_data = load_stepbible_lexicon()

    for strongs_num, entry in strongs_entries():
        if extended := stepbible_data.get(strongs_num):
            entry['extended_definition'] = {
                'gloss': extended['gloss'],
                'full_definition': extended['meaning'],
                'morphology': extended['morph']
            }
```

#### 2.3 Cross-Reference Processor
```python
def add_cross_references():
    """Add lexicon cross-references from OpenScriptures"""
    lexical_index = parse_lexical_index_xml()

    for strongs_num, entry in strongs_entries():
        if refs := lexical_index.get(strongs_num):
            entry['cross_references'] = refs
```

### Phase 3: File Generation

Follow existing pattern of separate data/code commits:

**Commit 1:** Code changes only
```bash
git add src/lib/strongs/
git commit -m "feat: add Strong's enhancement processors"
```

**Commit 2:** Data files only
```bash
git add bible/words/strongs/
git commit -m "data: enhance Strong's entries with synonyms and extended definitions (14,197 files)"
```

## Code Reusability

### Shared Components to Extract

Based on `src/lib/macula/`:

1. **Cache Management** (`src/util/cache.py`?)
   - Download and cache remote resources
   - Handle git clones
   - Check cache freshness

2. **TSV/CSV Parser** (`src/util/parsers.py`?)
   - Parse tab-delimited files
   - Handle Unicode properly
   - Type conversion utilities

3. **YAML Writer** (`src/util/file_helper.py` - already exists!)
   - Consistent YAML formatting
   - Directory structure creation
   - Batch file operations

4. **Logging Utilities** (pattern from macula_processor.py)
   - Timestamped logging
   - Progress tracking
   - Error reporting

## Resource Summary Table

| Resource | Type | License | Contains | Priority |
|----------|------|---------|----------|----------|
| Clear-Bible Proximity | TSV | CC BY 4.0 | Synonym scores, word relationships | High |
| STEPBible TBESG | TSV | CC BY 4.0 | Enhanced Greek definitions, morphology | High |
| STEPBible TBESH | TSV | CC BY 4.0 | Enhanced Hebrew definitions (BDB) | High |
| OpenScriptures HebrewLexicon | XML | CC BY 4.0 | Cross-refs, derivatives, corrections | Medium |
| OpenScriptures Strongs | XML/XHTML | CC BY 4.0 | Base Strong's data (current source) | Current |

## Next Steps

1. **Review & Approve:** Confirm which enhancements to implement
2. **Create Fetcher:** Build `strongs_fetcher.py` following macula pattern
3. **Create Processor:** Build `strongs_processor.py` with enhancement logic
4. **Test on Sample:** Process 10-20 entries to verify format
5. **Full Processing:** Generate all 14,197 enhanced entries
6. **Commit:** Separate code and data commits

## References

- Clear-Bible Macula Hebrew: https://github.com/Clear-Bible/macula-hebrew
- Clear-Bible Macula Greek: https://github.com/Clear-Bible/macula-greek
- STEPBible Data: https://github.com/STEPBible/STEPBible-Data
- OpenScriptures Strongs: https://github.com/openscriptures/strongs
- OpenScriptures Hebrew Lexicon: https://github.com/openscriptures/HebrewLexicon
