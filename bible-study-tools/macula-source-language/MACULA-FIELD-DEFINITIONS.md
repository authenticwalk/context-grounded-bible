# Macula Hebrew and Greek Field Definitions

This document defines all available fields from the Clear Bible Macula Hebrew and Greek datasets (lowfat format).

## Data Sources

- **Macula Hebrew**: https://github.com/Clear-Bible/macula-hebrew
- **Macula Greek**: https://github.com/Clear-Bible/macula-greek
- **License**: CC BY 4.0 (Creative Commons Attribution 4.0 International)
- **Copyright**: Biblica, Inc (2022-2024)

## Document Structure

### Root Element: `<chapter>` (Hebrew) or `<book>` (Greek)
- **lang**: Language code (`he` for Hebrew, `el` for Greek)
- **id**: Book identifier (e.g., `GEN 1` or `JHN`)

### Sentence Element: `<sentence>`
- **id**: Optional sentence identifier with verse reference

### Milestone Element: `<milestone>`
- **unit**: Always "verse"
- **id**: Verse reference (e.g., `GEN 1:1`, `JHN 1:1`)

### Word Group Element: `<wg>`
Represents syntactic constituents (phrases, clauses)
- **class**: Syntactic class (e.g., `cl` for clause, `pp` for prepositional phrase, `np` for noun phrase, `vp` for verb phrase)
- **rule**: Grammar rule describing structure (e.g., `PP-V-S-O`, `DetNP`, `PrepNp`)
- **role**: Syntactic role (e.g., `s` for subject, `v` for verb, `o` for object, `p` for predicate, `pp` for prepositional phrase)
- **head**: Boolean indicating if this is the head of the phrase
- **articular**: Boolean indicating if a phrase has an article (Greek only)

## Word Element: `<w>`

### Core Identification Fields

| Field | Description | Example (Hebrew) | Example (Greek) |
|-------|-------------|------------------|-----------------|
| `xml:id` | Unique identifier | `o010010010011` | `n43001001001` |
| `ref` | Verse reference with word position | `GEN 1:1!1` | `JHN 1:1!1` |
| `class` | Word class | `prep`, `noun`, `verb` | `prep`, `noun`, `verb` |
| `pos` | Part of speech | `preposition`, `noun`, `verb`, `conjunction`, `particle` | `preposition`, `noun`, `verb`, `conjunction`, `article` |

### Text Fields

| Field | Description | Example (Hebrew) | Example (Greek) |
|-------|-------------|------------------|-----------------|
| `unicode` | Original script text | `בְּרֵאשִׁ֖ית` | `Ἐν` |
| `lemma` | Dictionary/lexical form | `רֵאשִׁית` | `ἐν` |
| `transliteration` | Romanized form | `rēʾšiyṯ` | `En` |
| `normalized` | Normalized form (Greek only) | N/A | `Ἐν` |

### Translation Fields

| Field | Description | Example (Hebrew) | Example (Greek) |
|-------|-------------|------------------|-----------------|
| `english` | English gloss | `beginning` | `in` |
| `mandarin` | Mandarin translation (Hebrew only) | `起初` | N/A |
| `gloss` | Short gloss/translation | `beginning` | `In [the]` |

### Morphological Fields - Common

| Field | Description | Values |
|-------|-------------|--------|
| `morph` | Morphological code | Hebrew: `Ncfsa`, `Vqp3ms`<br>Greek: `PREP`, `N-DSF`, `V-IAI-3S` |
| `gender` | Grammatical gender | `masculine`, `feminine`, `both` (Hebrew), `neuter` (Greek) |
| `number` | Grammatical number | `singular`, `plural` |
| `person` | Grammatical person | `first`, `second`, `third` |

### Morphological Fields - Hebrew Specific

| Field | Description | Values |
|-------|-------------|--------|
| `state` | Noun state | `absolute`, `construct`, `determined` |
| `stem` | Verb stem | `qal`, `piel`, `hiphil`, `niphal`, `pual`, `hophal`, `hithpael` |
| `type` | Specific type | `common` (noun), `qatal`/`yiqtol`/`wayyiqtol` (verb), `direct object marker` (particle) |

### Morphological Fields - Greek Specific

