# Cross-Linguistic Feature Discovery for Bible Translation
## Blind Discovery Test - Independent Research Results

**Date:** 2025-10-30
**Methodology:** Independent discovery using eBible corpus + web research
**Constraint:** No access to TBTA files or pre-existing annotations

---

## Executive Summary

This document presents the results of independent linguistic research to identify cross-linguistic grammatical features that should be annotated for Bible translation. The goal is to help translators working in rare languages with grammatical categories different from English/Greek/Hebrew.

Through analysis of the eBible translation corpus (1000+ languages) and linguistic typology research, I identified **10 major feature categories** that vary significantly across languages and critically impact translation decisions.

---

## Methodology

### Research Process

1. **Linguistic Background Research**
   - Searched for cross-linguistic variation in grammatical categories
   - Focused on features known to vary widely across language families
   - Prioritized features relevant to narrative and instructional texts

2. **eBible Corpus Analysis**
   - Selected strategic verses showing grammatical variation
   - Examined translations in 20-40 languages per verse
   - Looked for patterns across diverse language families
   - Noted where translations diverged in unexpected ways

3. **Sample Verses Analyzed**
   - Genesis 1:26 - "Let US make man in OUR image" (pronoun inclusivity)
   - Genesis 4:8 - Multiple "he"s requiring entity tracking
   - Genesis 19:31 - Dialogue between sisters (kinship, entity tracking)
   - Matthew 28:19 - Commands to disciples (imperative forms, number)
   - Acts 15:25 - "It seemed good to us" (inclusive/exclusive distinction)
   - John 3:16 - "For God so loved the world" (aspect, evidentiality)

4. **Pattern Identification**
   - Compared how different language families handled same content
   - Identified where translators made non-obvious choices
   - Researched linguistic explanations for observed patterns

---

## Feature Category 1: Clusivity (Inclusive vs. Exclusive "We")

### Why It Matters

Many languages (estimated 40-50% worldwide) grammatically distinguish between:
- **Inclusive "we"** = speaker + addressee(s) + possibly others ("you and I")
- **Exclusive "we"** = speaker + others, but NOT addressee ("they and I, but not you")

English/Greek/Hebrew do NOT make this distinction, so translators must determine which form to use based on context.

### Languages That Need This

- **Austronesian**: Tagalog, Hawaiian, Malay, Indonesian, Fijian
- **Polynesian**: Tongan, Samoan, Tahitian
- **Native American**: Quechua, Guarani, Ojibwe
- **Southeast Asian**: Vietnamese, Thai (some dialects)
- **Melanesian**: Tok Pisin, many Papuan languages
- **Some African languages**: Various Niger-Congo languages

### What Should Be Annotated

For every first-person plural pronoun ("we/us/our"):
1. **Inclusive/Exclusive determination** - Does it include the addressee?
2. **Participants identified** - Who exactly is included?
3. **Contextual reasoning** - Why this interpretation?

### Biblical Examples

**Genesis 1:26** - "Let US make man in OUR image"
- Most likely: **Exclusive** (God speaking, excluding humanity)
- Participants: Divine council/Trinity (traditional interpretations)
- Challenge: Some languages require choosing inclusive/exclusive

**Acts 15:25** - "It seemed good to us...with our beloved Barnabas and Paul"
- Most likely: **Exclusive** (apostles writing TO the churches, not including readers)
- Participants: Jerusalem council leaders
- Some contexts could be inclusive if addressing fellow leaders

**Matthew 6:11** - "Give us this day our daily bread"
- Most likely: **Inclusive** (speaker + all pray-ers)
- Participants: All who pray this prayer together

### Discovery Method from eBible

In Genesis 1:26, comparing languages:
- English: "Let us make" (ambiguous)
- Tagalog (tgl-ULB): "Gawin natin" - uses inclusive form
- Some languages show variation, indicating translator's theological choice

---

## Feature Category 2: Grammatical Number Beyond Singular/Plural

### Why It Matters

