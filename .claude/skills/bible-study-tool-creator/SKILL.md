---
name: bible-study-tool-creator
description: Interactive skill for creating new bible study tools that generate AI-readable commentary data. Guides users through defining practical tasks, setting up proper file structure, and establishing self-learning loops for data generation.
---

# Bible Study Tool Creator

## Overview

This skill helps create new bible study tools for the Context-Grounded Bible project through an interactive, step-by-step process. Each tool generates specific types of AI-readable commentary data (YAML files) that ground AI systems in truth when working with Biblical texts.

## When to Use

Use this skill when:
- Creating a new bible study tool
- Initializing file structure for a data generation task
- Setting up a self-learning loop for AI-driven biblical analysis

Do NOT use this skill when:
- Working on an existing tool (use that tool directly)
- Just querying Bible data (use other skills like quote-bible)

## How It Works

This skill guides Claude to interactively gather information from the user one question at a time, then generates all necessary files. The process:

1. Check for duplicate tools
2. Ask focused questions using AskUserQuestion tool
3. Build tool definition progressively
4. Generate complete file structure
5. Set up self-learning loop

## Interactive Creation Process

### Step 1: Understand User Intent

First, check if the user already described what tool they want to create when invoking the skill. Look for context like:
- "create a tool to provide all the greek words for each verse"
- "I want to summarize Matthew Henry's Commentary"
- "analyze cultural metaphors across different translations"

**If the user already provided a description**: Capture that intent and proceed to Step 2.

**If no description was provided**: Brainstorm concrete tool ideas based on the project's mission to help Bible translators, pastors, and students.  You should have already done a ls -la of ./bible-study-tools when you checked for duplicates, *NEVER* suggest a tool that already exists.  Brainstorm similar ideas.  Then present them as options using AskUserQuestion:

```
Question: "What would you like this Bible study tool to do?"
Options (brainstorm 3-4 specific, valuable ideas):
- Extract Greek/Hebrew words with their definitions; focusing on the unique meaning in this verse
- Compare cultural adaptations of metaphors across minority language translations
- Analyze commentaries for key points about this verse
- Find movie clips, stories and other art that would illustrate this verse really well
- Other (I have a different idea)
```

When brainstorming ideas, focus on:
- Tasks that address real translation/interpretation challenges
- Analysis that LLMs can't do well from memory alone
- Data that would genuinely help translators/pastors/students

If user selects "Other", ask them to describe their idea in their own words.

Store their response as the initial tool concept.

### Step 2: Search for Existing Tools

Before proceeding, search for existing tools that might already do what the user wants. This avoids duplication.

**Check the directory**:
```bash
ls -la /Users/chrispriebe/projects/context-grounded-bible/bible-study-tools/
```

**For each existing tool**, read its `README.md` and check if it matches the user's intent:
- What does it do?
- What are its goals?
- How does it differ from what the user described?

**If tools match**: list them in a AskUserQuestion tool with the name for the description compare it's description/goals to the users.  Your dialogue will be "There are several tools similar to this, which one do you want to work on?"  The final option is explain how yours is unique

**If no match found**: Proceed with creation.

### Step 2b: Refine the edit they want to make 

If they are choosing to edit a tool carefully look through the tools `README.md` and `LEARNING.md` and determine if there are suggestions in there of creating a similar tool.  Find the most relevant and potentially helpful and suggest those with the last option being to edit this tool itself.

### Step 3: Suggest Tool Name

Based on the user's intent and existing tools, suggest 2-3 well-formed tool names following best practices. This single identifier will be used for both the directory name AND in filenames like `MAT-5-3-{tool-name}.yaml`.

You will need to read SCHEMA.md and STANDARDIZATION.md before suggesting a name.

It is better to only suggest 1 name then let them add their own instead of making up names to fill the space.  Only add more names if the task is a little unclear as you can use this to show the possibilities of what they mean in the task and refine their intention.

