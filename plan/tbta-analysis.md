# TBTA Database Export Analysis

## Purpose
Analyzing https://github.com/AllTheWord/tbta_db_export to understand:
1. What problem it solves for Bible translators
2. How it compares to Macula work in our project
3. How it could benefit our context-grounded Bible project

## Status
- [x] Fetch TBTA repository information
- [x] Review Macula implementation in our codebase
- [x] Understand TBTA's approach to encoding linguistic features
- [ ] Compare TBTA vs Macula approaches
- [ ] Generate concrete examples of translation edge cases
- [ ] Document findings for user review

## Initial Findings

### What TBTA Is
- **Full name**: The Bible Translator's Assistant
- **Approach**: Rules-based system with highly annotated source text
- **Format**: Converts internal database to JSON/XML exports
- **Focus**: Encoding semantic and syntactic information via character-based codes

### What Macula Is (Our Current Implementation)
- **Source**: Clear Bible's Macula Hebrew (WLC) and Greek (Nestle1904) datasets
- **Approach**: Scholarly linguistic annotation with morphological, lexical, semantic, and syntactic data
- **Format**: YAML files with structured fields
- **Focus**: Word-by-word analysis with domains (Louw-Nida, SDBH), morphology, discourse tracking

## Key Differences Emerging

### TBTA Strengths
1. **Participant tracking across discourse** - detailed noun indexing (1-9, A-Z)
2. **Speaker-listener demographics** - age, relationship, speech style encoding
3. **Implicit information** - marks culturally-dependent context
4. **Multiple valid interpretations** - supports alternative analyses
5. **Cross-linguistic variation focus** - designed for edge cases

### Macula Strengths
1. **Scholarly precision** - based on academic linguistic datasets
2. **Rich semantic domains** - Louw-Nida (Greek) and SDBH (Hebrew)
3. **Clear field structure** - easy to parse and query
4. **Translation glosses** - includes English/Mandarin (Hebrew)
5. **Critical for theology** - article presence, verbal aspect, etc.

## Translation Edge Cases to Explore

### Examples from User
- **Person/Number systems**: Languages with 1, 2, 3, 4, 5+ person distinctions (not just singular/plural)
- **Gender systems**: Languages with different gender categories
- **Evidentiality**: Languages requiring source-of-knowledge marking
- **Honorifics**: Languages with complex politeness/relationship marking

## Key Findings from TBTA Data

### Unique Features in TBTA (Not in Macula)

#### 1. **Number System** (Position 5 in Noun codes)
Beyond singular/plural:
- `S` - Singular
- `D` - Dual (exactly 2)
- `T` - Trial (exactly 3) ✨ FOUND IN GEN 1:26
- `Q` - Quadrial (exactly 4)
- `p` - Paucal (a few, small number)
- `P` - Plural

#### 2. **Person System** (Position 10 in Noun codes)
Beyond 1st/2nd/3rd person:
- `1` - First
- `2` - Second
- `3` - Third
- `A` - First Inclusive ✨ FOUND IN GEN 1:26 ("we" including the listener)
- `B` - First Exclusive ("we" excluding the listener)
- `F` - First as Third
- `S` - Second as Third
- `I` - First Inclusive as Third
- `E` - First Exclusive as Third

#### 3. **Participant Tracking** (Position 6 in Noun codes)
Tracks how entities are introduced/referenced:
- `I` - First Mention (new entity)
- `D` - Routine (established participant)
- `i` - Integration
- `E` - Exiting (leaving the narrative)
- `R` - Restaging (reintroduced after absence)
- `O` - Offstage
- `G` - Generic
- `Q` - Interrogative
- `F` - Frame Inferable (can be inferred from context)

#### 4. **Speaker-Listener Demographics** (Clause level)
✨ FOUND IN GEN 19:31
- Speaker's Age: "Young Adult (18-24)", "Middle Aged", "Old", etc.
- Speaker-Listener Age: "Essentially the Same Age", "Older", "Younger"
- Speech Style: Formal, Informal, etc.
- Speaker's Attitude: Neutral, Respectful, etc.

#### 5. **Proximity** (Position 8 in Noun codes)
Demonstrative distinctions:
- `N` - Near Speaker and Listener
- `S` - Near Speaker
- `L` - Near Listener
- `R` - Remote within Sight
- `r` - Remote out of Sight
- `T` - Temporally Near
- `t` - Temporally Remote
- `C` - Contextually Near with Focus
- `c` - Contextually Near

