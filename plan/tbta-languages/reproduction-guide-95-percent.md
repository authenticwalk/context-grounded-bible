# TBTA Annotation Reproduction Guide
## Achieving 95%+ Accuracy in Feature Identification

**Purpose:** Systematic guide to reproduce TBTA annotations with near-perfect accuracy.

**Based on:**
- `/plan/tbta-languages/complete-field-taxonomy.md` - All 41 fields cataloged
- `/plan/tbta-languages/blind-test-comparison.md` - 8.2/10 baseline
- Analysis of 10+ TBTA files across genres

**Goal:** Raise accuracy from 8.2/10 to 9.5+/10

---

## What the Blind Discovery Missed (and How to Fix It)

### Accuracy Gap Analysis

| Feature Category | Blind Score | Why Missed | How to Achieve 100% |
|-----------------|-------------|------------|---------------------|
| **Clusivity** | ✅ 100% | N/A - Perfect match | Continue current approach |
| **Number (Dual/Trial)** | ✅ 100% | N/A - Perfect match | Continue current approach |
| **Entity Tracking** | ✅ 100% | N/A - Perfect match (NounListIndex) | Continue current approach |
| **Speaker Demographics** | ⚠️ 60% | Thought it was only for honorific langs | Annotate for ALL dialogue |
| **Time Granularity** | ❌ 30% | Found "aspect" but missed 20+ categories | Use TBTA's taxonomy directly |
| **Participant Tracking** | ⚠️ 70% | Found concept but missed 9-state system | Use exact TBTA states |
| **Illocutionary Force** | ❌ 40% | Mentioned speech acts vaguely | Annotate every clause |
| **Proximity System** | ⚠️ 50% | Found 3-way but missed 9+ categories | Use full TBTA proximity taxonomy |
| **Discourse Genre** | ❌ 0% | Didn't identify | Always annotate |
| **Implicit** | ❌ 0% | Didn't identify | Mark for all words |
| **Sequence** | ❌ 0% | Didn't identify | Mark coordination patterns |
| **Vocabulary Alternate** | ❌ 0% | Didn't identify | Mark simple/complex variants |

---

## Complete Field-by-Field Reproduction Guide

### TIER 1: Discoverable Features (Blind Discovery Got Right)

These can be identified through eBible corpus analysis + linguistic knowledge:

#### 1. Clusivity (Inclusive/Exclusive)

**What TBTA Has:**
```yaml
Person: First Inclusive  # "we" including addressee
Person: First Exclusive  # "we" excluding addressee (not yet observed in sample)
```

**How to Identify:**
1. Find first-person plural pronouns ("we/us/our")
2. Determine discourse context:
   - **Inclusive**: Speaker + addressee(s) together
   - **Exclusive**: Speaker + others, but NOT addressee(s)

**Examples:**
- GEN 1:26 "Let US create" → First Inclusive (Trinity members addressing each other)
- GEN 4:8 "Let us go" → First Inclusive (Cain + Abel)
- ACT 15:25 "It seemed good to us" → First Exclusive (apostles writing TO churches)

**Languages That Need This:** Tagalog, Malay, Fijian, Quechua (~40% of world languages)

**Reproduction Accuracy:** ✅ **100%** - Blind discovery matched perfectly

---

#### 2. Number System

**What TBTA Has:**
```yaml
Number: Singular
Number: Dual        # Exactly 2
Number: Trial       # Exactly 3
Number: Plural      # 3 or more (general)
Number: Paucal      # A few (not observed in sample, but documented)
```

**How to Identify:**

**Singular:** One entity
- "the man," "God," "he"

**Dual:** Exactly 2 entities
- Two named people dialogue (GEN 4:8: Cain + Abel)
- Natural pairs ("heaven and earth")
- Context: "Let us go" when 2 people speaking

**Trial:** Exactly 3 entities
- GEN 1:26: God (as Trinity) = 3 persons
- Requires theological/exegetical analysis

**Plural:** More than 2 (or ambiguous count)
- "the disciples" (12)
- "people" (many)

**Languages That Need This:**
- Dual: Slovene, Arabic, Hebrew, Fijian, Hawaiian
- Trial: Larike, Marshallese, Biak (rare)
- Paucal: Murrinh-patha, Lihir, Sursurunga

**Reproduction Accuracy:** ✅ **100%** - Blind discovery matched

**Caveat:** Trial in GEN 1:26 requires theological insight (Trinity = 3 persons), not just linguistic analysis.

---

#### 3. Entity Tracking (NounListIndex)

