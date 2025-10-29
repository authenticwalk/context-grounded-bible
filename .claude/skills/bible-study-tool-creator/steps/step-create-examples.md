# STEP: Create examples

**This is the most critical step.** The goal is to demonstrate the WHY behind creating this tool by finding profound insights that go beyond typical LLM knowledge. You must do actual research to find these insights.

**Parallel Research, Sequential Presentation**:
- You will use your subagent tool to start 5 processes simultaneously with 5 different Bible verses
- After research completes, present examples ONE AT A TIME using separate AskUserQuestion calls
- CRITICAL: Each example must be in its OWN separate AskUserQuestion - do NOT bundle multiple examples into one question with multiSelect
- Each question presents the full example text and asks for rating (Excellent/Good/Verify/Weak/Other)
- You will refine anything not excellent, accepting user feedback till you have the 5 examples
- You will append all the examples to bible-study-tools/{tool-name}/{tool-name}.yaml after each one is validated, along with the rating and any analysis of why it was good, bad and how you got the data.
  
**Research Process**:
1. **Do actual research**: Use WebSearch, explore existing bible data, or dry-run the tool concept on 3-5 test verses
2. **Remember how**: List which tools you used (websites, sources) to get the data so you will know how to reproduce it.
3. **Find insights beyond LLM memory**: Look for specific linguistic details, cross-cultural patterns, theological nuances that a typical LLM wouldn't know
4. **Format as Context/Insight/Value**: Each example must follow this structure
5. **Validate with user**: Present each example and get feedback

**Example Quality Standards**:
- ✅ **EXCELLENT**: Specific linguistic detail, clear theological stakes, actionable for translators
- ✅ **EXCELLENT**: Cross-cultural patterns that prevent translation errors
- ✅ **EXCELLENT**: Translation principles with pastoral consequences
- ⚠️ **GOOD**: Interesting insights but lower practical urgency
- ❌ **WEAK**: Things LLMs already know

**Reference Examples from Actual Research**:

**Example 1 (✅ EXCELLENT - Linguistic Detail)**:
**Context**: John 11:35 - "Jesus wept"
**Insight**: John deliberately uses different Greek verbs for weeping: δακρύω (quiet, controlled tears) for Jesus in v.35, but κλαίω (loud wailing, uncontrolled grief) for Mary and the Jews in v.33. This isn't stylistic variation—it's Christological theology showing Jesus' composed authority vs helpless despair. Most English translations use "wept" for both, losing this theological distinction. Russian ("прослезился") and Japanese ("涙を流した") preserve the quiet tears nuance.
**Value**: Helps translators choose appropriate weeping verbs and pastors preach on Jesus' humanity with theological precision.

**Example 2 (✅ EXCELLENT - Cross-Cultural Translation)**:
**Context**: John 11:35 across cultural contexts
**Insight**: The acceptability of Jesus' tears varies dramatically by language family: Indo-European cultures accept grief tears, Semitic expects public male grief, Sino-Tibetan accepts if restrained (Confucian mean), Niger-Congo varies (some cultures stigmatize adult male tears). In some Niger-Congo cultures, literal "Jesus wept" could be culturally problematic for an adult male, requiring adaptation to "Jesus showed sorrow" (Swahili: "Yesu alionyesha huzuni").
**Value**: Prevents cultural mistranslation that could undermine Jesus' masculinity/authority in honor-shame cultures, and shows how each culture highlights different Christological facets.

**Example 3 (✅ EXCELLENT - Translation Principle)**:
**Context**: Matthew 5:4 - "Blessed are those who mourn"
**Insight**: Some Reformed/evangelical translations add "for their sins" to Matthew 5:4, but Matthew's ambiguity is pastoral—it allows mourning of sin, world's brokenness, death/loss, persecution, or God's absence. Adding "for their sins" closes all other interpretive options. A bereaved person mourning death may not see themselves in the beatitude if sin is specified.
**Value**: Teaches translators that inspired ambiguity shouldn't be "clarified" away—don't narrow what the inspired author wisely left broad.

