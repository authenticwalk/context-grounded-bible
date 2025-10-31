# morphhb and macula-hebrew: Relationship Analysis

**Date:** 2025-10-30
**Question:** Do we already have morphhb data through macula-hebrew?

## Answer: YES ✅

**macula-hebrew DOES include morphhb data**, but it's transformed and enhanced.

## What We Found

### 1. Confirmation from macula-hebrew README

**Quote from README:**
> "Morphology data — Sourced from the **Open Scriptures Hebrew Bible project** on Github"

**Location in repository:**
- `sources/OpenScriptures/xml/` - Contains all 39 OT books + VerseMap.xml
- These are the same morphhb files

### 2. How macula-hebrew Uses morphhb

**macula-hebrew transforms morphhb by:**
1. **Taking morphhb as a source** (raw OSIS XML)
2. **Adding additional layers:**
   - Syntax trees from Groves Center
   - Word sense data from UBS MARBLE/SDBH
   - Semantic roles
   - Participant referents
   - Cherith glosses
3. **Providing in multiple formats:**
   - `sources/OpenScriptures/xml` - Original morphhb XML
   - `WLC/nodes` - Nested node format with syntax trees
   - `WLC/lowfat` - Query-friendly format
   - `WLC/tsv` - Single TSV file with all data

### 3. Comparison of Data Formats

#### morphhb (raw):
```xml
<w lemma="c/1961" morph="HC/Vqw3ms" id="08xeN">וַ/יְהִ֗י</w>
```

#### macula-hebrew (transformed):
```xml
<m n="080010010012" morph="Vqw3ms" lang="H" lemma="1961"
   pos="verb" stem="qal" type="wayyiqtol"
   person="third" gender="masculine" number="singular"
   after=" ">יְהִ֗י</m>
```

**Differences:**
- **Prefix handling:** macula splits prefixes into separate elements
- **Attributes:** macula expands morph code into individual attributes
- **Word IDs:** Different format (`n="080010010012"` vs `id="08xeN"`)
- **Additional data:** macula adds pos, stem, type, person, gender, number as separate fields

### 4. Our Existing macula Infrastructure

**We already have:**
- ✅ `src/lib/macula/macula_fetcher.py` - Downloads macula-hebrew repo
- ✅ `src/lib/macula/macula_processor.py` - Processes macula data
- ✅ Cache location: `/tmp/macula/hebrew/`
- ✅ Downloads: `WLC/lowfat` directory (XML files)

**What we're currently using macula for:**
- Proximity data (synonyms) from `sources/Clear/synonyms/Proximity.tsv`
- Not currently processing the morphhb/OpenScriptures data

## Key Question: Should We Use morphhb or macula-hebrew?

### Option 1: Use morphhb Directly

**Source:** https://github.com/openscriptures/morphhb
**Format:** OSIS XML or JSON (via npm)

**Pros:**
- ✅ Original source, most authoritative
- ✅ Simple XML format
- ✅ Available as JSON via npm (easy to process)
- ✅ Smaller download (~10-15 MB)
- ✅ Unique immutable word IDs (`08xeN`)

**Cons:**
- ⚠️ Morphology codes need parsing (`HC/Vqw3ms`)
- ⚠️ Prefixes encoded in lemma (`c/1961`)

### Option 2: Use macula-hebrew

**Source:** https://github.com/Clear-Bible/macula-hebrew
**Format:** Multiple (nodes, lowfat, TSV)

**Pros:**
- ✅ Already downloaded via our fetcher
- ✅ Morphology expanded into attributes
- ✅ Additional linguistic layers (syntax trees, semantic roles)
- ✅ TSV format available (single file)
- ✅ Prefixes handled separately

**Cons:**
- ⚠️ Larger repo (~50+ MB)
- ⚠️ More complex structure
- ⚠️ Different word ID system
- ⚠️ TSV is Git LFS (large file, harder to fetch)

### Option 3: Use Both

**morphhb for:**
- Immutable word IDs (for cross-referencing)
- Simple format for basic lemma/morph extraction

**macula-hebrew for:**
- Expanded morphology attributes
- Syntax trees (if we add syntactic analysis later)
- Semantic domains from SDBH
- Already part of our infrastructure

## Recommendations

### For Our Current Strong's Enhancement Project:

**Use morphhb directly** (Option 1)

**Reasons:**
1. **Simpler for our use case** - We just need:
   - Strong's number → occurrence count
   - Strong's number → example verses
   - Strong's number → morphology patterns

2. **Easier to process:**
   - JSON format via npm: `npm install morphhb`
   - Small, focused dataset
   - Clear structure: `[book][chapter][verse][word]`

3. **Better word IDs:**
   - Immutable IDs (`08xeN`) are better for long-term referencing
   - macula's IDs (`080010010012`) are just positional

4. **We don't need the extras:**
   - Syntax trees - not needed for lexicon
   - Semantic roles - not needed for Strong's enhancement
   - Multiple formats - adds complexity

### Keep macula-hebrew for:

**Proximity/synonym data** (what we're already using it for)
- Clear-Bible Proximity.tsv
- Already have the fetcher/processor

**Future enhancements** (if we expand beyond lexicons):
- Syntax tree analysis
- Semantic role labeling
- Cross-reference with SDBH

## Implementation Plan

### Phase 1: Add morphhb Processing (Separate from macula)

**New script:** `src/lib/morphhb/morphhb_fetcher.py`

```python
# Download morphhb JSON from npm or GitHub
# Simpler, lighter than macula approach
MORPHHB_NPM = "morphhb"
MORPHHB_REPO = "https://github.com/openscriptures/morphhb.git"
```

**New script:** `src/lib/morphhb/morphhb_processor.py`

```python
# Process morphhb JSON
# Extract usage statistics by Strong's number
# Generate .usage.yaml files
```

**Why separate from macula:**
- Cleaner separation of concerns
- macula = proximity data
- morphhb = usage statistics
- Easier to maintain

### Phase 2: Integrate with Strong's Enhancement

**Output:** `bible/words/strongs/H{number}/H{number}.usage.yaml`

```yaml
strongs_number: H1961
language: hebrew
source: morphhb
license: CC BY 4.0

statistics:
  total_occurrences: 3562
  books: 39

examples:
  - ref: "Genesis 1:3"
    text: "וַיְהִי אוֹר"
    word_id: "01abc"
    morph: "Vqw3ms"
```

### Optionally: Use macula Later

If we want the expanded morphology attributes later:
- We already have the infrastructure
- Can add macula-hebrew processing alongside morphhb
- But for now, morphhb is simpler and sufficient

## Summary

**Question:** Do we already have morphhb through macula-hebrew?
**Answer:** YES - macula-hebrew includes morphhb in `sources/OpenScriptures/xml`

**Question:** Should we use it from there?
**Answer:** NO - Better to use morphhb directly

**Why:**
- Simpler format (JSON available)
- Smaller download
- Better word IDs
- Don't need macula's additional complexity for our use case
- macula is better used for what we're already using it for (proximity data)

**Action Items:**
1. ✅ Keep macula-fetcher for proximity data (already done)
2. ✅ Add separate morphhb fetcher/processor (new)
3. ✅ Use morphhb for usage statistics
4. ⚠️ Keep macula available for future enhancements

**Verdict:** We have access to the data via macula, but should use morphhb directly for cleaner, simpler processing.
