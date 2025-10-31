# Complete TBTA Field Taxonomy

**Analysis Date:** 2025-10-30
**Files Analyzed:** 10 diverse TBTA YAML files
**Purpose:** Comprehensive catalog of all fields, values, and contexts in TBTA database

---

## Table of Contents
1. [Meta Fields (Verse Level)](#meta-fields)
2. [Universal Fields (All Levels)](#universal-fields)
3. [Clause-Level Fields](#clause-level-fields)
4. [Phrase-Level Fields](#phrase-level-fields)
5. [Word-Level Fields (All Parts of Speech)](#word-level-fields-common)
6. [Noun-Specific Fields](#noun-specific-fields)
7. [Verb-Specific Fields](#verb-specific-fields)
8. [Adjective-Specific Fields](#adjective-specific-fields)
9. [Adverb-Specific Fields](#adverb-specific-fields)
10. [Conjunction-Specific Fields](#conjunction-specific-fields)
11. [Adposition-Specific Fields](#adposition-specific-fields)
12. [Particle-Specific Fields](#particle-specific-fields)
13. [Punctuation and Structural Elements](#punctuation-elements)

---

## Meta Fields (Verse Level) {#meta-fields}

### verse
- **Level:** Root/Document
- **Type:** String (structured identifier)
- **Format:** `{BOOK}.{CHAPTER}.{VERSE}` (e.g., "GEN.001.026", "MAT.005.010")
- **Purpose:** Unique identifier for the verse being annotated
- **Always Present:** Yes
- **Examples:**
  - `verse: GEN.001.026`
  - `verse: MAT.005.010`
  - `verse: PHP.002.004`
  - `verse: 1SA.026.012`

### source
- **Level:** Root/Document
- **Type:** String (constant)
- **Value:** `tbta` (always)
- **Purpose:** Identifies the annotation source/system
- **Always Present:** Yes

### version
- **Level:** Root/Document
- **Type:** String (semantic version)
- **Value:** `1.0.0` (in all observed files)
- **Purpose:** Version control for annotation schema
- **Always Present:** Yes

### clauses
- **Level:** Root/Document
- **Type:** Array
- **Purpose:** Contains all clause-level annotations for the verse
- **Always Present:** Yes
- **Children:** Clause objects with linguistic annotations

---

## Universal Fields (All Levels) {#universal-fields}

### children
- **Level:** Clause, Phrase, Word (nested structures)
- **Type:** Array
- **Purpose:** Contains nested linguistic units (clauses contain phrases, phrases contain words)
- **Context:** Present when a unit contains sub-units
- **Examples:**
  - Clause contains NP, VP, and punctuation elements
  - NP contains nouns, adjectives, adpositions
  - VP contains verbs and spaces

### Part
- **Level:** All linguistic units
- **Type:** String (categorical)
- **Purpose:** Identifies the type of linguistic unit
- **Always Present:** Yes (for all linguistic elements)

**Possible Values:**

**Clause-Level:**
- `Clause` - Main clause unit

**Phrase-Level:**
- `NP` - Noun Phrase
- `VP` - Verb Phrase
- `AdjP` - Adjective Phrase
- `AdvP` - Adverb Phrase

**Word-Level (Parts of Speech):**
- `Noun`
- `Verb`
- `Adjective`
- `Adverb`
- `Conjunction`
- `Adposition`
- `Particle`

**Structural/Punctuation:**
- `Space` - Whitespace marker
- `Period` - Sentence-ending punctuation
- `Paragraph` - Paragraph marker

**Examples:**
- `Part: Clause` (GEN.001.026, line 114)
- `Part: NP` (GEN.001.026, line 23)
- `Part: Noun` (GEN.001.026, line 15)
- `Part: Verb` (GEN.001.026, line 30)

---

## Clause-Level Fields {#clause-level-fields}

### Discourse Genre
- **Field Name:** `Discourse Genre`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Identifies the literary genre/register of the discourse

**Possible Values:**
- `Climactic Narrative Story` - Found in all observed files (100% of clauses)

**Frequency:** Present in nearly all clauses
**Examples:**
- GEN.001.026, line 104: `Discourse Genre: Climactic Narrative Story`
- MAT.005.010, line 183: `Discourse Genre: Climactic Narrative Story`
- PHP.002.004, line 93: `Discourse Genre: Climactic Narrative Story`

### Illocutionary Force
- **Field Name:** `Illocutionary Force`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Speech act type - what the speaker is doing with this utterance

**Possible Values:**
- `Declarative` - Statement of fact (most common)
- `Suggestive 'let's'` - Suggestion or proposal (hortative)
- `Yes-No Interrogative` - Yes/no question
- `'should' Obligation` - Obligation/deontic modality
- `'should not' Obligation` - Negative obligation

**Examples:**
- **Declarative:** GEN.001.026, line 116: `Illocutionary Force: Declarative`
- **Suggestive:** GEN.001.026, line 105: `Illocutionary Force: Suggestive 'let's'`
- **Interrogative:** LUK.006.034, line 260: `Illocutionary Force: Yes-No Interrogative`
- **Obligation:** PHP.002.004, line 137: `Illocutionary Force: 'should' Obligation`

### Speaker
- **Field Name:** `Speaker`
- **Level:** Clause
- **Type:** String (entity reference or category)
- **Purpose:** Identifies who is speaking in quoted/reported speech

**Possible Values:**
- Proper names: `God`, `Jesus`, `Brother`
- Categories: `Woman`, `Written Material to General Audience (letter,law,etc.)`
- (Absent for narrator/unmarked clauses)

**Examples:**
- GEN.001.026, line 108: `Speaker: God`
- LUK.006.034, line 80: `Speaker: Jesus`
- GEN.004.008, line 156: `Speaker: Brother`
- EPH.001.023, line 89: `Speaker: Written Material to General Audience (letter,law,etc.)`

### Listener
- **Field Name:** `Listener`
- **Level:** Clause
- **Type:** String (entity reference or category)
- **Purpose:** Identifies the addressee in quoted/reported speech

**Possible Values:**
- Proper names: `God`, `Brother`
- Categories: `Woman`, `Crowd`, `Group of Friends`
- (Absent for narrator/unmarked clauses)

**Examples:**
- GEN.001.026, line 106: `Listener: God`
- LUK.006.034, line 77: `Listener: Crowd`
- EPH.001.023, line 88: `Listener: Group of Friends`

### Speaker's Attitude
- **Field Name:** `Speaker\`s Attitude` (note: backtick escape in YAML)
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Emotional/social stance of the speaker

**Possible Values:**
- `Neutral` - Default/unmarked attitude (most common)
- `Familiar` - Intimate/informal register

**Examples:**
- GEN.001.026, line 109: `Speaker\`s Attitude: Neutral`
- GEN.019.031, line 152: `Speaker\`s Attitude: Familiar`

### Speaker's Age
- **Field Name:** `Speaker\`s Age`
- **Level:** Clause
- **Type:** Categorical (age band)
- **Purpose:** Age of the speaker (when relevant)

**Possible Values:**
- `Young Adult (18-24)`

**Examples:**
- GEN.004.008, line 158: `Speaker\`s Age: Young Adult (18-24)`
- GEN.019.031, line 151: `Speaker\`s Age: Young Adult (18-24)`

### Speaker-Listener Age
- **Field Name:** `Speaker-Listener Age`
- **Level:** Clause
- **Type:** Categorical (relationship)
- **Purpose:** Relative age relationship between speaker and listener

**Possible Values:**
- `Essentially the Same Age`

**Examples:**
- GEN.004.008, line 157: `Speaker-Listener Age: Essentially the Same Age`
- GEN.019.031, line 150: `Speaker-Listener Age: Essentially the Same Age`

### Topic NP
- **Field Name:** `Topic NP`
- **Level:** Clause
- **Type:** Categorical (semantic role reference)
- **Purpose:** Identifies which semantic role serves as the topic/focus

**Possible Values:**
- `Most Agent-like` - Agent or subject-like participant
- `Most Patient-like` - Patient or object-like participant

**Examples:**
- GEN.001.026, line 118: `Topic NP: Most Agent-like`
- MAT.005.010, line 206: `Topic NP: Most Patient-like`

### Type (Clause)
- **Field Name:** `Type`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Syntactic type of clause

**Possible Values:**
- `Independent` - Main clause
- `Patient (Object Complement)` - Complement clause (object)
- `Restrictive Thing Modifier (Relative Clause)` - Relative clause
- `Event Modifier (Adverbial Clause)` - Adverbial clause
- `Attributive Patient (Adjectival Object Complement)` - Adjectival complement

**Examples:**
- **Independent:** GEN.001.026, line 119: `Type: Independent`
- **Object Complement:** GEN.001.026, line 111: `Type: Patient (Object Complement)`
- **Relative Clause:** GEN.001.026, line 362: `Type: Restrictive Thing Modifier (Relative Clause)`
- **Adverbial:** GEN.004.008, line 336: `Type: Event Modifier (Adverbial Clause)`
- **Adjectival Complement:** GEN.019.031, line 328: `Type: Attributive Patient (Adjectival Object Complement)`

### Sequence
- **Field Name:** `Sequence`
- **Level:** Clause, Phrase, Word (various levels)
- **Type:** Categorical
- **Purpose:** Position in coordinated/sequential structures

**Possible Values:**
- `Not in a Sequence` - Not part of coordination (default)
- `First Coordinate` - First element in coordination
- `Coordinate` - Middle element in coordination
- `Last Coordinate` - Final element in coordination

**Examples:**
- GEN.001.026, line 117: `Sequence: Not in a Sequence`
- LUK.006.034, line 79: `Sequence: First Coordinate`
- GEN.001.026, line 449: `Sequence: Last Coordinate`

### Vocabulary Alternate
- **Field Name:** `Vocabulary Alternate`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Marks clauses that provide vocabulary variants (simple/complex)

**Possible Values:**
- `Single Sentence - Complex Vocabulary Alternate`
- `Single Sentence - Simple Vocabulary Alternate`

**Examples:**
- GEN.001.026, line 198: `Vocabulary Alternate: Single Sentence - Complex Vocabulary Alternate`
- GEN.001.026, line 258: `Vocabulary Alternate: Single Sentence - Simple Vocabulary Alternate`
- MAT.005.010, line 288: `Vocabulary Alternate: Single Sentence - Complex Vocabulary Alternate`

### Alternative Analysis
- **Field Name:** `Alternative Analysis`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Marks alternate linguistic analyses of the same text

**Possible Values:**
- `Primary Analysis` - Main interpretation
- `First Alternative Analysis` - First alternate interpretation
- `Literal Alternate` - Literal translation alternative
- `Dynamic Alternate` - Dynamic equivalence alternative

**Examples:**
- PRO.015.003, line 91: `Alternative Analysis: Literal Alternate`
- PRO.015.003, line 158: `Alternative Analysis: Dynamic Alternate`
- EPH.001.023, line 265: `Alternative Analysis: Primary Analysis`
- EPH.001.023, line 465: `Alternative Analysis: First Alternative Analysis`

### Implicit Information
- **Field Name:** `Implicit Information`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Marks clauses with implicit/understood information

**Possible Values:**
- `Implicit Situational Information`

**Examples:**
- GEN.004.008, line 248: `Implicit Information: Implicit Situational Information`

### Rhetorical Question
- **Field Name:** `Rhetorical Question`
- **Level:** Clause
- **Type:** Categorical or null
- **Purpose:** Identifies rhetorical questions and their expected answers

**Possible Values:**
- `Yes-No Question Expects 'No'` - Question expecting negative answer
- `Equivalent Statement` - Question functioning as statement
- `null` - Not a rhetorical question (or field absent)

**Examples:**
- LUK.006.034, line 262: `Rhetorical Question: Yes-No Question Expects 'No'`
- LUK.006.034, line 527: `Rhetorical Question: Equivalent Statement`
- 1KI.011.001, line 141: `Rhetorical Question: null`

### Salience Band
- **Field Name:** `Salience Band`
- **Level:** Clause
- **Type:** Categorical
- **Purpose:** Information structure prominence level

**Possible Values:**
- `Primary Storyline` - Main narrative events

**Examples:**
- LUK.006.034, line 78: `Salience Band: Primary Storyline`

### Location
- **Field Name:** `Location`
- **Level:** Clause
- **Type:** String or null
- **Purpose:** Geographical/spatial setting (when specified)

**Possible Values:**
- `null` - No specific location marked
- (Potentially location names, though null in observed data)

**Examples:**
- 1SA.026.012, line 185: `Location: null`

---

## Phrase-Level Fields {#phrase-level-fields}

### Semantic Role
- **Field Name:** `Semantic Role`
- **Level:** NP (Noun Phrase)
- **Type:** Categorical
- **Purpose:** Thematic role of the NP in relation to the predicate

**Possible Values:**
- `Most Agent-like` - Agent, subject
- `Most Patient-like` - Patient, direct object
- `Destination` - Goal, recipient, addressee
- `State` - Stative/predicative role
- `Beneficiary` - Beneficiary role

**Examples:**
- **Agent:** GEN.001.026, line 25: `Semantic Role: Most Agent-like`
- **Patient:** GEN.001.026, line 100: `Semantic Role: Most Patient-like`
- **Destination:** GEN.004.008, line 93: `Semantic Role: Destination`
- **State:** GEN.001.026, line 185: `Semantic Role: State`
- **Beneficiary:** MAT.005.010, line 198: `Semantic Role: Beneficiary`

### Relativized
- **Field Name:** `Relativized`
- **Level:** NP (Noun Phrase)
- **Type:** Boolean (string)
- **Purpose:** Indicates if NP is relativized (gap in relative clause)

**Possible Values:**
- `No` - Not relativized (vast majority)
- `Yes` - Relativized (gap site)

**Examples:**
- GEN.001.026, line 24: `Relativized: 'No'`
- (All observed instances are 'No')

### Usage
- **Field Name:** `Usage`
- **Level:** AdjP (Adjective Phrase)
- **Type:** Categorical
- **Purpose:** Syntactic function of adjective

**Possible Values:**
- `Attributive` - Modifies noun directly
- `Predicative` - Predicate adjective (after copula)

**Examples:**
- **Attributive:** GEN.001.026, line 21: `Usage: Attributive`
- **Predicative:** GEN.019.031, line 142: `Usage: Predicative`

### Implicit (Phrase Level)
- **Field Name:** `Implicit`
- **Level:** Phrase (VP, AdjP, AdvP, NP)
- **Type:** String (categorical)
- **Purpose:** Marks phrases with implicit/understood elements

**Possible Values:**
- `No` - Not implicit (default)
- `Implicit Argument` - Understood argument
- `Optional Agent of Passive` - Passive agent not expressed
- `Implicit Situational Information` - Understood from context

**Examples:**
- GEN.001.026, line 39: `Implicit: 'No'`
- MAT.005.010, line 100: `Implicit: Implicit Argument`
- MAT.005.010, line 19: `Implicit: Optional Agent of Passive`

---

## Word-Level Fields (All Parts of Speech) {#word-level-fields-common}

### Constituent
- **Field Name:** `Constituent`
- **Level:** Word
- **Type:** String (lexeme)
- **Purpose:** The actual word/morpheme in simplified English form
- **Always Present:** Yes (for content words)

**Examples:**
- `Constituent: God` (GEN.001.026, line 12)
- `Constituent: say` (GEN.001.026, line 28)
- `Constituent: create` (GEN.001.026, line 73)

**Special Values:**
- Grammatical markers: `-QuoteBegin`, `-QuoteEnd`, `-Generic Genitive`, `-Kinship`, `-Body Part`, `-Name`, `-Realm of Authority`, `-Begin Scene`, `-Subgroup`, `-Title`, `-Group`
- Structural: `|` (paragraph marker)

### LexicalSense
- **Field Name:** `LexicalSense`
- **Level:** Word
- **Type:** String (letter code)
- **Purpose:** Distinguishes different senses/meanings of the same word
- **Always Present:** Yes (for lexical items)

**Possible Values:**
- Letters: `A`, `B`, `C`, `D`, `E`, `F`, `J`, `L`, `T`, `U` (sense identifiers)

**Examples:**
- GEN.001.026, line 7: `LexicalSense: A`
- GEN.001.026, line 140: `LexicalSense: D`
- LUK.006.034, line 144: `LexicalSense: E`

### SemanticComplexityLevel
- **Field Name:** `SemanticComplexityLevel`
- **Level:** Word
- **Type:** String (numeric)
- **Purpose:** Complexity rating for translation (presumably 1-5 scale)

**Possible Values:**
- `'1'` - Basic/simple (all observed instances)
- (Potentially higher numbers for more complex items)

**Examples:**
- GEN.001.026, line 9: `SemanticComplexityLevel: '1'`

**Frequency:** Present on all lexical items, always value '1' in observed data

### Polarity
- **Field Name:** `Polarity`
- **Level:** Word (Nouns, Verbs, Adjectives)
- **Type:** Categorical
- **Purpose:** Positive or negative marking

**Possible Values:**
- `Affirmative` - Positive polarity (default, most common)
- `Negative` - Negative polarity (with negation)

**Examples:**
- **Affirmative:** GEN.001.026, line 20: `Polarity: Affirmative`
- **Negative:** GEN.019.031, line 173: `Polarity: Negative` (with "no" - "man" in negative context)

---

## Noun-Specific Fields {#noun-specific-fields}

### Number
- **Field Name:** `Number`
- **Level:** Noun
- **Type:** Categorical
- **Purpose:** Grammatical number

**Possible Values:**
- `Singular` - One entity
- `Plural` - Multiple entities
- `Dual` - Two entities (special dual number)
- `Trial` - Three entities (special trial number)

**Examples:**
- **Singular:** GEN.001.026, line 17: `Number: Singular`
- **Plural:** GEN.001.026, line 92: `Number: Plural`
- **Dual:** GEN.004.008, line 106: `Number: Dual`
- **Trial:** GEN.001.026, line 62: `Number: Trial`

**Distribution:**
- Singular: Very common
- Plural: Very common
- Dual: Rare (2 items, both speakers: "let's go")
- Trial: Very rare (3 items, God as Trinity: "let us create")

### Person
- **Field Name:** `Person`
- **Level:** Noun
- **Type:** Categorical
- **Purpose:** Grammatical person

**Possible Values:**
- `Third` - Third person (he/she/it/they) - most common
- `Second` - Second person (you)
- `First Inclusive` - First person including addressee (we-inclusive)

**Examples:**
- **Third:** GEN.001.026, line 19: `Person: Third`
- **Second:** PHP.002.004, line 14: `Person: Second`
- **First Inclusive:** GEN.001.026, line 64: `Person: First Inclusive`

### NounListIndex
- **Field Name:** `NounListIndex`
- **Level:** Noun
- **Type:** String (alphanumeric)
- **Purpose:** Index to track same referent across clause/verse
- **Always Present:** Yes (for nouns)

**Possible Values:**
- Numbers: `'1'`, `'2'`, `'3'`, `'4'`, `'5'`, `'6'`, `'7'`, `'8'`, `'9'`
- Letters: `A`, `B`, `C`
- Purpose: Same index = same referent

**Examples:**
- GEN.001.026, line 14: `NounListIndex: '1'` (God, first mention)
- GEN.001.026, line 59: `NounListIndex: '1'` (God, same referent)
- GEN.001.026, line 89: `NounListIndex: '2'` (person, different referent)

### Participant Tracking
- **Field Name:** `Participant Tracking`
- **Level:** Noun
- **Type:** Categorical
- **Purpose:** Discourse referential status

**Possible Values:**
- `Routine` - Known/active participant
- `Generic` - Generic/non-specific reference
- `Frame Inferable` - Inferable from semantic frame
- `First Mention` - New participant introduction

**Examples:**
- **Routine:** GEN.001.026, line 18: `Participant Tracking: Routine`
- **Generic:** GEN.001.026, line 93: `Participant Tracking: Generic`
- **Frame Inferable:** GEN.004.008, line 48: `Participant Tracking: Frame Inferable`
- **First Mention:** GEN.019.031, line 308: `Participant Tracking: First Mention`

### Proximity
- **Field Name:** `Proximity`
- **Level:** Noun
- **Type:** Categorical
- **Purpose:** Deictic/contextual nearness

**Possible Values:**
- `Contextually Near` - Near in discourse context (this/that)
- `Contextually Near with Focus` - Near with special focus
- (Absent for unmarked proximity)

**Examples:**
- GEN.001.026, line 131: `Proximity: Contextually Near`
- GEN.001.026, line 270: `Proximity: Contextually Near with Focus`

### Surface Realization
- **Field Name:** `Surface Realization`
- **Level:** Noun
- **Type:** Categorical
- **Purpose:** How the noun is expressed in surface syntax

**Possible Values:**
- `Noun` - Realized as full noun (most common)
- `Always a Noun` - Always expressed as noun (proper names)
- (Potentially pronouns, though not observed)

**Examples:**
- GEN.001.026, line 21: `Surface Realization: Noun`
- 1KI.011.001, line 21: `Surface Realization: Always a Noun`

---

## Verb-Specific Fields {#verb-specific-fields}

### Time
- **Field Name:** `Time`
- **Level:** Verb
- **Type:** Categorical
- **Purpose:** Temporal reference (tense-like)

**Possible Values:**
- `Present` - Present time reference
- `Discourse` - Narrative/discourse time (past narrative)
- `Immediate Future` - Near future
- `Later Today` - Later same day future
- `A Year from Now` - Distant future

**Examples:**
- **Present:** GEN.001.026, line 328: `Time: Present`
- **Discourse:** GEN.001.026, line 36: `Time: Discourse` (narrative past)
- **Immediate Future:** GEN.001.026, line 81: `Time: Immediate Future`
- **Later Today:** PHP.002.004, line 31: `Time: Later Today`
- **A Year from Now:** GEN.019.031, line 378: `Time: A Year from Now`

### Aspect
- **Field Name:** `Aspect`
- **Level:** Verb
- **Type:** Categorical
- **Purpose:** Aspectual marking

**Possible Values:**
- `Unmarked` - No special aspect (100% of observed cases)

**Examples:**
- GEN.001.026, line 33: `Aspect: Unmarked`

**Note:** All verbs show "Unmarked" aspect in observed data

### Mood
- **Field Name:** `Mood`
- **Level:** Verb
- **Type:** Categorical
- **Purpose:** Modal/mood marking

**Possible Values:**
- `Indicative` - Factual statement (most common)
- `'should' Obligation` - Deontic obligation (positive)
- `'should not' Obligation` - Deontic obligation (negative)

**Examples:**
- **Indicative:** GEN.001.026, line 34: `Mood: Indicative`
- **Should:** PHP.002.004, line 137: `Mood: 'should' Obligation`
- **Should Not:** PHP.002.004, line 29: `Mood: 'should not' Obligation`

### Adjective Degree
- **Field Name:** `Adjective Degree`
- **Level:** Verb
- **Type:** Categorical
- **Purpose:** Degree marking (apparently applies to verbs too)

**Possible Values:**
- `No Degree` - No degree marking (100% of observed verb instances)

**Examples:**
- GEN.001.026, line 32: `Adjective Degree: No Degree`

**Note:** Despite the name "Adjective Degree," this field appears on verbs with consistent "No Degree" value

---

## Adjective-Specific Fields {#adjective-specific-fields}

### Degree
- **Field Name:** `Degree`
- **Level:** Adjective
- **Type:** Categorical
- **Purpose:** Degree of comparison

**Possible Values:**
- `No Degree` - Positive/unmarked form (most common)
- `Comparative` - Comparative form (older, younger)

**Examples:**
- **No Degree:** GEN.001.026, line 515: `Degree: No Degree`
- **Comparative:** GEN.019.031, line 16: `Degree: Comparative` (with "old" → "older")
- **Comparative:** GEN.019.031, line 57: `Degree: Comparative` (with "young" → "younger")

---

## Adverb-Specific Fields {#adverb-specific-fields}

### Degree (Adverb)
- **Field Name:** `Degree`
- **Level:** Adverb
- **Type:** Categorical
- **Purpose:** Degree marking for adverbs

**Possible Values:**
- `No Degree` - Unmarked (all observed instances)

**Examples:**
- GEN.001.026, line 51: `Degree: No Degree`

---

## Conjunction-Specific Fields {#conjunction-specific-fields}

### Implicit (Conjunction)
- **Field Name:** `Implicit`
- **Level:** Conjunction
- **Type:** Boolean (string)
- **Purpose:** Marks if conjunction is implicit or explicit

**Possible Values:**
- `No` - Explicit/overt conjunction (100% of observed instances)

**Examples:**
- GEN.001.026, line 10: `Implicit: 'No'`

**Note:** All observed conjunctions are explicit; presumably `Yes` would mark implicit/understood conjunctions

---

## Adposition-Specific Fields {#adposition-specific-fields}

Adpositions (prepositions/postpositions) share many fields with nouns but have specific semantic functions indicated in the `Constituent` field through hyphenated markers:

### Grammatical Adpositions (Marked with Hyphens)
- **Type:** Grammatical/functional markers
- **Examples:**
  - `-Generic Genitive` - General possessive/genitive relation
  - `-Kinship` - Kinship relationship marker
  - `-Body Part` - Body part possession
  - `-Name` - Name marker/apposition
  - `-Realm of Authority` - Authority domain marker
  - `-Subgroup` - Subset marker
  - `-Title` - Title/honorific marker
  - `-Group` - Group membership marker

### Lexical Adpositions
- **Type:** Spatial/temporal/abstract relations
- **Examples:**
  - `in`, `on`, `at`, `near`, `while`, `if`, `because`, `in-order-to`, `just-like`

---

## Particle-Specific Fields {#particle-specific-fields}

Particles primarily mark discourse structure:

### Constituent Values for Particles:
- `-QuoteBegin` - Marks beginning of quotation
- `-QuoteEnd` - Marks end of quotation
- `-Begin Scene` - Marks scene boundary

**Examples:**
- GEN.001.026, line 42: `Constituent: -QuoteBegin`
- GEN.001.026, line 617: `Constituent: -QuoteEnd`
- GEN.019.031, line 6: `Constituent: -Begin Scene`

---

## Punctuation and Structural Elements {#punctuation-elements}

### Part: Space
- **Purpose:** Whitespace/word boundary marker
- **Fields:** Only `Part: Space`
- **Example:** GEN.001.026, line 22

### Part: Period
- **Purpose:** Sentence-final punctuation
- **Fields:** Only `Part: Period`
- **Example:** GEN.001.026, line 112

### Part: Paragraph
- **Purpose:** Paragraph boundary marker
- **Fields:** `Part: Paragraph` and `Constituent: '|'`
- **Example:** PRO.015.003, lines 5-6

---

## Field Co-occurrence Patterns

### Nouns Always Have:
- Part (= Noun)
- Constituent
- LexicalSense
- SemanticComplexityLevel
- Number
- Person
- NounListIndex
- Participant Tracking
- Polarity
- Surface Realization

### Nouns Sometimes Have:
- Proximity (when contextually near)

### Verbs Always Have:
- Part (= Verb)
- Constituent
- LexicalSense
- SemanticComplexityLevel
- Adjective Degree (despite name)
- Aspect
- Mood
- Polarity
- Time

### Adjectives Always Have:
- Part (= Adjective)
- Constituent
- LexicalSense
- SemanticComplexityLevel
- Degree

### Noun Phrases Always Have:
- Part (= NP)
- Relativized
- Sequence

### Noun Phrases Sometimes Have:
- Semantic Role (when argument of predicate)
- Implicit (when understood)
- children (when containing words)

### Clauses Always Have:
- Part (= Clause)
- Discourse Genre
- Illocutionary Force
- Sequence
- Topic NP
- Type

### Clauses Sometimes Have:
- Speaker (in direct/reported speech)
- Listener (in direct/reported speech)
- Speaker's Attitude (in speech)
- Speaker's Age (when relevant)
- Speaker-Listener Age (when relevant)
- Vocabulary Alternate (for variant expressions)
- Alternative Analysis (for multiple interpretations)
- Implicit Information (for understood content)
- Rhetorical Question (for rhetorical questions)
- Salience Band (for information structure)
- Location (for spatial setting)

---

## Summary Statistics

**Total Unique Fields Identified:** 41

**By Level:**
- Meta/Document: 3 fields
- Clause: 15 fields
- Phrase (NP/VP/AdjP/AdvP): 6 fields
- Word (common): 5 fields
- Noun-specific: 6 fields
- Verb-specific: 4 fields
- Adjective-specific: 2 fields
- Adverb-specific: 1 field
- Conjunction-specific: 1 field
- Structural: 3 types

**Most Common Values:**
- `SemanticComplexityLevel: '1'` - 100% of words
- `Aspect: Unmarked` - 100% of verbs
- `Relativized: 'No'` - 100% of observed NPs
- `Discourse Genre: Climactic Narrative Story` - 100% of clauses
- `Illocutionary Force: Declarative` - ~80% of clauses
- `Polarity: Affirmative` - ~95% of words

**Rare Values:**
- `Number: Trial` - 1 instance (God in Genesis 1:26)
- `Number: Dual` - 2 instances (speakers in reported speech)
- `Degree: Comparative` - 2 instances (older/younger sisters)
- `Proximity: *` - ~5% of nouns

---

## Notes on Linguistic Philosophy

### Design Principles Evident:
1. **Maximalist Annotation:** Every word receives extensive annotation even when predictable
2. **Redundancy for Robustness:** Information encoded at multiple levels (e.g., Speaker at clause level, Person in pronouns)
3. **Cross-linguistic Design:** Fields accommodate languages with different features (Trial number, inclusive/exclusive we)
4. **Translation-focused:** Fields like SemanticComplexityLevel and Vocabulary Alternate serve translation needs
5. **Discourse-aware:** Participant Tracking, Topic NP, and Salience Band track information flow

### Key Insights:
- **Trial Number:** Genesis 1:26 uses Trial number for "let us make" - theological interpretation (Trinity)
- **Person Encoding:** "We" distinguished as First Inclusive (includes addressee)
- **Quote Particles:** Explicit quote boundaries even in English simplification
- **Alternative Analyses:** System allows multiple competing interpretations (Proverbs, Ephesians)
- **Vocabulary Levels:** Same content in simple vs. complex vocabulary (kingdom = God is king)

---

## Files Analyzed

1. GEN.001.026 - Creation narrative, divine speech
2. GEN.004.008 - Cain and Abel, homicide narrative
3. GEN.019.031 - Lot's daughters, difficult moral content
4. MAT.005.010 - Beatitudes, teaching discourse
5. PRO.015.003 - Wisdom saying with metaphor
6. PHP.002.004 - Pauline epistle, ethical instruction
7. LUK.006.034 - Jesus's teaching, rhetorical questions
8. EPH.001.023 - Pauline epistle, complex theology
9. 1SA.026.012 - David and Saul narrative
10. 1KI.011.001 - Solomon's wives, list structure

**Genres Represented:**
- Narrative (Genesis, Samuel, Kings)
- Teaching (Matthew, Luke)
- Wisdom (Proverbs)
- Epistle (Philippians, Ephesians)

---

## End of Taxonomy

**Date Compiled:** 2025-10-30
**Analyst:** Claude (Sonnet 4.5)
**Status:** Complete for 10-file sample
