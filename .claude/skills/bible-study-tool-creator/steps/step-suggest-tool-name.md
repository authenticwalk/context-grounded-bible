# STEP: Suggest Tool Name

Based on the user's intent and existing tools, suggest 2-3 well-formed tool names following best practices. This single identifier will be used for both the directory name AND in filenames like `MAT-5-3-{tool-name}.yaml`.

You will need to read SCHEMA.md and STANDARDIZATION.md before suggesting a name.

It is better to only suggest 1 name then let them add their own instead of making up names to fill the space.  Only add more names if the task is a little unclear as you can use this to show the possibilities of what they mean in the task and refine their intention.

**CRITICAL: The tool name MUST match the user's narrowed scope from Step 1.** If the user refined their intent in Step 1 (e.g., from "sermon illustrations" to "illustrations from movies, stories, and art"), the tool name must reflect that specific narrowed scope, NOT the broader original concept.

**After tool name is selected, immediately create bible-study-tools/{tool-name}/{tool-name}.yaml** to preserve key information:
```yaml
tool_name: "[Tool Name in Proper Case]"
tool_name_kebab: "[kebab-case]"
foreach_scope: "verse"  # or "chapter", "book", etc. - from Step 1
intent_summary: "[user's refined intent from Step 1]"
status: "in-progress"
```

This prevents loss of critical information during context compaction.

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

**Example 1: Semantic grouping tool**
```
Question: "Which name best fits this tool?"
Options:
- clusters-multi-word-expressions
- clusters-semantic-meaning
- other: (write your own)
```

**Example 2: User narrowed scope in Step 1**
```
Step 1: User said "sermon illustrations" → refined to "from movies, stories, and art"
Step 2 (this step): Tool name options should reflect the NARROWED scope:
✅ CORRECT:
- illustrations-from-movies-stories-and-art
- illustrations-movies-stories-art

❌ WRONG:
- sermon-illustrations (too broad, doesn't match narrowed scope)
- illustrations (too vague)
```