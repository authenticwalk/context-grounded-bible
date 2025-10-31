# Strong's Enhancement - Consolidated Implementation Plan

**Date:** 2025-10-30
**Purpose:** Clear implementation plan for enhancing Strong's concordance data

## Overview

We will update the existing `strongs-fetcher.py` script to create comprehensive Strong's entries with:
1. **Extended definitions** from STEPBible
2. **Synonyms/related words** from Clear-Bible Proximity
3. **Usage statistics** from morphhb (Hebrew only, for now)

**All data integrated into single YAML file:** `bible/words/strongs/{number}/{number}.strongs.yaml`

## Data Sources Summary

| Source | Type | What It Provides | License |
|--------|------|------------------|---------|
| **openscriptures/strongs** | Base lexicon | Current Strong's data | CC-BY-SA |
| **STEPBible TBESG** | Greek lexicon | Abbott-Smith definitions, morphology | CC BY 4.0 |
| **STEPBible TBESH** | Hebrew lexicon | Abridged BDB definitions, morphology | CC BY 4.0 |
| **STEPBible TFLSJ** | Greek lexicon | Full LSJ (etymology) | CC BY 4.0 |
| **Clear-Bible Proximity** | Similarity scores | Synonym relationships, cross-language | CC BY 4.0 |
| **morphhb** | Tagged Bible text | Hebrew usage statistics, examples | CC BY 4.0 |

## Enhanced YAML File Structure

```yaml
# bible/words/strongs/G0026/G0026.strongs.yaml
strongs_number: G0026
language: greek
lemma: ἀγάπη
transliteration: agápē
pronunciation: null  # Hebrew only

# CURRENT DATA (from openscriptures/strongs):
definition: love, i.e. affection or benevolence; specially a love-feast
kjv_usage: (feast of) charity(-ably), dear, love
derivation: from G25 (ἀγαπάω)

# NEW: EXTENDED DEFINITIONS (from STEPBible):
extended_definition:
  gloss: love
  brief_definition: "affection or benevolence"
  full_definition: "affection or benevolence; specially a love-feast..."
  morphology: N-F  # Noun-Feminine
  source: STEPBible/Abbott-Smith

# NEW: LSJ ETYMOLOGY (from STEPBible TFLSJ - Greek only):
etymology:
  classical_usage: "love, affection; in poets, sexual love..."
  derivation: "from ἀγαπάω, to love"
  cognates: ["ἀγαπητός", "ἀγάπησις"]
  source: STEPBible/LSJ

# NEW: SYNONYMS (from Clear-Bible Proximity):
related_words:
  synonyms:
    - strongs: G0025
      lemma: ἀγαπάω
      proximity: 0.95
      relationship: "verbal form"
    - strongs: G5368
      lemma: φιλέω
      proximity: 0.82
      relationship: "similar love concept"

  cross_language:
    - strongs: H0160
      lemma: אַהֲבָה
      proximity: 0.78
      language: hebrew
      note: "via LXX"

# NEW: USAGE STATISTICS (from morphhb - Hebrew only):
usage_statistics:
  total_occurrences: 3562
  books_appearing_in: 39
  most_frequent_book:
    name: Genesis
    count: 327

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
      translation: "And there was light"
      morph: "Vqw3ms"
      word_id: "01abc"
    - ref: "Ruth 1:1"
      text: "וַיְהִי בִּימֵי"
      translation: "And it was in the days"
      morph: "Vqw3ms"
      word_id: "08xeN"

# METADATA:
source: openscriptures/strongs
enhancements:
  - STEPBible/Abbott-Smith
  - STEPBible/LSJ
  - Clear-Bible/proximity
  - morphhb
license: CC-BY-SA + CC BY 4.0
```

## Implementation: Update strongs-fetcher.py

### Current Script Location
`./strongs-fetcher.py` (root directory)

### Proposed Changes

#### 1. Add New Import/Download Functions

