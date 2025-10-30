---
name: lexicon-bible
description: Extract Strong's numbers, lexical data, morphological parsing, and original language information for Bible verses. Fetches comprehensive linguistic analysis including Greek/Hebrew words, transliterations, grammatical parsing, definitions, and textual variants. Use when detailed word-level analysis is needed.
---

# Lexicon Bible

## Overview

Extract comprehensive lexical and linguistic data for Bible verses, including Strong's concordance numbers, morphological parsing, original language text, transliterations, definitions, and manuscript variants. This skill provides word-level analysis for deep Bible study and translation work.

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

## Data Extracted

This skill extracts lexical data from multiple BibleHub sources:

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

## Data Storage

Lexical data is cached following the project structure:

```
./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-lexicon.yaml
```

Examples:
- `./bible/MAT/5/3/MAT-5-3-lexicon.yaml`
- `./bible/JHN/3/16/JHN-3-16-lexicon.yaml`

## Technical Notes

- Script uses BibleHub as primary data source
- Data is cached locally to reduce web requests
- YAML format enables both human and AI readability
- Manuscript variants are preserved for textual criticism
- Parsing codes follow standard grammatical abbreviations

## Resources

### references/

- `book_codes.md` - USFM 3.0 book codes and mappings

### scripts/

- `lexicon_fetcher.py` - Main script for fetching lexical data
- `biblehub_lexicon.py` - HTML parser for BibleHub lexicon pages
- `biblehub_interlinear.py` - Parser for interlinear pages
- `biblehub_text.py` - Parser for textual variant pages
- `book_codes.py` - Book code utilities (shared with quote-bible)
- `parsing_codes.py` - Morphological parsing code definitions

## Error Handling

If the script returns an error, check:
- Reference format is valid (USFM codes required)
- Verse exists in the specified book/chapter
- Internet connection available (for non-cached verses)
- BibleHub website is accessible

## Future Enhancements

Potential additions:
- Support for verse ranges
- Additional lexicon sources (Blue Letter Bible, STEPBible)
- Semantic domain information
- Word frequency analysis
- Cognate connections across verses
