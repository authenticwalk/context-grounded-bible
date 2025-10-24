# New Bible Study Tool Definition

Please fill out this template to define your new bible study tool. The information you provide will be used to generate the complete file structure and templates.

---

## Basic Information

**Tool Name** (use kebab-case, e.g., `greek-word-analysis`, `cultural-translations`):
```
[YOUR TOOL NAME HERE]
```

**Brief Description** (one sentence describing what this tool does):
```
[YOUR DESCRIPTION HERE]
```

**Task Name** (short identifier for YAML files, e.g., `greek-words`, `cult-trans`):
```
[YOUR TASK NAME HERE]
```

---

## Goals

⚠️ **IMPORTANT**: Goals must be practical and grounded in helping Bible translators, pastors, and students use AI accurately.

❌ **Avoid**:
- Easy facts LLMs already know (e.g., "list books of the Bible")
- Data for data's sake without clear value
- Vague or theoretical goals

✅ **Focus on**:
- Translation challenges
- Cultural/linguistic context
- Interpretive nuances
- Meaningful connections

**Primary Goals** (list 3-5 specific, practical goals):

1. ```
   [GOAL 1]
   ```

2. ```
   [GOAL 2]
   ```

3. ```
   [GOAL 3]
   ```

4. ```
   [GOAL 4 - optional]
   ```

5. ```
   [GOAL 5 - optional]
   ```

---

## Examples

🎯 **CRITICAL**: You need at least 5 concrete examples that demonstrate the VALUE of this tool.

Each example should show:
- **Context**: The verse or concept being analyzed
- **Insight**: What the tool reveals
- **Value**: How this helps translators/pastors/students

### Example 1
**Context**:
```
[e.g., "White as snow" in Isaiah 1:18 for cultures without snow]
```

**Insight**:
```
[e.g., Jungle translations use "white as egret feathers" (PNG) or "white as coconut meat" (Philippines)]
```

**Value**:
```
[e.g., Shows translators how to adapt culturally-specific imagery while preserving theological meaning]
```

### Example 2
**Context**:
```
[YOUR EXAMPLE]
```

**Insight**:
```
[YOUR EXAMPLE]
```

**Value**:
```
[YOUR EXAMPLE]
```

### Example 3
**Context**:
```
[YOUR EXAMPLE]
```

**Insight**:
```
[YOUR EXAMPLE]
```

**Value**:
```
[YOUR EXAMPLE]
```

### Example 4
**Context**:
```
[YOUR EXAMPLE]
```

**Insight**:
```
[YOUR EXAMPLE]
```

**Value**:
```
[YOUR EXAMPLE]
```

### Example 5
**Context**:
```
[YOUR EXAMPLE]
```

**Insight**:
```
[YOUR EXAMPLE]
```

**Value**:
```
[YOUR EXAMPLE]
```

---

## Output Structure

**Data Structure** (describe the YAML structure your tool will generate):

```yaml
verse:
  reference: "MAT-5-3"
  # Define your structure here
  # Example:
  # original_words:
  #   - word: "μακάριοι"
  #     transliteration: "makarioi"
  #     meaning: "blessed, happy, fortunate"
  # translations:
  #   - language: "eng"
  #     version: "NIV"
  #     text: "Blessed"
```

**Your structure**:
```yaml
[PASTE YOUR YAML STRUCTURE HERE]
```

---

## Related Tools

**Similar Tools** (have you checked `/bible-study-tools/` for similar existing tools?):
```
[ ] Yes, I checked and found: [list tools]
[ ] Yes, I checked and found none
[ ] No, I haven't checked yet
```

**If similar tools exist, how is this different?**:
```
[EXPLAIN DIFFERENCE OR SAY "N/A"]
```

**Related tools to cross-reference**:
```
[LIST ANY RELATED TOOLS, OR SAY "NONE"]
```

---

## Additional Context

**Initial Test Verse** (which verse would be good for the first test?):
```
[e.g., MAT 5:3, JHN 3:16, ISA 53:5]
```

**Why this verse?**:
```
[Explain why this verse is a good test case]
```

**Known Challenges** (what might be difficult about this task?):
```
[LIST ANTICIPATED CHALLENGES]
```

**Success Criteria** (how will you know if this tool is working well?):
```
[DEFINE SUCCESS METRICS]
```

---

## Review Checklist

Before submitting, verify:

- [ ] Tool name is in kebab-case
- [ ] Description is clear and one sentence
- [ ] 3-5 practical, specific goals listed
- [ ] 5 complete examples with context, insight, and value
- [ ] Examples demonstrate clear practical value
- [ ] YAML structure is defined
- [ ] Checked for similar existing tools
- [ ] Initial test verse selected
- [ ] Success criteria defined

---

**Ready to proceed?** Once you've filled this out completely, I'll create the full file structure with all templates populated!