**What TBTA Has:**
```yaml
NounListIndex: '1'  # Entity 1 (Cain)
NounListIndex: '2'  # Entity 2 (brother)
NounListIndex: '3'  # Entity 3 (Abel)
NounListIndex: '4'  # Entity 4 (field)
```

**How to Identify:**
1. For each noun in the verse, assign a unique index (1-9, A-Z, a-z)
2. If two nouns refer to the SAME entity, use the SAME index
3. If two nouns refer to DIFFERENT entities, use DIFFERENT indices

**Example:** GEN 4:8
- Cain → 1
- brother → 2 (separate from Cain)
- Abel → 3 (separate entity, even though "brother" refers to him)
- field → 4

**Purpose:** Helps pro-drop languages (Japanese, Korean, Spanish) know which entities to reintroduce when ambiguous.

**Languages That Need This:** Pro-drop languages (Japanese, Korean, Spanish, Italian, Chinese, Turkish)

**Reproduction Accuracy:** ✅ **100%** - Blind discovery matched

---

### TIER 2: Partially Discoverable (Need Refinement)

These were identified conceptually but missed specific taxonomies:

#### 4. Participant Tracking

**What TBTA Has (9 States):**
```yaml
Participant Tracking: Routine          # Established, active participant
Participant Tracking: Frame Inferable  # Inferable from context
Participant Tracking: Generic          # Generic reference
Participant Tracking: First Mention    # Newly introduced
Participant Tracking: Integration      # Being integrated
Participant Tracking: Exiting          # Leaving narrative
Participant Tracking: Restaging        # Reintroduced after absence
Participant Tracking: Offstage         # Not present in scene
Participant Tracking: Interrogative    # Question element
```

**What Blind Discovery Had:**
- "Same subject / Different subject" (switch-reference concept)
- Identified need but not the 9-state taxonomy

**How to Identify:**

| State | When to Use | Example |
|-------|-------------|---------|
| **Routine** | Entity already established, continues in narrative | Cain (after first mention) |
| **Frame Inferable** | Entity inferable from context/frame | "his brother" (whose brother? inferable) |
| **Generic** | Generic/non-specific reference | "person" (humanity in general) |
| **First Mention** | Entity introduced for first time | Abel (first appearance) |
| **Integration** | Entity being integrated into narrative | Character entering scene |
| **Exiting** | Entity leaving narrative | Abel (dying) |
| **Restaging** | Entity reintroduced after absence | Character returning |
| **Offstage** | Entity mentioned but not present | Someone talked about |
| **Interrogative** | Entity in question | "Who?" |

**Languages That Need This:** Switch-reference languages (70% of PNG languages, Quechua, Navajo)

**Reproduction Accuracy:** ⚠️ **70%** → Target: **95%**
- Need to learn the 9-state system
- Apply consistently across all nouns

---

#### 5. Time Granularity

**What TBTA Has (20+ Categories):**

**From complete-field-taxonomy.md:**
```yaml
Time: Discourse                 # Timeless/gnomic
Time: Present                   # Right now
Time: Immediate Past            # Just happened
Time: Immediate Future          # About to happen
Time: Earlier Today
Time: Yesterday
Time: A Week Ago
Time: A Month Ago
Time: A Year Ago
Time: Historic Past
Time: Later Today
Time: Tomorrow
Time: A Year from Now
Time: Unknown Future
Time: During Speaker's Lifetime
```

**What Blind Discovery Had:**
- "Grammatical aspect" (perfective/imperfective)
- Recognized temporal distance matters
- Missed the 20+ granular categories

**How to Identify:**

1. **For narrative past events:**
   - Immediate Past: seconds/minutes ago
   - Earlier Today: hours ago (same day)
   - Yesterday: 1 day ago
   - A Week Ago / A Month Ago / A Year Ago: as stated
   - Historic Past: ancient times, before living memory

2. **For future events:**
   - Immediate Future: about to happen
   - Later Today: hours from now (same day)
   - Tomorrow: next day
   - A Year from Now: distant future
   - Unknown Future: indefinite

3. **For timeless/discourse:**
   - Discourse: generic truths, gnomic statements
   - Present: right now

**Languages That Need This:** Bantu languages (Swahili, Zulu), Tagalog, Quechua

**Reproduction Accuracy:** ❌ **30%** → Target: **90%**
- Use TBTA's taxonomy directly
- Context analysis for narrative chronology
- Some ambiguity is inherent

---

#### 6. Speaker Demographics (Dialogue)

**What TBTA Has:**

