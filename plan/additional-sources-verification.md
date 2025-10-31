# Additional Sources Verification

**Date:** 2025-10-30
**Purpose:** Verify four additional sources suggested for Strong's enhancement

## Summary

| Source | Available? | License | Format | Recommendation |
|--------|-----------|---------|--------|----------------|
| OpenScriptures BDB | ✅ Yes | CC BY 4.0 | XML | ⚠️ ALREADY COVERED |
| unfoldingWord Lexicons | ✅ Yes | CC BY-SA 4.0 | Markdown | ✅ GOOD ALTERNATIVE |
| Thayer's XML | ❌ Not Clean | - | - | ❌ USE ABBOTT-SMITH |
| LSJ Greek Lexicon | ✅ Yes | CC BY-SA, CC BY 4.0 | XML, TSV | ✅ ALREADY IN STEPBIBLE |

## Detailed Findings

### 1. OpenScriptures BDB (Brown-Driver-Briggs) ✅

**Status:** Already identified and documented

**Source:** https://github.com/openscriptures/HebrewLexicon
**License:** CC BY 4.0 (public domain text)
**Format:** XML

**Files:**
- `BrownDriverBriggs.xml` - Complete BDB content
- `HebrewStrong.xml` - Strong's Hebrew with corrections
- `LexicalIndex.xml` - Cross-reference hub (BDB ↔ Strong's ↔ TWOT)

**What it provides:**
- Full BDB definitions for Hebrew/Aramaic
- Strong's number mappings
- TWOT (Theological Wordbook of OT) cross-references
- Derivative/etymology information
- Part of speech
- Scripture references

**Why we already have this covered:**
- **STEPBible TBESH** uses "Abridged BDB" - same source, more accessible format (TSV vs XML)
- **eliranwong/unabridged-BDB-Hebrew-lexicon** - Full BDB in JSON/CSV format

**Verdict:** ⚠️ **Already covered by STEPBible TBESH**
- STEPBible's abridged BDB is easier to parse (TSV format)
- If we want FULL unabridged BDB, use eliranwong's JSON/CSV version
- OpenScriptures XML is comprehensive but more complex to parse

### 2. unfoldingWord Resources ✅

**Important Clarification:** unfoldingWord has TWO different resources:

#### a) unfoldingWord Translation Words (UTW) ❌ NOT a lexicon
**Source:** https://github.com/unfoldingWord/translationWords
**License:** CC BY-SA 4.0
**Format:** Markdown

**What it is:**
- Concept-based articles (NOT word-by-word definitions)
- Organized by topics: key terms (kt/), other terms (other/), names (names/)
- Explains biblical concepts for translators
- Includes Strong's references but is NOT a replacement for lexicons

**Example:** Article on "prophet" explains the concept, not lexical definition of Hebrew נָבִיא

**Verdict:** ❌ **Not suitable for our purposes** - This is for translation concepts, not lexical data

#### b) unfoldingWord Lexicons (UHAL & UGL) ✅ GOOD ALTERNATIVE

**UHAL - Hebrew/Aramaic Lexicon**
- **Source:** https://git.door43.org/unfoldingWord/en_uhal
- **License:** CC BY-SA 4.0
- **Format:** Markdown (one file per Strong's number)
- **Path structure:** `/content/{Strong's-ID}.md`

**Features:**
- Strong's numbers (modified/consolidated)
- TWOT numbers (reference only)
- Based on multiple sources
- Openly licensed

**UGL - Greek Lexicon**
- **Source:** https://git.door43.org/unfoldingWord/en_ugl
- **License:** CC BY-SA 4.0
- **Format:** Markdown (one file per Strong's number)
- **Path structure:** `/content/G{number}/01.md`

**Features:**
- Based on Abbott-Smith lexicon (first version)
- Strong's number organization
- Linked to UGNT (Unlocked Greek New Testament)

**Pros:**
- ✅ CC BY-SA 4.0 (compatible)
- ✅ Strong's number indexed
- ✅ Markdown = easy to parse
- ✅ Based on Abbott-Smith (same as STEPBible)

**Cons:**
- ⚠️ Work in progress (especially UHAL)
- ⚠️ Markdown format requires conversion
- ⚠️ Door43 infrastructure (not GitHub)
- ⚠️ Less comprehensive than STEPBible

**Verdict:** ✅ **Good alternative to STEPBible, but STEPBible is better**
- STEPBible has more complete data in easier format (TSV)
- unfoldingWord is good for specific Strong's number lookups
- Could use as supplemental source if STEPBible missing entries

### 3. Thayer's Greek Lexicon XML ❌

**Searched for:** Clean, structured Thayer's XML

**What I found:**
- **MorphGNT Strong's XML:** ✅ Available (github.com/morphgnt/strongs-dictionary-xml)
  - License: CC0 (public domain)
  - Format: XML with actual Greek, SBL transliterations
  - BUT: This is Strong's dictionary, NOT Thayer's

- **Thayer's itself:** ❌ No clean structured data found
  - Public domain (1889) via Internet Archive (scanned PDFs)
  - Some web tools reference Thayer's but no downloadable structured data
  - OpenScriptures may have Thayer's XML but couldn't confirm

**Why we don't need it:**
- **Abbott-Smith is superior** - more modern, same public domain status
- **STEPBible TBESG** already uses Abbott-Smith + LSJ
- **Dodson Greek Lexicon** available if we need alternatives (public domain, XML/CSV)

**Verdict:** ❌ **Use Abbott-Smith instead (via STEPBible)**
- Abbott-Smith (1922) is newer than Thayer's (1889)
- Abbott-Smith is described as "best quality lexicon in public domain"
- Already in STEPBible TBESG in easy TSV format

### 4. LSJ Greek Lexicon (Liddell-Scott-Jones) ✅

**Multiple sources available:**

#### a) STEPBible TFLSJ ✅ RECOMMENDED
**Source:** https://github.com/STEPBible/STEPBible-Data
**File:** `Lexicons/TFLSJ 0-5624 - Translators Formatted full LSJ Bible lexicon - STEPBible.org CC BY.txt`
**License:** CC BY 4.0
**Format:** Tab-delimited UTF-8

**Features:**
- Full LSJ entries for ALL Bible words (NT, LXX, Apocrypha, variants)
- Up to G5624 (covers all Biblical Greek)
- Formatted for easy reading by Tyndale House
- Extended Strong's compatible
- TSV format = easy to parse

**Pros:**
- ✅ Biblical Greek focus (not all Classical Greek)
- ✅ Already processed for Bible study
- ✅ Easy format (TSV)
- ✅ Same source as TBESG (STEPBible)

#### b) Perseus Digital Library ✅ COMPREHENSIVE
**Source:** https://github.com/PerseusDL/lexica
**Path:** `CTS_XML_TEI/perseus/pdllex/grc/lsj/`
**License:** CC-BY-SA (Perseus digitization)
**Format:** TEI XML

**Features:**
- Complete LSJ lexicon
- Multiple XML files
- TEI (Text Encoding Initiative) standard
- Authoritative scholarly digitization

**Pros:**
- ✅ Complete, authoritative
- ✅ Open license

**Cons:**
- ⚠️ ALL Classical Greek (not just Biblical)
- ⚠️ Complex TEI XML structure
- ⚠️ Much larger dataset than needed
- ⚠️ Not keyed to Strong's numbers

#### c) Giuseppe Celano's Unicode Version
**Source:** https://github.com/gcelano/LSJ_GreekUnicode
**Format:** XML with Unicode Greek (not beta-code)

**Features:**
- Same Perseus data, converted to proper Unicode
- Easier to process than beta-code

**Why LSJ matters:**
- LSJ is THE authoritative Classical Greek lexicon
- Contains etymologies not in NT-focused lexicons
- Good for understanding word origins and classical usage
- Helps with LXX translation patterns

**Verdict:** ✅ **Use STEPBible TFLSJ - best option**
- Already filtered for Biblical words only
- TSV format much easier than TEI XML
- Same repository as TBESG/TBESH
- If we need full classical LSJ later, Perseus is available

## Updated Recommendations

### For Extended Definitions in `strongs-fetcher.py`:

**Primary Sources (High Priority):**
1. ✅ **STEPBible TBESG** (Greek) - Abbott-Smith + LSJ
2. ✅ **STEPBible TBESH** (Hebrew) - Abridged BDB
3. ✅ **STEPBible TFLSJ** (Greek) - Full LSJ for Bible words

**Supplemental Sources (Optional):**
4. ⚠️ **eliranwong BDB** (Hebrew) - If we want unabridged BDB (vs abridged in STEPBible)
5. ⚠️ **unfoldingWord UHAL/UGL** - As backup if STEPBible missing entries
6. ⚠️ **MorphGNT Strong's XML** - Already have this (openscriptures), but MorphGNT has cleaner XML with SBL transliterations

**Not Recommended:**
- ❌ OpenScriptures BDB XML - Use STEPBible TSV or eliranwong CSV instead
- ❌ Thayer's - Use Abbott-Smith (in STEPBible) instead
- ❌ Perseus LSJ XML - Use STEPBible TFLSJ instead (unless need classical usage)
- ❌ Translation Words - Not a lexicon (concept articles)

### Why STEPBible is the Winner

**Single source for everything:**
- TBESG (Greek brief definitions)
- TBESH (Hebrew brief definitions)
- TFLSJ (Greek full LSJ)
- All keyed to Strong's numbers
- All in simple TSV format
- All from one repository
- All CC BY 4.0 license
- All professionally curated by Tyndale House

**One download, three lexicons, easy parsing.**

## Implementation Priority

### Phase 1: Base Definitions
**Use STEPBible exclusively:**
1. Download TBESG, TBESH, TFLSJ from STEPBible repository
2. Parse TSV format
3. Add to `strongs-fetcher.py`

### Phase 2: Synonyms
**Use Clear-Bible Proximity data:**
1. Create `strongs-synonyms-fetcher.py`
2. Process Proximity.tsv files
3. Generate separate `.synonyms.yaml` files

### Phase 3: Future Enhancements (Optional)
**If we need more:**
- Unabridged BDB from eliranwong (vs abridged in STEPBible)
- Classical Greek usage from Perseus LSJ
- unfoldingWord as supplemental definitions
- UBS Semantic Dictionaries for domain groupings

## Conclusion

**All four suggested sources verified:**

1. ✅ **OpenScriptures BDB** - Available, but STEPBible's version is better format
2. ✅ **unfoldingWord Lexicons** - Available, good alternative, but STEPBible more complete
3. ❌ **Thayer's XML** - Not found in clean form; use Abbott-Smith instead
4. ✅ **LSJ** - Available, and STEPBible has best version for our needs

**Bottom line:** STEPBible repository provides everything we need from all these sources in the easiest format. Using it as our primary source is the right call.
