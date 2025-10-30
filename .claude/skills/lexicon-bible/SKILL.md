---
name: lexicon-bible
description: Extract Strong's numbers, lexical data, morphological parsing, and original language information for Bible verses. Fetches comprehensive linguistic analysis including Greek/Hebrew words, transliterations, grammatical parsing, definitions, and textual variants. For OT verses, automatically enhances data with morphhb (Westminster Leningrad Codex) morphological analysis. Use when detailed word-level analysis is needed.
---

# Lexicon Bible

## Overview

Extract comprehensive lexical and linguistic data for Bible verses, including Strong's concordance numbers, morphological parsing, original language text, transliterations, definitions, and manuscript variants. This skill provides word-level analysis for deep Bible study and translation work.

**NEW:** For Old Testament verses, this skill automatically integrates morphhb data (Westminster Leningrad Codex) which provides superior Hebrew morphological analysis including:
- Precise word segmentation (separates prefixes/suffixes)
- Complete morphological parsing (stem, tense, person, gender, number, state)
- Augmented Strong's numbers (includes prefix meanings)
- Unique word IDs for textual criticism

## When to Use

Use this skill when:
- User requests Strong's numbers for a verse
- User asks for Greek or Hebrew word analysis
- User needs morphological parsing (case, gender, number, tense, voice, mood)
- User wants lexical definitions and etymology
- User needs interlinear data (word-by-word translation)
- User requests textual variants or manuscript comparisons

Examples:
- "What are the Strong's numbers for John 3:16?"
- "Show me the Greek words in Matthew 5:3"
- "Parse the Hebrew in Genesis 1:1"
- "What's the lexical data for Romans 8:28?"

Do NOT use this skill when:
- User only wants verse translations (use quote-bible skill instead)
- User is doing topical study without word-level analysis
- User needs commentary or interpretation (use other tools)

## Data Sources

This skill combines data from multiple authoritative sources:

### 1. BibleHub (biblehub.com)
- Strong's concordance numbers
- English glosses and definitions
- Basic morphological parsing
- Textual variants across manuscript traditions

### 2. morphhb (OpenScriptures Hebrew Bible) - **NEW!**
- Original Hebrew text from Westminster Leningrad Codex
- Complete morphological analysis for every word
- Augmented Strong's numbers with prefix/suffix meanings
- Unique immutable word IDs
- License: CC BY 4.0
- Repository: https://github.com/openscriptures/morphhb

**Integration:** For OT verses, the skill automatically merges both sources, preferring morphhb for morphology (more accurate) while retaining BibleHub glosses (in English).

## Data Extracted

From BibleHub:

### 1. Lexicon Data (`/lexicon/` page)
- Strong's numbers (e.g., G976, H430)
- Original language word (Greek/Hebrew)
- Transliteration
- Morphological parsing:
  - Part of speech (noun, verb, adjective, etc.)
  - Case (nominative, genitive, dative, accusative, vocative)
  - Gender (masculine, feminine, neuter)
  - Number (singular, plural)
  - Tense (present, aorist, perfect, etc.)
  - Voice (active, passive, middle)
  - Mood (indicative, subjunctive, imperative, etc.)
- Root word
- Definition/gloss
- Etymology

### 2. Interlinear Data (`/interlinear/` page)
- Word order in original text
- Word-by-word English translation
- Original script display
- Strong's number cross-reference

### 3. Textual Variants (`/text/` page)
- Multiple Greek manuscript traditions:
  - Nestle 1904
  - Westcott and Hort 1881
  - RP Byzantine Majority Text 2005
  - Tischendorf 8th Edition
  - Scrivener's Textus Receptus 1894
  - Stephanus Textus Receptus 1550
  - Greek Orthodox Church
- Variant readings and differences

From morphhb (for OT verses only):

### 4. Hebrew Morphological Data
- **Original Hebrew text** with vowel points and cantillation marks
- **Word segmentation** separating prefixes, root words, and suffixes
  - Example: `בְּ/רֵאשִׁ֖ית` = prefix ב + word רֵאשִׁית
- **Augmented Strong's numbers** with prefix meanings
  - Example: `b/7225` = "b (in, with, by) + H7225 (beginning)"
