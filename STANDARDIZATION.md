# Format Standardization - eBible/USFM 3.0 Alignment

---

## Purpose

Align our Bible text organization with established standards from:
- **eBible corpus** (BibleNLP): https://github.com/BibleNLP/ebible
- **USFM 3.0 specification**: Standard book codes
- **ISO-639 language codes**: Standard language identification

---

## Standards Adopted

### 1. Book Codes (USFM 3.0)

**Format:**3-letter uppercase codes per USFM 3.0 specification

**Examples:**
- Matthew: `MAT` (not `mt` or `Matt`)
- Genesis: `GEN`
- Revelation: `REV`

**Source:** https://ubsicap.github.io/usfm/identification/books.html

### 2. Language Codes (ISO-639-3)

**Format:** 3-letter lowercase codes per ISO-639-3 standard

**Rationale:** Biblical scholarship uses ISO-639-3 for ancient languages and better granularity

**Common codes:**
```yaml
eng: English
spa: Spanish
fra: French
deu: German (Deutsch)
por: Portuguese
rus: Russian
zho: Chinese
kor: Korean
ara: Arabic
grc: Ancient Greek
heb: Biblical Hebrew
lat: Latin
```

**Note:** We use ISO-639-3 (3 letters) instead of ISO-639-1 (2 letters) because:
- Ancient languages like `grc` (Ancient Greek) have no ISO-639-1 equivalent
- Consistency across modern and ancient languages
- Standard in biblical text repositories

### 3. Directory Structure

**Format:** `/bible/{BOOK}/{chapter}/{BOOK}.{chapter}.{verse}-{type}.yaml`

**Examples:**
```
/bible/MAT/5/MAT.5.3-translations.yaml
/bible/MAT/5/MAT.5.3-semantic-clusters.yaml
/bible/GEN/1/GEN.1.1-translations.yaml
```

**Rationale:**
- Book code visible in filename (easier to identify files out of context)
- Period separators for chapter.verse (standard in biblical references)
- Hyphen before type descriptor (translations, semantic-clusters, etc.)

### 4. Translation Version Keys (Incremental Format)

**Format:** Incremental specificity as needed: `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

**Principles:**
1. Use minimum specificity needed to uniquely identify the translation
2. Add components only when disambiguation is required
3. Maintain consistency within language families

**Examples:**
```yaml
# Single translation in language (language code only)
ara: "Standard Arabic translation"
heb: "Standard Hebrew text"

# Multiple translations, no version conflict (language + version)
eng-niv: "New International Version"
eng-kjv: "King James Version"
eng-esv: "English Standard Version"

# Same version, different years (language + version + year)
eng-niv-1984: "NIV 1984 edition"
eng-niv-2011: "NIV 2011 edition"
spa-rv-1909: "Reina Valera 1909"
spa-rv-1960: "Reina Valera 1960"
```

**Components (add incrementally as needed):**
1. `lang`: ISO-639-3 language code (3 letters, lowercase) - **REQUIRED**
2. `version`: Translation abbreviation (UPPERCASE: NIV, ESV, KJV, etc.) - add when multiple translations exist
3. `year`: Publication year (4 digits) - add only when same version has multiple editions

**Version Code Standards:**
- Version abbreviations: UPPERCASE (NIV, KJV, ESV, RV, NA28)
- Language codes: lowercase (eng, spa, grc, heb)
- Separator: hyphen (`-`)
- No redundancy: Don't repeat language in version (❌ `eng-engNIV`, ✅ `eng-NIV`)

**Rationale:**
- Minimal format reduces verbosity for unique translations
- Year precision only when needed (NIV 1984 vs 2011 has significant differences)
- Matches eBible corpus naming conventions
- Easy to extend when disambiguation needed

---

## Migration from Previous Format

### Changed Elements:

| Element | Old Format | New Format | Example |
|---------|-----------|------------|---------|
| Book code | `mt` (2 letters, lowercase) | `MAT` (3 letters, uppercase) | Matthew |
| Verse reference | `mt-5-3` | `MAT.5.3` | Matthew 5:3 |
| Directory | `/bible/mt/5/` | `/bible/MAT/5/` | Matthew chapter 5 |
| Filename | `MAT.5.003-translations.yaml` | `MAT.5.3-translations.yaml` | Verse data |
| Semantic clusters | `MAT.5.003-semantic-clusters.yaml` | `MAT.5.3-semantic-clusters.yaml` | Cluster data |

### Unchanged Elements:

- Language codes: Already using ISO-639-3 ✅
- Translation key format: Already detailed ✅
- YAML structure: No changes needed ✅
- Citation system: No changes needed ✅

---

## Benefits

1. **Interoperability:** Compatible with eBible corpus and other Bible NLP tools
2. **Clarity:** USFM 3.0 codes are unambiguous (MAT vs mt vs Matt vs Matthew)
3. **Standard compliance:** Aligns with existing biblical scholarship infrastructure
4. **Future-proofing:** Easy integration with external Bible text sources
5. **Professional consistency:** Matches established open-source Bible projects

---

## References

- **eBible corpus:** https://github.com/BibleNLP/ebible
- **USFM 3.0 book codes:** https://ubsicap.github.io/usfm/identification/books.html
- **ISO-639-3 codes:** https://iso639-3.sil.org/code_tables/639/data
- **BibleHub:** https://biblehub.com (translation source)

---

## Implementation Status

- ✅ Standardization documented
- ✅ Directory structure migrated
- ✅ Translation files updated
- ✅ Semantic cluster files updated
- ✅ Planning documents updated
- ✅ Source abbreviations updated

**Date implemented:** 2025-10-04