```python
def download_stepbible_lexicons():
    """Download STEPBible TBESG, TBESH, TFLSJ"""
    base_url = "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"

    files = {
        'greek_brief': 'TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt',
        'hebrew_brief': 'TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt',
        'greek_full': 'TFLSJ  0-5624 - Translators Formatted full LSJ Bible lexicon - STEPBible.org CC BY.txt'
    }

    # Download and cache TSV files
    # Return parsed dictionaries keyed by Strong's number

def download_proximity_data():
    """Download Clear-Bible Proximity.tsv from macula repos"""
    hebrew_url = "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/sources/Clear/synonyms/Proximity.tsv"
    greek_url = "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/sources/Clear/synonyms/Proximity.tsv"

    # Download TSV files
    # Parse into dictionary: {strong_num: [(related_num, proximity_score), ...]}

def download_morphhb():
    """Download morphhb JSON from npm or GitHub"""
    # Option 1: npm install morphhb (if Node.js available)
    # Option 2: Clone repo and parse XML
    # Option 3: Use pre-generated JSON

    # Return parsed dictionary: {strong_num: usage_data}
```

#### 2. Update Main Generation Loop

```python
def generate_strongs_entries():
    """Generate enhanced Strong's YAML files"""

    # Load all data sources
    base_strongs = load_openscriptures_strongs()
    stepbible_greek = load_stepbible_greek()
    stepbible_hebrew = load_stepbible_hebrew()
    stepbible_lsj = load_stepbible_lsj()
    proximity_data = load_proximity_data()
    morphhb_data = load_morphhb_data()  # Hebrew only

    for strong_num, entry in base_strongs.items():
        enhanced_entry = {
            # Base data
            'strongs_number': entry['strongs_number'],
            'language': entry['language'],
            'lemma': entry['lemma'],
            'transliteration': entry['transliteration'],
            'pronunciation': entry.get('pronunciation'),
            'definition': entry['definition'],
            'kjv_usage': entry['kjv_usage'],
            'derivation': entry['derivation'],
        }

        # Add STEPBible extended definitions
        if strong_num in stepbible_greek or strong_num in stepbible_hebrew:
            enhanced_entry['extended_definition'] = get_stepbible_definition(strong_num)

        # Add LSJ etymology (Greek only)
        if entry['language'] == 'greek' and strong_num in stepbible_lsj:
            enhanced_entry['etymology'] = get_lsj_etymology(strong_num)

        # Add synonyms from proximity data
        if strong_num in proximity_data:
            enhanced_entry['related_words'] = get_related_words(strong_num, proximity_data)

        # Add usage statistics (Hebrew only, for now)
        if entry['language'] == 'hebrew' and strong_num in morphhb_data:
            enhanced_entry['usage_statistics'] = get_usage_stats(strong_num, morphhb_data)

        # Add metadata
        enhanced_entry['source'] = 'openscriptures/strongs'
        enhanced_entry['enhancements'] = list_enhancements(enhanced_entry)
        enhanced_entry['license'] = 'CC-BY-SA + CC BY 4.0'

        # Write YAML file
        write_strongs_yaml(strong_num, enhanced_entry)
```

## Processing Steps

### Step 1: Data Download & Caching

```bash
# Run once to download all sources
python strongs-fetcher.py --download-sources

# Downloads to cache:
/tmp/strongs_enhancement/
  ├── stepbible/
  │   ├── TBESG.tsv
  │   ├── TBESH.tsv
  │   └── TFLSJ.tsv
  ├── proximity/
  │   ├── hebrew_proximity.tsv
  │   └── greek_proximity.tsv
  └── morphhb/
      └── morphhb.json
```

### Step 2: Parse Data Sources

```python
# Parse TSV files
def parse_stepbible_tsv(filepath):
    """Parse STEPBible TSV into dictionary"""
    # Columns: eStrong, dStrong, uStrong, Greek/Hebrew, Transliteration, Morph, Gloss, Meaning
    # Return: {strongs_num: {gloss, morph, meaning}}

def parse_proximity_tsv(filepath):
    """Parse Proximity TSV into relationships"""
    # Columns: StrongNumberX1, StrongNumberX2, Distance
    # Return: {strongs_num: [(related_num, score), ...]}

def parse_morphhb_json(filepath):
    """Parse morphhb JSON into usage statistics"""
    # Structure: {book: [chapter: [verse: [word]]]}
    # Process: Count occurrences by Strong's number
    # Return: {strongs_num: {total, examples, morph_dist}}
```