- **Complete morphological parsing:**
  - Part of speech (noun, verb, adjective, etc.)
  - For verbs: stem (Qal, Niphal, Piel, etc.), tense, person, gender, number
  - For nouns: type, gender, number, state (absolute/construct)
  - For pronouns: type, person, gender, number
- **Unique word IDs** for cross-reference and textual criticism
  - Example: `01xeN` (first word of Genesis 1:1)
- **Parsed display** in human-readable format
  - Example: "Verb: Qal Perfect, third-person masculine singular"

### 5. morphhb Extraction Tool

For generating YAML files with morphhb data:

```bash
python3 .claude/skills/lexicon-bible/scripts/morphhb_extractor.py "GEN 1:1"
python3 .claude/skills/lexicon-bible/scripts/morphhb_extractor.py "PSA 23:1" --save
python3 .claude/skills/lexicon-bible/scripts/morphhb_extractor.py "ISA 53:5" --format yaml
```

The `--save` flag saves data to `bible/{book}/{chapter}/{verse}/` following project structure.

## How to Use

### Step 1: Parse the Bible Reference

Extract the Bible reference from the user's request:
- **Book code**: Convert to USFM 3.0 three-letter codes (e.g., "JHN", "GEN", "MAT")
  - See `references/book_codes.md` for complete list
- **Chapter number**: The chapter number
- **Verse number**: Single verse only (ranges not supported for lexical analysis)

### Step 2: Execute the Fetch Script

Use the Bash tool to execute the lexicon fetcher:

```bash
python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "<book> <chapter>:<verse>"
```

Examples:
- `python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "GEN 1:1"`
- `python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "JHN 3:16"`
- `python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "MAT 5:3"`

### Step 3: Display Results

Present the lexical data to the user in a clear, organized format:

1. **Word-by-word analysis**: Show each word with its:
   - Position in verse
   - Original language text
   - Transliteration
   - Strong's number
   - Parsing information
   - English gloss
   - Definition

2. **Textual notes**: Mention any significant variants if requested

3. **Citations**: Follow project citation format

## Output Format

The script outputs YAML data with this structure:

```yaml
reference: MAT 1:1
testament: NT
language: greek
words:
  - position: 1
    original: Βίβλος
    transliteration: Biblos
    strongs: G976
    parsing:
      pos: noun
      case: nominative
      gender: feminine
      number: singular
    gloss: book
    definition: "bark of a papyrus plant, hence a scroll or book"
    root: βίβλος
  - position: 2
    original: γενέσεως
    transliteration: geneseōs
    strongs: G1078
    parsing:
      pos: noun
      case: genitive
      gender: feminine
      number: singular
    gloss: "of origin"
    definition: "origin, birth"
    root: γένεσις
manuscripts:
  - name: "Nestle 1904"
    text: "Βίβλος γενέσεως Ἰησοῦ Χριστοῦ..."
  - name: "Westcott and Hort 1881"
    text: "Βίβλος γενέσεως Ἰησοῦ Χριστοῦ..."
    variants: ["Δαυίδ vs Δαυείδ"]
```

## Examples

### Example 1: Strong's Numbers Request

**User:** "What are the Strong's numbers for John 3:16?"

**Action:**
```bash
python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "JHN 3:16"
```

**Response:** Display each word with its Strong's number, original Greek, and basic definition.

### Example 2: Greek Word Analysis

**User:** "Show me the Greek words in Matthew 5:3"

**Action:**
```bash
python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "MAT 5:3"
```

**Response:** Show Greek text, transliterations, and word meanings.

### Example 3: Morphological Parsing

**User:** "Parse the Greek in Romans 8:28"

**Action:**
```bash
python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "ROM 8:28"
```

**Response:** Display full parsing information for each word (case, gender, number, tense, voice, mood).

### Example 4: Hebrew Morphology with morphhb (NEW!)

**User:** "Show me the Hebrew morphology for Genesis 1:1"

**Action:**
```bash
python3 .claude/skills/lexicon-bible/scripts/lexicon_fetcher.py "GEN 1:1"
```