For EVERY dialogue clause:
```yaml
Speaker: [identity]                # Who is speaking
Listener: [identity]               # Who is listening
Speaker's Age: [age category]      # Speaker's age
Speaker-Listener Age: [relationship] # Age comparison
Speaker's Attitude: [attitude]     # Speaker's attitude toward listener
```

**Possible Values:**

**Speaker / Listener Identity:**
- Brother, Sister, Father, Mother, Son, Daughter
- Man, Woman, King, Servant
- Jesus, God, Angel, Disciple
- Religious Leader, Government Official
- Crowd, Group of Friends
- Written Material

**Speaker's Age:**
- Young Adult (18-24)
- Adult (25-49)
- Elder (50+)
- Middle Aged
- Old

**Speaker-Listener Age:**
- Essentially the Same Age
- Older
- Younger
- Older - Different Generation
- Younger - Different Generation

**Speaker's Attitude:**
- Neutral
- Familiar
- Honorable/Respectful

**What Blind Discovery Had:**
- Identified honorifics matter for Japanese, Korean, Javanese
- Missed that TBTA annotates this for ALL dialogue (not just honorific languages)

**How to Identify:**

1. **For every direct speech clause** (marked with QuoteBegin/QuoteEnd):
   - Identify speaker from narrative context
   - Identify listener(s)
   - Determine ages from narrative context (may require broader context)
   - Determine relationship (sibling, parent-child, etc.)
   - Determine attitude from tone/words used

2. **Example:** GEN 19:31
   ```yaml
   Speaker: Woman (older daughter)
   Listener: Woman (younger daughter)
   Speaker's Age: Young Adult (18-24)
   Speaker-Listener Age: Essentially the Same Age
   Speaker's Attitude: Familiar
   ```

**Languages That Need This:**
- Japanese (です/ます levels)
- Korean (7 speech levels)
- Javanese (ngoko/krama)
- Thai, Vietnamese (pronouns/particles)
- Hindi/Urdu (तू/तुम/आप)

**Reproduction Accuracy:** ⚠️ **60%** → Target: **95%**
- Annotate for ALL dialogue
- Not just "honorific languages"
- Requires narrative context knowledge

---

#### 7. Proximity / Demonstrative Systems

**What TBTA Has (9+ Categories):**

```yaml
Proximity: Near Speaker and Listener
Proximity: Near Speaker
Proximity: Near Listener
Proximity: Remote within Sight
Proximity: Remote out of Sight
Proximity: Temporally Near
Proximity: Temporally Remote
Proximity: Contextually Near
Proximity: Contextually Near with Focus
```

**What Blind Discovery Had:**
- Identified 3-way systems (Japanese, Korean, Spanish)
- Missed TBTA's full 9+ category system

**How to Identify:**

For demonstratives ("this," "that," "these," "those"):

1. **Spatial:**
   - Near Speaker and Listener: Both in proximity
   - Near Speaker: Close to speaker only
   - Near Listener: Close to listener only
   - Remote within Sight: Visible but distant
   - Remote out of Sight: Not visible

2. **Temporal:**
   - Temporally Near: Recent in time
   - Temporally Remote: Distant in time

3. **Discourse/Contextual:**
   - Contextually Near: In current discourse context
   - Contextually Near with Focus: In context + emphasized

**Languages That Need This:**
- 3-way: Japanese (kore/sore/are), Korean, Spanish, Turkish
- 4+ way: Some Native American languages

**Reproduction Accuracy:** ⚠️ **50%** → Target: **90%**
- Use full 9-category system
- Spatial analysis for narrative context
- Discourse tracking for contextual references

---

### TIER 3: Completely Missed (Need New Identification)

These were not identified in blind discovery:

#### 8. Illocutionary Force (Speech Acts)

**What TBTA Has:**

```yaml
Illocutionary Force: Declarative                # Statement
Illocutionary Force: Suggestive 'let's'         # Hortative
Illocutionary Force: Yes-No Interrogative       # Yes/no question
Illocutionary Force: Content Interrogative      # Wh- question
Illocutionary Force: 'should' Obligation        # Deontic obligation
Illocutionary Force: 'should not' Obligation    # Negative obligation
Illocutionary Force: Imperative                 # Command
```

**What Blind Discovery Had:**
- Mentioned speech acts vaguely
- Didn't realize every clause is annotated

**How to Identify:**

Analyze clause mood/function:

| Type | Markers | Example |
|------|---------|---------|
| **Declarative** | Statement of fact | "God created heaven and earth" |
| **Suggestive** | "Let's..." proposals | "Let us make man" |
| **Interrogative** | Questions | "Why do you...?" |
| **Imperative** | Commands | "Go and make disciples" |
| **Obligation** | "should," "must" | "You should not..." |

