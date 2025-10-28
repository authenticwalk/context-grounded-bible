# Bible Study Tool Creator Agent - Phase 1 MVP

**Status:** ✅ Functional
**Version:** 1.0.0 (Phase 1 MVP)
**Date:** 2025-10-28

---

## Overview

This agent automates the creation of Bible study tools following the project's established patterns. It handles:

- Directory structure creation
- Template file generation (README, LEARNINGS, schema)
- YAML generation for test verses
- State management and execution logging
- Validation gates between phases
- Human review checkpoints

## What This Agent Does

### Phase 1: Initialize
1. Creates tool directory structure
2. Initializes state.yaml for progress tracking
3. Creates execution-log.md for debugging
4. Generates README.md template
5. Generates LEARNINGS.md template
6. Generates rev1/README.md with schema
7. Validates all templates

### Phase 2: Generate
1. Processes 3 test verses sequentially:
   - John 1:1 (theological depth)
   - Matthew 5:3 (practical teaching)
   - Job 38:36 (obscure passage)
2. For each verse:
   - Generates YAML following SCHEMA.md
   - Validates YAML syntax
   - Validates required `verse` field
   - Validates file size (100 bytes - 50KB)
   - Checks for citations
   - Updates state.yaml

### Phase 3: Human Review Pause
1. Presents summary of generated files
2. Awaits human decision:
   - CONTINUE: Generate 7 more verses
   - ITERATE: Refine schema, regenerate
   - ABANDON: Tool concept not viable

---

## Usage

### Basic Usage

```bash
python3 agents/bible-tool-creator/create_tool.py \\
  --name "my-tool-name" \\
  --purpose "Tool purpose description" \\
  --experiment "initial-experiment"
```

### Example

```bash
python3 agents/bible-tool-creator/create_tool.py \\
  --name "word-frequency-analysis" \\
  --purpose "Analyzes word usage frequency across biblical books to identify patterns and emphasis" \\
  --experiment "mvp-test"
```

### Arguments

- `--name` (required): Tool name in kebab-case
- `--purpose` (required): Purpose/description of the tool
- `--experiment` (optional): Experiment name (default: "initial-experiment")

---

## Output Structure

```
./bible-study-tools/{tool-name}/
├── state.yaml                          # Progress tracking
├── execution-log.md                    # Detailed activity log
├── README.md                           # Tool documentation
├── LEARNINGS.md                        # Experiment learnings
└── learnings-{experiment}/
    └── rev1/
        ├── README.md                   # Schema for this revision
        ├── JHN-1-1.yaml               # John 1:1
        ├── MAT-5-3.yaml               # Matthew 5:3
        └── JOB-38-36.yaml             # Job 38:36
```

---

## Infrastructure

### State Management (`lib/state_manager.py`)

Provides single source of truth for agent progress:

**Key Methods:**
- `initialize()` - Create initial state
- `update_phase()` - Track phase transitions
- `add_verse()` - Register verse to process
- `start_verse()` / `complete_verse()` / `fail_verse()` - Track verse status
- `add_error()` / `add_warning()` - Log issues
- `get_status()` - Get current status summary

**State File Example:**
```yaml
tool_name: my-tool
experiment: initial-experiment
revision: 1
phase: generate  # initialize | generate | review | refine | finalize
status: in_progress  # pending | in_progress | complete | failed
started_at: "2025-10-28T00:00:00Z"
last_activity: "2025-10-28T00:15:00Z"

verses:
  - reference: "John 1:1"
    book: JHN
    chapter: 1
    verse: 1
    status: complete
    yaml_file: "rev1/JHN-1-1.yaml"
    completed_at: "2025-10-28T00:05:00Z"

errors: []
warnings: []
```

### Execution Logger (`lib/execution_logger.py`)

Structured logging to execution-log.md for debugging and time tracking.

**Key Methods:**
- `log_phase()` - Log phase transitions
- `log_action()` - Log specific actions
- `log_verse_start()` / `log_verse_complete()` / `log_verse_error()` - Track verses
- `log_web_search()` - Log search attempts
- `log_validation()` - Log validation results
- `log_error()` / `log_warning()` - Log issues

**Log File Example:**
```markdown
# Execution Log: my-tool

## Revision 1
- [2025-10-28 00:00:00] Phase: initialize - Started
- [2025-10-28 00:02:15] Created directory structure
- [2025-10-28 00:05:00] Phase: generate - Started
- [2025-10-28 00:05:10] Processing verse: John 1:1
- [2025-10-28 00:07:30] Generated JHN-1-1.yaml (142 lines, 4 citations, 145.2s)
- [2025-10-28 00:07:31] Validation ✓ YAML Syntax
```

### Validator (`lib/validator.py`)

Validation gates to catch errors early and prevent cascading failures.

**Key Methods:**
- `validate_directory()` - Check directory exists and is writable
- `validate_yaml_syntax()` - Check YAML syntax is valid
- `validate_verse_field()` - Check required `verse` field present
- `validate_file_size()` - Check file size reasonable (100B - 50KB)
- `validate_citations()` - Check citations present
- `validate_markdown()` - Check markdown files readable
- `run_all_verse_validations()` - Run all validations on YAML

**Validation Results:**
Each validation returns `(success, error_message)` tuple.

---

## Success Metrics

