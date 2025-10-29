# YAML Schema Standard

**Purpose:** Define the standard structure for all Bible verse YAML files. This is a prescriptive standard—all new files must follow these conventions.

**Philosophy:** Standardize common patterns, allow unstructured additions using predictable conventions. Files should be human-readable, machine-parseable, and merge-friendly.

---

## Core Required Field

### Verse Reference (REQUIRED)
```yaml
verse: MAT.005.003
```

**Rules:**
- Field name: `verse` (always, no exceptions)
- Format: `{BOOK}.{chapter}.{verse}` per STANDARDIZATION.md
- Book code: 3-letter UPPERCASE per USFM 3.0
- Zero-padded: 3 digits for chapter and verse (e.g., `005`, `003`)

**Examples:**
```yaml
verse: JHN.011.035  # John 11:35
verse: PSA.023.001  # Psalm 23:1
verse: REV.021.004  # Revelation 21:4
verse: GEN.001.001  # Genesis 1:1
verse: MAT.005.003  # Matthew 5:3
```

---

## Citation Format

**Standard:** All quoted text, explanations, and sources use inline citation in curly braces.

### Format
```
"{content}" {source-id}
```
or
```
|
  Multi-line content that needs citation. {source-id}
```

### Source ID Format
Per STANDARDIZATION.md incremental specificity:
1. `{lang}` - if only one translation in that language
2. `{lang}-{VERSION}` - if multiple translations exist
3. `{lang}-{VERSION}-{year}` - if same version has multiple editions

**Examples:**
```yaml
text: "Jesus wept." {eng-NIV-2011}
note: "Shortest verse in the Bible" {llm-cs45}
rationale: |
  The verb ἐδάκρυσεν means silent tears, distinct from loud wailing. {grc-NA28-1993}
```

**Special Sources:**
- LLM analysis: `{llm-cs45}`, `{llm-gpt4}`, etc.
- Original language texts: `{grc-NA28-1993}`, `{heb-BHS-1997}`
- Strong's Concordance: `{strongs}`
- Database/System: `{dbs}`
- Manual curation: `{manual}`
- Textual variants: `{grc-TR-1550}`, `{grc-WH-1881}`, `{heb-DSS}`

**Multiple Citations:**
```yaml
example: "Blessed are the poor in spirit" {eng-ESV-2016} {eng-NASB-2020}
```

---

## Optional Standard Sections

### Source Text (Optional)

The original language text being analyzed. Optional because some files may only contain translation or analysis data.

```yaml
source:
  language: GRC
  text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-NA28-1993}
```

**Rules:**
- Field name: `source` (not `greek` or `hebrew`—must apply to all verses in the Bible)
- Language: 3-letter UPPERCASE language code per our standard
  - New Testament: `GRC` (Ancient Greek)
  - Old Testament: `HEB` (Biblical Hebrew)
  - Other texts: Use appropriate ISO-639-3 code UPPERCASE (LAT, ARA, SYR, etc.)
- Text: Original language text with inline citation showing which manuscript/edition

**Examples:**

New Testament (Greek):
```yaml
source:
  language: GRC
  text: "μακάριοι οἱ πτωχοὶ τῷ πνεύματι" {grc-NA28-1993}
```

Old Testament (Hebrew):
```yaml
source:
  language: HEB
  text: "יְהוָה רֹעִי לֹא אֶחְסָר" {heb-BHS-1997}
```

Latin Vulgate:
```yaml
source:
  language: LAT
  text: "lacrimatus est Iesus" {lat-VUL-405}
```

Septuagint:
```yaml
source:
  language: GRC
  text: "κύριος ποιμαίνει με" {grc-LXX-250BC}
```

### Alternate Manuscripts (Optional)

When analyzing textual variants, include alternate manuscript readings:

```yaml
source:
  language: GRC
  text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-NA28-1993}

alternates:
  - manuscript: "Textus Receptus"
    language: GRC
    text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-TR-1550}
    note: "Same reading" {manual}
  
  - manuscript: "Codex Sinaiticus"
    language: GRC
    text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-Sin-350}
    note: "Identical to NA28" {manual}
```

**When Variants Differ:**
```yaml
verse: JHN.007.053-008.011

source:
  language: GRC
  text: "[Pericope adulterae omitted in earliest manuscripts]" {grc-NA28-1993}
  note: "Most scholars consider this passage a later addition" {manual}

alternates:
  - manuscript: "Textus Receptus"
    language: GRC
    text: "Καὶ ἐπορεύθησαν ἕκαστος εἰς τὸν οἶκον αὐτοῦ..." {grc-TR-1550}
    note: "Includes full Pericope Adulterae (woman caught in adultery)" {manual}
  
  - manuscript: "Codex Bezae"
    language: GRC
    text: "Καὶ ἐπορεύθησαν ἕκαστος εἰς τὸν οἶκον αὐτοῦ..." {grc-D-400}
    note: "One of few early manuscripts with this passage" {manual}
```

---

## Word-Level Analysis (Optional)

Word-level breakdown is a **separate top-level section**, not nested under `source`. This allows analysis even when source text isn't provided.