### Step 3: Generate Enhanced Files

```bash
# Generate all Strong's entries
python strongs-fetcher.py --generate-all

# Or by language
python strongs-fetcher.py --generate-hebrew
python strongs-fetcher.py --generate-greek

# Or single entry for testing
python strongs-fetcher.py --generate H1961
```

## File Organization

```
bible/words/strongs/
├── G0001/
│   └── G0001.strongs.yaml  # Enhanced with all data
├── G0026/
│   └── G0026.strongs.yaml  # Enhanced with all data
├── H0001/
│   └── H0001.strongs.yaml  # Enhanced with all data + usage stats
└── H1961/
    └── H1961.strongs.yaml  # Enhanced with all data + usage stats
```

**Note:** All data in single file per Strong's number (not separate files)

## Data Processing Notes

### STEPBible TSV Format

**TBESG (Greek):**
```tsv
eStrong	dStrong	uStrong	Greek	Transliteration	Morph	Gloss	Meaning
G0026	G0026	G0026	ἀγάπη	agápē	N-F	love	affection or benevolence; specially a love-feast...
```

**TBESH (Hebrew):**
```tsv
eStrong#	dStrong#	uStrong#	Hebrew	Transliteration	Morph	Gloss	Meaning
H1961	H1961	H1961	הָיָה	hāyāh	V	to be	to exist, i.e. be or become, come to pass...
```

**TFLSJ (Greek):**
```tsv
Strong	Greek	Transliteration	LSJ_Entry
G0026	ἀγάπη	agápē	love, affection; in poets, sexual love...
```

### Proximity TSV Format

```tsv
StrongNumberX1	StrongNumberX2	Distance
G0026	G0025	0.95123456
G0026	G5368	0.82345678
G0026	H0160	0.78123456
```

### morphhb JSON Format

```json
{
  "Genesis": [
    [  // Chapter 1
      [  // Verse 1
        ["בְּרֵאשִׁית", "b/7225", "HR/Ncfsa"],
        ["בָּרָא", "1254", "HVqp3ms"],
        ["אֱלֹהִים", "430", "HNcmpa"]
      ]
    ]
  ]
}
```

## Processing Algorithms

### Synonym Extraction (from Proximity)

```python
def extract_synonyms(strongs_num, proximity_data, min_score=0.70):
    """Extract related words above threshold"""

    related = []
    for (num1, num2, score) in proximity_data:
        if score < min_score:
            continue

        if num1 == strongs_num:
            related.append({
                'strongs': num2,
                'proximity': score,
                'language': get_language(num2)
            })
        elif num2 == strongs_num:
            related.append({
                'strongs': num1,
                'proximity': score,
                'language': get_language(num1)
            })

    # Sort by proximity (highest first)
    related.sort(key=lambda x: x['proximity'], reverse=True)

    # Separate same-language from cross-language
    same_lang = [r for r in related if r['language'] == get_language(strongs_num)]
    cross_lang = [r for r in related if r['language'] != get_language(strongs_num)]

    return {
        'synonyms': same_lang[:10],  # Top 10
        'cross_language': cross_lang[:5]  # Top 5
    }
```

### Usage Statistics (from morphhb)

```python
def extract_usage_stats(strongs_num, morphhb_data):
    """Calculate usage statistics for Hebrew word"""

    occurrences = []
    morph_counts = defaultdict(int)
    book_counts = defaultdict(int)

    for book, chapters in morphhb_data.items():
        for ch_num, chapter in enumerate(chapters, 1):
            for v_num, verse in enumerate(chapter, 1):
                for word in verse:
                    text, lemma, morph = word

                    # Extract Strong's number from lemma (may have prefixes)
                    strong = extract_strongs_from_lemma(lemma)

                    if strong == strongs_num:
                        occurrences.append({
                            'ref': f"{book} {ch_num}:{v_num}",
                            'text': text,
                            'morph': morph
                        })
                        morph_counts[morph] += 1
                        book_counts[book] += 1

    # Calculate distribution
    total = len(occurrences)
    morph_dist = [
        {
            'morph': morph,
            'description': decode_morph(morph),
            'count': count,
            'percentage': round(count / total * 100, 1)
        }
        for morph, count in sorted(morph_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    # Get examples (5-10 representative verses)
    examples = select_example_verses(occurrences, count=5)

    return {
        'total_occurrences': total,
        'books_appearing_in': len(book_counts),
        'most_frequent_book': {
            'name': max(book_counts, key=book_counts.get),
            'count': max(book_counts.values())
        },
        'morphological_distribution': morph_dist,
        'example_verses': examples
    }
```