**Naming Best Practices**:
1. **Largest theme first**: "semantic-groups-overlapping" not "overlapping-semantic-groups" (enables scalability)
2. **Consistent terminology**: Use "bible" consistently (not mixing "bible" and "scripture")
3. **Dash separators**: Use kebab-case (e.g., "cultural-metaphors")
4. **Schema alignment**: Use terminology that aligns with SCHEMA.md headings when possible
5. **Descriptive specificity**: Name should clearly indicate what the tool does
6. **Favor readability**: Keep it concise with abbreviations where natural, but prioritize clarity
7. **Avoid expert-only acronyms**: Don't use industry-specific jargon that requires expertise to understand
8. **Prefer industry standard terms**: Prefer words that are industry specific, for example if it is about word parsing and grouping use the term prefered by the bible translation industry.

**Process**:
1. Check existing tools in `/bible-study-tools/` to identify naming patterns
2. Read SCHEMA.md to understand schema terminology
3. Based on user intent, suggest 2-3 names using AskUserQuestion

**Special Cases**
1. If their task is an extension of another task then share the same prefix whenever possible. For example: "source-language-strongs" to "source-language-strongs-in-content" as they will also use strongs but focus more on which strong definition is the best
2. If they described it incorrectly like "greek word analysis" but to cover all books it should be "source word analysis" suggest the correct
3. If they describe it using one word like "semantic grouping" but there are synonyms used in the current tools suggest the synomyn word as the first option then their words second.  Ex. semantic-groupings a) multi-word-expression-grouping b)semantic-grouping c) (write your own)

Example for "semantic grouping" tool:
```
Question: "Which name best fits this tool?"
Options:
- clusters-multi-word-expressions
- clusters-semantic-meaning
- other: (write your own)
```

### Step 4: Research and Propose Concrete Examples

**This is the most critical step.** The goal is to demonstrate the WHY behind creating this tool by finding profound insights that go beyond typical LLM knowledge. You must do actual research to find these insights.

**Research Process**:
1. **Do actual research**: Use WebSearch, explore existing bible data, or dry-run the tool concept on 3-5 test verses
2. **Find insights beyond LLM memory**: Look for specific linguistic details, cross-cultural patterns, theological nuances that a typical LLM wouldn't know
3. **Format as Context/Insight/Value**: Each example must follow this structure
4. **Validate with user**: Present each example and get feedback

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

After researching and formulating an example, 

present it to the user using AskUserQuestion:

```
Question: "{example}

Options:
- This is really helpful, make this a goal (✅ EXCELLENT)
- Interesting but not critical (⚠️ GOOD but lower priority)
- Are you sure this is accurate, check more sources and verify it first.
- Not helpful or incorrect (❌ WEAK - needs refinement)
- Other: (share your feedback or suggest a different example to explore)
```

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

### Step 5: Define Output Structure

Ask the user to describe the YAML structure they envision. Provide guidance:

```
"What data should each YAML file contain? Describe the structure, for example:
- Field names
- What each field represents
- Whether fields contain simple values, lists, or nested objects"
```

From their description, create both:
- `data_structure`: A complete example with sample data
- `yaml_structure_inline`: A concise version showing just the field hierarchy

### Step 6: Select Test Verse

Ask the user which verse to use for initial testing:

```
Question: "Which verse should we use for initial testing?"
Options:
- JHN 3:16 (Very familiar, good baseline)
- MAT 5:3 (Beatitudes, theological depth)
- GEN 1:1 (Creation, ancient context)
- PSA 23:1 (Poetry, metaphor-rich)
- Other (specify a verse)
```

### Step 7: Build Tool Definition YAML

Consolidate all gathered information into a YAML file at `/tmp/tool-definition.yaml`:

```yaml
tool_name: "[Tool Name in Proper Case, e.g., 'Semantic Groups']"
tool_name_kebab: "[kebab-case identifier, e.g., 'semantic-groups']"
task_name: "[SAME as tool_name_kebab - used in filenames like MAT-5-3-semantic-groups.yaml]"
description: "[One sentence description]"
test_verse: "[Selected verse e.g., JHN 3:16]"

goals_formatted: |
  1. [Goal 1]
  2. [Goal 2]
  3. [Goal 3]
  [etc.]

examples_formatted: |
  ### Example 1
  **Context**: [Context from user]
  **Insight**: [Insight from user]
  **Value**: [Value from user]

  ### Example 2
  [...]

  [... all 5 examples ...]

related_tools: "[List any related tools or 'None yet']"

data_structure: |
  ```yaml
  [Complete example structure with sample data]
  ```

yaml_structure_inline: |
  [Concise field hierarchy]
```

