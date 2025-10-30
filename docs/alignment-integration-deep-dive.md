# Alignment and Entity Data Integration - Deep Dive Analysis

## Overview

This document provides a comprehensive analysis of two major Bible data repositories and their integration potential with the lexicon-bible skill:

1. **Clear-Bible Alignments**: Word-to-word translation alignments across 10+ languages
2. **BibleAquifer ACAI**: Entity-based annotations with word-level references

Both systems use identical word ID formats that match morphhb, enabling seamless integration.

## 1. Clear-Bible Alignments Repository

**Repository**: https://github.com/Clear-Bible/Alignments
**Purpose**: Manual and automatic word-level translation alignments
**Data Format**: JSON records linking source (Hebrew/Greek) to target (translation) words

### 1.1 Repository Structure

```
/data/
  ├── eng/          # English translations
  │   └── alignments/
  │       ├── BSB/  # Berean Study Bible
  │       │   ├── WLCM-BSB-manual.json      (270,398 records - Hebrew)
  │       │   ├── SBLGNT-BSB-manual.json    (115,008 records - Greek)
  │       │   └── BGNT-BSB-manual.json      (115,998 records - Byzantine Greek)
  │       └── YLT/  # Young's Literal Translation
  │           ├── WLC-YLT-manual.json       (437,265 records - Hebrew)
  │           └── SBLGNT-YLT-manual.json    (127,902 records - Greek)
  ├── spa/          # Spanish (RV09)
  ├── fra/          # French (LSG)
  ├── arb/          # Arabic (AVD)
  ├── hin/          # Hindi (IRVHin)
  ├── por/          # Portuguese
  ├── rus/          # Russian (RUSSYN)
  ├── asm/          # Assamese
  ├── ben/          # Bengali
  └── hau/          # Hausa
```

### 1.2 Data Format

#### File Structure

```json
{
  "documents": [
    {"docid": "WLCM", "scheme": "BCVWP"},
    {"docid": "BSB", "scheme": "BCVW"}
  ],
  "meta": {
    "conformsTo": "0.3",
    "creator": "BiblioNexus"
  },
  "roles": ["source", "target"],
  "type": "translation",
  "records": [...]
}
```

#### Alignment Record Structure

```json
{
  "source": ["o010010010011", "o010010010012"],
  "target": ["01001001001", "01001001002", "01001001003"],
  "meta": {
    "id": "01001001.001",
    "origin": "manual",
    "status": "created"
  }
}
```

**Fields:**
- `source`: Array of Hebrew/Greek word IDs (morphhb format)
- `target`: Array of target language word IDs (translation-specific)
- `meta.id`: Alignment group ID (BCVVV.NNN format)
- `meta.origin`: "manual" or "automatic"
- `meta.status`: "created", "reviewed", etc.

### 1.3 Source Text Corpora

**Hebrew Old Testament:**
- **WLCM**: Westminster Leningrad Codex with morphology
- **WLC**: Westminster Leningrad Codex (standard)

**Greek New Testament:**
- **SBLGNT**: Society of Biblical Literature Greek New Testament
- **BGNT**: Byzantine Greek New Testament

### 1.4 Alignment Examples

#### Example 1: Genesis 1:1 - Hebrew to English (BSB)

```json
{
  "source": ["o010010010011", "o010010010012"],
  "target": ["01001001001", "01001001002", "01001001003"],
  "meta": {"id": "01001001.001", "origin": "manual"}
}
```

**Interpretation:**
- Hebrew words `o010010010011` + `o010010010012` (בְּרֵאשִׁית)
- Align to English BSB: word 1 ("In") + word 2 ("the") + word 3 ("beginning")

#### Example 2: Same Hebrew Word - Spanish (RV09)

```json
{
  "source": ["o010010010012"],
  "target": ["01001001003"],
  "meta": {"id": "01001001.1", "origin": "manual"}
}
```

**Interpretation:**
- Hebrew word `o010010010012`
- Aligns to Spanish word 3 ("principio")

#### Example 3: Matthew 1:1 - Greek to English (BSB)

```json
{
  "source": ["n40001001001"],
  "target": ["40001001001"],
  "meta": {"id": "40001001.001", "origin": "manual"}
}
```

