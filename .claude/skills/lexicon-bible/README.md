# Lexicon Bible Skill

Extract Strong's numbers, lexical data, morphological parsing, and original language information for Bible verses.

## Features

- **Strong's Concordance**: Get Strong's numbers (G### for Greek, H### for Hebrew) for every word
- **Original Language**: Display original Greek/Hebrew text with transliterations
- **Lexical Definitions**: Comprehensive glosses and definitions for each word
- **Etymology**: Root words and word origins
- **Testament Detection**: Automatically determines if verse is OT (Hebrew) or NT (Greek)

## Usage

```bash
python3 scripts/lexicon_fetcher.py "BOOK CHAPTER:VERSE" [--format text|yaml]
```

### Examples

```bash
# Get lexical data for John 3:16
python3 scripts/lexicon_fetcher.py "JHN 3:16"

# Get Genesis 1:1 in YAML format
python3 scripts/lexicon_fetcher.py "GEN 1:1" --format yaml

# Matthew 5:3
python3 scripts/lexicon_fetcher.py "MAT 5:3" --format text
```

## Output Format

### Text Format

```
Lexical Data for MAT 5:3
Testament: NT (Greek)
================================================================================

Word 1:
  Original: Μακάριοι
  Transliteration: makarioi
  Strong's: G3107
  Gloss: blessed, happy
  Root: makar
```

### YAML Format

```yaml
reference: MAT 5:3
testament: NT
language: greek
words:
  - position: 1
    original: Μακάριοι
    transliteration: makarioi
    strongs: G3107
    gloss: blessed, happy
    root: makar
```

## Data Sources

Primary data source: **BibleHub** (https://biblehub.com)
- Lexicon pages: `/lexicon/{book}/{chapter}-{verse}.htm`
- Provides NASB-aligned lexical analysis
- Includes Strong's numbers, transliterations, and glosses

### Additional Resources Identified

Other valuable lexical resources (for future enhancements):
1. **Blue Letter Bible** - Comprehensive lexicons with Thayer's, TDNT
2. **STEPBible** - Strong's with morphology
3. **BibleHub Text pages** - Manuscript variants (8 Greek traditions)
4. **BibleHub Interlinear** - Word-by-word translations
5. **Bolls Bible API** - Programmatic access to lexicons

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- pyyaml

Install with:
```bash
pip install -r requirements.txt
```

## Book Codes

The skill uses USFM 3.0 three-letter book codes:
- Old Testament: GEN, EXO, LEV, PSA, ISA, etc.
- New Testament: MAT, MRK, LUK, JHN, ACT, ROM, etc.

See `references/book_codes.md` for complete list.

## Files

- `SKILL.md` - Skill definition and usage instructions
- `scripts/lexicon_fetcher.py` - Main command-line tool
- `scripts/biblehub_lexicon.py` - HTML parser for BibleHub lexicon pages
- `scripts/biblehub_urls.py` - URL templates for various BibleHub pages
- `scripts/book_codes.py` - USFM book code utilities
- `scripts/parsing_codes.py` - Morphological parsing code definitions
- `references/book_codes.md` - USFM 3.0 book code reference

## Features Implemented

- ✅ Strong's concordance numbers (G### for Greek, H### for Hebrew)
- ✅ Original language text with transliterations
- ✅ Lexical definitions and glosses
- ✅ Etymology and root words
- ✅ Morphological parsing (case, gender, number, tense, voice, mood)
- ✅ Textual variants from 8+ Greek manuscript traditions
- ✅ Local caching for improved performance

## Usage with Advanced Features

### Include Textual Variants

```bash
python3 scripts/lexicon_fetcher.py "JHN 3:16" --with-variants
```

Shows the verse in:
- Nestle 1904
- Westcott and Hort 1881
- RP Byzantine Majority Text 2005
- Tischendorf 8th Edition
- Scrivener's Textus Receptus 1894
- Stephanus Textus Receptus 1550
- Greek Orthodox Church
- Hebrew Bible (for NT)
- Peshitta (Aramaic)

### Bypass Cache

```bash
python3 scripts/lexicon_fetcher.py "MAT 5:3" --no-cache
```

## Future Enhancements

Potential additions:
- [ ] Support for verse ranges
- [ ] Additional lexicon sources (Blue Letter Bible, STEPBible)
- [ ] Semantic domain information:
  - **Greek**: Louw-Nida lexicon (commercial, not freely available)
  - **Hebrew**: Semantic Dictionary of Biblical Hebrew (SDBH) - freely available at semanticdictionary.org under CC BY-SA 4.0 license
- [ ] Cross-reference integration
- [ ] Cognate analysis

## Related Skills

- **quote-bible**: Fetch Bible verses in multiple translations
- Use both skills together for comprehensive verse analysis

## License

Part of the Context-Grounded Bible project (MIT License)
