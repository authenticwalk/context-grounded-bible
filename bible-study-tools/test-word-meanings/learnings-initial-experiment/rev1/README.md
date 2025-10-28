# Schema: Test Word Meanings - Revision 1

## Tool Purpose

Analyzes the meanings of original language words in their verse context, showing how different translations handle key theological terms.

## YAML Schema

This tool generates YAML files with the following structure:

```yaml
verse: BOOK.CCC.VVV  # Required, zero-padded

source:
  language: [GRC|HEB]  # Original language code
  text: "[Text]" {source-id}  # With citation

# Add tool-specific fields here following SCHEMA.md standards
# Examples:
# - words: Word-level analysis
# - clusters: Semantic groupings
# - translations: Translation patterns
# - theological: Theological insights
# - cross_refs: Related verses

# All content must include inline citations {source-id}
```

## Field Descriptions

### Required Fields

- `verse`: Verse reference in format BOOK.CCC.VVV (per STANDARDIZATION.md)

### Optional Fields

[Describe the specific fields this tool generates]

## Citation Format

Per SCHEMA.md, all content uses inline citation:
- `{grc-NA28-1993}` - Greek Nestle-Aland 28th edition
- `{heb-BHS-1997}` - Hebrew Biblia Hebraica Stuttgartensia
- `{llm-cs45}` - LLM analysis (Claude Sonnet 4.5)
- `{eng-NIV-2011}` - English NIV 2011
- `{manual}` - Human curation

## Output Example

```yaml
verse: JHN.001.001

source:
  language: GRC
  text: "Ἐν ἀρχῇ ἦν ὁ λόγος" {grc-NA28-1993}

analysis:
  insight: "Key insight here" {llm-cs45}
```

---

**Revision:** 1
**Experiment:** initial-experiment
**Created:** 2025-10-28
