# Bible Study Tool Creator Skill

## Overview

This skill helps you create new bible study tools for the Context-Grounded Bible project. It provides a complete workflow for:

1. Checking for duplicate tools
2. Gathering tool requirements from users
3. Verifying practical value through concrete examples
4. Generating complete file structures
5. Setting up self-learning loops for quality improvement

## What Gets Created

When you use this skill to create a new tool, it generates:

```
/bible-study-tools/{tool-name}/
├── README.md                      # Tool documentation with goals and examples
├── LEARNING.md                    # Experiment log for tracking improvements
├── {tool-name}-template.md        # Agent prompt template for data generation
└── tests/                         # Self-learning loop test framework
    └── README.md                  # Test documentation
```

## Files in This Skill

### SKILL.md
The main skill definition that Claude uses. Contains step-by-step workflow for creating new tools.

### init-tool.py
Python script that generates all files from a YAML definition. Takes user input and populates templates.

### templates/

- **user-input.template.md**: Interactive form for gathering tool requirements
- **README.template.md**: Template for tool README
- **LEARNING.template.md**: Template for experiment tracking
- **tool-template.template.md**: Template for agent prompts
- **tests-README.template.md**: Template for test framework documentation
- **analysis.template.md**: Template for test output analysis

## How to Use

### Option 1: Via Claude Skill

Invoke the skill directly:

```
Hey Claude, I want to create a new bible study tool using bible-study-tool-creator
```

Claude will:
1. Check for existing similar tools
2. Present you with a template to fill out
3. Review your examples for practical value
4. Generate all files automatically
5. Give you next steps for the self-learning loop

### Option 2: Manual Script Execution

If you already have a tool definition:

```bash
python3 .claude/skills/bible-study-tool-creator/init-tool.py /path/to/tool-definition.yaml
```

## Tool Definition Format

The YAML file should follow this structure:

```yaml
tool_name: "Greek Word Analysis"
tool_name_kebab: "greek-word-analysis"
task_name: "greek-words"
description: "One sentence description"
test_verse: "MAT 5:3"

goals_formatted: |
  1. Goal one
  2. Goal two
  3. Goal three

examples_formatted: |
  ### Example 1
  **Context**: ...
  **Insight**: ...
  **Value**: ...

  ### Example 2
  ...

related_tools: "tool-name-1, tool-name-2"

data_structure: |
  ```yaml
  verse:
    reference: "MAT-5-3"
    your_data:
      field1: "..."
      field2: "..."
  ```

yaml_structure_inline: |
  your_data:
    field1: "..."
    field2: "..."
```

## Requirements Philosophy

### The 5 Examples Rule

Every tool MUST have 5 concrete examples showing:
- **Context**: What verse/concept is being analyzed
- **Insight**: What the tool reveals
- **Value**: How this helps translators/pastors/students

Why 5? Because if you can't find 5 compelling examples, the tool might not be valuable enough to build.

### Practical Value Focus

Goals must be grounded in helping real people (Bible translators, pastors, students) use AI more effectively. Avoid:
- Data that's easy for LLMs to remember (basic facts)
- Data for data's sake
- Theoretical or vague objectives

Focus on:
- Translation challenges
- Cultural context
- Interpretive nuances
- Meaningful connections

## Self-Learning Loop

Each tool is designed for continuous improvement:

1. **Test**: Run agent with template on a verse
2. **Analyze**: Critically evaluate output quality
3. **Learn**: Document findings in LEARNING.md
4. **Refine**: Improve the template
5. **Repeat**: Test again until excellent

This ensures the generated data is:
- Accurate
- Useful
- Complete
- Unique (not just regurgitating LLM training data)

## Examples of Good vs Bad Tools

### ✅ Good Tool: Cultural Translation Adaptations

**Why it's good**:
- Addresses real translation challenge (culturally-specific words)
- 5 strong examples (snow → egret feathers, sheep → caribou, etc.)
- Clear value for translators
- Data not easily remembered by LLMs

### ❌ Bad Tool: List All Books of the Bible

**Why it's bad**:
- LLMs already know this
- No practical translation/interpretation value
- Doesn't need a "book's worth of context"
- Not grounded in the project's mission

## Contributing

If you improve this skill:
1. Update templates in `templates/` directory
2. Update `SKILL.md` with new workflow steps
3. Update `init-tool.py` if changing data structure
4. Document changes in this README

## Related Documentation

- [Project README](../../../README.md) - Overall project goals and task ideas
- [CLAUDE.md](../../../CLAUDE.md) - Project structure and conventions
- [quote-bible skill](../quote-bible/SKILL.md) - Example of well-structured skill

## License

MIT License - same as the parent project