#### 6. **Time Granularity** (Position 4 in Verb codes)
Fine-grained temporal distinctions:
- `D` - Immediate Past
- `A` - Earlier Today
- `a` - Yesterday
- `b` - 2 Days Ago
- `c` - 3 Days Ago
... up to eternity past/future

#### 7. **Noun List Index** (Position 4 in Noun codes)
Tracks which nouns refer to same entity:
- Uses `1-9, A-Z, a-z` (62 possible entities per verse)
- If two nouns have same index, they're the exact same thing
- If two "thing"s have different indices, they're different items

## TBTA vs Macula: Complementary Strengths

### Macula Excels At:
1. **Scholarly linguistic precision** - morphology, case, tense, aspect
2. **Semantic domains** - Louw-Nida (Greek), SDBH (Hebrew)
3. **Strong's numbers** - lexical connections
4. **Syntactic roles** - subject, object, predicate
5. **Theological precision** - article presence, verbal aspect critical for theology

### TBTA Excels At:
1. **Cross-linguistic edge cases** - number/person systems that don't match English
2. **Discourse tracking** - participant flow through narrative
3. **Translation pragmatics** - speaker/listener relationships, age, attitude
4. **Contextual inference** - what can be left implicit in target language
5. **Entity disambiguation** - which nouns refer to same thing

### They Are Complementary!
- Macula: "What does the Greek/Hebrew say grammatically?"
- TBTA: "How should this be rendered in a language with different categories?"

## Concrete Translation Edge Cases (How TBTA Helps)

### Example 1: Trial Number in Genesis 1:26

**Verse:** "Then God said, 'Let us create person...'"

**TBTA Data:**
```json
{
  "Constituent": "God",
  "Number": "Trial",          // Exactly 3 persons!
  "Person": "First Inclusive"  // "us" including the listener
}
```

**Translation Problem:**
- English: Only singular/plural ("we" is ambiguous)
- Many Austronesian & Polynesian languages: Have **dual** (2), **trial** (3), **paucal** (few)
- In these languages, you MUST choose the right number or it sounds wrong

**How TBTA Helps:**
A translator working in a language with trial number now knows:
- God is speaking as exactly **3 persons** (Trinity!)
- Use trial form, not plural
- First Inclusive means "we" includes the Trinity members being addressed

**Without TBTA:** Translator might default to generic plural, losing the theological precision.

---

### Example 2: First Inclusive vs Exclusive (Malay, Tagalog, Fijian, etc.)

**Problem:** Many languages distinguish:
- **Inclusive "we"** = me + you (speaker + listener)
- **Exclusive "we"** = me + others (speaker + others, but NOT you the listener)

**English doesn't distinguish this!** "We" is ambiguous.

**Example Verse:** Acts 15:25 - "It seemed good to us..."
- Is this "us" = apostles + congregation (inclusive)?
- Or "us" = apostles only, speaking to congregation (exclusive)?

**TBTA Encoding:**
```
Person: "First Exclusive" = apostles speaking, congregation listening
```

**How This Helps:**
- Tagalog translator knows to use **"kami"** (exclusive), not **"tayo"** (inclusive)
- Without this, translator must guess from context
- TBTA has already analyzed the discourse participants

---

### Example 3: Participant Tracking - Which "he" is which?

**Verse:** Genesis 4:8 - "Cain said to Abel his brother, and he rose up and he killed him"

**Problem:** Multiple "he"s - who did what?

**TBTA Noun List Index:**
```
Cain - Index "1"
Abel - Index "2"
brother - Index "2" (same as Abel)
```

**Plus Participant Tracking:**
```
Cain: "Routine" (established participant, subject)
Abel: "Routine" then "Exiting" (dies in this verse)
```

**How This Helps:**
Languages with **switch-reference** (many Native American, Papua New Guinea languages) need to know when subject changes:
- Cain speaks (subject = Cain)
- Cain rose up (same subject marker)
- Cain killed Abel (same subject, different object)

Without explicit tracking, translator might misidentify who did what!

---

### Example 4: Demonstrative Proximity - "this" vs "that" distinctions

**English:** Near (this/these) vs Far (that/those) - 2-way system