Note: `task_name` should always equal `tool_name_kebab` to maintain consistency.

### Step 8: Run Initialization Script

Execute the Python script to generate all files:

```bash
python3 /Users/chrispriebe/projects/context-grounded-bible/.claude/skills/bible-study-tool-creator/init-tool.py /tmp/tool-definition.yaml
```

The script creates this structure in `/bible-study-tools/{tool-name}/`:

**Files created**:
- `README.md` - Tool overview with description, goals, and examples
- `LEARNING.md` - Experiment log for self-learning loop
- `{tool-name}-template.md` - Agent prompt template
- `tests/README.md` - Test framework documentation

### Step 9: Update Related Tools (if applicable)

If this tool is a variant of or related to existing tools, update those tools' README.md files to cross-reference the new tool. Also summarize key learnings from related tools' LEARNING.md files.

### Step 10: Confirm Creation

Show the user a concise summary:

```
✅ Successfully created bible study tool: {tool-name}

Created files in /bible-study-tools/{tool-name}/:
- README.md (tool overview, goals, examples)
- LEARNING.md (experiment log)
- {tool-name}-template.md (agent prompt template)
- tests/README.md (test framework)

Next steps:
1. Review generated files
2. Customize {tool-name}-template.md with specific instructions
3. Run first test on {test_verse}
4. Document learnings and iterate
```

## Best Practices

**Check Initial Context First**: Always check if the user already described their intent when invoking the skill. Don't ask redundant questions if the user already told you what they want.

**Progressive Question Flow**: Ask questions one at a time. Don't overwhelm the user with multiple questions simultaneously.

**Search Before Building**: Always search for existing tools before starting the interactive flow. This prevents duplicate work.

**Validate Examples**: The 5 examples are crucial - they justify the tool's existence. Ensure each example:
- Is specific and concrete
- Shows clear practical value
- Demonstrates how the tool helps translators/pastors/students

**Use AskUserQuestion**: For structured choices (test verse, goal collection method), use the AskUserQuestion tool with clear options.

**Natural Conversation**: For open-ended responses (tool intent, descriptions, goals, examples), use natural conversation rather than forcing everything into multiple choice.

**Concise Feedback**: After gathering each piece of information, provide brief acknowledgment before moving to the next question.

## Example Interaction Flow

**Scenario A: User provides intent upfront**
```
User: "create a new bible study tool to extract all Greek words from each verse"
```
1. Capture intent: "extract all Greek words from each verse"
2. Search existing tools → None found
3. Ask: "Tool name?" → User: "greek-word-extraction"
4. Ask: "One-sentence description?" → User provides
5. Ask: "How to provide goals?" → User: "All at once"
6. User provides 4 goals → Acknowledged
7. Ask: "First example?" → User provides → Validate → Good
8. Continue for examples 2-5
9. Ask about YAML structure → User describes → Create structure
10. Ask: "Test verse?" → User selects JHN 3:16
11. Build YAML file → Run init script → Confirm creation

**Scenario B: User provides no initial context**
```
User: "create a new bible study tool"
```
1. Brainstorm 3-4 valuable tool ideas
2. Ask (with AskUserQuestion): "What would you like this tool to do?"
   - Options: [Greek/Hebrew extraction, Cultural metaphor adaptations, Translation patterns, Theological terms, Other]
   - User selects: "Cultural metaphor adaptations"
3. Search existing tools → None found
4. Ask: "Tool name?" → User: "cultural-metaphor-adaptations"
5. Continue with standard flow...

## Notes

- Follow USFM 3.0 book codes (MAT, JHN, GEN, etc.)
- Follow ISO-639-3 language codes
- YAML format ensures both human and AI readability
- The self-learning loop is essential for quality
- Goals must provide clear practical value, not just data for data's sake