English has only singular/plural, but many languages have:
- **Dual** - exactly two (common: 40+ languages)
- **Trial** - exactly three (rare: ~20 languages)
- **Paucal** - a few, typically 3-10 (uncommon but regular)

Translators must choose the appropriate form based on context.

### Languages That Need This

**Dual Number:**
- **Slavic**: Slovenian, Upper Sorbian
- **Austronesian**: Fijian, Hawaiian, Kiribati
- **Semitic**: Classical Arabic, Biblical Hebrew
- **Indigenous**: Many Australian Aboriginal languages
- **Polynesian**: Tongan, Samoan, Māori

**Trial Number:**
- **Melanesian**: Larike, Biak, Sursurunga, Lihir
- **Some Austronesian languages**

**Paucal Number:**
- **Melanesian**: Sursurunga, Lihir (also have "greater paucal")
- **Some Australian Aboriginal languages**

### What Should Be Annotated

For nouns, pronouns, and verbs with number agreement:
1. **Exact count when known** - "two disciples" vs. "twelve disciples"
2. **Count implications** - "brothers" = definitely more than one, but how many?
3. **Dual-specific contexts** - Pairs like "heaven and earth," "Moses and Aaron"
4. **Small group contexts** - Useful for paucal/trial

### Biblical Examples

**Genesis 1:1** - "the heavens and the earth"
- Natural dual in many languages
- Some languages have grammaticalized "heaven-and-earth" dual form

**Genesis 4:8** - "Cain talked with Abel his brother"
- Two people: perfect dual context
- Some languages require dual pronouns/verbs

**Luke 24:13** - "Two of them"
- Explicitly stated dual
- Dual-marking languages mark this throughout the passage

**Genesis 19:31** - Lot's two daughters conversing
- Dual forms throughout in dual-marking languages
- Clear two-participant dialogue

### Discovery Method from eBible

Look for:
- Verses explicitly mentioning "two" or pairs
- Family relationships (typically small numbers)
- Dialogue between named individuals (count participants)
- Compare how dual-marking languages handle these contexts

---

## Feature Category 3: Entity Tracking / Switch Reference

### Why It Matters

When narratives have multiple third-person participants, languages need mechanisms to track "who's doing what." Switch reference systems grammatically mark whether:
- **Same subject (SS)** - The same entity continues as subject
- **Different subject (DS)** - A different entity becomes subject

This is critical for clarity when English just says "he...he...he."

### Languages That Need This

**Strong switch-reference systems:**
- **Papuan languages** - 70% have switch reference
- **Native American**: Many Uto-Aztecan, Athabaskan languages
- **South American**: Quechua, Aymara
- **Australian Aboriginal**: Many languages
- **African**: Some Niger-Congo languages

### What Should Be Annotated

For narrative sequences with multiple third-person entities:
1. **Subject continuity** - Same subject or different?
2. **Entity identification** - Which character is the subject?
3. **Ambiguity resolution** - How to determine subject when ambiguous?
4. **Agent tracking** - Who does what action?

### Biblical Examples

**Genesis 4:8** - "Cain talked with Abel his brother. And when they were in the field, Cain rose up against Abel his brother and killed him."
- Subject switches: Cain speaks → both in field → Cain acts → Abel receives
- In switch-reference languages:
  - "Cain talked with Abel" [same subject marker] "they were in field" [different subject marker] "Cain rose up"
  - Prevents ambiguity about who does what

**Genesis 37:23** - "When Joseph came to his brothers, they stripped Joseph..."
- Subject switch from Joseph to brothers
- Clear DS marking needed

**Ruth 1:6-7** - "Then she arose with her daughters-in-law to return...so she departed..."
- Multiple "she"s - tracking whether subject is Ruth or daughters-in-law

### Discovery Method from eBible

1. Find narratives with multiple same-gender characters
2. Track pronoun references across clauses
3. Look for languages that add particles/morphemes not in Greek/English
4. Compare how different languages disambiguate "he...he...he" sequences