### Basic Word List
```yaml
words:
  - pos: 1
    word: "ἐδάκρυσεν"
    strongs: G1145
  
  - pos: 2
    word: "ὁ"
    strongs: G3588
  
  - pos: 3
    word: "Ἰησοῦς"
    strongs: G2424
```

**Rules:**
- Field name: `words` (top-level array, sibling to `verse` and `source`)
- Position: Sequential numbering starting at 1
- Word: The actual word in original language
- Strong's numbers: Optional, format `G{number}` (Greek) or `H{number}` (Hebrew)

### Extended Word Analysis

Beyond Strong's numbers, word entries can include rich linguistic data:

```yaml
words:
  - pos: 1
    word: "ἐδάκρυσεν"
    strongs: G1145
    lemma: "δακρύω"
    
    morphology:
      part_of_speech: verb
      tense: aorist
      voice: active
      mood: indicative
      person: 3
      number: singular
    
    gloss: "wept, shed tears" {manual}
    
    semantic:
      domain: "Emotions > Sorrow > Expression"
      field: "grief-manifestation"
    
    syntax:
      function: "main-verb"
      dependents: [2, 3]
    
    alignment:
      eng-NIV-2011: "wept"
      eng-ESV-2016: "wept"
      spa-RVR-1960: "lloró"
  
  - pos: 2
    word: "ὁ"
    strongs: G3588
    lemma: "ὁ"
    
    morphology:
      part_of_speech: article
      case: nominative
      number: singular
      gender: masculine
    
    gloss: "the" {manual}
    
    syntax:
      function: "determiner"
      head: 3
    
    alignment:
      eng-NIV-2011: null  # Article not translated
      eng-ESV-2016: null
      spa-RVR-1960: null
  
  - pos: 3
    word: "Ἰησοῦς"
    strongs: G2424
    lemma: "Ἰησοῦς"
    
    morphology:
      part_of_speech: noun
      proper: true
      case: nominative
      number: singular
      gender: masculine
    
    gloss: "Jesus" {manual}
    
    semantic:
      entity_type: person
      referent: "Jesus of Nazareth"
    
    syntax:
      function: "subject"
      head: 1
    
    alignment:
      eng-NIV-2011: "Jesus"
      eng-ESV-2016: "Jesus"
      spa-RVR-1960: "Jesús"
```

### Word Field Guide

**Core Fields (Minimal):**
- `pos`: Position number (required)
- `word`: The word itself (required)
- `strongs`: Strong's number (optional but recommended)
- `lemma`: Dictionary form (optional)

**Morphological Analysis (Optional):**
- `part_of_speech`: verb, noun, adjective, article, pronoun, etc.
- For **verbs**: `tense`, `voice`, `mood`, `person`, `number`
- For **nouns**: `case`, `number`, `gender`, `proper` (boolean)
- For **adjectives**: `case`, `number`, `gender`, `degree` (positive/comparative/superlative)
- For **pronouns**: `case`, `number`, `gender`, `person`, `type` (personal/demonstrative/relative/etc.)
- For **participles**: `tense`, `voice`, `case`, `number`, `gender`

**Semantic Analysis (Optional):**
- `gloss`: English meaning with citation
- `domain`: Semantic domain hierarchy (e.g., "Actions > Motion > Vertical")
- `field`: Semantic field (e.g., "spatial-movement")
- `entity_type`: For proper nouns (person, place, deity, etc.)
- `referent`: Specific referent identification

**Syntactic Analysis (Optional):**
- `function`: Grammatical function (subject, object, verb, modifier, etc.)
- `head`: Position number of syntactic head (what this word modifies or depends on)
- `dependents`: Array of position numbers that depend on this word
- `clause`: Clause number if analyzing clause structure

**Translation Alignment (Optional):**
- Map to specific words in target translations
- Format: `{lang-VERSION-year}: "translated_word"`
- Use `null` when word isn't explicitly translated

**Discourse/Pragmatic Analysis (Optional):**
- `topic`: Theme or topic marker
- `focus`: Focus/emphasis marker
- `given_new`: Information structure (given/new)
- `connective`: Discourse connector function

**Examples of Different Language Morphology:**

Hebrew verb:
```yaml
- pos: 2
  word: "רֹעִי"
  strongs: H7462
  lemma: "רָעָה"
  
  morphology:
    part_of_speech: verb
    stem: qal
    conjugation: participle
    number: singular
    gender: masculine
    state: construct
  
  gloss: "shepherd (of me)" {manual}
  
  suffix:
    type: pronominal
    person: 1
    number: singular
    meaning: "my"
```

Greek participle:
```yaml
- pos: 3
  word: "πενθοῦντες"
  strongs: G3996
  lemma: "πενθέω"
  
  morphology:
    part_of_speech: participle
    tense: present
    voice: active
    case: nominative
    number: plural
    gender: masculine
  
  gloss: "mourning (ones)" {manual}
  
  syntax:
    function: substantival-participle
    substantivized_by: 2  # position of article
```

---

## Translation Files

