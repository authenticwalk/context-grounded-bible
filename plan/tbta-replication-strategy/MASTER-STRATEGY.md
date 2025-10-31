# TBTA Replication Strategy

## Goal

Reproduce TBTA annotations with 95%+ accuracy using Opus subagent with extensive reasoning, validated by main agent evaluation.

## Core Approach

```
Opus Subagent (deep thinking) → Generates annotations
    ↓
Main Agent (evaluator) → Validates against actual TBTA
    ↓
Debug & Iterate → Fix mismatches, improve prompts
```

## Phase 1: Language Research (REQUIRED BEFORE REPLICATION)

### Objective
For each TBTA field, document ALL languages that need it with 7+ real examples.

### Requirements Per Field

**For each of 41 TBTA fields, create:**

`/plan/tbta-replication-strategy/fields/{field-name}.md`

**Must contain:**
1. **Field definition** (from TBTA schema)
2. **7+ languages** that grammatically require this (confirmed, not guessed)
3. **7+ real examples** (specific Bible translations showing usage)
4. **Coverage assessment** (what % of world's 7000+ languages need this)

**Example:** `fields/trial-number.md`
```markdown
# Trial Number (Exactly 3 Entities)

## Definition
Grammatical number marking for exactly 3 items (separate from plural).

## Languages Confirmed (7+)
1. **Kilivila** (kij) - Austronesian, PNG - Has sg/du/trial/pl
2. **Larike** (lar) - Austronesian, Maluku - Full trial system
3. **Marshallese** (mah) - Micronesian - Trial in pronouns
4. **Biak** (bhw) - Papua - Trial marking required
5. **Tolomako** (tlm) - Vanuatu - Trial distinct from plural
6. **Mokilese** (mkj) - Micronesian - Trial in all noun classes
7. **Owa** (stn) - Solomon Islands - Trial obligatory

## Real Examples (7+)
1. GEN.1.26 in Kilivila: [translation showing trial form]
2. GEN.1.26 in Larike: [translation showing trial form]
[... 5 more examples with actual translations]

## Coverage
~7 languages confirmed (0.1% of world languages)
Primarily: Austronesian family, Oceania region
TBTA marks this in 1 verse (GEN.1.26 - Trinity)
```

### Research Sources
- WALS (World Atlas of Language Structures)
- eBible corpus (1000+ translations)
- Ethnologue language profiles
- Grammar references (search: "{language} grammar trial number")

### Success Criteria
- ✅ All 41 fields documented
- ✅ 7+ languages per field (confirmed, not theoretical)
- ✅ 7+ real translation examples per field
- ✅ Coverage % calculated

## Phase 2: Reproduction Testing

### Test Verses (Diverse Coverage)

```
GEN.1.26   - Trial number, First Inclusive, clusivity
GEN.4.8    - Dual number, entity tracking, dialogue
GEN.19.31  - Speaker demographics (age, relationship, attitude)
MAT.5.10   - Beatitude structure, passive voice
PRO.15.3   - Wisdom genre, metaphor, poetic structure
PHP.2.4    - Obligation illocutionary force, epistolary
LUK.6.34   - Rhetorical questions, indirect speech acts
EPH.1.23   - Complex theology, abstract concepts
1SA.26.12  - Narrative, multiple participants
1KI.11.1   - List structure, multiple entities
```

### Replication Process

**For each test verse:**

1. **Subagent Generation** (Opus with thinking)
   ```
   Prompt includes:
   - Full TBTA field taxonomy
   - Reproduction guide (95% accuracy path)
   - Language research for relevant fields
   - Verse text from multiple translations
   - Deep thinking enabled
   ```

2. **Main Agent Evaluation**
   - Load actual TBTA file for verse
   - Compare field-by-field
   - Calculate match rate
   - Identify mismatches with reasons

3. **Debug & Iterate**
   - For each mismatch:
     - Why did subagent get it wrong?
     - Missing context?
     - Ambiguous guidance?
     - Update prompt/documentation
   - Re-test same verse
   - Track improvement

4. **Track Alternates**
   - Fields TBTA has that seem questionable
   - Fields TBTA missed that languages need
   - Document in `/plan/tbta-replication-strategy/improvements.md`

### Evaluation Metrics

**Per Verse:**
```yaml
total_fields: 147
matched: 140
mismatched: 7
accuracy: 95.2%

mismatches:
  - field: "Speaker's Age"
    tbta_value: "Young Adult (18-24)"
    generated_value: "Adult (25-49)"
    reason: "Age not explicit in text, inference differs"

  - field: "Participant Tracking"
    tbta_value: "Frame Inferable"
    generated_value: "Routine"
    reason: "Discourse context interpretation differs"
```

**Target:**
- ✅ 95%+ accuracy on clear fields (Part, Number, Constituent)
- ✅ 80-90% on interpretive fields (Speaker Age, Time Granularity)
- ✅ 100% on fields marked for review when uncertain

## Phase 3: Prompt Engineering

### Iteration Cycle

```
Test → Evaluate → Debug → Update Prompt → Re-test
```

### Prompt Components

1. **Field Taxonomy** (complete-field-taxonomy.md)
2. **Reproduction Guide** (reproduction-guide-95-percent.md)
3. **Language Research** (fields/*.md for relevant features)
4. **Verse Context** (from eBible translations)
5. **Evaluation Rubric** (what counts as correct match)

### Debugging Log

Track in `/plan/tbta-replication-strategy/debug-log.md`:

```markdown
## GEN.1.26 - Iteration 1
**Accuracy:** 87.2% (128/147 fields)

**Major Mismatches:**
- Trial Number: Generated "Plural" → Should be "Trial"
  - Fix: Emphasized theological context, Trinity = exactly 3

- First Inclusive: Generated "Third" → Should be "First Inclusive"
  - Fix: Added clusivity decision tree

## GEN.1.26 - Iteration 2
**Accuracy:** 94.5% (139/147 fields)
[improvements noted]
```

## Phase 4: Scale & Validate

### Test Across Bible

1. **Genesis** (narrative, creation, patriarchs)
2. **Psalms** (poetry, metaphor, emotion)
3. **Proverbs** (wisdom, gnomic)
4. **Isaiah** (prophecy, complex imagery)
5. **Gospels** (teaching, dialogue, parables)
6. **Epistles** (abstract theology, argumentation)
7. **Revelation** (apocalyptic, symbolism)

### Success Criteria

- ✅ 95%+ accuracy across all genres
- ✅ 100% accuracy on Tier 1 fields (mechanical)
- ✅ 90%+ accuracy on Tier 2 fields (interpretive)
- ✅ Items flagged for review when uncertain

## File Structure

```
plan/tbta-replication-strategy/
├── MASTER-STRATEGY.md (this file)
├── complete-field-taxonomy.md (41 fields cataloged)
├── reproduction-guide-95-percent.md (how to achieve 95%)
├── comprehensive-language-research.md (initial research)
├── fields/
│   ├── trial-number.md (7+ langs, 7+ examples)
│   ├── clusivity.md (7+ langs, 7+ examples)
│   ├── dual-number.md (7+ langs, 7+ examples)
│   └── [... 38 more field docs]
├── debug-log.md (iteration tracking)
├── improvements.md (TBTA gaps/additions)
└── test-results/
    ├── GEN.1.26-iteration-1.yaml
    ├── GEN.1.26-iteration-2.yaml
    └── [... more test outputs]
```

## Key Principles

1. **Deep Thinking First** - Opus with extensive reasoning before generation
2. **Evidence-Based** - 7+ confirmed languages, 7+ real examples per field
3. **Iterate Rapidly** - Test, evaluate, debug, improve, repeat
4. **Track Everything** - All mismatches logged with reasons
5. **Conservative Marking** - Flag uncertainty, don't guess

## Next Steps

1. ✅ Research complete (comprehensive-language-research.md exists)
2. ✅ Field taxonomy complete (complete-field-taxonomy.md exists)
3. ✅ Reproduction guide complete (reproduction-guide-95-percent.md exists)
4. ⏳ **START HERE:** Create detailed field docs (fields/*.md)
5. ⏳ Build Opus subagent prompt
6. ⏳ Test first verse (GEN.1.26)
7. ⏳ Evaluate and iterate

---

**Status:** Ready to begin field documentation and subagent testing

**Target Accuracy:** 95%+ with uncertainty flagging

**Model:** Opus (maximum thinking capability)