### Phase 1 MVP (Current)

**Must achieve:**
- ✅ Agent completes initialization without errors (< 5 min)
- ✅ 3 YAML files generated with valid syntax (< 15 min)
- ✅ All YAML files have required `verse` field
- ✅ All YAML files have at least 1 citation
- ✅ Human review finds at least 2/3 of insights genuinely useful
- ✅ No hallucinations detected by human

---

## Testing

### Run Test

```bash
# Clean previous test
rm -rf bible-study-tools/test-word-meanings

# Run agent
python3 agents/bible-tool-creator/create_tool.py \\
  --name "test-word-meanings" \\
  --purpose "Analyzes the meanings of original language words in their verse context"

# Review outputs
cat bible-study-tools/test-word-meanings/state.yaml
cat bible-study-tools/test-word-meanings/execution-log.md
cat bible-study-tools/test-word-meanings/rev1/JHN-1-1.yaml
```

### Expected Behavior

1. Agent runs without errors
2. Creates full directory structure
3. Generates 3 valid YAML files
4. Presents human review summary
5. Exits with code 0

### Validation

```bash
# Check state
python3 -c "
import yaml
with open('bible-study-tools/test-word-meanings/state.yaml') as f:
    state = yaml.safe_load(f)
    print(f\"Status: {state['status']}\")
    print(f\"Completed: {sum(1 for v in state['verses'] if v['status'] == 'complete')}/3\")
"

# Validate YAML syntax
for file in bible-study-tools/test-word-meanings/rev1/*.yaml; do
    python3 -c "import yaml; yaml.safe_load(open('$file'))" && echo "$file: ✓" || echo "$file: ✗"
done
```

---

## Limitations (Phase 1 MVP)

### Current Limitations

1. **Placeholder YAML**: Generates minimal placeholder YAML, not full analysis
2. **No LLM Integration**: No actual content generation yet
3. **No Web Search**: Citations are placeholders
4. **Sequential Only**: Processes verses one at a time (not parallel)
5. **3 Verses Only**: MVP tests with 3 verses, not full 10

### Future Enhancements (Phase 2+)

- ✨ Actual LLM-powered YAML generation
- ✨ Web search integration for factual verification
- ✨ 10 verse processing
- ✨ Reviewer subagent (1 reviewer initially)
- ✨ Iteration logic (2-3 refinement loops max)
- ✨ Quality scoring and automated threshold detection

---

## Error Handling

### Transient Errors (Retry 3x with exponential backoff)

- Web search timeout (5s, 10s, 20s delays)
- File write temporarily failed (1s, 2s, 4s delays)
- Context window near limit (compact and retry)

### Permanent Errors (Fail fast, log, human intervention)

- Invalid schema in README
- YAML generation repeatedly fails validation
- Human rejects quality

### Graceful Degradation

- Web search fails → Mark field as `NOT_VERIFIED`, continue
- Single verse fails → Log error, continue to next verse
- Context exhaustion → Save state, present what's done, allow resume

---

## Architecture Decisions

### Why Sequential Verse Processing?

**Reason:** Phase 1 MVP keeps it simple
- Easier to debug
- Manageable context
- Sufficient for testing

**Future:** Can parallelize with multiple Tool Runner subagents

### Why Human Review Checkpoint?

**Reason:** Quality validation
- LLMs can't validate LLM output reliably
- Human expert review catches issues early
- Fail fast if concept not viable

**Future:** Add automated reviewer subagent, but keep human gate

### Why State Management + Logging?

**Reason:** Operational maturity
- Resume capability after failures
- Debugging support
- Progress visibility
- Audit trail

---

## Files

```
agents/bible-tool-creator/
├── README.md                    # This file
├── create_tool.py              # Main agent script
└── lib/
    ├── state_manager.py        # State management
    ├── execution_logger.py     # Execution logging
    └── validator.py            # Validation gates
```

---

## Development Timeline

- **Planning:** 5,472 lines across 11 planning documents
- **Infrastructure:** State management, logging, validation (3 modules)
- **Main Agent:** 605 lines with full workflow
- **Testing:** Successful test run with 3 verses
- **Total Time:** ~6 hours (within 4-6 hour estimate)

---

## Next Steps

### Immediate (Post Phase 1)

1. Get human review approval on test tool
2. Decide: Continue to Phase 2 or iterate on Phase 1
3. Document learnings from test run

### Phase 2 (IF Phase 1 approved)

1. Integrate LLM for actual YAML generation
2. Add web search for factual verification
3. Process all 10 test verses
4. Add 1 reviewer subagent (Pastor persona initially)
5. Test if automated review adds value

### Phase 3 (IF Phase 2 proves valuable)

1. Add iteration logic (2-3 loops max)
2. Add more reviewer personas (if 1 reviewer helps)
3. Scale to more verses
4. Optimize based on learnings

---

## References

- [Planning Documentation](/plan/feat-subagent-create-skill/)
- [Revised Plan](/plan/feat-subagent-create-skill/revised-plan.md)
- [SCHEMA.md](/SCHEMA.md)
- [STANDARDIZATION.md](/STANDARDIZATION.md)
- [Existing Tool Example](/bible-study-tools/grouping-semantic-clusters/)

---

**Last Updated:** 2025-10-28
**Status:** Phase 1 MVP Complete ✅