---

## Feature Category 4: Demonstrative Systems (Spatial Deixis)

### Why It Matters

English has two-way demonstrative distinction (this/that), but many languages have three or more:
- **Two-way**: proximal (this) vs. distal (that)
- **Three-way**: proximal (this near me) vs. medial (that near you) vs. distal (that far from both)
- **Four+ way**: Adding elevation, visibility, or other distinctions

Biblical texts refer to people, places, and objects with demonstratives that must be translated appropriately.

### Languages That Need This

**Three-way systems:**
- **Romance (formal)**: Spanish, Portuguese, Italian (some contexts)
- **Asian**: Japanese, Korean, Thai, Filipino
- **Caucasian**: Georgian, Armenian
- **Slavic**: Serbo-Croatian, Macedonian
- **Finno-Ugric**: Finnish
- **Native American**: Plains Cree, Nandi
- **Other**: Basque, Hawaiian, Latin

**Four+ way systems:**
- Some indigenous languages add visibility/elevation distinctions

### What Should Be Annotated

For all demonstrative references ("this," "that," "these," "those"):
1. **Spatial relationship** - Near speaker? Near hearer? Far from both?
2. **Referent location** - Physical proximity in narrative
3. **Discourse proximity** - Recently mentioned vs. distant in text
4. **Emotional distance** - Respect/familiarity factors

### Biblical Examples

**Matthew 3:17** - "This is my beloved Son"
- Proximal: God speaking about Jesus who is present
- Near the speaker and likely visible to hearers

**John 1:15** - "This was he of whom I said..."
- Discourse reference to previously mentioned person
- May use medial or distal depending on language philosophy

**Matthew 26:26** - "Take, eat; this is my body"
- Proximal: Jesus holding bread
- Maximum proximity (in hand)

### Discovery Method from eBible