**Example 4 (✅ EXCELLENT - Theological/Pastoral Stakes)**:
**Context**: Matthew 5:4 - "will be comforted" vs "are comforted"
**Insight**: Changing future tense to present tense seems minor but has critical consequences: future tense sustains hope amid present grief (inaugurated eschatology: blessed now, comforted later) and is pastorally realistic. Present tense creates cognitive dissonance ("If I'm comforted now, why am I still grieving?"), false expectations of immediate comfort, and violates Matthew's eschatological framework.
**Value**: Prevents theological distortion and pastoral damage—this isn't stylistic, it's eschatological theology.

**Example 5 (✅ EXCELLENT - Fundamental Translation Principle)**:
**Context**: Matthew 5:4 - "will be comforted" (passive voice)
**Insight**: Indo-European preserves passive naturally ("will be comforted"), Semitic uses divine passive idiom (recognizes unstated agent is God), Niger-Congo requires explicit agent ("God will comfort them"), Sino-Tibetan uses active reception ("will receive comfort" - 必得安慰). All four preserve identical theology (God comforts, they receive) through different grammatical vehicles.
**Value**: Shows translators that grammatical variation ≠ theological contradiction; challenges Indo-European bias that passive must be preserved.

**Example 6 (⚠️ GOOD - Interesting but Lower Priority)**:
**Context**: Ephesians 1:3 - Paul's εὐλογ- wordplay
**Insight**: Paul uses εὐλογ- root three times: εὐλογητός (blessed be), εὐλογήσας (who blessed), εὐλογίᾳ (with blessing) - "Blessed be God who blessed us with every blessing." Most English translations flatten this wordplay which creates an intensive spiral. Russian captures some of it.
**Value**: Helps pastors see Paul's rhetorical intensity for preaching, but less critical for translation work.

**Example 7 (❌ WEAK - Typical LLM Knowledge)**:
**Context**: John 11:35
**Insight**: "Jesus wept" shows His humanity and compassion for those who grieve.
**Value**: Encourages believers that Jesus understands their pain.
**Why WEAK**: Any LLM would already say this. No specific linguistic detail, no cross-cultural insight, no translation challenge addressed.

**Format for Each Example**:
```
**Context**: [Specific verse or concept being analyzed]
**Insight**: [What the tool reveals - must be beyond typical LLM knowledge]
**Value**: [How this helps Bible translators, pastors, or students]
```

**Process for Each Example**:

After researching and formulating an example, present it to the user using **ONE** AskUserQuestion call per example.

**CRITICAL**: Ask about examples ONE AT A TIME in separate AskUserQuestion calls. Do NOT bundle all 5 examples into a single multiSelect question.

**Template for EACH individual example**:
```
AskUserQuestion with:
- question: "[Full example text with **Context**, **Illustration**, **Connection**, **Value** sections]"
- header: "Example [N] Rating"
- multiSelect: false
- options:
  - label: "✅ EXCELLENT - Make this a goal"
    description: "Really helpful, profound insight beyond typical LLM knowledge"
  - label: "⚠️ GOOD - Interesting but not critical"
    description: "Useful but lower priority or practical urgency"
  - label: "🔍 VERIFY - Check sources first"
    description: "Potentially good but needs verification for accuracy"
  - label: "❌ WEAK - Needs refinement"
    description: "Not helpful, incorrect, or something LLMs already know"
```

**Present examples sequentially**: After getting feedback on Example 1, move to Example 2, etc. This allows the user to review each example thoroughly in its own tab.

**Critical Validation Questions**:
- Does this insight go beyond what a typical LLM would say?
- Is it specific and concrete (names actual verses, languages, or cultural patterns)?
- Does it have clear practical value for translators/pastors/students?
- Does it prevent errors or unlock new understanding?
- Ensure it is noteworthy.  If a user asks an LLM, tell me everything you know about this verse in 1000 words or less would this likely come up?  If so, likely not worth adding.
- Is it true.  LLMs tend to hallucinate, is this potentially made up?  Can it be supported by multiple sites and books
- Is it helpful.  Will it make any practical difference.
- Is it family friendly.  Only show examples that are rated E for everyone. 

Collect 5 examples total. Aim for at least 4-5 "EXCELLENT" rated examples. If an example gets "Not helpful" feedback, research a replacement.

**After gathering 5 validated examples**, stub in the tools README.md file with the tool's name and these examples.