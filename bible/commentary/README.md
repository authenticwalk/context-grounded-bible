# MyBibleToolbox - Commentary Data

This repository contains AI-generated commentary data for Bible verses, organized by book, chapter, and verse.

## Repository Structure

```
commentary/          # Verse-by-verse commentary
├── MAT/            # Matthew
│   ├── 5/          # Chapter 5
│   │   ├── 3/      # Verse 3
│   │   │   ├── MAT-5-3-greek-words.yaml
│   │   │   ├── MAT-5-3-interpretations.yaml
│   │   │   └── ...
commentaries/       # Additional commentary collections
```

## Contents

### Generated Commentary Data

AI-generated analysis for Bible verses:
- **~2.5GB** of commentary data
- **49,508 files** across 68 Bible books
- Multiple commentary types per verse

### Commentary Types

Each verse may have multiple commentary files:

- **`{ref}-greek-words.yaml`** - Original Greek word analysis
- **`{ref}-hebrew-words.yaml`** - Original Hebrew word analysis
- **`{ref}-interpretations.yaml`** - Different interpretations
- **`{ref}-cross-references.yaml`** - Related verses
- **`{ref}-context.yaml`** - Historical and cultural context
- **`{ref}-applications.yaml`** - Practical applications
- And more...

## Data Format

All commentary is stored in YAML format:

```yaml
# Example: commentary/MAT/5/3/MAT-5-3-greek-words.yaml
verse_reference: MAT 5:3
translation: ESV
greek_words:
  - word: μακάριοι
    transliteration: makarioi
    strongs: G3107
    definition: blessed, happy
    usage_in_verse: |
      Describes a state of spiritual well-being and prosperity.
      Not merely happiness, but deep spiritual contentment.
```

## Usage

### Clone This Repository

**⚠️ IMPORTANT:** This repo is 2.5GB. Use sparse checkout to get only what you need!

**Recommended - Sparse checkout by book:**
```bash
# Clone with minimal data
git clone --filter=blob:none --sparse https://github.com/authenticwalk/mybibletoolbox-commentary
cd mybibletoolbox-commentary

# Add only specific books
git sparse-checkout set commentary/MAT commentary/JHN

# Or add commentaries directory
git sparse-checkout add commentaries/PHP
```

**Full clone (NOT recommended - 2.5GB!):**
```bash
git clone https://github.com/authenticwalk/mybibletoolbox-commentary
```

### Access Commentary Data

**Python example:**
```python
import yaml
from pathlib import Path
from glob import glob

def get_verse_commentary(book, chapter, verse):
    """Load all commentary for a specific verse."""
    pattern = f'commentary/{book}/{chapter}/{verse}/*.yaml'
    commentary = {}

    for file_path in glob(pattern):
        file_name = Path(file_path).stem
        with open(file_path, 'r') as f:
            commentary[file_name] = yaml.safe_load(f)

    return commentary

# Example usage
matt_5_3 = get_verse_commentary('MAT', '5', '3')
print(matt_5_3['MAT-5-3-greek-words'])
```

**Bash example:**
```bash
# Get all commentary for Matthew 5:3
cat commentary/MAT/5/3/*.yaml

# Merge all commentary into one file
cat commentary/MAT/5/3/*.yaml > merged-commentary.yaml
```

### Book Codes

Books use USFM 3.0 standard 3-letter codes:

**New Testament:**
- MAT, MRK, LUK, JHN, ACT
- ROM, 1CO, 2CO, GAL, EPH, PHP, COL
- 1TH, 2TH, 1TI, 2TI, TIT, PHM
- HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD, REV

**Old Testament:**
- GEN, EXO, LEV, NUM, DEU
- JOS, JDG, RUT, 1SA, 2SA, 1KI, 2KI
- 1CH, 2CH, EZR, NEH, EST
- JOB, PSA, PRO, ECC, SNG
- ISA, JER, LAM, EZK, DAN
- HOS, JOL, AMO, OBA, JON, MIC, NAM, HAB, ZEP, HAG, ZEC, MAL

## Commentary Generation

This commentary is generated using AI tools from the MyBibleToolbox project.

### How It's Created

1. AI agent analyzes each verse
2. Generates task-specific commentary (Greek words, interpretations, etc.)
3. Data is reviewed and refined
4. Stored in structured YAML format

### Quality Notes

- ✅ Grounded in extensive context and source data
- ✅ Reviewed for accuracy
- ⚠️ AI-generated content - always verify important details
- 📚 Designed to augment, not replace, human study

## Updates

This repository is **actively updated** as new commentary is generated.

**Current coverage:** Partial coverage of Bible books
**Update frequency:** Regular (as commentary is generated)

## Related Repositories

This is part of the MyBibleToolbox project:

- **[mybibletoolbox-code](https://github.com/authenticwalk/mybibletoolbox-code)** - Tools and scripts for Bible study
- **mybibletoolbox-commentary** (this repo) - Generated verse commentary data
- **[mybibletoolbox-lexicon](https://github.com/authenticwalk/mybibletoolbox-lexicon)** - Static reference data (Strong's dictionary)

## Sparse Checkout Patterns

Common patterns for selective checkout:

**New Testament only:**
```bash
git sparse-checkout set \
  commentary/{MAT,MRK,LUK,JHN,ACT,ROM,1CO,2CO,GAL,EPH,PHP,COL,1TH,2TH,1TI,2TI,TIT,PHM,HEB,JAS,1PE,2PE,1JN,2JN,3JN,JUD,REV}
```

**Old Testament only:**
```bash
git sparse-checkout set \
  commentary/{GEN,EXO,LEV,NUM,DEU,JOS,JDG,RUT,1SA,2SA,1KI,2KI,1CH,2CH,EZR,NEH,EST,JOB,PSA,PRO,ECC,SNG,ISA,JER,LAM,EZK,DAN,HOS,JOL,AMO,OBA,JON,MIC,NAM,HAB,ZEP,HAG,ZEC,MAL}
```

**Gospels only:**
```bash
git sparse-checkout set commentary/{MAT,MRK,LUK,JHN}
```

**Paul's letters:**
```bash
git sparse-checkout set commentary/{ROM,1CO,2CO,GAL,EPH,PHP,COL,1TH,2TH,1TI,2TI,TIT,PHM}
```

## Size Management

**Tips for managing this large repository:**

1. **Always use sparse checkout** - Don't clone everything
2. **Clone specific books** - Only get what you need for your study
3. **Use `--filter=blob:none`** - Reduces initial clone size
4. **Clean up occasionally** - `git gc` to optimize

**Size breakdown:**
- commentary/: ~2.3GB (30,966 files)
- commentaries/: ~246MB (18,542 files)

## License

This generated commentary is released under the MIT License. See [LICENSE](../LICENSE) for details.

## Contributing

Want to improve the commentary generation?

1. See the main [mybibletoolbox-code](https://github.com/authenticwalk/mybibletoolbox-code) repo
2. Improve the tools and generators
3. Submit pull requests to enhance commentary quality

## Support

- **Issues**: https://github.com/authenticwalk/mybibletoolbox-commentary/issues
- **Main Project**: https://github.com/authenticwalk/mybibletoolbox-code
- **Documentation**: See main project README

---

**Size:** ~2.5GB | **Files:** ~49,508 | **Format:** YAML | **Status:** Actively Growing