### Complete Structure
```yaml
verse: MAT.005.003

source:
  language: GRC
  text: "μακάριοι οἱ πτωχοὶ τῷ πνεύματι, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν" {grc-NA28-1993}

translations:
  eng-NIV-2011: "Blessed are the poor in spirit, for theirs is the kingdom of heaven."
  eng-ESV-2016: "Blessed are the poor in spirit, for theirs is the kingdom of heaven."
  eng-KJV-1769: "Blessed are the poor in spirit: for theirs is the kingdom of heaven."
  eng-NLT-2015: "God blesses those who are poor and realize their need for him, for the Kingdom of Heaven is theirs."
  spa-RVR-1960: "Bienaventurados los pobres en espíritu, porque de ellos es el reino de los cielos."
  fra-LSG-1910: "Heureux les pauvres en esprit, car le royaume des cieux est à eux!"
  deu-LUT-1984: "Selig sind, die da geistlich arm sind; denn ihrer ist das Himmelreich."
```

**Rules:**
- `translations` is a flat dictionary/map
- Keys follow incremental specificity standard from STANDARDIZATION.md
- Values are the translated text (no inline citations needed—the key IS the citation)
- All translations at same level (no nesting)

### Minimal Valid Translation File
```yaml
verse: JHN.011.035

translations:
  eng-NIV-2011: "Jesus wept."
  eng-ESV-2016: "Jesus wept."
```

Note: Even the minimal file doesn't require `source`—could be just translations.

---

## Semantic Cluster Files

### Purpose
Semantic clusters group words from the source text that form meaningful units for translation analysis.

### Core Structure
```yaml
verse: JHN.011.035

source:
  language: GRC
  text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-NA28-1993}

words:
  - pos: 1
    word: "ἐδάκρυσεν"
    strongs: G1145
  - pos: 2
    word: "ὁ"
    strongs: G3588
  - pos: 3
    word: "Ἰησοῦς"
    strongs: G2424

clusters:
  - id: jesus-wept
    positions: [1, 2, 3]
    text: "ἐδάκρυσεν ὁ Ἰησοῦς"
    
    rationale: |
      Shortest verse in English Bible. The verb ἐδάκρυσεν (aorist of δακρύω) means 
      to shed tears silently, distinct from κλαίω (loud weeping in v33). {llm-cs45}
    
    patterns:
      - rendering: "Jesus wept."
        note: "Standard rendering preserving Greek simplicity" {llm-cs45}
        examples:
          - "Jesus wept." {eng-NIV-2011}
          - "Jesus wept." {eng-ESV-2016}
          - "Jesus wept." {eng-KJV-1769}
      
      - rendering: "Then Jesus wept."
        note: "Adds temporal connector absent in Greek" {llm-cs45}
        examples:
          - "Then Jesus wept." {eng-NLT-2015}
```

### Cluster Fields

#### Required Fields
- `id`: kebab-case identifier unique within this verse
- `positions`: Array of word positions from `words` section
- `text`: The source text for this cluster

#### Optional Standard Fields
- `rationale`: Multi-line explanation with citations
- `patterns`: Array of translation pattern objects
- `theological`: Theological analysis (see below)
- `grammatical`: Grammatical analysis (see below)

### Pattern Structure

**⚠️ Important:** The `patterns` field should NOT have a `sources` field. Use `examples` array with inline citations instead.

**WRONG:**
```yaml
patterns:
  - rendering: "Jesus wept."
    sources: [eng-NIV-2011, eng-ESV-2016]  # ❌ Don't do this
```

**CORRECT:**
```yaml
patterns:
  - rendering: "Jesus wept."
    note: "Universal rendering" {llm-cs45}
    examples:
      - "Jesus wept." {eng-NIV-2011}
      - "Jesus wept." {eng-ESV-2016}
      - "Jesus wept." {eng-KJV-1769}
```

**Pattern Fields:**
- `rendering`: The translation pattern (without citation)
- `note`: Explanation with citation
- `examples`: Array of actual translations with citations

### Theological Section
```yaml
theological:
  debate: "Why does Jesus weep if he knows he'll raise Lazarus?" {llm-cs45}
  
  traditions:
    - name: "Empathy view"
      view: |
        Jesus weeps in solidarity with Mary and Martha's grief, showing divine 
        compassion entering human suffering. {llm-cs45}
    
    - name: "Anger at death view"
      view: |
        Jesus weeps in grief and anger at death's ravages. The word ἐμβριμάομαι 
        (deeply moved, v33) can mean indignant. {llm-cs45}
  
  cross_refs:
    - ref: JHN.011.033
      note: "Mourners wail (κλαίω), Jesus deeply moved" {llm-cs45}
    
    - ref: HEB.004.015
      note: "High priest able to sympathize with weaknesses" {llm-cs45}
  
  pregnant_words:
    - word: "ἐδάκρυσεν"
      note: |
        Not κλαίω (loud wailing in v33) but δακρύω (silent tears). Shows Jesus' 
        controlled emotional response vs mourners' loud grief. {llm-cs45}
```

**Theological Fields:**
- `debate`: Statement of theological question with citation
- `traditions`: Array of different theological interpretations
  - `name`: Short identifier
  - `view`: Explanation with citation