## Git Commit Strategy

Following project guidelines (separate data and code commits):

**Commit 1: Code Changes**
```bash
git add strongs-fetcher.py
git add src/lib/stepbible/  # If we create helper modules
git add src/lib/morphhb/    # If we create helper modules
git commit -m "feat: enhance Strong's fetcher with STEPBible, proximity, and morphhb data"
```

**Commit 2: Data Changes**
```bash
git add bible/words/strongs/
git commit -m "data: enhance Strong's entries with definitions, synonyms, and usage (14,197 files)"
```

## Testing Strategy

### Test on Sample Entries

```bash
# Test a few well-known words first
python strongs-fetcher.py --generate H1961  # Hebrew: "to be"
python strongs-fetcher.py --generate G0026  # Greek: "love"
python strongs-fetcher.py --generate H0430  # Hebrew: "God"
python strongs-fetcher.py --generate G2316  # Greek: "God"

# Verify:
# 1. All fields present
# 2. Data quality (definitions make sense)
# 3. Synonyms are relevant
# 4. Usage statistics accurate (for Hebrew)
# 5. YAML format valid
```

### Validation Checks

```python
def validate_enhanced_entry(entry):
    """Validate enhanced Strong's entry"""

    # Required base fields
    assert 'strongs_number' in entry
    assert 'language' in entry
    assert 'definition' in entry

    # Enhancement fields (if applicable)
    if 'extended_definition' in entry:
        assert 'gloss' in entry['extended_definition']
        assert 'source' in entry['extended_definition']

    if 'related_words' in entry:
        for syn in entry['related_words'].get('synonyms', []):
            assert 0 <= syn['proximity'] <= 1
            assert syn['strongs'].startswith(('H', 'G'))

    if 'usage_statistics' in entry:
        assert entry['usage_statistics']['total_occurrences'] > 0
        assert len(entry['usage_statistics']['example_verses']) > 0

    return True
```

## Timeline Estimate

**Phase 1: Implementation** (Update strongs-fetcher.py)
- Download functions: 2-3 hours
- Parser functions: 3-4 hours
- Integration logic: 2-3 hours
- **Total:** ~8-10 hours of development

**Phase 2: Testing**
- Sample testing: 1 hour
- Validation: 1 hour
- Bug fixes: 1-2 hours
- **Total:** ~3-4 hours

**Phase 3: Full Generation**
- Run time: 30-60 minutes (14,197 entries)
- Verification: 30 minutes
- **Total:** ~1-2 hours

**Grand Total:** ~12-16 hours of work

## Success Criteria

✅ **All 14,197 Strong's entries enhanced with:**
1. Extended definitions from STEPBible (where available)
2. LSJ etymology for Greek words (where available)
3. Synonym relationships from Clear-Bible Proximity
4. Usage statistics from morphhb (Hebrew only)

✅ **Data Quality:**
- Valid YAML format
- All fields properly typed
- No missing required data
- Synonyms filtered by relevance (proximity > 0.70)
- Usage examples representative

✅ **Attribution:**
- All sources credited
- Licenses properly noted
- CC BY 4.0 compliance

## Next Steps

1. **Review this plan** - Confirm approach
2. **Update strongs-fetcher.py** - Implement enhancements
3. **Test on samples** - Verify output
4. **Run full generation** - Process all entries
5. **Commit changes** - Code first, then data

---

**This is the master implementation plan for Strong's enhancement project.**
