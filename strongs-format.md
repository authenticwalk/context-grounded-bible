# Strong's Concordance Format Specification

## Overview

This document specifies the format and structure for Strong's Hebrew and Greek concordance data in the Context-Grounded Bible project.

## Purpose

Standardized reference database for every Hebrew and Greek word in the Bible, providing:
- Original language lemmas
- Transliterations and pronunciations
- Definitions and usage examples
- Etymological derivations
- Cross-references to biblical usage

## Directory Structure

**Path:** `/bible/words/strongs/{strongs-number}/{strongs-number}.strongs.yaml`

**Number Format:** 4-digit zero-padded with language prefix
- Greek: `G0001` through `G5624` (prefix `G`)
- Hebrew: `H0001` through `H8674` (prefix `H`)

### Examples

```
/bible/words/strongs/G0001/G0001.strongs.yaml    # Α (Alpha) - first letter
/bible/words/strongs/G0025/G0025.strongs.yaml    # ἀγαπάω (agapáō) - divine love
/bible/words/strongs/G0026/G0026.strongs.yaml    # ἀγάπη (agápē) - love (noun)
/bible/words/strongs/G5368/G5368.strongs.yaml    # φιλέω (philéō) - brotherly love
/bible/words/strongs/H0001/H0001.strongs.yaml    # אָב (ab) - father
/bible/words/strongs/H0157/H0157.strongs.yaml    # אָהַב (ahab) - to love
```

## YAML File Structure

### Complete Example

```yaml
strongs_number: G0025
language: greek
lemma: ἀγαπάω
transliteration: agapáō
pronunciation: ag-ap-ah'-o         # Hebrew only
definition: to love (in a social or moral sense)
kjv_usage: (be-)love(-ed)
derivation: perhaps from (much) (or compare G5689);
source: openscriptures/strongs
license: CC-BY-SA
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `strongs_number` | string | Yes | Zero-padded identifier (G0001-G5624 or H0001-H8674) |
| `language` | string | Yes | Either `greek` or `hebrew` |
| `lemma` | string | Yes | Original language word in native script |
| `transliteration` | string | Yes | Romanized version of the word |
| `pronunciation` | string | Hebrew only | Phonetic pronunciation guide |
| `definition` | string | Yes | Strong's original definition |
| `kjv_usage` | string | Yes | How the word appears in King James Version |
| `derivation` | string | Optional | Etymological origin and related Strong's numbers |
| `source` | string | Yes | Data source (`openscriptures/strongs`) |
| `license` | string | Yes | License (`CC-BY-SA`) |

### Field Details

**strongs_number**
- Format: `G####` or `H####` with 4-digit zero padding
- Greek range: G0001-G5624
- Hebrew range: H0001-H8674
- Always matches directory and filename

**language**
- Valid values: `greek`, `hebrew`
- Lowercase only

**lemma**
- Hebrew: Uses Unicode Hebrew characters (U+0590 to U+05FF)
- Greek: Uses Unicode Greek characters (U+0370 to U+03FF)
- Includes vowel points and diacritical marks as provided in source

**transliteration**
- Greek uses scientific transliteration system
- Hebrew uses standard scholarly transliteration
- May include diacritics (á, ē, ō, etc.)

**pronunciation** (Hebrew only)
- Phonetic guide for pronunciation
- Uses simplified English-like phonetics
- Includes stress marks with apostrophes

**definition**
- Strong's original English definition
- May reference other Strong's numbers (e.g., "from G1537")
- Preserves original punctuation and parentheticals

**kjv_usage**
- Shows how the word is translated in KJV
- Multiple translations separated by commas
- May include grammatical notes in brackets
- Uses `[idiom]` marker for idiomatic expressions

**derivation**
- Etymological information
- References to related Strong's numbers
- May indicate primitive roots or compound words

## Database Statistics

- **Total Entries:** 14,197
- **Greek Entries:** 5,523 (G0001-G5624)
- **Hebrew Entries:** 8,674 (H0001-H8674)
- **Total Size:** ~63MB

## Cross-Referencing