| Field | Description | Values |
|-------|-------------|--------|
| `case` | Grammatical case | `nominative`, `genitive`, `dative`, `accusative`, `vocative` |
| `tense` | Verb tense | `present`, `imperfect`, `future`, `aorist`, `perfect`, `pluperfect` |
| `voice` | Verb voice | `active`, `passive`, `middle` |
| `mood` | Verb mood | `indicative`, `subjunctive`, `optative`, `imperative`, `infinitive`, `participle` |

### Lexical Reference Fields

| Field | Description | Example (Hebrew) | Example (Greek) |
|-------|-------------|------------------|-----------------|
| `stronglemma` | Strong's lemma | `רֵאשִׁית` | N/A |
| `strong` | Strong's number | N/A | `1722` |
| `strongnumberx` | Extended Strong's | `7225` | N/A |

### Semantic Fields (Hebrew)

| Field | Description | Example |
|-------|-------------|---------|
| `sdbh` | Semantic Dictionary of Biblical Hebrew ID | `006653001001000` |
| `lexdomain` | Lexical domain code | `002003003004` |
| `coredomain` | Core semantic domain(s) | `168` or `028 055` |
| `sensenumber` | Sense/meaning number | `1`, `2`, `3` |

### Semantic Fields (Greek)

| Field | Description | Example |
|-------|-------------|---------|
| `domain` | Louw-Nida semantic domain | `067002` |
| `ln` | Louw-Nida number | `67.33` |

### Cross-Reference Fields

| Field | Description | Example (Hebrew) | Example (Greek) |
|-------|-------------|------------------|-----------------|
| `greek` | Greek equivalent | `ἐν` | N/A |
| `greekstrong` | Greek Strong's number | `1722` | N/A |

### Syntactic/Semantic Role Fields

| Field | Description | Example |
|-------|-------------|---------|
| `role` | Syntactic role in clause | `v` (verb), `s` (subject), `o` (object), `p` (predicate), `vc` (verbal clause) |
| `frame` | Semantic frame with argument structure | `A0:010010010031; A1:010010010052;010010010072;` |

### Formatting Fields

| Field | Description | Values |
|-------|-------------|--------|
| `after` | Text/whitespace after word | ` `, `,`, `.`, `׃` (Hebrew sof pasuq) |
| `lang` | Language code | `H` (Hebrew), `el` (Greek) |

## Morphological Code System

### Hebrew Morphology Codes (OSHB format)

Structure: `[POS][subtype][gender][number][state/person/etc]`

Examples:
- `Ncfsa` = Noun, common, feminine, singular, absolute
- `Vqp3ms` = Verb, qal, perfect (qatal), 3rd person, masculine, singular
- `R` = Preposition (R = Relator)
- `Td` = Particle (T), definite article (d)

### Greek Morphology Codes (various formats)

Examples:
- `PREP` = Preposition
- `N-DSF` = Noun, Dative, Singular, Feminine
- `V-IAI-3S` = Verb, Imperfect, Active, Indicative, 3rd person, Singular
- `T-NSM` = Article (sidenote), Nominative, Singular, Masculine
- `CONJ` = Conjunction

## Data Quality Notes

1. **Not all fields are present for every word** - The available fields depend on the part of speech and the specific analyses completed
2. **Multiple domain values** - Some Hebrew words have multiple core domains separated by spaces (e.g., `055 090`)
3. **Frame annotations** - Hebrew verbs may include semantic frame information identifying arguments (A0=agent, A1=patient, etc.)
4. **Sense numbers** - Indicate which meaning of a polysemous word is intended in context

## Citation

When using this data, cite as:
"MACULA Hebrew Linguistic Datasets, available at https://github.com/Clear-Bible/macula-hebrew/" (for Hebrew)
"MACULA Greek Linguistic Datasets, available at https://github.com/Clear-Bible/macula-greek/" (for Greek)

## Additional Documentation

For more detailed information about the Macula Hebrew project:
- Full documentation: https://github.com/Clear-Bible/macula-hebrew/blob/main/doc/MACULA%20Hebrew%20Treebank%20for%20Open%20Scriptures%20Hebrew%20Bible.pdf
- Repository README: https://github.com/Clear-Bible/macula-hebrew/blob/main/README.md

For Macula Greek project:
- Repository README: https://github.com/Clear-Bible/macula-greek/blob/main/README.md
