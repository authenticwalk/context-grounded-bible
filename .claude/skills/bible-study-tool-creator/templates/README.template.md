# {{TOOL_NAME}}

## Description

{{DESCRIPTION}}

## Goals

{{GOALS}}

## Examples

{{EXAMPLES}}

## Related Tools

{{RELATED_TOOLS}}

## Usage

This tool is run as an AI agent task. See `{{TOOL_NAME_KEBAB}}-template.md` for the prompt template.

### Running the Tool

```bash
# Example: Process a single verse
claude "Using the {{TOOL_NAME_KEBAB}}-template.md, process MAT 5:3"

# Example: Process an entire chapter
claude "Using the {{TOOL_NAME_KEBAB}}-template.md, process all verses in MAT 5"
```

## Output

Files are generated following this pattern:
```
./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-{{TASK_NAME}}.yaml
```

Example: `./bible/MAT/5/3/MAT-5-3-{{TASK_NAME}}.yaml`

## Data Structure

{{DATA_STRUCTURE}}

## Self-Learning Loop Status

See [LEARNING.md](LEARNING.md) for experiment history and current status.

**Current Status**: {{STATUS}}

## Contributing

If you discover improvements or issues with this tool:
1. Document the finding in `LEARNING.md`
2. Create a test case in `tests/`
3. Refine the template in `{{TOOL_NAME_KEBAB}}-template.md`
4. Re-run tests to verify improvement
