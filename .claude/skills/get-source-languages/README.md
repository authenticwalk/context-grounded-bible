# Get Source Languages Skill

Fetch and analyze source language (Greek/Hebrew) data for Bible verses.

## Quick Start

```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "JHN 3:16"
```

## Use Cases

- Study Greek or Hebrew words in specific verses
- Analyze morphology (tense, case, gender, number, etc.)
- Look up Strong's dictionary definitions
- Research original language meanings
- Compare lemmas and semantic domains

## Data Returned

Each verse returns:
- **Original text**: Hebrew or Greek Unicode text
- **Words array**: Each word with:
  - Text, lemma, transliteration
  - Morphology (pos, case, tense, gender, etc.)
  - Strong's number and full dictionary entry
  - English gloss and semantic domain
- **Metadata**: Language, source, word count

## Data Sources

### Macula Project
Morphologically analyzed source texts:
- **Hebrew**: Westminster Leningrad Codex (WLC)
- **Greek**: Nestle 1904

Cached in: `./bible/commentaries/{BOOK}/{chapter}/{verse}/`

### Strong's Dictionary
Hebrew and Greek lexicon with definitions, KJV usage, and etymology.

Cached in: `./bible/words/strongs/{STRONG_NUMBER}/`

## Prerequisites

1. **Download Macula datasets**:
   ```bash
   python3 src/lib/macula/macula_fetcher.py
   ```

2. **Download Strong's dictionary**:
   ```bash
   python3 strongs-fetcher.py
   ```

## Auto-Generation

If Macula data is missing, the script automatically generates it from the downloaded datasets.

## Options

```bash
# Output to file
python3 src/lib/source_languages_fetcher.py "JHN 3:16" --output jhn-3-16.yaml

# JSON format
python3 src/lib/source_languages_fetcher.py "JHN 3:16" --json

# Don't auto-generate if missing
python3 src/lib/source_languages_fetcher.py "JHN 3:16" --no-generate
```

## Examples

### Greek Word Study
```bash
python3 src/lib/source_languages_fetcher.py "JHN 1:1"
```

Returns Greek words with:
- Text: "ἐν", "ἀρχῇ", "ἦν"
- Lemmas: "ἐν", "ἀρχή", "εἰμί"
- Strong's: G1722, G0746, G2258
- Morphology: preposition, noun (dative/singular/feminine), verb (imperfect/active/3rd/singular)

### Hebrew Word Study
```bash
python3 src/lib/source_languages_fetcher.py "GEN 1:1"
```

Returns Hebrew words with:
- Text: "בְּרֵאשִׁ֖ית", "בָּרָ֣א"
- Lemmas: "רֵאשִׁית", "בָּרָא"
- Strong's: H7225, H1201
- Morphology: noun, verb (qal/perfect/3rd/masculine/singular)

## Integration Notes

### For Tool Experimentation
When `tool-experimenter` is improving Bible tools, consider this skill if the tool needs:
- Source language data
- Strong's definitions
- Morphological analysis
- Hebrew/Greek text processing

### For Bible Study Tools
Tools can import the fetcher module:
```python
from src.lib.source_languages_fetcher import fetch_source_languages

data = fetch_source_languages("JHN 3:16")
```

## Technical Details

### YAML Merging
The script uses `src/util/yaml_merger.py` to merge multiple YAML files for each Strong's entry:
- Nested merge preserves structure
- Different strings are concatenated
- Lists are extended

### Book Codes
Uses USFM 3.0 three-letter codes:
- NT: MAT, MRK, LUK, JHN, ACT, ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM, HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD, REV
- OT: GEN, EXO, LEV, NUM, DEU, JOS, JDG, RUT, 1SA, 2SA, 1KI, 2KI, 1CH, 2CH, EZR, NEH, EST, JOB, PSA, PRO, ECC, SNG, ISA, JER, LAM, EZK, DAN, HOS, JOL, AMO, OBA, JON, MIC, NAM, HAB, ZEP, HAG, ZEC, MAL

## Resources

- [Macula Project](https://github.com/Clear-Bible/macula-greek) - Source language datasets
- [OpenScriptures Strong's](https://github.com/openscriptures/strongs) - Strong's dictionary
- USFM 3.0 - Bible book code standard