- `cross_refs`: Array of related scripture references
  - `ref`: Reference in `BOOK.chapter.verse` format (zero-padded)
  - `note`: Explanation with citation
- `pregnant_words`: Theologically significant terms
  - `word`: The original language word
  - `note`: Significance explanation with citation

### Grammatical Section
```yaml
grammatical:
  construction: "Aorist active indicative verb + article + proper noun" {llm-cs45}
  
  significance: |
    Aorist ἐδάκρυσεν indicates point action—he wept at that moment. The article ὁ 
    makes Ἰησοῦς definite and emphasizes the subject. Verb-first word order (unusual 
    in Greek) emphasizes the action itself. {llm-cs45}
  
  contrasts:
    - term: "κλαίω (weep/wail)"
      difference: |
        Used for mourners in v33. Louder, more audible grief. Jesus uses δακρύω 
        (silent tears), showing controlled dignity in sorrow. {llm-cs45}
```

**Grammatical Fields:**
- `construction`: Technical grammatical description with citation
- `significance`: Explanation of why grammar matters with citation
- `contrasts`: Array of related terms (optional)
  - `term`: The contrasting word/construction
  - `difference`: Explanation with citation

---

## Prompt Analysis Files

Prompt files follow the same standard structure with additional specialized sections.

### Base Structure (Always the Same)
```yaml
verse: MAT.005.004

source:
  language: GRC
  text: "μακάριοι οἱ πενθοῦντες, ὅτι αὐτοὶ παρακληθήσονται" {grc-NA28-1993}

words:
  - pos: 1
    word: "μακάριοι"
    strongs: G3107
  # ... etc

prompt: convergence-first
```

**Rules:**
- `verse`: Same standard format (zero-padded)
- `source`: Same standard format (optional)
- `words`: Same standard format (optional but recommended)
- `prompt`: Identifies the analysis type (kebab-case)

**Prompt Types:**
- `convergence-first`: Common patterns across translations
- `divergence-first`: Edge cases and variations
- `grammatical-first`: Grammatical construction analysis
- `cultural-typology`: Language family patterns
- `semantic-domains`: Semantic field analysis
- `minimal-pairs`: Contrasting similar terms
- `lexical-richness`: Compression and winner words

### Convergence Analysis
```yaml
clusters:
  - id: those-who-mourn
    positions: [2, 3]
    text: "οἱ πενθοῦντες"
    
    convergence:
      pattern: "those who mourn"
      languages: "Most Indo-European and Semitic languages" {llm-cs45}
      strength: "Very strong consensus" {llm-cs45}
      
      baseline: |
        Present participle construction (ongoing mourning) translated with present 
        tense verbs universally. The intensity of πενθέω (deep mourning) preserved 
        via formal grief terms rather than casual sadness words. {llm-cs45}
      
      examples:
        - "those who mourn" {eng-NIV-2011}
        - "those who mourn" {eng-ESV-2016}
        - "die da Leid tragen" {deu-LUT-1984}
        - "los que lloran" {spa-RVR-1960}
    
    exceptions:
      - pattern: "sad" or "sorrowful"
        usage: "Small minority—accessibility-focused versions" {llm-cs45}
        
        analysis: |
          Lexical downgrade loses mourning's intensity. πενθέω describes deep 
          grief/lamentation, not mild sadness. This shift reduces theological 
          weight of the blessing. {llm-cs45}
        
        risk: "Moderate to high—theological precision lost" {llm-cs45}
```

### Divergence Analysis
```yaml
clusters:
  - id: those-who-mourn
    positions: [2, 3]
    text: "οἱ πενθοῦντες"
    
    divergence:
      - pattern: "mourn for their sins"
        usage: "Very small minority—theologically interpretive" {llm-cs45}
        
        why:
          theological: |
            Reformed tradition reads mourning as repentance grief. Adds cause 
            specification Matthew doesn't provide. {llm-cs45}
        
        strategy:
          type: interpretive-addition
          method: "Add cause specification" {llm-cs45}
        
        preserved: "Mourning concept, intensity of grief" {llm-cs45}
        
        added: "Mourning cause (for their sins), theological interpretation" {llm-cs45}
        
        implications: |
          Matthew's πενθοῦντες is unspecified—could be sin, death, injustice, or 
          God's absence. Adding "for sins" closes interpretive options and imposes 
          one tradition's reading. {llm-cs45}
        
        risk:
          level: high
          necessary: false
          warning: |
            Never add cause specification in translation text. This is interpretation, 
            not translation. Use study notes for interpretation. {llm-cs45}
```