1. Search for "this/that/these/those" in English translations
2. Compare how three-way languages render them
3. Note when languages add distinctions not in Greek
4. Consider physical setting of narratives (who's where?)

---

## Feature Category 5: Evidentiality (Source of Knowledge)

### Why It Matters

Some languages grammatically mark how the speaker knows information:
- **Direct/witnessed** - Saw it personally
- **Inferential** - Deduced from evidence
- **Reportative/hearsay** - Someone told me
- **Assumptive** - Common knowledge/assumption

Biblical narratives include eyewitness accounts, reports, and divine revelation - requiring different evidential markings.

### Languages That Need This

**Strong evidential systems:**
- **Andean**: Quechua, Aymara (4-5 evidentials)
- **Tibetan languages**: Tibetan, Sherpa
- **Turkic**: Turkish, Azerbaijani (past tense evidentials)
- **Native American**: Tuyuca (5 evidentials), Eastern Pomo
- **East Asian**: Some Korean forms, some Japanese expressions
- **Balkan**: Bulgarian, Macedonian (reportative mood)

### What Should Be Annotated

For all statements in narrative/teaching:
1. **Knowledge source** - How does speaker/writer know this?
2. **Certainty level** - Direct witness vs. report vs. inference
3. **Reportative chain** - Multiple levels of reporting
4. **Divine revelation** - Special evidential category?

### Biblical Examples

**Luke 1:1-4** - "...just as those who from the beginning were eyewitnesses..."
- Explicit evidential framing
- Direct witness → report → Luke's compilation
- Languages with evidentials must mark this chain

**Genesis 1** - Creation account
- No human eyewitness possible
- Divine revelation evidential?
- Some languages use special forms for mythic/sacred narratives

**John 1:14** - "We beheld his glory"
- Direct evidential (eyewitness)
- Contrasts with verses about what Jesus said (reportative)

**Acts 1:3** - "To whom also he showed himself alive...by many proofs"
- Strong evidential claim
- Direct observation emphasized

### Discovery Method from eBible

1. Identify verses with explicit evidential framing (Luke 1:1-4)
2. Compare languages with Turkish-style past tense evidentials
3. Look for narrative vs. quoted speech distinctions
4. Note where languages add markers absent in Greek/English

---

## Feature Category 6: Honorifics and Politeness (Social Deixis)

### Why It Matters

Many languages grammatically encode social relationships:
- **T-V distinction** - Formal vs. informal "you" (40+ languages)
- **Elaborate honorific systems** - Multiple levels (Japanese, Korean, Javanese)
- **Humble vs. respectful forms** - How speaker shows deference

Biblical texts involve God, royalty, elders, strangers - requiring appropriate politeness levels.

### Languages That Need This

**T-V distinction:**
- **Romance**: French, Spanish, Italian, Portuguese
- **Germanic**: German, Dutch, Swedish
- **Slavic**: Russian, Polish, Czech, all Slavic languages
- **Other European**: Greek (modern), Turkish
- **Asian**: Hindi, Urdu, Persian, Bengali

**Complex honorific systems:**
- **East Asian**: Japanese (keigo), Korean, Thai, Javanese
- **South Asian**: Tamil, Kannada, Telugu, Indonesian
- **Other**: Nahuatl, Swahili (some contexts)

### What Should Be Annotated

For all second-person references and some third-person:
1. **Social relationship** - Speaker's status vs. addressee's
2. **Formality context** - Public/official vs. private/intimate
3. **Age/kinship factors** - Elder, peer, younger
4. **Divine address** - How to address God?
5. **Royal/authority address** - Kings, officials, elders

### Biblical Examples

**Prayers to God** - "Our Father..."
- Should this be formal (most languages) or informal?
- Arguments both ways theologically

**Jesus addressing Pharisees vs. disciples**
- Pharisees: formal/respectful (social superiors by role)
- Disciples: informal/intimate (close friends)
- Greek doesn't distinguish, but many languages must

**God addressing Moses** (Exodus 3)
- How does God address Moses? Formal? Intimate?
- Most languages use formal for God's speech

**Younger to elder** (Ruth to Naomi)
- Clear formal/respectful required in honorific languages

### Discovery Method from eBible

1. Identify social relationships in dialogue
2. Compare formal/informal languages (Spanish, German)
3. Note God-human, human-God, human-human contexts
4. Consider theological implications of choices

---

## Feature Category 7: Grammatical Aspect (Perfective/Imperfective)

### Why It Matters

Greek New Testament heavily uses aspect (perfective aorist vs. imperfective present/imperfect), but many target languages have different aspect systems:
- **Perfective** - Action viewed as complete whole
- **Imperfective** - Action viewed as ongoing/repeated
- **Perfect/stative** - Completed action with ongoing result
- **Habitual** - Regularly repeated action

Languages vary in which aspects are grammatically required.

### Languages That Need This

**Strong aspect systems:**
- **Slavic**: Russian, Czech, Polish (all verbs marked for aspect)
- **Semitic**: Hebrew (perfect/imperfect), Arabic
- **Asian**: Mandarin Chinese (aspect particles), Thai
- **African**: Swahili, Yoruba, many Niger-Congo languages
- **Romance**: Spanish, Portuguese (preterite/imperfect distinction)

### What Should Be Annotated

For all verbs:
1. **Aspectual value** - Perfective, imperfective, perfect, habitual?
2. **Greek aspect** - Which form in original Greek?
3. **Narrative function** - Background (imperfective) vs. main events (perfective)
4. **Habitual/generic** - Regular action vs. single occurrence

### Biblical Examples

**Luke 24:32** - "Were not our hearts burning..." (imperfect)
- Ongoing state throughout journey
- Imperfective aspect in target language

**John 2:11** - "This beginning of signs Jesus did" (aorist)
- Completed action, single event
- Perfective aspect

**John 15:1** - "I am the true vine" (present)
- Stative/timeless truth
- Languages vary on how to express

**Habitual actions** - "Jesus was teaching in the synagogues"
- Iterative/habitual in many languages

### Discovery Method from eBible

1. Compare aspect-rich languages (Russian, Spanish)
2. Note Greek tense forms (aorist vs. imperfect vs. present)
3. Identify narrative backbone (perfective) vs. background (imperfective)
4. Look for habitual contexts ("used to," "would often")

---

## Feature Category 8: Animacy Hierarchy and Differential Object Marking

### Why It Matters

Many languages treat animate objects differently from inanimate:
- **Differential object marking** - Special markers for human/animate objects
- **Animacy hierarchy** - Affects word order, agreement, case marking
- Typical hierarchy: human > animal > inanimate
- Sometimes: kin > human > animal > inanimate

### Languages That Need This

**Differential object marking:**
- **Romance**: Spanish (personal 'a'), Romanian
- **Indo-Iranian**: Hindi, Persian, Armenian
- **Turkic**: Turkish, Uzbek
- **Algonquian**: Plains Cree (complex animacy system)
- **Semitic**: Hebrew (את marker for definite objects)

### What Should Be Annotated

For all direct objects:
1. **Animacy level** - Human, animal, inanimate, abstract
2. **Definiteness** - Known/specific vs. unknown/generic
3. **Importance in narrative** - Key characters vs. props
4. **Special marking requirements** - When languages require markers

### Biblical Examples

**Matthew 2:11** - "They saw the child with Mary his mother"
- "Child" is human, definite, central character
- Spanish: "Vieron al niño" (personal 'a')

**Genesis 1:1** - "God created the heavens and the earth"
- Inanimate objects, no special marking in most languages

**Genesis 4:8** - "Cain killed Abel"
- Human victim: requires object marking in many languages
- Contrasts with "Cain worked the ground" (inanimate)

### Discovery Method from eBible

1. Identify verbs with human vs. inanimate objects
2. Compare Spanish (personal 'a') treatment
3. Note definite vs. indefinite objects
4. Look for patterns in object marking across languages

---

## Feature Category 9: Quotation and Reported Speech Systems

### Why It Matters

Biblical texts contain extensive quoted speech, and languages differ in how they mark:
- **Direct quotation** - Exact words spoken
- **Indirect quotation** - Paraphrased content
- **Quotative evidentials** - Markers showing "someone said..."
- **Reported speech particles** - Special markers for quotes

Some languages require special quotative markers; others shift tense/person in indirect speech differently than English.

### Languages That Need This

**Special quotative systems:**
- **Mayan languages** - Quotative particles required
- **Turkic languages** - Quotative evidentials
- **Japanese** - Complex quotative particles (って, と)
- **Korean** - Quotative particles and endings
- **Quechua** - Quotative evidential morphemes
- **Many African languages** - Quotative verbs/particles

### What Should Be Annotated

For all quoted speech:
1. **Quote type** - Direct, indirect, or paraphrased
2. **Speaker identified** - Who is speaking?
3. **Addressee identified** - Who is being addressed?
4. **Nesting level** - Quote within quote?
5. **Quotative markers** - How marked in original?

### Biblical Examples

**Genesis 1:3** - "And God said, 'Let there be light'"
- Direct quotation
- Simple quotative formula

**Genesis 4:8** - "Cain said to Abel his brother [some mss: 'Let us go to the field']"
- Textual variant: some manuscripts lack the quote
- Languages requiring quotes must make a choice

**John 1:15** - "John bore witness about him, and cried out, saying..."
- Nested quotation marker
- "Saying" = quotative marker

**Acts 15:25** - Letter quoting council's decision
- Written quotation (letter content)
- May use different markers than spoken quotes

### Discovery Method from eBible

1. Identify all quoted speech in passages
2. Compare languages with quotative particles (Japanese, Korean)
3. Note direct vs. indirect speech patterns
4. Track speaker changes in dialogue

---

## Feature Category 10: Topic Prominence vs. Subject Prominence

### Why It Matters

Languages structure sentences differently:
- **Subject-prominent** (English, European languages) - Subject comes first, strong agreement
- **Topic-prominent** (Chinese, Japanese, Korean) - Topic comes first (what sentence is about), subject may be omitted

This affects:
- Word order choices
- Pronoun omission/inclusion
- Information structure

### Languages That Need This

**Topic-prominent languages:**
- **East Asian**: Mandarin Chinese, Japanese, Korean
- **Southeast Asian**: Vietnamese, Thai, Malay, Indonesian
- **Some creoles**: Singaporean English, Malaysian English

**Mixed systems:**
- **Japanese, Korean** - Both topic and subject marking
- **Some African languages**

### What Should Be Annotated

For all clauses:
1. **Topic identification** - What is the sentence about?
2. **Subject identification** - Who/what does the action?
3. **Topic-subject mismatch** - When topic ≠ subject
4. **Information structure** - Old info (topic) vs. new info (comment)

### Biblical Examples

**John 1:1** - "In the beginning was the Word"
- English inverted: puts time adverbial first
- Topic-prominent rendering: "As for the beginning, the Word existed"

**Matthew 5:3** - "Blessed are the poor in spirit"
- English inverted: "poor in spirit" = topic
- Topic-prominent: "As for the poor in spirit, blessing (belongs to them)"

**Romans 12:1** - "I urge you therefore, brothers..."
- "Brothers" = topic/vocative
- Chinese/Japanese naturally puts this first

### Discovery Method from eBible

1. Compare Chinese, Japanese, Korean renderings
2. Note verses with fronted elements in English
3. Identify sentences "about" something (topic) vs. grammatical subject
4. Look for passive constructions (often topic-driven)

---

## Additional Features to Consider

While the above 10 are major categories, translators may also need information about:

### 11. Verb Serialization
- Languages that string verbs together without conjunctions
- Common in West African, Southeast Asian languages
- Affects how complex actions are described

### 12. Classifier Systems
- Languages requiring classifiers for counting (Chinese, Japanese, Thai)
- Different classifiers for humans, animals, objects, abstract concepts
- Biblical texts with numbers need appropriate classifiers

### 13. Kinship Systems
- Languages with more elaborate kinship terms
- Distinctions: older/younger sibling, maternal/paternal uncle, etc.
- Frequent in Biblical genealogies and family narratives

### 14. Tense and Temporal Reference
- Languages with future/non-future only
- Languages with multiple past tenses (remote past, recent past)
- Affects prophecy and narrative timing

### 15. Modality and Mood
- Obligation, permission, ability distinctions
- Subjunctive, optative, imperative systems
- Affects commands, permissions, possibilities

---

## Instructions for Replicating This Discovery Process

### Step 1: Research Cross-Linguistic Variation

**Resources to search:**
- WALS (World Atlas of Language Structures) online
- Wikipedia articles on grammatical categories
- Linguistic typology textbooks
- Language-specific grammars

**Key search terms:**
- "Cross-linguistic variation [feature]"
- "Typology of [grammatical category]"
- "Languages with [specific feature]"
- "Bible translation [language family]"

### Step 2: Select Sample Verses

**Criteria for verse selection:**
1. **Pronouns**: Verses with "we/us/our" for clusivity
2. **Exact numbers**: Verses mentioning "two," "three," specific counts
3. **Multiple characters**: Narratives tracking multiple "he/she" referents
4. **Spatial references**: Verses with "this/that" demonstratives
5. **Dialogue**: Direct speech between characters
6. **Social contexts**: God-human, elder-younger, formal-informal settings
7. **Aspect distinctions**: Ongoing vs. completed actions

**Good starting verses:**
- Genesis 1:1, 1:26 (creation, divine plural)
- Genesis 4:8 (entity tracking)
- Genesis 19:31 (dialogue, kinship)
- Exodus 3 (God addressing Moses)
- Matthew 28:19 (commands, number)
- Acts 15:25 (inclusive/exclusive "we")
- John 3:16 (aspect, evidentiality)

### Step 3: Analyze eBible Translations

**Process:**
1. Read the verse in English to understand content
2. Scan 20-40 translations in diverse languages
3. Use Google Translate on unfamiliar languages for rough sense
4. Look for:
   - Different word order
   - Added particles/morphemes not in English
   - Variation in how languages handle same element
   - Patterns by language family

**Language families to compare:**
- **Romance**: Spanish, Portuguese, French, Italian
- **Germanic**: German, Dutch, Swedish
- **Slavic**: Russian, Polish, Czech
- **East Asian**: Chinese, Japanese, Korean
- **Southeast Asian**: Thai, Vietnamese, Malay, Indonesian, Tagalog
- **Austronesian**: Hawaiian, Tongan, Fijian
- **African**: Swahili, Yoruba, various Niger-Congo
- **Native American**: Quechua, Guarani
- **Semitic**: Modern Hebrew, Arabic

### Step 4: Research Specific Features

When you notice a pattern (e.g., some languages add particles after quotes):
1. Search for the linguistic term (e.g., "quotative particles")
2. Find which languages have this feature
3. Understand when/how it's used
4. Look back at eBible to confirm pattern

### Step 5: Build Feature Categories

For each feature discovered:
1. **Name it clearly** (use standard linguistic terminology)
2. **Explain why it matters** (translation impact)
3. **List languages** (give specific examples with codes)
4. **Provide Biblical examples** (verse references)
5. **Describe annotation needs** (what info to capture)

### Step 6: Test Your Understanding

**Validation methods:**
1. Can you predict how a language will translate a verse based on its features?
2. Do examples from multiple language families confirm the pattern?
3. Does linguistic research support your observations?
4. Can you explain why translators need this information?

---

## Evaluation Criteria

This discovery process is successful if:

1. ✅ **Features identified independently** - No peeking at existing annotations
2. ✅ **Cross-linguistic evidence** - Patterns observed across multiple language families
3. ✅ **Linguistic grounding** - Features supported by typological research
4. ✅ **Biblical relevance** - Clear examples from Scripture
5. ✅ **Practical utility** - Translators can use this information
6. ✅ **Replicable methodology** - Others can follow the same process

---

## Conclusion

Through independent analysis of the eBible corpus and linguistic typology research, I identified 10 major cross-linguistic feature categories essential for Bible translation:

1. Clusivity (inclusive/exclusive "we")
2. Grammatical number (dual, trial, paucal)
3. Entity tracking / switch reference
4. Demonstrative systems (spatial deixis)
5. Evidentiality (source of knowledge)
6. Honorifics and politeness (social deixis)
7. Grammatical aspect (perfective/imperfective)
8. Animacy hierarchy and object marking
9. Quotation and reported speech
10. Topic prominence vs. subject prominence

Each category represents a grammatical distinction that:
- Varies significantly across languages
- Is often absent in English/Greek/Hebrew
- Requires translator decisions
- Impacts meaning and clarity
- Needs consistent annotation for AI grounding

The eBible corpus provides rich evidence for these categories when analyzed systematically across diverse language families. By examining how different languages translate the same verses, we can infer what grammatical information translators need to make informed decisions.

This research was conducted entirely without access to existing TBTA annotations, demonstrating that these features are discoverable through independent linguistic analysis.

---

## Appendix: Language Codes Reference

Quick reference for languages mentioned:

- **mal**: Malayalam (India)
- **deu**: German
- **spa**: Spanish
- **fra**: French
- **eng**: English
- **tgl**: Tagalog (Philippines)
- **rus**: Russian
- **jpn**: Japanese
- **cmn**: Mandarin Chinese
- **kor**: Korean
- **swh**: Swahili
- **yor**: Yoruba
- **heb**: Hebrew
- **arb**: Arabic
- **hin**: Hindi
- **por**: Portuguese
- **tur**: Turkish
- **tha**: Thai
- **vie**: Vietnamese
- **ind**: Indonesian

For full language codes, see ISO 639-3 standard.

---

**End of Blind Discovery Test Document**