### From Word Files to Strong's

```yaml
# In /bible/words/grc/αγαπη/αγαπη.yaml
strongs: G0026                      # Reference to Strong's entry

# In /bible/words/heb/אהב/אהב.yaml
strongs: H0157                      # Reference to Strong's entry
```

### From Strong's to Strong's (in derivation field)

```yaml
# Example showing cross-references
derivation: from G1537 (ἐκ) and G5055 (τελέω);
```

## Zero-Padding Rationale

**Why 4-digit zero-padding?**

1. **Consistent string length** - All numbers are same width for sorting and display
2. **File system organization** - Directories sort naturally (G0001, G0002... G0100, G0200)
3. **Standard alignment** - Matches digital Bible tools and reference software
4. **Prevents ambiguity** - G0001 is standard, not G1
5. **Easier programmatic handling** - No special sorting logic required
6. **Visual clarity** - Clear at a glance whether it's G0025 or G0250

## Data Source

- **Repository:** https://github.com/openscriptures/strongs
- **License:** CC-BY-SA (Creative Commons Attribution-ShareAlike)
- **Original Work:** James Strong's Exhaustive Concordance (1890)
- **Conversion:** Open Scriptures Hebrew Lexicon Project
- **Format:** JavaScript dictionaries converted to YAML

## Generation Script

Data files are generated using `strongs-fetcher.py`:

```bash
python3 strongs-fetcher.py
```

The script:
1. Downloads Greek and Hebrew dictionaries from openscriptures/strongs
2. Parses JavaScript dictionary format
3. Converts to YAML with zero-padded Strong's numbers
4. Creates directory structure: `{number}/{number}.strongs.yaml`
5. Generates 14,197 files (5,523 Greek + 8,674 Hebrew)

## File Naming Convention

- Directory name: `{G|H}{0000-9999}` (e.g., `G0025`, `H0157`)
- File name: `{directory}.strongs.yaml` (e.g., `G0025.strongs.yaml`)
- Always match: directory name = file prefix

## Usage Examples

### Looking up a Strong's Number

```bash
# Greek word for love (agape)
cat bible/words/strongs/G0026/G0026.strongs.yaml

# Hebrew word for love
cat bible/words/strongs/H0157/H0157.strongs.yaml
```

### Finding all Greek words

```bash
ls bible/words/strongs/G*/
```

### Finding all Hebrew words

```bash
ls bible/words/strongs/H*/
```

## Integration with Other Data

Strong's numbers serve as a bridge between:
- **Original language word files** (`/bible/words/grc/`, `/bible/words/heb/`)
- **Verse analysis** (references in commentary files)
- **Interlinear texts** (word-by-word alignment)
- **Lexicons and dictionaries** (cross-referencing)

## Maintenance

### Updating Data

To update Strong's data:

1. Run the fetcher script: `python3 strongs-fetcher.py`
2. Review changes: `git diff bible/words/strongs/`
3. Commit data separately: `git add bible/words/strongs && git commit -m "data: update Strong's entries"`

### Validation

Ensure data integrity:

```bash
# Check file count
find bible/words/strongs -name "*.strongs.yaml" | wc -l
# Should output: 14197

# Check Greek count
find bible/words/strongs/G* -name "*.strongs.yaml" | wc -l
# Should output: 5523

# Check Hebrew count
find bible/words/strongs/H* -name "*.strongs.yaml" | wc -l
# Should output: 8674
```

## License Compliance

All Strong's data is distributed under **CC-BY-SA** license:

- **Attribution Required:** Credit to Open Scriptures and James Strong
- **ShareAlike:** Derivative works must use same license
- **Commercial Use:** Permitted with attribution
- **Modifications:** Allowed with attribution and same license

## References

- **Open Scriptures Project:** https://github.com/openscriptures
- **Strong's Dictionaries:** https://github.com/openscriptures/strongs
- **USFM Standards:** https://ubsicap.github.io/usfm/
- **BibleHub Strong's:** https://biblehub.com/greek/ and https://biblehub.com/hebrew/
