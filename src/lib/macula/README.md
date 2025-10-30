# Macula Source Language Processor

Extracts detailed linguistic data from Hebrew and Greek Bible texts using Clear Bible's Macula datasets.

## Overview

This library processes the Macula Hebrew (WLC) and Macula Greek (Nestle1904) datasets, extracting word-by-word morphological, lexical, semantic, and syntactic information into structured YAML files.

## Data Sources

- **Hebrew**: [Clear Bible Macula Hebrew](https://github.com/Clear-Bible/macula-hebrew) - Westminster Leningrad Codex
- **Greek**: [Clear Bible Macula Greek](https://github.com/Clear-Bible/macula-greek) - Nestle1904
- **License**: CC BY 4.0 (Biblica, Inc 2022-2024)

## Usage

### 1. Fetch Data (First Time Only)

```bash
python src/lib/macula/macula_fetcher.py --all
```

This downloads ~500MB of linguistic data to `/tmp/macula/`.

**Options:**
- `--all` - Fetch both Hebrew and Greek
- `--hebrew-only` - Fetch only Hebrew
- `--greek-only` - Fetch only Greek
- `--status` - Check cached data status

### 2. Process Verses

**Single verse:**
```bash
python src/lib/macula/macula_processor.py --verse "JHN 1:1"
```

**Single book:**
```bash
python src/lib/macula/macula_processor.py --book MAT
```

**New Testament:**
```bash
python src/lib/macula/macula_processor.py --nt
# Or: python src/lib/macula/macula_processor.py --testament NT
```

**All verses** (takes 30-60 minutes):
```bash
python src/lib/macula/macula_processor.py --all
```

## Output

Generated files follow this structure:

```
./bible/commentaries/{BOOK}/{CHAPTER}/{VERSE}/{BOOK}-{CHAPTER}-{VERSE}-macula.yaml
```

**Examples:**
- `./bible/commentaries/JHN/001/001/JHN-001-001-macula.yaml`
- `./bible/commentaries/MAT/005/003/MAT-005-003-macula.yaml`

## Output Format

```yaml
source: macula-greek
version: 1.0.0
language: grc
verse: JHN 1:1
text: "Ἐν ἀρχῇ ἦν ὁ Λόγος..."

words:
  - position: 1
    ref: JHN 1:1!1
    text: "Ἐν"
    lemma: "ἐν"
    normalized: "Ἐν"
    transliteration: "En"  # Hebrew only

    translation:
      gloss: "in"
      english: "in"      # Hebrew only
      mandarin: "在"      # Hebrew only

    morphology:
      class: "prep"
      morph: "PREP"
      pos: "preposition"
      gender: "masculine"
      number: "singular"
      person: "third"
      # Hebrew specific:
      state: "absolute"  # absolute|construct|determined
      stem: "qal"        # qal|niphal|piel|etc
      # Greek specific:
      case: "nominative"  # nominative|genitive|dative|accusative
      tense: "imperfect"  # present|imperfect|aorist|etc
      voice: "active"     # active|middle|passive
      mood: "indicative"  # indicative|subjunctive|etc
      degree: "comparative"  # comparative|superlative (adjectives)
      has_article: true   # Greek article presence

    lexical:
      strong: "1722"
      stronglemma: "ἐν"  # Hebrew uses stronglemma

    semantic:
      # Hebrew:
      sdbh: ["006653001001000"]  # Semantic Dictionary of Biblical Hebrew
      lexdomain: ["002003003004"]
      coredomain: ["168"]
      sense: "1"
      # Greek:
      domain: "067002"
      ln: "67.33"  # Louw-Nida number

    syntax:
      role: "p"  # p=predicate, s=subject, v=verb, o=object, vc=verb-clause
      frame: "A0:...; A1:...;"  # Semantic frame (Hebrew verbs)
      discontinuous: "true"  # Greek discontinuous constituents
      junction: "coordinate"  # Greek clause connections

    discourse:
      # Hebrew:
      participant: "n01001001007"  # Participant tracking
      subject: "n01001001005"
      # Greek:
      referent: "n40005003007"  # Discourse referent
      subject: "n40005003005"

    lxx:  # Hebrew only - LXX cross-reference
      text: "ἐν"
      strong: "1722"
```

## Field Categories

### Core Fields (Always Present)
- `position` - Word position in verse (1-indexed)
- `ref` - Verse reference with word position (e.g., "JHN 1:1!1")
- `text` - Original language text
- `lemma` - Dictionary/lexical form

### Translation
- `gloss` - Short English gloss
- `english` - English translation (Hebrew)
- `mandarin` - Mandarin translation (Hebrew)

### Morphology
- **Basic**: `class`, `morph`, `pos`
- **Hebrew**: `state`, `stem`, `type`
- **Greek**: `case`, `tense`, `voice`, `mood`, `degree`, `has_article`
- **Common**: `gender`, `number`, `person`

### Lexical References
- **Hebrew**: `stronglemma`, `strong` (strongnumberx)
- **Greek**: `strong`

### Semantic Domains
- **Hebrew**: `sdbh`, `lexdomain`, `coredomain`, `sense`
- **Greek**: `domain`, `ln` (Louw-Nida)

### Syntax
- `role` - Syntactic function
- `frame` - Semantic frame with arguments (Hebrew verbs)
- `discontinuous` - Discontinuous constituents (Greek)
- `junction` - Clause connection type (Greek)

### Discourse
- **Hebrew**: `participant`, `subject`
- **Greek**: `referent`, `subject`

### Cross-References
- **Hebrew only**: `lxx` - Septuagint cross-reference

## Critical Fields by Use Case

### For Translation
**Hebrew:**
- `state` (absolute vs construct → definiteness)
- `stem` (qal/piel/hiphil → meaning changes)
- `sdbh`, `coredomain` (semantic domains)
- `lxx` (for rare words - ancient interpretation)

**Greek:**
- `case` (grammatical function)
- `has_article` (definiteness - critical for theology!)
- `tense`, `voice`, `mood` (verbal aspect)
- `ln` (Louw-Nida semantic domain)

### For Exegesis
- `syntax.role` - Clause structure
- `discourse.referent` - Who does what to whom
- `semantic` fields - Meaning disambiguation
- `morphology` - Grammatical precision

## Multiple Values

When fields contain multiple values (arrays), this indicates scholarly uncertainty:

```yaml
semantic:
  sdbh: ["002680001001000", "002680001002000"]  # Two interpretations
  coredomain: ["010", "106"]  # Physical vs Mental debate
```

This is especially common for:
- Hapax legomena (words appearing once)
- Rare words
- Ambiguous contexts

## Documentation

- **[MACULA-FIELD-DEFINITIONS.md](./MACULA-FIELD-DEFINITIONS.md)** - Complete field reference with all possible values

## Requirements

- Python 3.7+
- PyYAML: `pip install pyyaml`
- Git (for fetching datasets)

## Performance

- Single verse: < 1 second
- Single book: 10-20 seconds
- Full Testament: 5-10 minutes
- Full Bible: 30-60 minutes

## Example: Matthew 5:3

```yaml
source: macula-greek
version: 1.0.0
language: grc
verse: MAT 5:3
text: "Μακάριοι οἱ πτωχοὶ τῷ πνεύματι..."

words:
  - position: 3
    text: "πτωχοὶ"
    lemma: "πτωχός"
    morphology:
      class: "adj"
      morph: "A-NPM"
      case: "nominative"
    semantic:
      ln: "88.57"  # Domain 88.G "Humility" (NOT economic poverty!)
      domain: "088007"
```

The Louw-Nida code `88.57` definitively shows this refers to **spiritual poverty/humility**, not economic poverty - critical for accurate translation!

## License

**Tool**: MIT License

**Data**:
- Macula Hebrew: CC BY 4.0 (Biblica, Inc)
- Macula Greek: CC BY 4.0 (Biblica, Inc)

**Citation**:
> MACULA Hebrew Linguistic Datasets, available at https://github.com/Clear-Bible/macula-hebrew/
> MACULA Greek Linguistic Datasets, available at https://github.com/Clear-Bible/macula-greek/