### 1.5 Alignment Statistics

| Language | Translation | Hebrew Records | Greek Records |
|----------|-------------|----------------|---------------|
| English | BSB | 270,398 | 115,008 |
| English | YLT | 437,265 | 127,902 |
| Spanish | RV09 | 257,188 | 117,388 |
| French | LSG | 203,597 | - |
| Arabic | AVD | 257,724 | - |
| Hindi | IRVHin | 257,929 | - |
| Russian | RUSSYN | 182,339 | - |

### 1.6 Integration Opportunities

1. **Translation Comparison**: Show how one Hebrew/Greek word is translated across 10+ languages
2. **Translation Variants**: Identify verses with high translation divergence
3. **Semantic Analysis**: Study translation patterns for specific Strong's numbers
4. **Literal vs Dynamic**: Compare literal (YLT) vs dynamic (BSB) alignments
5. **Per-Word Data**: Store all translations aligned to each source word ID

### 1.7 Target Word ID Format

Target IDs use a different format than source IDs:

```
BBCCCVVVWWW
|  |   |  |
|  |   |  └─ Word position (3 digits)
|  |   └──── Verse (3 digits)
|  └──────── Chapter (3 digits)
└─────────── Book (2 digits)
```

**Example**: `01001001003` = Genesis 1:1, word 3

Note: No prefix ('o' or 'n') because target language determines corpus.

## 2. BibleAquifer ACAI Repository

**Repository**: https://github.com/BibleAquifer/ACAI
**Purpose**: Aligned Corpus of Ancient Inscriptions - entity-based biblical annotations
**Data Format**: JSON entity files with word-level references
**Total Files**: 6,644 entity JSON files

### 2.1 Repository Structure

```
/ACAI/
  ├── people/          3,426 files (Aaron, Moses, David, etc.)
  ├── places/          1,418 files (Jerusalem, Egypt, Babylon, etc.)
  ├── deities/            79 files (God, YHWH, Holy Spirit, etc.)
  ├── groups/            307 files (Israelites, Philistines, etc.)
  ├── keyterms/          868 files (Love, Faith, Covenant, etc.)
  ├── fauna/              97 files (Lion, Lamb, Serpent, etc.)
  ├── flora/             104 files (Cedar, Fig Tree, Vine, etc.)
  └── realia/            345 files (Ark, Temple, Altar, etc.)
```

### 2.2 Entity Types

#### 2.2.1 People
Biblical persons with genealogy, roles, and relationships.

**Example**: `people/json/Aaron.json`
- 435 verse references
- Family relationships (father, mother, siblings, children)
- Roles (Husband, Priest, High Priest)
- Tribe affiliation
- Speeches, pronominal references

#### 2.2.2 Places
Geographic locations and regions.

**Example**: `places/json/Jerusalem.json` (file too large, >25k tokens)
- Multiple localizations (English, Hebrew, Greek names)
- Geographic type (city, region, mountain, etc.)
- Historical periods of significance

#### 2.2.3 Deities
Divine beings and spiritual entities.

**Example**: `deities/json/God.json` (file >256KB)
- Thousands of references
- Multiple names/titles
- Theological attributes

#### 2.2.4 Fauna
Animals mentioned in scripture.

**Example**: `fauna/json/Lion.json`
- 203 verse references
- Hebrew lemmas: אַרְיֵה, כְּפִיר, לִבְאָה, לָבִיא, לַיִשׁ, שַׁחַל
- Greek lemmas: λέων
- UBS taxonomy references

#### 2.2.5 Flora
Plants, trees, and vegetation.

**Example**: `flora/json/Cedar.json`
- 121 verse references
- Hebrew lemma: אֶרֶז
- Flora type: "Wild Trees and Shrubs"
- UBS flora taxonomy: `flora:1.5`

#### 2.2.6 Keyterms
Theological and conceptual terms.

**Example**: `keyterms/json/Love.json`
- Hebrew lemmas: אהב, אַהֲבָה
- Greek lemmas: ἀγαπάω, ἀγάπη
- UBS lexicon references (UBSDGNT, UBSDBH)
- 200+ verse references

#### 2.2.7 Realia
Cultural objects, artifacts, and concepts.

