---
name: get-source-languages
description: Fetch source language (Greek/Hebrew) word data for Bible verses. Use this when users want to study Greek or Hebrew words, understand original language meanings, or analyze source text morphology. The skill retrieves Macula source language data and merges it with Strong's dictionary entries to provide comprehensive linguistic information.
---

# Get Source Languages

## Overview

Retrieve detailed source language (Greek/Hebrew) data for Bible verses, including original text, morphology, Strong's dictionary entries, and semantic information. This skill combines Macula linguistic datasets with Strong's dictionary to provide comprehensive word-level analysis.

## When to Use

Use this skill when:
- User wants to study Greek or Hebrew words in a verse
- User asks about original language meanings or etymology
- User needs morphological analysis (tense, case, gender, etc.)
- User is doing word studies or comparative analysis
- User mentions "Greek", "Hebrew", "original language", "source text", or "Strong's"

Do NOT use this skill when:
- User only wants English translations (use quote-bible skill)
- User is doing topical study without language focus
- User needs commentary rather than linguistic data

## How to Use

### Step 1: Parse the Bible Reference

Extract the Bible reference from the user's request. The reference must use USFM 3.0 three-letter codes:
- **Book code**: Use USFM 3.0 (e.g., "JHN", "GEN", "MAT")
- **Chapter:Verse format**: "JHN 3:16", "GEN 1:1"

### Step 2: Execute the Source Languages Fetcher

Use the Bash tool to execute the fetcher script:

```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "<reference>"
```

Where `<reference>` is the verse reference:
- "JHN 3:16" (John 3:16)
- "GEN 1:1" (Genesis 1:1)
- "ROM 8:28" (Romans 8:28)

### Step 3: Display Results

The script returns YAML data containing:
- **verse**: Verse reference
- **language**: Source language (heb/grc)
- **text**: Original language text
- **words**: Array of word objects with:
  - `text`: Original language word
  - `lemma`: Dictionary form
  - `morphology`: Grammatical properties (pos, case, tense, gender, number, etc.)
  - `translation`: English gloss
  - `strongs_data`: Full Strong's dictionary entry merged from all sources
  - `lexical`: Strong's number references
  - `semantic`: Semantic domain information

Present the information clearly to the user, highlighting:
- Original text with transliteration
- Strong's numbers and definitions
- Morphological information relevant to their question
- English glosses for understanding

### Step 4: Options

Optional flags:
- `--output <file>`: Save results to a YAML file
- `--json`: Output as JSON instead of YAML
- `--no-generate`: Don't auto-generate Macula data if missing

## Examples

### Example 1: Study Greek Words in John 3:16

**User:** "What are the Greek words in John 3:16?"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "JHN 3:16"
```

**Expected behavior:** Display each Greek word with lemma, morphology, and Strong's definition

### Example 2: Hebrew Word Study

**User:** "I want to study the Hebrew words in Genesis 1:1"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "GEN 1:1"
```

**Expected behavior:** Display Hebrew text with transliteration, morphology, and Strong's entries

### Example 3: Strong's Number Lookup

**User:** "What does the Greek word in Romans 8:28 mean?"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "ROM 8:28"
```

**Expected behavior:** Display all Greek words with Strong's definitions and usage information

## Technical Details

### Data Sources

The skill combines data from:
1. **Macula Project**: Morphologically analyzed Hebrew (WLC) and Greek (Nestle 1904) texts
   - Location: `./bible/commentaries/{BOOK}/{chapter}/{verse}/{BOOK}-{chapter}-{verse}-macula.yaml`
   - Contains: Original text, lemmas, morphology, syntax, semantic domains

2. **Strong's Dictionary**: Hebrew and Greek lexicon entries
   - Location: `./bible/words/strongs/{STRONG_NUMBER}/`
   - Contains: Lemma, definition, KJV usage, derivation, transliteration

### Auto-Generation

If Macula data doesn't exist for a verse, the script automatically:
1. Calls `macula_processor.py --verse "<reference>"`
2. Generates the macula.yaml file from cached XML datasets
3. Returns the newly generated data

This requires that Macula datasets have been downloaded via `macula_fetcher.py`.

### Data Merging

The skill uses `yaml_merger.py` to merge multiple YAML files:
- All files in a Strong's number directory are merged
- Nested merge preserves structure
- String values are concatenated if different
- Lists are extended

## Error Handling

If the script fails:
1. **"Macula data not found"**: Run `python3 src/lib/macula/macula_fetcher.py` first to download datasets
2. **"Strong's entry not found"**: Run `python3 strongs-fetcher.py` to download Strong's dictionary
3. **"Invalid verse reference"**: Check reference format (BOOK CHAPTER:VERSE)

## Integration with Tool Ecosystem

When the `tool-experimenter` skill is improving Bible study tools, it should consider this skill as an option if the tool:
- Deals with source language data
- Needs Strong's definitions
- Requires morphological analysis
- Works with Hebrew or Greek text

## Notes

- Greek text uses Unicode (polytonic Greek)
- Hebrew text uses Unicode (Hebrew with vowel points)
- Strong's numbers follow format: G0001-G5624 (Greek), H0001-H8674 (Hebrew)
- Morphology codes follow standard linguistic conventions (see Macula documentation)
