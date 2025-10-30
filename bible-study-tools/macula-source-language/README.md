# Macula Source Language Tool

Extract detailed linguistic information from Hebrew and Greek Bible texts using Clear Bible's Macula datasets.

## Overview

This tool provides word-by-word analysis of the original Hebrew (Old Testament) and Greek (New Testament) texts, including:

- **Morphological analysis** - Parts of speech, gender, number, case, tense, mood, etc.
- **Semantic domains** - Meaning classifications (SDBH for Hebrew, Louw-Nida for Greek)
- **Lexical references** - Strong's numbers, SDBH IDs, lemmas
- **Syntactic structure** - Word order patterns, grammatical roles, phrase structure
- **Translation insights** - Handling rare words, hapax legomena, scholarly debates

## Purpose

This tool is designed for:

1. **Bible Translators** - Grounding new translations in original language data
2. **Pastors/Teachers** - Preparing sermons with deeper understanding of source texts
3. **Bible Students** - Studying original languages without extensive training

## Data Sources

- **Hebrew**: [Clear Bible Macula Hebrew](https://github.com/Clear-Bible/macula-hebrew)
  - Base text: Westminster Leningrad Codex (WLC)
  - Format: lowfat XML
  - License: CC BY 4.0

- **Greek**: [Clear Bible Macula Greek](https://github.com/Clear-Bible/macula-greek)
  - Base text: Nestle1904
  - Format: lowfat XML
  - License: CC BY 4.0

**Copyright**: Biblica, Inc (2022-2024)

## Installation

### Requirements

- Python 3.7+
- Git
- PyYAML

```bash
pip install pyyaml
```

## Usage

### 1. Fetch the Macula Datasets

First time setup (downloads ~500MB of data):

```bash
python bible-study-tools/macula-source-language/macula_fetcher.py --all
```

Check status:

```bash
python bible-study-tools/macula-source-language/macula_fetcher.py --status
```

### 2. Process Verses

Process a single verse:

```bash
python bible-study-tools/macula-source-language/macula_processor.py --verse "JHN 1:1"
```

Process a book:

```bash
python bible-study-tools/macula-source-language/macula_processor.py --book JHN
```

Process a testament:

```bash
python bible-study-tools/macula-source-language/macula_processor.py --testament NT
# Or use the shortcut:
python bible-study-tools/macula-source-language/macula_processor.py --nt
```

Process all verses (takes 30-60 minutes):

```bash
python bible-study-tools/macula-source-language/macula_processor.py --all
```

### 3. Use via Claude Skill

The easiest way to use this tool is through the Claude skill:

```
extract source language for John 1:1
```

Claude will automatically:
1. Check if data is cached
2. Process the verse
3. Present key insights formatted for your use case

## Output Structure

Generated files follow the project convention:

```
./bible/commentaries/{BOOK}/{CHAPTER}/{VERSE}/{BOOK}-{CHAPTER}-{VERSE}-macula.yaml
```

Examples:
- `./bible/commentaries/JHN/001/001/JHN-001-001-macula.yaml`
- `./bible/commentaries/GEN/001/001/GEN-001-001-macula.yaml`
- `./bible/commentaries/JOB/038/036/JOB-038-036-macula.yaml`

## Output Format

See `YAML-TEMPLATE.yaml` for the complete structure.

### Key Sections

```yaml
verse:
  reference: "John 1:1"
  book_code: "JHN"
  chapter: 1
  verse: 1

source:
  dataset: "MACULA Greek Linguistic Datasets"
  license: "CC BY 4.0"
  url: "https://github.com/Clear-Bible/macula-greek"

source_text:
  language: "grc"
  unicode: "Ἐν ἀρχῇ ἦν ὁ Λόγος..."

words:
  - position: 1
    unicode: "Ἐν"
    lemma: "ἐν"
    class: "prep"
    gloss: "in"
    # ... 15-20 additional fields

syntax:
  word_order: "P-VC-S"
```

## Critical Fields by Testament

### Hebrew (Most Important)

| Field | Purpose | Example |
|-------|---------|---------|
| `state` | Definiteness | `absolute`, `construct` |
| `stem` | Verb meaning | `qal`, `piel`, `hiphil` |
| `sdbh` | Semantic ID | `006653001001000` |
| `lexdomain` | Domain code | `002003003004` |
| `coredomain` | Core meaning | `168` |
| `sensenumber` | Polysemy | `1`, `2` |
| `greek` | LXX equivalent | Critical for rare words |
| `frame` | Verb arguments | `A0:...; A1:...;` |

### Greek (Most Important)

| Field | Purpose | Example |
|-------|---------|---------|
| `case` | Function | `nominative`, `accusative` |
| `has_article` | Definiteness | `true`, `false` |
| `tense` | Aspect | `imperfect`, `aorist` |
| `voice` | Verb voice | `active`, `passive` |
| `mood` | Modality | `indicative`, `subjunctive` |
| `ln` | Louw-Nida | `88.57` (most critical!) |
| `domain` | Domain code | `088007` |
| `role` | Syntax | `s`, `p`, `v`, `o` |

## Understanding Multiple Values

When you see multiple values in a field (e.g., `sdbh: ["002680001001000", "002680001002000"]`), this indicates **scholarly uncertainty** - a feature, not a bug!

This is especially common for:
- Hapax legomena (words appearing only once)
- Rare words
- Ambiguous contexts

The tool documents all scholarly positions, allowing translators to make informed decisions.

## Examples

### Example 1: John 1:1 (Greek)

Key insights from the data:

**Word 14 - θεὸς (God):**
- `has_article: false` - CRITICAL: anarthrous
- `role: "p"` - Predicate nominative
- `position_in_clause: 1` - Fronted for emphasis
- **Translation**: "God" (qualitative nature, not "the God")
- **Significance**: Foundation for Trinitarian theology

### Example 2: Job 38:36 (Hebrew)

Contains TWO hapax legomena:

**Word 4 - טֻחוֹת:**
- `rarity: "hapax"`
- `sdbh: ["002680001001000", "002680001002000"]` - Multiple IDs = uncertainty
- `coredomain: ["010", "106"]` - Physical vs. Mental debate
- `greek: "ὑφάσματος"` - LXX: "woven fabric"
- **Translation options**: "inward parts", "heart", "innermost being"

### Example 3: Genesis 1:1 (Hebrew)

**Word 2 - רֵאשִׁ֖ית (beginning):**
- `state: "absolute"` - CRITICAL: affects definiteness
- `lexdomain: "002003003004"` - Temporal domain
- **Translation debate**: "in beginning" vs. "in the beginning"

## Documentation

- **[MACULA-FIELD-DEFINITIONS.md](./MACULA-FIELD-DEFINITIONS.md)** - Complete field reference
- **[YAML-TEMPLATE.yaml](./YAML-TEMPLATE.yaml)** - Output structure template

## Testing

Test verses used in development (demonstrates various challenges):

- **John 1:1** - Greek, article presence, predicate nominatives
- **Job 38:36** - Hebrew, hapax legomena, extreme rarity
- **Matthew 5:3** - Greek, semantic domains, common misinterpretations
- **Genesis 1:1** - Hebrew, syntax, theological foundations

## Limitations

1. **Processing time** - Full Bible takes 30-60 minutes
2. **Cache size** - ~500MB for complete datasets
3. **XML dependency** - Requires original Macula XML structure
4. **Field availability** - Not all fields present for all words

## Contributing

Improvements welcome:
- Additional semantic analysis
- Cross-reference to other datasets
- Performance optimizations
- Better handling of edge cases

## License

This tool: MIT License

Data sources:
- Macula Hebrew: CC BY 4.0 (Biblica, Inc)
- Macula Greek: CC BY 4.0 (Biblica, Inc)

## Citation

When using this tool in research or publication:

**Hebrew data:**
> MACULA Hebrew Linguistic Datasets, available at https://github.com/Clear-Bible/macula-hebrew/

**Greek data:**
> MACULA Greek Linguistic Datasets, available at https://github.com/Clear-Bible/macula-greek/

## Support

For issues with:
- **This tool** - Open issue in context-grounded-bible repository
- **Macula data** - See Clear Bible repositories linked above

## Version History

- **1.0.0** (2025-10-30) - Initial release
  - Hebrew and Greek processing
  - Full field extraction
  - YAML output format
  - Claude skill integration