### Grammatical Analysis
```yaml
clusters:
  - id: those-who-mourn
    positions: [2, 3]
    text: "οἱ πενθοῦντες"
    
    grammatical:
      construction:
        structure: article-plus-present-active-participle
        components:
          - word: "οἱ"
            function: "Article nominative plural masculine" {llm-cs45}
            role: "Substantivizer (makes participle function as noun)" {llm-cs45}
          
          - word: "πενθοῦντες"
            function: "Participle present active nominative plural" {llm-cs45}
            role: "Describes ongoing action as characteristic state" {llm-cs45}
      
      significance: |
        Present tense aspect is key. πενθοῦντες (present) ≠ πενθήσαντες (aorist). 
        Present = ongoing action: those who ARE mourning (current, continuous state). 
        Blessing pronounced WHILE mourning continues, not after it ends. {llm-cs45}
      
      preservation:
        - strategy: "Use present tense verbs"
          rendering: "those who mourn" {eng}
          maintains: "Ongoing aspect via matching tense system" {llm-cs45}
        
        - strategy: "Use continuous construction"
          rendering: "those who are mourning" {eng}
          maintains: "Makes ongoing aspect explicit" {llm-cs45}
      
      violations:
        - error: "those who mourned (aorist sense)"
          impact: |
            Changes pastoral message—shifts to past completed action instead of 
            present state. Destroys already/not-yet tension. {llm-cs45}
          severity: critical
```

### Cultural-Typology Analysis
```yaml
clusters:
  - id: those-who-mourn
    positions: [2, 3]
    text: "οἱ πενθοῦντες"
    
    typology:
      - family: indo-european
        subfamilies: "Germanic, Romance, Slavic" {llm-cs45}
        
        pattern:
          rendering: "those who mourn (article + participle/relative clause)"
          structure: "Pronoun/Determiner + Relative/Participial + Verb" {llm-cs45}
          
          examples:
            - lang: eng
              text: "those who mourn"
              structure: "demonstrative + relative clause" {llm-cs45}
            
            - lang: deu
              text: "die da Leid tragen"
              structure: "article + relative + verb phrase" {llm-cs45}
            
            - lang: spa
              text: "los que lloran"
              structure: "article + relative + verb" {llm-cs45}
        
        enables: |
          Indo-European languages preserve participial and relative clause constructions 
          for substantivizing actions. Greek present participle maps naturally. {llm-cs45}
        
        cultural: |
          IE speakers distinguish intensity levels of grief: sadness < sorrow < mourning. 
          This parallels Greek πενθέω (mourn) vs λυπέω (be sad). {llm-cs45}
      
      - family: sino-tibetan
        subfamilies: "Sinitic (Mandarin, Cantonese)" {llm-cs45}
        
        pattern:
          rendering: "哀慟的人 (those of mourning/grief)"
          structure: "Noun/Compound + 的 (attributive) + 人 (people)" {llm-cs45}
          
          examples:
            - lang: cmn
              text: "哀慟的人"
              literal: "mourning/grief's people"
              structure: "grief-compound + attributive + people" {llm-cs45}
        
        enables: |
          Mandarin uses attributive 的 to create descriptive phrases: [ATTRIBUTE] 的 人 
          = "people characterized by [ATTRIBUTE]." {llm-cs45}
        
        cultural: |
          Confucian filial mourning—elaborate mourning rituals, 哀慟 carries filial 
          piety connotations. Mourning is duty and virtue. {llm-cs45}
```

---

## Unstructured Extensions

### Principle
Clusters and analysis can include additional fields not specified above. Follow these rules:

### Rules for Unstructured Data

1. **Use Standard Field Names When Possible**
   - If describing grammatical function: use `grammatical`
   - If describing theological debate: use `theological`
   - If describing translation patterns: use `patterns`
   - Don't invent new top-level cluster fields unless necessary

2. **Follow Well-Known Standards**
   - Grammatical terms: Use standard linguistic terminology (NP, VP, complement, adjunct, etc.)
   - Morphological analysis: Use standard categories (tense, aspect, mood, case, gender, number, etc.)
   - Semantic analysis: Use semantic domain hierarchies (Louw-Nida, etc.)
   - Theological terms: Use standard doctrinal vocabulary
   - Citation format: Always use `{source-id}` for references
   - Multi-line: Use YAML literal block `|` for longer content

3. **Maintain Merge Compatibility**
   - New fields should not conflict with standard field names
   - Use nested objects for complex custom data
   - Keep cluster `id` unique within verse

4. **Examples of Valid Extensions**

Discourse analysis:
```yaml
clusters:
  - id: example
    positions: [1, 2]
    text: "example text"
    
    discourse:
      connection: "Contrasts with previous verse" {llm-cs45}
      particle: "δέ (adversative)" {llm-cs45}
      topic_shift: true
      information_structure:
        given: "Jesus at tomb"
        new: "Jesus' emotional response"
```

Lexical semantic analysis:
```yaml
clusters:
  - id: example
    positions: [1]
    text: "example"
    
    lexical:
      compression_ratio: "2:1"
      winner_word: "compassion"
      analysis: |
        English "compassion" compresses Greek συμπαθέω (συν + πάθος) 
        meaning "suffer with." Single English word captures compound concept. {llm-cs45}
      
      semantic_field:
        domain: "Emotions > Empathy"
        related_terms: ["sympathy", "empathy", "mercy", "pity"]
        louw_nida: "25.49"
```

