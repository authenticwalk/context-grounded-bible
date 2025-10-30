# TBTA (The Bible Translator's Assistant) Processor

Processes TBTA database export files into structured YAML commentary files for the Context-Grounded Bible project.

## Overview

TBTA is a rules-based Bible translation assistance tool that encodes detailed cross-linguistic features to help translators working in languages with grammatical categories that differ from English. This processor extracts TBTA data from JSON export files and converts it to our YAML format.

## Data Source

- **Source**: [AllTheWord/tbta_db_export](https://github.com/AllTheWord/tbta_db_export)
- **License**: Check repository for licensing details
- **Format**: JSON export from TBTA databases

## Prerequisites

Clone the TBTA database export:

```bash
cd /tmp
git clone https://github.com/AllTheWord/tbta_db_export.git
```

## Usage

### Process Specific Verses

```bash
# Single verse
python src/lib/tbta/tbta_processor.py --verse "GEN 1:1"

# Single chapter
python src/lib/tbta/tbta_processor.py --chapter "GEN 1"

# Entire book
python src/lib/tbta/tbta_processor.py --book GEN

# All verses (entire Bible)
python src/lib/tbta/tbta_processor.py --all
```

### Test Without Writing Files

```bash
# Dry run on Genesis 1
python src/lib/tbta/tbta_processor.py --chapter "GEN 1" --dry-run
```

## Output Format

Generated files follow this structure:

```
./bible/commentaries/{BOOK}/{CHAPTER}/{VERSE}/{BOOK}-{CHAPTER}-{VERSE}-tbta.yaml
```

**Examples:**
- `./bible/commentaries/GEN/001/001/GEN-001-001-tbta.yaml`
- `./bible/commentaries/MAT/005/003/MAT-005-003-tbta.yaml`

## Output Structure

```yaml
source: tbta
version: 1.0.0
verse: GEN 1:26
clauses:
  - children:
      - Constituent: God
        Part: Noun
        Number: Trial              # Exactly 3 persons
        Person: First Inclusive    # "we" including listener
        Participant Tracking: Routine
        Participant Status: Not Applicable
        Semantic Role: Most Agent-like
        # ... more fields
      - Part: VP
        children:
          - Constituent: create
            Part: Verb
            Time: Historic Past
            Aspect: Unmarked
            Mood: Indicative
            # ... more fields
    Part: Clause
    Discourse Genre: Climactic Narrative Story
    Illocutionary Force: Suggestive 'let's'
    Speaker: God
    Listener: God
    # ... more clause-level fields
```

## Key TBTA Features

### 1. Number Systems
Beyond singular/plural:
- **Singular**: One item
- **Dual**: Exactly 2
- **Trial**: Exactly 3 (e.g., Trinity in Gen 1:26)
- **Quadrial**: Exactly 4
- **Paucal**: A few
- **Plural**: Many

### 2. Person Systems
Beyond 1st/2nd/3rd:
- **First Inclusive**: "we" including listener
- **First Exclusive**: "we" excluding listener
- **First as Third**, **Second as Third**, etc.

### 3. Participant Tracking
Tracks entity flow through discourse:
- **First Mention**: Newly introduced
- **Routine**: Established participant
- **Exiting**: Leaving narrative
- **Restaging**: Reintroduced after absence
- **Frame Inferable**: Can be inferred from context

### 4. Proximity Systems
Demonstrative distinctions:
- **Near Speaker/Listener**
- **Remote within Sight / out of Sight**
- **Temporally Near / Remote**
- **Contextually Near**

### 5. Time Granularity
20+ temporal distinctions:
- Immediate Past
- Earlier Today
- Yesterday
- 2-7 Days Ago
- Weeks/Months/Years Ago
- Historic Past / Eternity Past

### 6. Speaker Demographics
- Speaker's Age (Young Adult, Middle Aged, Old, etc.)
- Speaker-Listener Age Relationship
- Speech Style (Formal, Informal, etc.)
- Speaker's Attitude

## Use Cases

### For Translation Into Languages With:

1. **Number systems beyond singular/plural** (Polynesian, Austronesian languages)
   - Example: Kilivila has dual, trial, quadrial

2. **Inclusive/exclusive distinction** (Tagalog, Malay, Fijian, many others)
   - Example: Tagalog "tayo" (inclusive) vs "kami" (exclusive)

3. **Switch-reference marking** (Native American, Papua New Guinea languages)
   - Tracks which participant is subject/object across clauses

4. **Complex demonstrative systems** (Japanese, Korean, Spanish)
   - Japanese: これ (near me) / それ (near you) / あれ (far)

5. **Temporal distance marking** (Tagalog, many others)
   - Different verb forms for immediate vs remote past

6. **Social register/honorifics** (Japanese, Korean, Javanese)
   - Age and relationship determine required verb forms

## Comparison with Macula

TBTA and Macula are **complementary**:

| Feature | Macula | TBTA |
|---------|--------|------|
| **Focus** | Source text linguistics | Cross-linguistic translation |
| **Strength** | Morphology, syntax, semantics | Translation edge cases |
| **Data** | Strong's, Louw-Nida, SDBH | Number/person systems, discourse |
| **Question** | "What does Greek/Hebrew say?" | "How to render in language X?" |

**Use both together** for comprehensive AI-grounded translation support.

## Performance

- **Single verse**: < 1 second
- **Genesis 1** (31 verses): < 1 second
- **Entire book**: Seconds to minutes
- **Full Bible**: Several minutes

## Data Quality

TBTA data is **manually created** by linguistic experts:
- ✅ High quality semantic/pragmatic annotation
- ✅ Carefully analyzed discourse structure
- ⚠️ May contain some errors (human-created)
- ⚠️ Not all linguistic features coded in all verses

## Requirements

- Python 3.7+
- PyYAML: `pip install pyyaml`
- TBTA export repository cloned to `/tmp/tbta_db_export`

## Example: Genesis 1:26 - Trinity as Trial Number

```yaml
verse: GEN 1:26
clauses:
  - children:
      - Constituent: God
        Number: Trial           # Exactly 3 persons!
        Person: First Inclusive # "us" includes Trinity members
        # ... God speaking as 3 persons in unity
```

This explicitly encodes the **Trial number** (3 persons) which is critical for translating into languages that distinguish dual/trial/plural.

## License

**Tool**: MIT License (Context-Grounded Bible project)

**Data**: Check [tbta_db_export repository](https://github.com/AllTheWord/tbta_db_export) for TBTA data licensing

## Related Documentation

- Full TBTA analysis: `/plan/tbta-analysis.md`
- Macula processor: `src/lib/macula/README.md`
- TBTA export README: https://github.com/AllTheWord/tbta_db_export
