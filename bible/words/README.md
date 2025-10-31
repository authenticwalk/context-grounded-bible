# MyBibleToolbox - Lexicon Data

This repository contains static reference data for Bible word studies, including Strong's Greek and Hebrew dictionaries.

## Repository Structure

```
words/
└── strongs/
    ├── greek/          # Greek Strong's dictionary (G1-G5624)
    └── hebrew/         # Hebrew Strong's dictionary (H1-H8674)
```

## Contents

### Strong's Dictionary

Complete Strong's Concordance data in YAML format:
- **14,197 entries** total
- **Greek entries**: 5,624 words (G1-G5624)
- **Hebrew entries**: 8,674 words (H1-H8674)

Each entry includes:
- Strong's number
- Transliteration
- Pronunciation
- Definition
- Usage notes
- Cross-references

## Data Format

All data is stored in YAML format for both human and AI readability:

```yaml
# Example: words/strongs/greek/G0025.yaml
strongs_number: G25
word: ἀγαπάω
transliteration: agapaō
pronunciation: ag-ap-ah'-o
definition: to love (in a social or moral sense)
usage: |
  Perhaps from agan (much) (or compare Hebrew 'ahab');
  to love (in a social or moral sense)
```

## Usage

### Clone This Repository

**Full clone (63MB):**
```bash
git clone https://github.com/authenticwalk/mybibletoolbox-lexicon
```

**Sparse checkout (clone only what you need):**
```bash
# Clone with minimal data
git clone --filter=blob:none --sparse https://github.com/authenticwalk/mybibletoolbox-lexicon
cd mybibletoolbox-lexicon

# Add only Greek words
git sparse-checkout set words/strongs/greek

# Or add only Hebrew words
git sparse-checkout set words/strongs/hebrew
```

### Access Strong's Data

**Python example:**
```python
import yaml
from pathlib import Path

def get_strongs_entry(number):
    """Load a Strong's dictionary entry."""
    # Determine if Greek (G) or Hebrew (H)
    lang = 'greek' if number.startswith('G') else 'hebrew'

    # Load the YAML file
    file_path = f'words/strongs/{lang}/{number}.yaml'
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# Example usage
entry = get_strongs_entry('G25')  # ἀγαπάω (agapaō - to love)
print(entry['definition'])
```

**Bash example:**
```bash
# Get a specific Strong's entry
cat words/strongs/greek/G0025.yaml

# Search for a word
grep -r "ἀγαπάω" words/strongs/greek/
```

## Data Sources

This data is compiled from:
- Strong's Greek Dictionary of the New Testament
- Strong's Hebrew Dictionary of the Old Testament
- Public domain sources

See [ATTRIBUTION.md](../ATTRIBUTION.md) for full attribution details.

## Updates

This repository contains **static reference data** that rarely changes. Updates occur only for:
- Corrections to existing entries
- Format improvements
- Additional reference data

**Last updated:** 2025-10-31

## Related Repositories

This is part of the MyBibleToolbox project:

- **[mybibletoolbox-code](https://github.com/authenticwalk/mybibletoolbox-code)** - Tools and scripts for Bible study
- **[mybibletoolbox-commentary](https://github.com/authenticwalk/mybibletoolbox-commentary)** - Generated verse commentary data
- **mybibletoolbox-lexicon** (this repo) - Static reference data

## License

This data is released under the MIT License. See [LICENSE](../LICENSE) for details.

Strong's dictionary data is in the public domain.

## Contributing

Found an error or want to improve the data?

1. Fork this repository
2. Make your changes
3. Submit a pull request

Please include:
- Source of the correction
- Explanation of the change
- Affected Strong's numbers

## Support

- **Issues**: https://github.com/authenticwalk/mybibletoolbox-lexicon/issues
- **Main Project**: https://github.com/authenticwalk/mybibletoolbox-code
- **Documentation**: See main project README

---

**Size:** 63MB | **Files:** 14,197 | **Format:** YAML
