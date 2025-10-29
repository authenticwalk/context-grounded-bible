# Fair Use Policy for Copyrighted Biblical Resources

**Version**: 1.0  
**Date**: 2025-10-29  
**Status**: Active

---

## Purpose

The Context-Grounded Bible project creates scholarly tools for comparative translation analysis, linguistic research, and Bible study. This document establishes the methodology for utilizing copyrighted biblical resources (Bible translations, commentaries, lexicons, sermon collections, study notes, and other scholarly materials) in a manner consistent with fair use principles under U.S. Copyright Law (17 U.S.C. § 107) and international copyright frameworks.

---

## Educational and Transformative Purpose

This project serves non-commercial educational purposes by:

1. **Comparative Translation Analysis** - Examining how different translations render source language texts, documenting translation patterns, and analyzing translation philosophy differences
2. **Linguistic Research** - Studying semantic ranges, cross-linguistic patterns, and translation theory applications
3. **Scholarly Commentary** - Creating transformative analysis that enhances understanding of biblical texts and translation practice
4. **Educational Tools** - Developing resources for translators, scholars, pastors, and students that complement and enhance Bible study

The work is transformative in nature, adding substantial scholarly analysis, comparative insights, and linguistic commentary that creates new educational value beyond the original translations.

---

## Methodology for Copyrighted Resources

### Source-Language Anchored Approach

All analysis is **anchored in public domain source texts**:

- **Greek**: Nestle-Aland 28th Edition (NA28), Byzantine/Majority Text, Textus Receptus
- **Hebrew/Aramaic**: Biblia Hebraica Stuttgartensia (BHS), Leningrad Codex, Westminster Leningrad Codex
- **Public Domain Resources**: Strong's Concordance, classical lexicons, morphological databases

Modern copyrighted resources (Bible translations, commentaries, lexicons, sermon illustrations, study notes, etc.) serve as **derivative evidence** of how source language texts can be interpreted and rendered, not as primary content. Bible translations are the primary example of this methodology, but the same principles apply to all copyrighted biblical materials.

### Data Structure Design