**Example**: `realia/json/Ark_of_the_Covenant.json` (file doesn't exist in sample)
**Sample files**: AHalfShekel.json, Altar.json, AnointingOil.json

### 2.3 Entity Data Structure

#### Common Fields (All Entity Types)

```json
{
  "id": "entity_type:Name",
  "primary_id": "entity_type:Name",
  "type": "entity_type",
  "localizations": {
    "eng": {
      "preferred_label": "Label",
      "alternate_labels": ["Alternative"],
      "descriptions": [...]
    }
  },
  "lemmas": {
    "he": ["Hebrew lemmas"],
    "el": ["Greek lemmas"]
  },
  "key_references": ["BBCCCVVV"],
  "references": ["BBCCCVVV", ...],
  "explicit_instances": {
    "wlc": [["word_id"]],
    "SBLGNT": [["word_id"]]
  }
}
```

#### Word-Level References

**Four types of word references:**

1. **explicit_instances**: Direct mentions of the entity
2. **pronominal_referents**: Pronouns referring to the entity
3. **subject_referents**: Subject references (implicit)
4. **speeches**: Words spoken by the entity (people only)

### 2.4 Example: Aaron (Person)

```json
{
  "id": "person:Aaron",
  "type": "person",
  "gender": "male",
  "father": "person:Amram",
  "mother": "person:Jochebed",
  "partners": ["person:Elisheba"],
  "offspring": ["person:Nadab", "person:Abihu", "person:Eleazar.2", "person:Ithamar"],
  "siblings": ["person:Moses", "person:Miriam"],
  "roles": ["Husband", "Priest", "High Priest"],
  "tribe": "group:Levi",
  "key_references": ["02004027", "03008012", "04020028", "58009004"],
  "references": [435 verse IDs],
  "explicit_instances": {
    "wlc": [
      ["o020040140071"],  // Exodus 4:14, word 71
      ["o020040270041"],  // Exodus 4:27, word 41
      ...
    ],
    "SBLGNT": [
      ["n42001005022"],  // Luke 1:5, word 22
      ["n44007040003"],  // Acts 7:40, word 3
      ...
    ]
  },
  "pronominal_referents": {
    "wlc": [["o020040140141"], ...]  // Pronouns referring to Aaron
  },
  "speeches": {
    "wlc": [{
      "quote_type": "Normal",
      "words": ["o020050010081", "o020050010091", ...]  // Aaron's spoken words
    }]
  }
}
```

### 2.5 Example: Lion (Fauna)

```json
{
  "id": "fauna:Lion",
  "type": "fauna",
  "fauna_type": "Mammals",
  "ubsdbh": ["000682001001000", "003399001001000", ...],
  "ubsdgnt": ["4.14"],
  "lemmas": {
    "he": ["אַרְיֵה", "כְּפִיר", "לִבְאָה", "לָבִיא", "לַיִשׁ", "שַׁחַל"],
    "el": ["λέων"]
  },
  "localizations": {
    "eng": {
      "preferred_label": "Lion",
      "alternate_labels": ["Lioness"],
      "descriptions": [{
        "description": "A huge cat with yellowish fur and a mane on males, known for its strength and fearlessness."
      }]
    }
  },
  "key_references": ["01049009", "11013024", "66005005"],
  "references": [203 verse IDs],
  "explicit_instances": {
    "wlc": [
      ["o010490090021"],
      ["o010490090092"],
      ...
    ],
    "SBLGNT": [
      ["n55004017024"],
      ["n58011033012"],
      ...
    ]
  }
}
```

### 2.6 Example: Cedar (Flora)

```json
{
  "id": "flora:Cedar",
  "type": "flora",
  "flora_type": "Wild Trees and Shrubs",
  "ubsdbh": ["000671001001000"],
  "lemmas": {
    "he": ["אֶרֶז"]
  },
  "key_references": ["07009015", "11005013", "38011001"],
  "references": [121 verse IDs],
  "explicit_instances": {
    "wlc": [
      ["o030140040101"],  // Leviticus 14:4
      ["o030140060082"],  // Leviticus 14:6
      ...
    ]
  },
  "pronominal_referents": {
    "wlc": [
      ["o120140090212"],  // Pronouns referring to cedar
      ...
    ]
  }
}
```

### 2.7 UBS Lexicon References

ACAI links to United Bible Societies lexicon numbering:

**UBSDBH** (Hebrew):
- Format: 15-digit code
- Example: `000671001001000` (Cedar)

**UBSDGNT** (Greek):
- Format: Semantic domain number
- Example: `25.43` (Love)

**UBS Fauna/Flora**:
- Format: `fauna:X.Y` or `flora:X.Y`
- Example: `fauna:2.24` (Lion), `flora:1.5` (Cedar)

### 2.8 Integration Opportunities

1. **Entity Annotations**: Link every word to entities it references
2. **Pronoun Resolution**: Identify what pronouns refer to
3. **Speaker Attribution**: Track who said what words
4. **Thematic Analysis**: Find all verses mentioning specific entities
5. **Semantic Networks**: Map relationships between entities
6. **Multilingual Labels**: Provide entity names in multiple languages
7. **Taxonomy Integration**: Link UBS taxonomies to word data

## 3. Integration Architecture

### 3.1 Word ID as Universal Key

```
Word ID: o020040140071
    ↓
├─ morphhb:      Morphology, Hebrew text, parsing
├─ BibleHub:     Strong's, lexicon, gloss, definition
├─ Clear-Bible:  Translations in 10+ languages
└─ ACAI:         Entity references (Aaron)
```

### 3.2 Data Flow

```
User Query: "Exodus 4:14"
    ↓
1. Get word IDs for verse (from morphhb)
    → ["o020040140071", "o020040140072", ...]
    ↓
2. For each word ID, fetch:
    ├─ Morphology (morphhb_extractor.py)
    ├─ Lexicon data (biblehub_strongs.py)
    ├─ Alignments (Clear-Bible JSON)
    └─ Entity refs (ACAI JSON)
    ↓
3. Merge and return comprehensive word data
```

### 3.3 Proposed Data Schema (Per Word)

```yaml
word_id: o020040140071
reference:
  book: Exodus
  book_code: EXO
  chapter: 4
  verse: 14
  word_position: 71

# From morphhb
text: אַהֲרֹ֣ן
transliteration: 'a·hă·rōn
lemma: אַהֲרֹן
morphology:
  strongs: H175
  parsing: Noun: Proper name masculine

# From BibleHub
lexicon:
  gloss: Aaron
  definition: "Moses' brother, Israel's first high priest"
  usage_frequency:
    total: 348

# From Clear-Bible Alignments
alignments:
  eng_BSB: ["02004014015"]     # "Aaron"
  eng_YLT: ["02004014019"]     # "Aaron"
  spa_RV09: ["02004014016"]    # "Aarón"
  fra_LSG: ["02004014014"]     # "Aaron"

# From ACAI
entities:
  people:
    - id: person:Aaron
      role: subject
      reference_type: explicit_instance
      relationships:
        sibling: person:Moses
        father: person:Amram
        roles: [Priest, High Priest]
```

### 3.4 File Organization

#### Option A: Word-Centric (Recommended)

```
./bible/words/heb/02/o020040140071.yaml
./bible/words/grk/43/n43003016001.yaml
```

Each file contains complete word data from all sources.

#### Option B: Hybrid (Verse + Word)

```
./bible/EXO/4/14/EXO-4-14-context.yaml        # Verse-level commentary
./bible/words/heb/02/o020040140071.yaml       # Word-level data
```

Verse files for human commentary, word files for structured data.

## 4. Implementation Roadmap

### Phase 1: Data Extraction (1 week)

- [ ] Clone/download ACAI repository locally
- [ ] Clone/download Clear-Bible Alignments repository locally
- [ ] Build ACAI entity search/query tool
- [ ] Build alignment extraction tool
- [ ] Test with sample verses

### Phase 2: Integration (1-2 weeks)

- [ ] Extend lexicon-bible skill to include alignment data
- [ ] Add ACAI entity resolution
- [ ] Design unified YAML output format
- [ ] Implement word-ID-based file generation

### Phase 3: Data Generation (2-3 weeks)

- [ ] Generate word files for entire Bible (~161,000 files)
- [ ] Validate data completeness
- [ ] Build search/query tools
- [ ] Create usage documentation

### Phase 4: Enhancement (ongoing)

- [ ] Add translation comparison features
- [ ] Implement entity network visualization
- [ ] Integrate additional lexicons (Young's, Thayer's)
- [ ] Add semantic domain analysis
- [ ] Build verse-to-word navigation tools

## 5. Sample Queries

### Query 1: "Show me all data for Exodus 4:14, word 71"

**Word ID**: `o020040140071`

**Returns**:
- Morphology: אַהֲרֹ֣ן (Aaron)
- Strong's: H175
- Entity: person:Aaron (with family tree, roles, all references)
- Translations: Aaron (English), Aarón (Spanish), etc.
- Context: This is Aaron's first mention in Exodus 4

### Query 2: "Where is 'Lion' mentioned in the Bible?"

**Search ACAI**: `fauna:Lion`

**Returns**:
- 203 verse references
- 6 Hebrew lemmas, 1 Greek lemma
- Word IDs for all 203+ explicit instances
- For each word ID, can fetch full lexical data

### Query 3: "How is Genesis 1:1 translated across languages?"

**Word ID**: `o010010010011` (בְּרֵאשִׁית)

**Returns**:
- English BSB: "In the beginning" (words 1-3)
- Spanish RV09: "principio" (word 3)
- French LSG: "commencement" (word 2)
- 7+ other language alignments

### Query 4: "Show me all words spoken by Aaron"

**ACAI Query**: `person:Aaron` → `speeches.wlc`

**Returns**:
- All word IDs from Aaron's speeches
- Can fetch full text and translation for each

## 6. Technical Considerations

### 6.1 Data Volume

- **morphhb**: ~23,000 Hebrew words, ~138,000 Greek words
- **ACAI**: 6,644 entity files
- **Alignments**: ~1.5M alignment records across all languages
- **Generated word files**: ~161,000 YAML files (estimated 5-20KB each = 1-3GB total)

### 6.2 Performance

- Word ID lookups: O(1) with file path construction
- Entity searches: Require indexing (build entity→word_id map)
- Alignment queries: Pre-load into SQLite or similar

### 6.3 Caching Strategy

```python
# Cache structure
cache/
  ├── acai_index.json           # Entity ID → word IDs map
  ├── alignment_index.db        # SQLite: word_id → translations
  ├── strongs_cache/            # BibleHub Strong's data
  └── morphhb_cache/            # Processed morphhb data
```

## 7. Conclusion

Both Clear-Bible Alignments and ACAI provide rich, complementary data that integrates seamlessly via the universal word ID system. This enables:

✅ **Multi-language translation comparison** (10+ languages)
✅ **Entity-based biblical study** (6,644 entities)
✅ **Word-level precision** (161,000 unique words)
✅ **Standardized data model** (universal word IDs)
✅ **Scalable architecture** (word-centric file organization)

The integration of these data sources transforms the lexicon-bible skill from a simple lexicon lookup tool into a comprehensive biblical word analysis system.

## Appendix A: Reference Verse ID Format

ACAI and alignment metadata use a compact verse reference format:

```
BBCCCVVV
|  |   |
|  |   └─ Verse (3 digits)
|  └───── Chapter (3 digits)
└──────── Book (2 digits)
```

**Examples**:
- `01001001` = Genesis 1:1
- `02004014` = Exodus 4:14
- `43003016` = John 3:16

This is different from word IDs but related (word IDs add 4-digit word position).

## Appendix B: Alignment Quality Levels

**Manual alignments**: Human-verified, high quality
- Marked with `"origin": "manual"`
- More accurate but fewer available

**Automatic alignments**: Algorithm-generated, variable quality
- Marked with `"origin": "automatic"`
- More comprehensive but may have errors

**Status indicators**:
- `"status": "created"` - Initial alignment
- `"status": "reviewed"` - Human-verified
- `"status": "approved"` - Finalized

## Appendix C: Book Number Reference

| Code | Book | Hebrew/Greek |
|------|------|--------------|
| 01 | Genesis | Hebrew |
| 02 | Exodus | Hebrew |
| ... | ... | ... |
| 39 | Malachi | Hebrew |
| 40 | Matthew | Greek |
| 41 | Mark | Greek |
| ... | ... | ... |
| 66 | Revelation | Greek |