**Many languages:** 3-way, 4-way, or even 5-way systems!
- Japanese: これ (kore - near me) / それ (sore - near you) / あれ (are - far from both)
- Korean: Similar 3-way
- Spanish: este (this near me) / ese (that near you) / aquel (that far away)
- Some Native American languages: Near me / Near you / Near us both / Remote visible / Remote invisible

**TBTA Proximity Codes:**
```
N - Near Speaker and Listener
S - Near Speaker
L - Near Listener
R - Remote within Sight
r - Remote out of Sight
T - Temporally Near
t - Temporally Remote
C - Contextually Near with Focus
```

**Example:** John 1:29 - "Behold the Lamb of God"
- Is Jesus near John? Near the audience? Far but visible?
- TBTA can encode: "Near Speaker (John), Remote from original listeners"
- Japanese translator knows: use それ (sore)

---

### Example 5: Time Granularity - When did it happen?

**Problem:** Some languages **require** specific time markers

**Tagalog:** Different verb forms for:
- Just now
- Earlier today
- Yesterday
- Long ago

**TBTA Time Codes:** (20+ distinctions!)
```
D - Immediate Past
A - Earlier Today
a - Yesterday
b - 2 Days Ago
c - 3 Days Ago
d - A Week Ago
e - A Month Ago
...
h - Historic Past
```

**How This Helps:**
- Narrative in Genesis: Use "Historic Past" → Tagalog past remote form
- Jesus' words in John: May use "Discourse" (timeless) → Tagalog generic form
- Translator doesn't have to guess the temporal distance

---

### Example 6: Speaker Demographics - Age & Relationship

**Verse:** Genesis 19:31 - Older sister speaking to younger sister

**TBTA Data:**
```json
{
  "Speaker": "daughter",
  "Listener": "daughter",
  "Speaker`s Age": "Young Adult (18-24)",
  "Speaker-Listener Age": "Essentially the Same Age",
  "Speaker`s Attitude": "Neutral"
}
```

**How This Helps:**

**Japanese/Korean:** Must choose verb endings based on:
- Age (older/younger)
- Social relationship (sibling, stranger, superior)
- Formality level

**Example:**
- Sisters of same age → casual form (よ / yo)
- Younger to older → respectful form (です / desu)
- Without age data, translator might use wrong register!

**Javanese/Balinese:** Have 3-5 politeness levels that are REQUIRED:
- Ngoko (low, intimate)
- Madya (middle)
- Krama (high, respectful)

TBTA provides the social context to choose correctly.

---

## Summary: Why This Matters for Our Project

### For AI-Grounded Bible Translation

When an AI helps with Bible translation, it needs to know:

1. **What the source says** (Macula provides this)
   - Morphology, syntax, semantics
   - Greek/Hebrew grammatical details

2. **How to map it to target language** (TBTA provides this)
   - Number systems beyond singular/plural
   - Person systems with inclusive/exclusive
   - Participant tracking across discourse
   - Demonstrative/proximity distinctions
   - Time granularity requirements
   - Social register (age, relationship, formality)

### Macula + TBTA = Comprehensive AI Context

**Current state:** Our project has Macula
- ✅ Excellent for linguistic analysis
- ✅ Great for exegesis
- ✅ Strong's numbers, semantic domains
- ❌ Doesn't address cross-linguistic edge cases

**With TBTA added:**
- ✅ All of the above
- ✅ PLUS guidance for 1000+ language features that differ from English
- ✅ Prevents translation errors in edge-case languages
- ✅ Provides explicit discourse tracking
- ✅ Encodes social/pragmatic information

### Real-World Impact

**Scenario:** AI assists translator working in:
- Kilivila (Papua New Guinea) - has trial number
- Ilokano (Philippines) - has inclusive/exclusive distinction
- Japanese - needs demonstrative proximity + age-based register

**Without TBTA:** AI might say:
- "Use plural" → Wrong! Should be trial.
- "Use 'we'" → Ambiguous! Inclusive or exclusive?
- "Use 'that'" → Which "that"? Japanese has 3!

**With TBTA:** AI can say:
- "Source has Trial number (3 persons) → use trial form"
- "First Inclusive → use inclusive 'we' (including listener)"
- "Near Speaker → use これ (kore) not それ (sore)"

This prevents **translation errors** and provides **cultural-linguistic precision**.