Syntactic tree analysis:
```yaml
clusters:
  - id: example
    positions: [1, 2, 3]
    text: "example text"
    
    syntax:
      tree: |
        [S [VP [V ἐδάκρυσεν] [NP [Det ὁ] [N Ἰησοῦς]]]]
      
      constituency:
        - type: S
          span: [1, 3]
        - type: VP
          span: [1, 3]
          head: 1
        - type: NP
          span: [2, 3]
          head: 3
      
      dependencies:
        - rel: root
          head: 0
          dep: 1
        - rel: nsubj
          head: 1
          dep: 3
        - rel: det
          head: 3
          dep: 2
```

Textual criticism:
```yaml
clusters:
  - id: example
    positions: [5]
    text: "disputed text"
    
    textual_criticism:
      variant_reading: true
      
      manuscripts_supporting:
        - "Codex Sinaiticus (ℵ, 4th c.)" {manual}
        - "Codex Vaticanus (B, 4th c.)" {manual}
      
      manuscripts_omitting:
        - "Codex Bezae (D, 5th c.)" {manual}
      
      scholarly_consensus: "Likely original reading" {manual}
      
      explanation: |
        The longer reading is found in the earliest and most reliable manuscripts. 
        Omission in Western witnesses likely due to homoioteleuton. {llm-cs45}
```

### Invalid Extensions

❌ **Don't redefine standard fields:**
```yaml
patterns:
  sources: [eng-NIV, eng-ESV]  # Wrong! Use examples with citations
```

❌ **Don't skip citations:**
```yaml
rationale: |
  This is an explanation without any citation.  # Wrong! Always cite
```

❌ **Don't use inconsistent formats:**
```yaml
verse: mt-5-3  # Wrong! Use MAT.005.003 format
verse: MAT.5.3  # Wrong! Need zero-padding
```

❌ **Don't nest words under source:**
```yaml
source:
  language: GRC
  text: "example"
  words:  # Wrong! Words should be top-level, not under source
    - pos: 1
      word: "example"
```

---

## Complete Examples

### Minimal Translation File
```yaml
verse: JHN.011.035

translations:
  eng-NIV-2011: "Jesus wept."
  eng-ESV-2016: "Jesus wept."
  eng-KJV-1769: "Jesus wept."
```

### Standard Translation File with Source
```yaml
verse: JHN.011.035

source:
  language: GRC
  text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-NA28-1993}

translations:
  eng-NIV-2011: "Jesus wept."
  eng-ESV-2016: "Jesus wept."
  eng-KJV-1769: "Jesus wept."
  eng-NLT-2015: "Then Jesus wept."
  spa-RVR-1960: "Jesús lloró."
  fra-LSG-1910: "Jésus pleura."
  deu-LUT-1984: "Und Jesus weinte."
```

### Standard Semantic Cluster File
```yaml
verse: JHN.011.035

source:
  language: GRC
  text: "ἐδάκρυσεν ὁ Ἰησοῦς" {grc-NA28-1993}

words:
  - pos: 1
    word: "ἐδάκρυσεν"
    strongs: G1145
  - pos: 2
    word: "ὁ"
    strongs: G3588
  - pos: 3
    word: "Ἰησοῦς"
    strongs: G2424

clusters:
  - id: jesus-wept
    positions: [1, 2, 3]
    text: "ἐδάκρυσεν ὁ Ἰησοῦς"
    
    rationale: |
      Shortest verse in English Bible (2 words), 3 words in Greek. The verb ἐδάκρυσεν 
      (aorist active of δακρύω) means to shed tears silently, distinct from κλαίω 
      (loud weeping/wailing in v33). This verb choice is theologically significant. {llm-cs45}
    
    patterns:
      - rendering: "Jesus wept."
        note: "Universal rendering preserving Greek simplicity—no connector" {llm-cs45}
        examples:
          - "Jesus wept." {eng-NIV-2011}
          - "Jesus wept." {eng-ESV-2016}
          - "Jesus wept." {eng-NASB-2020}
          - "Jesus wept." {eng-KJV-1769}
      
      - rendering: "Then Jesus wept."
        note: "Adds 'Then' connecting to narrative sequence though absent in Greek" {llm-cs45}
        examples:
          - "Then Jesus wept." {eng-NLT-2015}
    
    theological:
      debate: "Why does Jesus weep if he knows he'll raise Lazarus?" {llm-cs45}
      
      traditions:
        - name: "Empathy/Compassion view"
          view: |
            Jesus weeps in solidarity with Mary/Martha's grief—shows divine compassion 
            entering human suffering. {llm-cs45}
        
        - name: "Anger at death view"
          view: |
            Jesus weeps in grief/anger at death's ravages (v33 'deeply moved' = 
            ἐμβριμάομαι can mean indignant)—grief at sin's consequences. {llm-cs45}
      
      cross_refs:
        - ref: JHN.011.033
          note: "Mourners wail (κλαίω), Jesus deeply moved—contrast loud wailing vs silent tears" {llm-cs45}
        
        - ref: HEB.004.015
          note: "High priest able to sympathize with weaknesses—Jesus' tears demonstrate this" {llm-cs45}
      
      pregnant_words:
        - word: "ἐδάκρυσεν"
          note: |
            Not κλαίω (loud wailing used in v33) but δακρύω (silent tears)—Jesus' 
            controlled emotional response vs mourners' loud grief, showing dignity 
            in sorrow. {llm-cs45}
```

