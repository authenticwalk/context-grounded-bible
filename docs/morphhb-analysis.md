# OpenScriptures Hebrew Bible (morphhb) - Deep Dive Analysis

## Executive Summary

The morphhb repository is a **goldmine** of structured Hebrew Bible data with full morphological analysis. It contains the Westminster Leningrad Codex (WLC) with:
- Strong's numbers for every word
- Complete morphological parsing
- Unique immutable word IDs
- Creative Commons Attribution 4.0 license (open source!)

## Repository Overview

**Repository**: https://github.com/openscriptures/morphhb
**License**: CC BY 4.0 (lemma/morphology), Public Domain (WLC text)
**Size**: ~28MB (9.4MB pre-compiled JSON)
**Coverage**: Entire Hebrew Bible (39 books)

## Data Structure

### Raw XML Format (in `wlc/` directory)

```xml
<verse osisID="Gen.1.1">
  <w lemma="b/7225" n="1.0" morph="HR/Ncfsa" id="01xeN">בְּ/רֵאשִׁ֖ית</w>
  <w lemma="1254 a" morph="HVqp3ms" id="01Nvk">בָּרָ֣א</w>
  <w lemma="430" n="1" morph="HNcmpa" id="01TyA">אֱלֹהִ֑ים</w>
  <w lemma="853" morph="HTo" id="01vuQ">אֵ֥ת</w>
  <w lemma="d/8064" n="0.0" morph="HTd/Ncmpa" id="01TSc">הַ/שָּׁמַ֖יִם</w>
  <w lemma="c/853" morph="HC/To" id="01k5P">וְ/אֵ֥ת</w>
  <w lemma="d/776" n="0" morph="HTd/Ncbsa" id="01nPh">הָ/אָֽרֶץ</w>
</verse>
```

**Each word contains**:
- `lemma`: Augmented Strong's number (e.g., "b/7225" = prefix + number)
- `morph`: Morphological code (e.g., "HR/Ncfsa")
- `id`: Unique immutable identifier (e.g., "01xeN")
- Text content: Hebrew word with vowel points and cantillation marks

### Pre-compiled JSON Format (`index.js`)

```javascript
{
  "Genesis": [
    [  // Chapter 1
      [  // Verse 1
        ["ב/ראשית", "Hb/H7225", "HR/Ncfsa"],  // Word 1
        ["ברא", "H1254", "HVqp3ms"],           // Word 2
        ["אלהים", "H430", "HNcmpa"]           // Word 3
        // ... more words
      ]
      // ... more verses
    ]
    // ... more chapters
  ]
  // ... more books
}
```

**Structure**: `[wordText, strongsNumber, morphologyCode]`

## Morphology Codes Explained

### Format: `H + POS + features`

Example: `HVqp3ms`
- `H` = Hebrew (prefix)
- `V` = Verb (part of speech)
- `qp` = Qal, Perfect (stem + conjugation)
- `3ms` = 3rd person, masculine, singular

### Part of Speech Codes:
- `N` = Noun
- `V` = Verb
- `A` = Adjective
- `R` = Preposition
- `C` = Conjunction
- `T` = Particle
- `d` = Definite article

### Verb Features:
- **Stem (Binyan)**: `q`=Qal, `N`=Niphal, `p`=Piel, `P`=Pual, `h`=Hiphil, `H`=Hophal, `t`=Hithpael
- **Tense**: `p`=Perfect, `i`=Imperfect, `w`=Waw consecutive, `v`=Imperative, `r`=Participle
- **Person**: `1`, `2`, `3`
- **Gender**: `m`=Masculine, `f`=Feminine, `c`=Common
- **Number**: `s`=Singular, `p`=Plural, `d`=Dual

### Noun Features:
- **State**: `a`=Absolute, `c`=Construct
- **Gender**: `m`/`f`/`c`
- **Number**: `s`/`p`/`d`

### Example Breakdown:

**Word**: `בְּרֵאשִׁ֖ית` (bereshit, "in the beginning")
- **Strong's**: `b/7225` (preposition ב + word 7225)
- **Morph**: `HR/Ncfsa`
  - `H` = Hebrew
  - `R` = Preposition (ב)
  - `/`
  - `N` = Noun (רֵאשִׁית)
  - `c` = Construct state
  - `f` = Feminine
  - `s` = Singular
  - `a` = Absolute

