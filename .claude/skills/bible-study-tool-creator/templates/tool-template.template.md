# {{TOOL_NAME}} - Agent Prompt Template

## Context

You are an AI agent working on the Context-Grounded Bible project. The goal is to create AI-readable commentary that grounds text prediction models in truth when working with Biblical texts.

## Task

For the given Bible verse reference `{book} {chapter}:{verse}`, generate a YAML file containing {{TASK_DESCRIPTION}}.

## Objectives

{{OBJECTIVES}}

## Guidelines

1. **Accuracy First**: All information must be factually correct and verifiable
2. **Practical Value**: Focus on insights that help Bible translators, pastors, and students
3. **Cultural Sensitivity**: Consider diverse cultural and linguistic contexts
4. **Avoid Redundancy**: Don't include information easily remembered by base LLMs (e.g., basic facts like "John wrote John")
5. **Structured Output**: Follow the YAML format exactly
6. **Citations**: Include sources where applicable using format: `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

## Specific Instructions

{{SPECIFIC_INSTRUCTIONS}}

## Output Format

The output must be valid YAML following this structure:

```yaml
verse:
  reference: "{book}-{chapter}-{verse}"
  {{YAML_STRUCTURE}}
```

### Field Definitions

{{FIELD_DEFINITIONS}}

## Quality Standards

Before finalizing output, verify:

- [ ] All information is accurate and verifiable
- [ ] Data provides practical value (not just "nice to know")
- [ ] YAML is properly formatted and valid
- [ ] Examples are concrete and specific
- [ ] Citations follow project format
- [ ] {{CUSTOM_QUALITY_CHECK_1}}
- [ ] {{CUSTOM_QUALITY_CHECK_2}}

## Example Input

**Verse Reference**: MAT 5:3

## Example Output

{{EXAMPLE_OUTPUT}}

## Notes

- Use USFM 3.0 book codes (MAT, JHN, GEN, etc.)
- Use ISO-639-3 language codes
- File naming: `{book}-{chapter}-{verse}-{{TASK_NAME}}.yaml`
- Output directory: `./bible/{book}/{chapter}/{verse}/`

## Resources Available

You may use:
- Bible translation databases
- Greek/Hebrew lexicons
- Cultural anthropology resources
- Historical commentaries
- Cross-reference tools

Do NOT include:
- Speculative interpretations
- Personal theological opinions
- Unverifiable claims
- Information easily available in base LLM training