### Old Testament Example with Rich Word Analysis
```yaml
verse: PSA.023.001

source:
  language: HEB
  text: "יְהוָה רֹעִי לֹא אֶחְסָר" {heb-BHS-1997}

words:
  - pos: 1
    word: "יְהוָה"
    strongs: H3068
    lemma: "יְהוָה"
    
    morphology:
      part_of_speech: noun
      proper: true
      state: absolute
    
    gloss: "YHWH, the LORD" {manual}
    
    semantic:
      entity_type: deity
      referent: "Covenant name of God"
  
  - pos: 2
    word: "רֹעִי"
    strongs: H7462
    lemma: "רָעָה"
    
    morphology:
      part_of_speech: verb
      stem: qal
      conjugation: participle
      number: singular
      gender: masculine
      state: construct
    
    suffix:
      type: pronominal
      person: 1
      number: singular
      meaning: "my"
    
    gloss: "shepherd (of me), my shepherd" {manual}
    
    syntax:
      function: predicate-nominative
      head: 1
  
  - pos: 3
    word: "לֹא"
    strongs: H3808
    lemma: "לֹא"
    
    morphology:
      part_of_speech: particle
      type: negative
    
    gloss: "not" {manual}
    
    syntax:
      function: negation
      scope: 4
  
  - pos: 4
    word: "אֶחְסָר"
    strongs: H2637
    lemma: "חָסֵר"
    
    morphology:
      part_of_speech: verb
      stem: qal
      conjugation: imperfect
      person: 1
      number: singular
    
    gloss: "lack, be in want" {manual}
    
    syntax:
      function: main-verb

clusters:
  - id: yhwh-is-my-shepherd
    positions: [1, 2]
    text: "יְהוָה רֹעִי"
    
    rationale: |
      Divine name יְהוָה (YHWH/Yahweh) with possessive form רֹעִי (my shepherd). 
      Creates covenant relationship—personal possession "my shepherd" rather than 
      "a shepherd." The verbless clause (no "is" in Hebrew) creates timeless 
      statement of identity. {llm-cs45}
    
    patterns:
      - rendering: "The LORD is my shepherd"
        note: "Standard small-caps LORD for YHWH, adds copula 'is'" {llm-cs45}
        examples:
          - "The LORD is my shepherd" {eng-NIV-2011}
          - "The LORD is my shepherd" {eng-ESV-2016}
      
      - rendering: "Jehová es mi pastor"
        note: "Spanish uses Jehovah transliteration" {llm-cs45}
        examples:
          - "Jehová es mi pastor" {spa-RVR-1960}
    
    theological:
      debate: "Translation of יְהוָה—preserve divine name or use title?" {llm-cs45}
      
      traditions:
        - name: "Jewish tradition"
          view: |
            Don't pronounce YHWH, substitute Adonai (Lord) in reading—preserves 
            reverence. {llm-cs45}
        
        - name: "Sacred Name movement"
          view: |
            Use Yahweh or Jehovah to preserve actual name rather than title 
            substitution. {llm-cs45}
      
      pregnant_words:
        - word: "יְהוָה"
          note: |
            Covenant name revealed to Moses (Exod 3:14), implies personal relationship 
            and faithfulness, not generic deity. {llm-cs45}
  
  - id: i-shall-not-want
    positions: [3, 4]
    text: "לֹא אֶחְסָר"
    
    rationale: |
      Negative לֹא with imperfect verb אֶחְסָר creates future/ongoing negation. The verb 
      חָסֵר means to lack, be in need, be deficient. Imperfect tense indicates habitual/
      continuous action—"I will not (continually) lack." {llm-cs45}
    
    patterns:
      - rendering: "I shall not want"
        note: "Classic rendering using 'want' in older sense of 'lack,' formal 'shall'" {llm-cs45}
        examples:
          - "I shall not want" {eng-KJV-1769}
          - "I shall not want" {eng-ESV-2016}
      
      - rendering: "I lack nothing"
        note: "Contemporary language replacing archaic 'want' with 'lack'" {llm-cs45}
        examples:
          - "I lack nothing" {eng-NIV-2011}
```