The project employs data structures that prevent programmatic reconstruction of any single copyrighted work. This approach is inspired by the [eBible corpus methodology](https://github.com/BibleNLP/ebible/tree/main), which demonstrates how to structure biblical text data for scholarly research while respecting copyright.

**Convergence Documentation**: When multiple translations render source text similarly, they are grouped collectively:

```yaml
source_text:
  greek: "ἐν ἀρχῇ ἦν ὁ λόγος" {grc-na28}

translation_convergence:
  pattern: "In the beginning was the Word"
  translations: [NIV, ESV, NASB, KJV, RSV, NRSV, CSB, NET]
  note: "Near-universal consensus on translation of ἐν ἀρχῇ prologue" {llm-cs45}
```

This approach documents scholarly consensus without extracting individual translation texts.

**Divergence Analysis**: When translations employ different rendering strategies, they are quoted in comparative scholarly context:

```yaml
divergence_analysis:
  focus: "Translation of λόγος in John 1:1"
  
  formal_equivalence:
    rendering: "Word" {niv-2011, esv-2016, nasb-2020, kjv-1769}
    rationale: "Preserves Greek theological terminology" {llm-cs45}
  
  dynamic_equivalence:
    rendering: "Message" {msg-2002}
    analysis: "Contextualizes λόγος for modern readers as divine 
              communication rather than technical theological term" {llm-cs45}
    example: "The Word {msg-2002} was first, the Word {msg-2002} present 
              to God, God present to the Word {msg-2002}. The Word 
              {msg-2002} was God {msg-2002}"
```

This structure presents copyrighted content within transformative comparative analysis rather than as standalone text.

### Programmatic Reconstruction Prevention

The data architecture intentionally prevents simple extraction of any single copyrighted work. Following principles similar to the [eBible corpus](https://github.com/BibleNLP/ebible/tree/main), there is no systematic key-value mapping such as:

```yaml
# NOT USED - would enable reconstruction
translations:
  niv: "verse text..."
  esv: "verse text..."

# Also NOT USED - would enable reconstruction
commentaries:
  barclay: "full commentary text..."
  henry: "full commentary text..."
```

Instead, copyrighted materials appear in:
1. Convergence groups (listed collectively when they agree)
2. Comparative analysis contexts (quoted for scholarly discussion of differences)
3. Semantic clustering (referenced as evidence of interpretive patterns)
4. Summary insights (key points extracted with citations, not full reproduction)

This design ensures the work cannot function as a database substitute for purchasing original copyrighted resources.

---

## Scope of Coverage

### Exhaustive Verse Analysis

The project provides comprehensive coverage of biblical texts (all canonical verses) because:

1. **Scholarly Completeness** - Comparative translation analysis requires systematic coverage to identify patterns, document trends, and support research
2. **Source-Language Primary** - The basis of coverage is public domain Greek/Hebrew texts, not extraction of copyrighted translations
3. **Educational Utility** - Tools are most valuable when comprehensive, enabling users to study any biblical passage
4. **Complementary Function** - The work enhances but does not substitute for Bible ownership

### Selective Quotation Principle

Copyrighted resources (translations, commentaries, etc.) are quoted when:

1. **Divergence is Significant** - Interpretive or translation choices differ meaningfully, warranting scholarly discussion
2. **Comparative Context** - Multiple sources are compared to illustrate interpretive or translation philosophy differences
3. **Pattern Documentation** - Specific renderings or interpretations exemplify broader patterns
4. **Scholarly Analysis** - Quotations support transformative commentary on interpretive decisions

When sources converge on standard renderings or interpretations, they are documented collectively without individual quotation.

---

## Four-Factor Fair Use Analysis

### Factor 1: Purpose and Character of Use

**Educational and Transformative**:
- Non-commercial scholarly research project
- Adds substantial transformative analysis (comparative linguistics, translation theory, semantic analysis)
- Creates new educational value distinct from original translations
- Serves different purpose than original works (analysis vs. reading)

### Factor 2: Nature of Copyrighted Work

**Factual and Scholarly**:
- Bible translations are factual works (translating ancient texts)
- Project uses published works, appropriately cited
- Analysis focuses on translation methodology and linguistic choices, which are appropriate subjects of scholarly examination

### Factor 3: Amount and Substantiality

**Limited and Contextual**:
- No single copyrighted work is used in its entirety
- Copyrighted content appears in convergence groups or divergence analysis contexts
- Quotations are necessary for comparative scholarly analysis
- Amount used is proportionate to scholarly purpose
- Data structure prevents extraction of complete works

### Factor 4: Effect on Market

**Complementary, Not Substitutive**:
- Work requires users to own original resources (translations, commentaries, etc.) for full utility
- Cannot be used as a substitute for reading original works
- Enhances market for biblical resources by serving educational community
- Does not harm publishers' ability to license their works
- Supports biblical scholarship and study, benefiting the entire ecosystem

---

## Open Source and Public Domain Resources

The following categories may be used without restriction:

### Public Domain Bible Translations
- King James Version (KJV, 1769 edition)
- American Standard Version (ASV)
- Darby Translation
- Young's Literal Translation
- Webster's Bible
- World English Bible (WEB)

### Open License Bible Translations
- [eBible.org translations](https://github.com/BibleNLP/ebible/tree/main) (various open licenses)
- Unlocked Literal Bible (ULB)
- Unlocked Dynamic Bible (UDB)
- Free Bible Version

### Public Domain Commentaries and Resources
- Matthew Henry's Commentary (public domain)
- John Gill's Exposition (public domain)
- Albert Barnes' Notes (public domain)
- Strong's Concordance (public domain)
- Classical lexicons (BDB, Thayer's, etc.)

These resources may be quoted extensively, stored systematically, and used as primary examples in analysis.

---


### Proper Citation

Every quotation or reference includes inline source citation per [STANDARDIZATION.md](../../STANDARDIZATION.md):

```yaml
analysis: "Most formal translations render μακάριοι as 'blessed' {niv-2011} 
          {esv-2016} {nasb-2020} {rsv-1971}, preserving Hebrew 'ashrei' 
          influence from OT beatitude patterns {llm-cs45}."

commentary_insight: "Barclay notes the 'anawim' {barclay-dsb-mat-1975} 
                     tradition connects to OT piety patterns {llm-cs45}."
```

See [STANDARDIZATION.md](../../STANDARDIZATION.md) for complete citation standards.

---

## Use Restrictions for Downstream Users

### Not Permitted

Users of this project's outputs may NOT:

1. Extract copyrighted texts (translations, commentaries, etc.) for redistribution
2. Reconstruct complete copyrighted works from project data
3. Remove or alter inline citations and attributions

### Permitted Uses

Users may:

1. Study the comparative analysis for educational purposes
2. Reference analysis in scholarly work with proper attribution
3. Use insights for translation practice and Bible study
4. Build research tools that operate on the transformative analysis
5. Contribute improvements to the scholarly analysis

### License Terms

Project outputs are licensed under:
- **Original Content and Analysis**: MIT License (permissive, AI/ML training friendly)
- **Copyrighted Excerpts**: Fair use only; not for redistribution
- **Full Attribution**: See [ATTRIBUTION.md](../../ATTRIBUTION.md) for all source credits

The MIT License is chosen to maximize reusability, including for AI training datasets, while fair use excerpts remain subject to original copyright holders' terms.

---

## Validation and Review

### Mandatory Fair Use Checks

All tool outputs must pass fair use validation:

1. ✅ **Source-language anchored** - Greek/Hebrew primary, modern resources derivative
2. ✅ **Convergence grouping** - Resources listed collectively when they agree
3. ✅ **Divergence context** - Copyrighted materials quoted in comparative analysis
4. ✅ **Transformative analysis** - Substantial scholarly commentary present
5. ✅ **Anti-reconstruction** - Data structure prevents programmatic extraction
6. ✅ **Complementary use** - Work requires ownership of original resources for full utility
7. ✅ **Proper citation** - Inline citations per STANDARDIZATION.md present

See [REVIEW-GUIDELINES.md](../../REVIEW-GUIDELINES.md) for validation checklist.

### Quality Standards

Fair use is strengthened by high-quality scholarship:

- **Accuracy**: All citations verified against source data files
- **Substance**: Transformative analysis adds genuine educational value
- **Balance**: Multiple translation traditions represented
- **Integrity**: No fabricated data or unsupported claims

---

## Technical Implementation

### Data File Structure

Recommended YAML structure for fair use compliance:

```yaml
verse_reference: "JHN 1:1"

source_text:
  greek: "Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν" {grc-na28}
  
word_analysis:
  - position: 1
    greek: "ἐν"
    lemma: "ἐν"
    strongs: "G1722"
    gloss: "in, on, at, by, with"
    
translation_patterns:
  consensus_rendering: "In"
  translations: [NIV, ESV, NASB, KJV, RSV, NRSV, CSB, NET, WEB, ASV]
  note: "Standard preposition rendering" {llm-cs45}

semantic_clusters:
  - cluster_id: 1
    theme: "Beginning/origin"
    greek_words: ["ἀρχῇ"]
    analysis: |
      Translation convergence on 'beginning' reflects both temporal
      and qualitative aspects of ἀρχή. Most translations {NIV, ESV,
      NASB, KJV consensus} preserve ambiguity allowing both 'starting
      point' and 'first principle' readings. This mirrors Greek
      philosophical usage (cf. Aristotle) while evoking Genesis 1:1
      intertextual connection. {llm-cs45 citing BDAG}
      
comparative_analysis:
  focus: "Translation of λόγος"
  
  formal_approach:
    rendering: "Word" {niv-2011} {esv-2016} {nasb-2020} {kjv-1769}
    rationale: "Maintains Greek theological terminology, allowing
               readers to engage with Johannine Christology through
               established vocabulary" {llm-cs45}
  
  functional_approach:
    rendering: "Message" {msg-2002}
    rationale: "Contextualizes λόγος for contemporary readers as divine
               communication rather than abstract theological concept" {llm-cs45}
    example: "The Word {msg-2002} was first, the Word {msg-2002} present 
             to God, God present to the Word {msg-2002}. The Word 
             {msg-2002} was God {msg-2002}"
```

This structure demonstrates:
- Source language primary (Greek text leads)
- Convergence grouping (listed collectively)
- Transformative analysis (scholarly commentary)
- Comparative context (divergence discussed)
- Proper attribution (inline citations)

---


**Version**: 1.0  
**Effective Date**: 2025-10-29  
**Next Review**: 2026-10-29  
**Maintained By**: Project maintainers and community

