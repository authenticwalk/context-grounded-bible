# extract-source-language

Extract source language (Hebrew/Greek) information for a Bible verse using Clear Bible's Macula datasets.

## Skill Type
project

## Description
This skill extracts detailed linguistic information from the original Hebrew or Greek text for a given Bible verse. It uses Clear Bible's Macula Hebrew and Greek datasets to provide:

- Morphological analysis (parts of speech, case, tense, etc.)
- Semantic domain information (meaning classifications)
- Lexical references (Strong's numbers, SDBH IDs)
- Syntactic structure (word order, grammatical roles)
- Translation insights for rare or challenging words

This is particularly valuable for:
1. **Bible translators** - Understanding original language nuances
2. **Pastors/teachers** - Preparing sermons grounded in source text
3. **Bible students** - Deeper study of original languages

## When to Use
Use this skill when the user requests:
- "Extract source language for [verse]"
- "Show me the Hebrew/Greek for [verse]"
- "Analyze the original language of [verse]"
- "What does the Hebrew/Greek say about [verse]?"

## Instructions

When this skill is invoked:

1. **Parse the verse reference** from the user's request
   - Format: "Book Chapter:Verse" (e.g., "John 1:1", "Genesis 1:1")
   - Extract book code, chapter, verse numbers

2. **Check if data is cached**
   - Run: `python bible-study-tools/macula-source-language/macula_fetcher.py --status`
   - If not cached, run: `python bible-study-tools/macula-source-language/macula_fetcher.py --all`

3. **Determine testament**
   - OT books → Hebrew (macula-hebrew)
   - NT books → Greek (macula-greek)

4. **Process the verse**
   - Run: `python bible-study-tools/macula-source-language/macula_processor.py --verse "{BOOK} {C}:{V}"`
   - This generates: `./bible/commentaries/{BBB}/{CCC}/{VVV}/{BBB}-{CCC}-{VVV}-macula.yaml`

5. **Read and present the data**
   - Read the generated YAML file
   - Present key insights to the user:
     - **For translators**: Morphology, semantic domains, rare word handling
     - **For pastors**: Syntactic structure, theological notes, preaching points
     - **For students**: Lexical references, cross-language comparisons

6. **Highlight critical fields**
   - **Hebrew**: state, stem, sdbh, lexdomain, coredomain, greek (for rare words)
   - **Greek**: case, has_article, tense, ln (Louw-Nida), role

7. **Explain uncertainties**
   - If fields have multiple values (arrays), explain scholarly debate
   - For hapax legomena, emphasize Greek LXX insights
   - Provide translation options with rationale

## Example Interactions

### Example 1: Greek Verse
```
User: Extract source language for John 1:1
Assistant: I'll extract the Greek source language data for John 1:1...

[Runs scripts, reads YAML]

John 1:1 Analysis (Greek - Nestle1904):

Key Insights:
1. Word 14 - θεὸς (theos):
   - CRITICAL: No article (anarthrous)
   - Role: Predicate nominative
   - Position: Fronted (before verb)
   - Translation: "God" (qualitative, not "the God")
   - Theological: Affirms divine nature while maintaining personal distinction

2. Word 10 - πρὸς (pros):
   - Case: Governs accusative
   - Louw-Nida: 89.112 (relationship domain)
   - Translation: "with/toward" (face-to-face relationship)

3. Verb ἦν (imperfect, 3x):
   - Tense: Imperfect (continuous past)
   - Meaning: "was already existing" (eternal pre-existence)
   - Contrast: Not aorist (which would mean "came into being")

[Additional details...]
```

### Example 2: Hebrew Verse with Rare Words
```
User: Show me the Hebrew for Job 38:36
Assistant: I'll extract the Hebrew source language data for Job 38:36...

[Runs scripts, reads YAML]

Job 38:36 Analysis (Hebrew - WLC):

This verse contains TWO hapax legomena (words appearing only once):

1. טֻחוֹת (tuchot) - Position 4:
   - Rarity: HAPAX LEGOMENON
   - Multiple scholarly positions:
     * SDBH IDs: 002680001001000, 002680001002000
     * Core domains: 010 (Physical), 106 (Mind/Knowledge)
   - Greek LXX: ὑφάσματος ("woven fabric")
   - Translation options:
     * "inward parts" (KJV, ESV)
     * "heart" (NIV)
     * "innermost being" (NASB)

2. שֶׂכְוִי (sekhvi) - Position 7:
   - Rarity: HAPAX LEGOMENON
   - Greek LXX: ποικιλτικὴν ("variegated, colorful")
   - Translation options:
     * "mind" (ESV, NASB, KJV)
     * "rooster" (NIV!) - based on visual aspect
     * "meteor" (some scholars)

[Additional details...]
```

## Files Created

This skill uses the following files:
- `bible-study-tools/macula-source-language/macula_fetcher.py` - Downloads data
- `bible-study-tools/macula-source-language/macula_processor.py` - Processes XML to YAML
- `bible-study-tools/macula-source-language/MACULA-FIELD-DEFINITIONS.md` - Field documentation
- `bible-study-tools/macula-source-language/YAML-TEMPLATE.yaml` - Output structure

## Data Sources

- **Hebrew**: https://github.com/Clear-Bible/macula-hebrew (WLC/lowfat)
- **Greek**: https://github.com/Clear-Bible/macula-greek (Nestle1904/lowfat)
- **License**: CC BY 4.0
- **Copyright**: Biblica, Inc (2022-2024)

## Output Location

Generated files follow the project structure:
```
./bible/commentaries/{BOOK}/{CHAPTER}/{VERSE}/{BOOK}-{CHAPTER}-{VERSE}-macula.yaml
```

Examples:
- `./bible/commentaries/JHN/001/001/JHN-001-001-macula.yaml`
- `./bible/commentaries/GEN/001/001/GEN-001-001-macula.yaml`

## Error Handling

- If Macula data not cached → Run fetcher script
- If verse not found → Check book code spelling (USFM 3.0)
- If XML parse error → Report issue with specific file
- If no words extracted → Verse may be missing milestone marker

## Notes

- Processing all verses takes significant time (~30-60 minutes)
- Cache is stored in `/tmp/macula` and persists between sessions
- YAML files are human-readable and AI-optimized
- Multiple values in fields indicate scholarly uncertainty (a feature, not a bug!)