**Languages That Need This:**
- Affects verb mood selection
- Imperative forms vary widely
- Some languages distinguish subtypes

**Reproduction Accuracy:** ❌ **40%** → Target: **95%**
- Annotate EVERY clause
- Use linguistic analysis of mood/modality

---

#### 9. Discourse Genre

**What TBTA Has:**

```yaml
Discourse Genre: Climactic Narrative Story
```

**Observed:** 100% of clauses have this value in sample files.

**What Blind Discovery Had:** Nothing - completely missed

**How to Identify:**

In the sample, ALL verses are "Climactic Narrative Story." This appears to be because:
- Genesis: Narrative
- Matthew: Gospel narrative
- Proverbs: Embedded in narrative frame
- Epistles: Narrative mode (telling what happened)

**Hypothesis:** TBTA may only cover narrative portions of Scripture.

**Languages That Need This:**
- Affects aspect/tense selection
- Some languages have special narrative morphology
- Information structure differs by genre

**Reproduction Accuracy:** ❌ **0%** → Target: **100%**
- In practice: Always use "Climactic Narrative Story" for TBTA's covered verses
- For non-narrative genres (poetry, wisdom, prophecy), research needed

---

#### 10. Implicit

**What TBTA Has:**

```yaml
Implicit: 'No'   # Information is explicit
Implicit: 'Yes'  # Information is implicit/inferable (not observed in sample)
```

**Observed:** 100% of annotated words have `Implicit: 'No'`

**What Blind Discovery Had:** Nothing

**How to Identify:**

Mark whether information is:
- **Explicit ('No')**: Stated directly in the text
- **Implicit ('Yes')**: Inferable but not stated (e.g., subject pro-drop)

**Example (Hypothetical):**
- English: "He went" (subject explicit)
- Spanish: "Fue" (subject implicit - pro-drop language)
- If translating to Spanish, mark implicit

**Languages That Need This:**
- Pro-drop languages (Spanish, Italian, Japanese, Korean)
- Ellipsis languages
- Context-dependent languages

**Reproduction Accuracy:** ❌ **0%** → Target: **95%**
- Annotate for all words/phrases
- In sample, always 'No' (may be because source texts are explicit)

---

#### 11. Sequence

**What TBTA Has:**

```yaml
Sequence: Not in a Sequence    # Standalone
Sequence: First Coordinate      # First in "A and B"
Sequence: Coordinate            # Middle in "A, B, and C"
Sequence: Last Coordinate       # Last in "A and B"
```

**What Blind Discovery Had:** Nothing

**How to Identify:**

For coordinated structures ("and," "or"):

| Pattern | Sequence Value |
|---------|---------------|
| Single item | Not in a Sequence |
| A and B | A: First Coordinate, B: Last Coordinate |
| A, B, and C | A: First, B: Coordinate, C: Last |

**Example:** GEN 1:26 "fish and birds"
```yaml
- fish: First Coordinate
- and: [conjunction]
- birds: Last Coordinate
```

**Languages That Need This:**
- Affects coordinator placement (some languages use different words for first/last)
- Some languages mark sequence differently
- Information structure in coordinated clauses

**Reproduction Accuracy:** ❌ **0%** → Target: **100%**
- Straightforward syntactic analysis
- Mark all coordinated structures

---

#### 12. Vocabulary Alternate

**What TBTA Has:**

```yaml
Vocabulary Alternate: Single Sentence - Simple Vocabulary Alternate
Vocabulary Alternate: Single Sentence - Complex Vocabulary Alternate
```

**Example:** GEN 1:26 has TWO clause analyses:
1. Simple: "person be God"
2. Complex: "person have God image"

Both express "in God's image" but with different complexity.

**What Blind Discovery Had:** Nothing

**How to Identify:**

TBTA sometimes provides multiple translation strategies:
- **Simple:** Use simpler grammatical structures
- **Complex:** Use more sophisticated constructions

**Purpose:** Helps translators working with limited vocabulary or preliterate audiences.

**Languages That Need This:**
- Languages with limited Bible translation history
- Oral-focused translations
- Simple vocabulary for children

**Reproduction Accuracy:** ❌ **0%** → Target: **80%**
- Requires translation expertise
- May not be present in all verses

---

### TIER 4: Always-Present Universal Fields

These are straightforward and easily reproducible:

#### 13. Constituent