## Comparison: morphhb vs ebible Corpus

### ebible Corpus Approach (reference)

The ebible corpus approach (from `feat/download-ebible` branch) involved:
1. Cloning the repository to `/tmp`
2. Extracting translations from USFX XML files
3. Parsing verse-by-verse for multiple translations
4. Caching results locally

**ebible provided**:
- ✅ Multiple translations (200+ languages)
- ✅ Modern translations (NIV, ESV, etc.)
- ❌ No morphological data
- ❌ No Strong's numbers
- ❌ No original language text

### morphhb Repository Approach

**morphhb provides**:
- ✅ Original Hebrew text (Westminster Leningrad Codex)
- ✅ Complete morphological parsing
- ✅ Strong's numbers (augmented)
- ✅ Unique word IDs for textual criticism
- ✅ Pre-compiled JSON (9.4MB, ready to use!)
- ❌ Only Hebrew Bible (OT only, no NT)
- ❌ No English translations

## Key Advantages of morphhb

### 1. **Structured Data Ready to Use**
- Pre-compiled JSON available (`index.js`)
- No parsing needed - just require/import
- 9.4MB file covers entire Hebrew Bible
- Published to npm as `morphhb` package

### 2. **Rich Linguistic Data**
- Full morphological analysis
- Part of speech tagging
- Verb conjugations (stem, tense, person, gender, number)
- Noun states (absolute vs construct)
- Prefixes/suffixes separated (e.g., ב/רֵאשִׁית)

### 3. **Augmented Strong's Numbers**
- Includes prefixes (b/, d/, c/, etc.)
- More precise than standard Strong's
- Maps to root lemmas

### 4. **Unique Word IDs**
- Every word has immutable ID (e.g., "01xeN")
- Enables data association across different tools
- Facilitates textual criticism
- First 2 digits = KJV book number

### 5. **Open Source & Well-Maintained**
- CC BY 4.0 license (can be used freely with attribution)
- Regular updates (last release: 2017.12.10 - full morphology)
- Based on Westminster Leningrad Codex (scholarly standard)
- Active community

### 6. **Multiple Export Options**
- XML (OSIS format)
- JSON (via Perl/Python scripts)
- npm package (JavaScript)
- Docker containerization available

## Integration Strategy for Context-Grounded Bible

### Phase 1: Direct JSON Usage (Recommended First Step)

**Approach**: Use the pre-compiled `index.js` directly

```python
# Copy morphhb to our project
cp /tmp/morphhb/index.js ./data/morphhb.json

# Or clone as submodule
git submodule add https://github.com/openscriptures/morphhb.git data/morphhb
```

**Benefits**:
- Instant access to all data
- No parsing required
- Can query any verse immediately
- Only 9.4MB storage

### Phase 2: Create Verse-Level YAML Files

**Transform morphhb data into our project structure**:

```
./bible/GEN/1/1/GEN-1-1-hebrew-morphology.yaml
```

**Example YAML output**:

```yaml
reference: GEN 1:1
text: בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ
translation: "In the beginning God created the heavens and the earth"
words:
  - position: 1
    text: "בְּרֵאשִׁ֖ית"
    normalized: "ב/ראשית"
    strongs: "b/7225"
    strongs_full: "Hb/H7225"
    morph_code: "HR/Ncfsa"
    morphology:
      prefix: "ב"
      prefix_meaning: "in, with, by"
      word: "רֵאשִׁית"
      word_meaning: "beginning, first"
      pos: "noun"
      state: "construct"
      gender: "feminine"
      number: "singular"
    id: "01xeN"

  - position: 2
    text: "בָּרָ֣א"
    strongs: "1254a"
    strongs_full: "H1254a"
    morph_code: "HVqp3ms"
    morphology:
      pos: "verb"
      stem: "qal"
      conjugation: "perfect"
      person: "third"
      gender: "masculine"
      number: "singular"
    id: "01Nvk"
    meaning: "created"
```

### Phase 3: Create Extraction Tool

**New skill**: `hebrew-morphology`

```bash
# Extract morphological data for a verse
python3 .claude/skills/hebrew-morphology/extract_morphology.py "GEN 1:1"

# Batch extract entire books
python3 .claude/skills/hebrew-morphology/batch_extract.py --book GEN

# Generate all OT morphology data
python3 .claude/skills/hebrew-morphology/generate_all.py
```