### Prompt Analysis with Textual Variants
```yaml
verse: JHN.005.003-004

source:
  language: GRC
  text: "ἐν ταύταις κατέκειτο πλῆθος τῶν ἀσθενούντων" {grc-NA28-1993}
  note: "Verse 4 omitted in NA28 as later addition" {manual}

alternates:
  - manuscript: "Textus Receptus"
    language: GRC
    text: "ἐν ταύταις κατέκειτο πλῆθος τῶν ἀσθενούντων, τυφλῶν, χωλῶν, ξηρῶν, ἐκδεχομένων τὴν τοῦ ὕδατος κίνησιν. ἄγγελος γὰρ κατὰ καιρὸν κατέβαινεν ἐν τῇ κολυμβήθρᾳ..." {grc-TR-1550}
    note: "Includes verse 4 about angel troubling the water" {manual}
  
  - manuscript: "Codex Sinaiticus"
    language: GRC
    text: "ἐν ταύταις κατέκειτο πλῆθος τῶν ἀσθενούντων" {grc-Sin-350}
    note: "Omits verse 4, agrees with NA28" {manual}

prompt: divergence-first

words:
  - pos: 1
    word: "ἐν"
    strongs: G1722
  - pos: 2
    word: "ταύταις"
    strongs: G3778
  # etc.

clusters:
  - id: sick-at-pool
    positions: [1, 2, 3, 4, 5, 6]
    text: "ἐν ταύταις κατέκειτο πλῆθος τῶν ἀσθενούντων"
    
    divergence:
      - pattern: "Include verse 4 about angel"
        usage: "KJV and other TR-based translations" {llm-cs45}
        
        why:
          textual: |
            Based on Textus Receptus which includes later scribal addition. Not in 
            earliest manuscripts (P66, P75, Sinaiticus, Vaticanus). {manual}
        
        strategy:
          type: textual-variant-inclusion
          method: "Include disputed passage" {llm-cs45}
        
        added: |
          Verse 4: "For an angel of the Lord went down at certain seasons into the 
          pool and stirred up the water..." Explains why people waited at pool. {llm-cs45}
        
        implications: |
          Including verse 4 provides explicit supernatural explanation. Omitting it 
          leaves healing mechanism ambiguous. Most modern translations place verse 4 
          in footnote or omit entirely. {llm-cs45}
        
        risk:
          level: moderate
          necessary: false
          warning: |
            Textual criticism overwhelmingly supports omission. If included, mark as 
            textually disputed. {manual}
```

---

## Summary: Required vs Optional

### Always Required
- ✅ `verse: BOOK.chapter.verse` (zero-padded, 3 digits each)
- ✅ Inline citations `{source-id}` on all content except translation values
- ✅ Follow STANDARDIZATION.md for naming and codes

### Optional Standard Structures
- `source`: Original language text with citation
- `alternates`: Alternate manuscript readings
- `words`: Word-level breakdown (top-level, not under source)
- `translations`: For translation files
- `clusters`: For analysis files
- `prompt`: For prompt analysis files
- `patterns`: Translation pattern analysis
- `theological`: Theological analysis
- `grammatical`: Grammatical analysis

### Word-Level Optional Fields
Beyond the basics, `words` entries can include:
- Morphology: `part_of_speech`, `tense`, `voice`, `mood`, `case`, `gender`, `number`, `person`, `degree`
- Lexical: `lemma`, `strongs`, `gloss`
- Semantic: `domain`, `field`, `entity_type`, `referent`
- Syntactic: `function`, `head`, `dependents`, `clause`
- Alignment: Map to target language words
- Discourse: `topic`, `focus`, `given_new`
- Hebrew-specific: `stem`, `state`, `suffix`

### Unstructured Extensions
- Allowed with predictable conventions
- Must not conflict with standard fields
- Must include citations
- Should use standard terminology (linguistic, theological, semantic standards)

---

## Cross-Referencing Standards

### Word References

When referencing words across files, use the full directory path format from STANDARDIZATION.md:

**Format:** `{lang}/{word-root}/{word-inflected}`

**Examples:**
```yaml
# In a word file
related_words:
  - grc/αγαπη/αγαπη      # Greek agape (root form)
  - heb/אהב/אהב          # Hebrew ahav (root form)
  - eng/love/love        # English love (base form)
  - grc/λογος/λογου      # Greek logos (genitive inflection)
```

**Benefits:**
- Unambiguous: Full path identifies exact file
- Language-aware: Language code makes target clear
- Inflection-aware: Can reference specific forms
- Bidirectional: Easy to trace relationships

### Topic References

Topics may overlap or reference each other. Use `@` prefix to indicate an alias/reference to another topic file.

**Format:** `{lcc-code}/{slug}` - LCC code + slug for precision and readability

**Examples:**
```yaml
# In /bible/topics/BT750/justification/justification.yaml
related_topics:
  - BT750/sanctification          # Sibling topic
  - BT198/atonement               # Different category
  - @BV4627/sin                   # Alias to practical theology

# If this topic is primarily defined elsewhere
primary_topic: "@BT750/soteriology"
see_also:
  - "@BS1199/covenant"            # Cross-reference to biblical studies
```

**Common LCC Codes** (for human reference):
```
BS1199: Biblical Topics    BT109: Trinity          BT130: Divine Attributes
BT198:  Christology        BT695: Creation & Fall  BT750: Soteriology
BT819:  Eschatology        BV210: Worship & Prayer BV4627: Sins & Virtues
BV4909: Suffering          BX:    Denominations
```

**Use Cases:**
- **Aliases** (`@`): When same concept appears in multiple LCC categories
- **See-also**: Cross-references to related but distinct topics
- **Hierarchies**: Parent-child relationships between topics
- **Redirects**: Deprecated or alternate topic names

---

**Last Updated:** 2025-10-28
**Version:** 1.2