**What TBTA Has:**
```yaml
Constituent: God      # The actual word/morpheme
Constituent: create
Constituent: heaven
```

**How to Identify:** Simply the text of the word.

**Reproduction Accuracy:** ✅ **100%** - Trivial

---

#### 14. Part (Part of Speech)

**What TBTA Has:**
```yaml
Part: Noun
Part: Verb
Part: Adjective
Part: Adverb
Part: Conjunction
Part: Adposition
Part: Particle
Part: Space
Part: Period
```

**How to Identify:** Standard POS tagging.

**Reproduction Accuracy:** ✅ **100%** - Standard NLP

---

#### 15. LexicalSense

**What TBTA Has:**
```yaml
LexicalSense: A    # Primary sense
LexicalSense: B    # Secondary sense
LexicalSense: C    # Tertiary sense
[etc.]
```

**How to Identify:** Requires lexicon with sense distinctions.

**Reproduction Accuracy:** ⚠️ **Variable** - Needs lexicon

---

#### 16. SemanticComplexityLevel

**What TBTA Has:**
```yaml
SemanticComplexityLevel: '1'   # Always '1' in sample (100%)
```

**How to Identify:** In practice, always '1' for TBTA's data.

**Hypothesis:** May be a placeholder or planned feature not fully implemented.

**Reproduction Accuracy:** ✅ **100%** - Just use '1'

---

## Summary: Achieving 95%+ Accuracy

### What to Do Differently

| Feature | Old Approach | New Approach | Accuracy Gain |
|---------|-------------|--------------|---------------|
| **Speaker Demographics** | Only for honorific langs | Annotate ALL dialogue | +35% |
| **Time Granularity** | "Aspect" concept | Use 20+ categories | +60% |
| **Participant Tracking** | "Same/Different subject" | Use 9-state system | +25% |
| **Illocutionary Force** | Vague mention | Annotate every clause | +55% |
| **Proximity** | 3-way systems | Use 9-category system | +40% |
| **Discourse Genre** | Missed | Always annotate | +100% |
| **Sequence** | Missed | Mark coordination | +100% |
| **Implicit** | Missed | Mark all words | +100% |
| **Vocabulary Alternate** | Missed | Identify when present | +100% |

**Target Overall Score:** 9.5/10 (up from 8.2/10)

---

## Implementation Checklist

### For Each Verse:

**Document Level:**
- [ ] verse (identifier)
- [ ] source (tbta)
- [ ] version (1.0.0)

**For Each Clause:**
- [ ] Discourse Genre
- [ ] Illocutionary Force
- [ ] Speaker (if dialogue)
- [ ] Listener (if dialogue)
- [ ] Speaker's Age (if dialogue)
- [ ] Speaker-Listener Age (if dialogue)
- [ ] Speaker's Attitude (if dialogue)
- [ ] Topic NP
- [ ] Type
- [ ] Sequence

**For Each Phrase (NP, VP, etc.):**
- [ ] Semantic Role
- [ ] Relativized
- [ ] Sequence
- [ ] Implicit

**For Each Word:**
- [ ] Constituent
- [ ] Part
- [ ] LexicalSense
- [ ] SemanticComplexityLevel
- [ ] Implicit

**For Each Noun:**
- [ ] Number
- [ ] Person
- [ ] NounListIndex
- [ ] Participant Tracking
- [ ] Proximity (if demonstrative)
- [ ] Polarity
- [ ] Surface Realization

**For Each Verb:**
- [ ] Time
- [ ] Aspect
- [ ] Mood
- [ ] Polarity
- [ ] Adjective Degree (always "No Degree" for verbs)

**For Each Adjective:**
- [ ] Degree (No Degree, Comparative, Superlative)

**For Each Conjunction:**
- [ ] Implicit

---

## Validation: Test Your Accuracy

**Sample Verses to Test:**
1. Genesis 1:26 (clusivity, trial, speaker demographics)
2. Genesis 4:8 (entity tracking, participant tracking, dual)
3. Genesis 19:31 (speaker demographics, age, dual)
4. Matthew 5:10 (beatitude structure)
5. Philippians 2:4 (obligation illocutionary force)

**Compare your annotations against actual TBTA files**

**Success Metrics:**
- ✅ 90%+ field presence match (you identify all fields TBTA has)
- ✅ 90%+ value match (your values match TBTA's)
- ✅ 100% for core features (clusivity, number, entity tracking)

---

**Document Status:** Ready for Implementation
**Next Step:** Build annotation tool with this guide as reference
**Expected Accuracy:** 9.5/10 (95%) or higher