### Phase 4: Integrate with lexicon-bible Skill

**Enhance our existing lexicon-bible skill**:
- Add morphhb as data source for Hebrew verses
- Fallback to BibleHub if morphhb unavailable
- Compare morphhb morphology vs BibleHub morphology
- Cross-reference Strong's numbers

## Data We Can Extract

### 1. **Word-Level Analysis**
- Hebrew text (with vowel points)
- Normalized text (without vowel points option)
- Strong's numbers (augmented with prefixes)
- Complete morphological parsing
- Unique word IDs

### 2. **Morphological Statistics**
- Verb frequency by stem (Qal, Niphal, etc.)
- Noun state distribution (absolute vs construct)
- Gender/number patterns
- Prefix/suffix analysis

### 3. **Lemma Database**
- All Hebrew lemmas with Strong's numbers
- Morphological variants of each lemma
- Frequency counts per lemma

### 4. **Cross-Reference Data**
- Link verses to specific word IDs
- Track word usage across Bible
- Concordance generation

### 5. **Textual Criticism Data**
- Unique IDs enable comparison with other codices
- Variant tracking
- Manuscript comparison

## Practical Use Cases

### For Bible Translation
- **Verb analysis**: Identify stem, tense, person, gender, number
- **Noun states**: Understand construct chains
- **Prefix meanings**: Correctly translate prepositions
- **Context**: See how words are used throughout Scripture

### For AI Grounding
- **Training data**: Rich morphological features
- **Disambiguation**: Morphology helps disambiguate meanings
- **Contextual understanding**: Grammatical role clarifies meaning
- **Cross-referencing**: Link related verses by lemma

### For Scholarly Research
- **Linguistic analysis**: Study Hebrew grammar patterns
- **Frequency studies**: Most common stems, forms
- **Textual criticism**: Compare manuscripts via word IDs
- **Concordance work**: Track word usage

## Implementation Recommendation

### Recommended Approach:

**1. Add morphhb as a git submodule** (preserves attribution, stays updated)
```bash
cd /home/user/context-grounded-bible
git submodule add https://github.com/openscriptures/morphhb.git data/morphhb
```

**2. Create Python extraction tool**
- Read from `data/morphhb/index.js` (or convert to Python dict)
- Generate YAML files per verse
- Follow our project structure: `bible/{book}/{chapter}/{verse}/`

**3. Create morphology parser module**
- Decode morphology codes (HVqp3ms → verb, qal, perfect, 3ms)
- Map Strong's numbers to meanings
- Format for human readability

**4. Integrate with existing skills**
- Enhance `lexicon-bible` to use morphhb data for Hebrew
- Compare morphhb vs BibleHub morphology
- Prefer morphhb (more accurate, open source)

**5. Generate batch data**
- Extract all Genesis for testing
- Generate full OT if desired
- Store in `bible/` directory structure

## Next Steps

1. ✅ Clone morphhb to `/tmp` (DONE)
2. ✅ Analyze structure and data format (DONE)
3. ⏭️ Copy morphhb to project (git submodule)
4. ⏭️ Create Python morphology parser
5. ⏭️ Build extraction tool
6. ⏭️ Generate sample data (Genesis 1)
7. ⏭️ Integrate with lexicon-bible skill
8. ⏭️ Test and validate

## Licensing & Attribution

**morphhb License**: Creative Commons Attribution 4.0 International

**Required Attribution**:
"Hebrew text and morphology from Open Scriptures Hebrew Bible (CC BY 4.0)"

**Link**: https://github.com/openscriptures/morphhb

This is compatible with our MIT-licensed project!

## Conclusion

The morphhb repository is **superior to ebible for Hebrew lexical data**:
- ✅ Open source (CC BY 4.0)
- ✅ Complete morphological analysis
- ✅ Strong's numbers included
- ✅ Pre-compiled JSON (ready to use!)
- ✅ Scholarly standard (Westminster Leningrad Codex)
- ✅ Unique word IDs for advanced features
- ✅ Active maintenance

**Recommendation**: Integrate morphhb immediately to enhance our Hebrew Bible analysis capabilities.

The ebible corpus remains valuable for **translations** (200+ languages), while morphhb provides **original language analysis**. Both are complementary!