**Response:** The skill automatically enhances OT verses with morphhb data, showing:
- Hebrew text with proper word segmentation (prefixes/suffixes separated)
- Augmented Strong's numbers with prefix meanings (e.g., "b (in, with, by) + H7225")
- Complete morphological parsing (e.g., "Verb: Qal Perfect, third-person masculine singular")
- Unique word IDs for each Hebrew word
- English glosses from BibleHub

**Alternative - Pure morphhb output:**
```bash
python3 .claude/skills/lexicon-bible/scripts/morphhb_extractor.py "GEN 1:1"
```

This shows only morphhb data without BibleHub merging.

## Data Storage

Lexical data is cached and saved following the project structure:

### BibleHub Cache
```
.cache/lexicon/{book}-{chapter}-{verse}-lexicon.json
```

### Saved YAML Files
```
./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-lexicon.yaml
./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-hebrew-morphology.yaml
```

Examples:
- `./bible/MAT/5/3/MAT-5-3-lexicon.yaml` (BibleHub data)
- `./bible/JHN/3/16/JHN-3-16-lexicon.yaml` (BibleHub data)
- `./bible/GEN/1/1/GEN-1-1-hebrew-morphology.yaml` (morphhb data)

## Technical Notes

- **Data Sources:** BibleHub (NT & OT) + morphhb (OT only, automatically integrated)
- **BibleHub Cache:** Data is cached locally in `.cache/lexicon/` to reduce web requests
- **morphhb Integration:** For OT verses, morphhb data is automatically fetched and merged
  - Preferring morphhb for morphology (more accurate word segmentation)
  - Retaining BibleHub for English glosses and definitions
  - Handles different word segmentations intelligently
- **YAML Format:** Enables both human and AI readability
- **Manuscript Variants:** Preserved for textual criticism (use `--with-variants` flag)
- **Parsing Codes:** Follow standard grammatical abbreviations
- **Morphological Parsing:**
  - Greek: Extracted from BibleHub KJV Lexicon section
  - Hebrew: Parsed from morphhb codes (comprehensive verb stems, noun states, etc.)
- **Supports:** Both Greek (NT) and Hebrew (OT) texts
- **License Attribution:**
  - BibleHub data: Educational use
  - morphhb data: CC BY 4.0 (attribution required)

## Resources

### references/

- `book_codes.md` - USFM 3.0 book codes and mappings

### scripts/

**Main Tools:**
- `lexicon_fetcher.py` - Main script for fetching lexical data (auto-integrates morphhb for OT)
- `morphhb_extractor.py` - Extract pure morphhb data for Hebrew verses (NEW!)

**BibleHub Parsers:**
- `biblehub_lexicon.py` - HTML parser for BibleHub lexicon pages
- `biblehub_interlinear.py` - Parser for interlinear pages
- `biblehub_text.py` - Parser for textual variant pages

**morphhb Parsers (NEW!):**
- `hebrew_morphology.py` - Hebrew morphology code parser for morphhb data
- `cache_manager.py` - File-based caching system

**Utilities:**
- `book_codes.py` - Book code utilities (shared with quote-bible)
- `parsing_codes.py` - Greek morphological parsing code definitions
- `biblehub_urls.py` - URL templates for BibleHub pages

## Error Handling

If the script returns an error, check:
- Reference format is valid (USFM codes required)
- Verse exists in the specified book/chapter
- Internet connection available (for non-cached verses)
- BibleHub website is accessible
- For morphhb errors:
  - morphhb submodule is initialized: `git submodule update --init data/morphhb`
  - Verse is in the Old Testament (morphhb only covers OT)
  - Book code is valid USFM 3.0 format

## Future Enhancements

Completed:
- ✅ Morphological parsing for Hebrew (morphhb integration)
- ✅ Textual variants from multiple manuscript traditions
- ✅ Local caching system
- ✅ Hebrew word segmentation (prefixes/suffixes)
- ✅ Augmented Strong's numbers

Potential additions:
- Support for verse ranges
- Additional lexicon sources (Blue Letter Bible, STEPBible)
- Semantic domain information (SDBH for Hebrew, Louw-Nida for Greek)
- Word frequency analysis across corpus
- Cognate connections across verses
- Greek NT morphology from similar open-source projects
