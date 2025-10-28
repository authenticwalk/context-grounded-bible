# Claude Code Agents Research
**Date:** 2025-10-28
**Purpose:** Best practices and patterns for building Claude Code agents and skills

---

## Executive Summary

Based on research from official Anthropic documentation and community best practices, this document provides guidance for implementing the Bible study tool creator agent system.

**Key Decision:** This should be an **AGENT-based system** rather than a Skill, due to:
1. Complex multi-step workflows with state management
2. Need for parallel subagent execution (reviewers, researchers)
3. Iterative refinement loops requiring context preservation
4. File system operations and data generation

---

## Best Practices for Claude Code Agents

### 1. Research and Planning First

**Pattern:** Always ask Claude to research and plan before coding
- Without this step, Claude jumps straight to coding
- Research phase significantly improves performance for complex problems
- Use explicit planning phases with TodoWrite tool

**Implementation for Bible Tool Creator:**
```
1. Research existing patterns in project
2. Create explicit plan with TodoWrite
3. Get approval/feedback before execution
4. Execute with clear milestones
```

### 2. Test-Driven Development (TDD)

**Pattern:** Write tests based on expected input/output pairs
- Be explicit about TDD approach
- Avoid mock implementations
- Focus on real data validation

**Implementation:**
- Test verse parsing (JHN.011.035 format)
- Test YAML schema validation
- Test file path generation
- Validate against SCHEMA.md standards

### 3. Extended Thinking Mode

**Trigger Words:**
- "think" - basic extended thinking
- "think hard" - moderate computation
- "think harder" - significant computation
- "ultrathink" - maximum computation budget

**When to Use:**
- Complex architectural decisions
- Schema design choices
- Feedback synthesis from multiple reviewers
- Optimization of prompt engineering

---

## Subagent Patterns

### Task Tool - The Core Delegation Mechanism

**What is a Subagent?**
- Lightweight instance of Claude Code with separate context window
- Task-specific configuration and system prompts
- Access to same tools as main agent (by default)

**Key Capabilities:**
- Basic file reads and writes
- Code searches and file analysis
- Bash operations
- Research tasks
- Parallel execution (up to 10 concurrent)

### Pattern 1: Parallel Multi-Angle Research

```
Use Case: Get diverse perspectives on same problem
Implementation:
1. Launch 4-10 parallel subagents with different personas
2. Each analyzes same artifact with different lens
3. Main agent synthesizes feedback
4. Make informed decision based on consensus/divergence
```

**For Bible Tool Creator:**
- Spawn 5 reviewer subagents simultaneously
- Each with different persona (theologian, translator, engineer, student, pastor)
- Parallel execution = faster feedback cycles

### Pattern 2: Structured Workflows with Roles

```
Roles:
- Product Spec: Define requirements
- Architect: Validate design
- Implementer/Tester: Build and test
- QA: Verify results
```

**For Bible Tool Creator:**
- Main Agent: Orchestrator
- Tool Runner Subagent: Execute experiment on 10 verses
- Reviewer Subagents: Evaluate output quality
- Synthesis Agent: Extract learnings

### Pattern 3: Iterative Refinement Loops

```
Pattern:
1. Generate initial output
2. Review with multiple perspectives
3. Identify issues
4. Refine and regenerate
5. Repeat until quality threshold or max iterations
```

**For Bible Tool Creator:**
- Generate YAML for sample verses
- Get reviewer feedback
- Refine schema/prompt
- Regenerate problematic verses
- Max 7 loops per experiment

### Important Limitations

**No Nested Subagents:**
- Subagents CANNOT spawn their own subagents
- Must flatten workflow hierarchy
- Main agent orchestrates all delegation

**No Interactive Planning:**
- Subagents execute immediately
- No "thinking" mode or transparent intermediate output
- Provide complete, explicit instructions upfront

**Context Isolation:**
- Each subagent has separate context window
- Cannot share memory directly
- Use file system for communication

---

## Agent Skills - When to Use

### What are Skills?

**Structure:**
- Organized folders with SKILL.md file
- YAML frontmatter + Markdown content
- Optional supporting scripts/templates
- Model-invoked (Claude decides when to use)

**Key Fields:**
- `name`: lowercase, hyphens, max 64 chars
- `description`: what it does + when to use (max 1024 chars)

### Skills vs Agents Decision Matrix

| Factor | Use Skill | Use Agent/Subagent |
|--------|-----------|-------------------|
| Complexity | Simple, focused task | Multi-step workflow |
| Invocation | Model decides | Explicit delegation |
| State Management | Stateless | Needs state/iteration |
| Context Size | Small instructions | Large context needed |
| Parallel Execution | Single invocation | Multiple concurrent |
| File Generation | Simple templates | Complex data structures |

**Decision for Bible Tool Creator: AGENT**
- ✅ Multi-step workflow with iterations
- ✅ Needs parallel reviewer execution
- ✅ State management across experiment rounds
- ✅ Complex YAML generation with validation
- ✅ Explicit orchestration required

### When Skills Would Be Appropriate

For simpler, focused tasks in this project:
- Parse verse reference (e.g., "John 3:16" → "JHN.003.016")
- Validate YAML against schema
- Format citations correctly
- Generate file paths from verse references

---

## Context Management

### Compact Feature

**Automatic Summarization:**
- Triggers when context limit approaches
- Summarizes previous messages
- Agent won't run out of context

**Best Practice:**
- Design subagents with clear, focused tasks
- Minimize context handoff between agents
- Use file system for large data transfers

### Tool Design for Context Efficiency

**Principle:** Tools are prominent in context window
- Primary actions Claude considers
- Be conscious of tool design
- Maximize context efficiency

**For Bible Tool Creator:**
- Keep agent instructions focused and concise
- Use file references instead of embedding large data
- Load SCHEMA.md by reference, not inline
- Use YAML for structured data exchange

---

## Security & Production Best Practices

### Permission Management

**Principle:** Treat tool access like production IAM
- Start from deny-all
- Allowlist only needed commands/directories
- Avoid permission sprawl

**For Bible Tool Creator:**
- Limit subagents to specific directories
- Read-only access where possible
- Write access only to designated output folders

### Model Selection Strategy (2025)

**Claude Haiku 4.5:**
- 90% of Sonnet 4.5 agentic performance
- 2x faster
- 3x cost savings ($1/$5 vs $3/$15)

**Recommendation:**
- Use Sonnet 4.5 for main orchestration
- Consider Haiku 4.5 for repetitive reviewer tasks
- Balance cost vs quality for high-volume operations

---

## Implementation Recommendations

### For Bible Study Tool Creator Agent

**Architecture:**
```
Main Agent (Orchestrator)
├── Tool Runner Subagent (Processes 10 verses)
│   └── Writes YAML files
├── 5 Reviewer Subagents (Parallel evaluation)
│   ├── Theologian persona
│   ├── Translator persona
│   ├── Engineer persona
│   ├── Student persona
│   └── Pastor persona
└── Synthesis Process (Main agent)
    └── Extracts learnings, refines schema
```

**Workflow Pattern:**
1. **Research Phase** (Main Agent)
   - Read existing tools
   - Understand SCHEMA.md
   - Plan tool structure

2. **Generation Phase** (Tool Runner Subagent)
   - Process 10 verses sequentially
   - Generate YAML per SCHEMA.md
   - Record all outputs

3. **Review Phase** (5 Parallel Reviewer Subagents)
   - Each with different persona
   - Evaluate usefulness, accuracy, noise
   - Write individual review files

4. **Synthesis Phase** (Main Agent)
   - Read all reviews
   - Identify patterns
   - Refine schema/prompts

5. **Iteration Phase** (Conditional, max 7 loops)
   - Regenerate problematic verses
   - Re-review
   - Repeat until quality threshold

**Key Design Decisions:**

1. **Use TodoWrite extensively**
   - Track experiment progress
   - Visibility for user
   - State management across iterations

2. **File-based communication**
   - YAML for structured data
   - Markdown for learnings
   - Clear directory structure

3. **Explicit delegation**
   - Don't rely on Claude deciding
   - Precise subagent instructions
   - Clear success criteria

4. **Parallel where possible**
   - All 5 reviewers simultaneously
   - Faster feedback cycles
   - Diverse perspectives

5. **Iteration controls**
   - Max 7 refinement loops
   - Clear exit criteria
   - Prevent infinite loops

---

## Risks and Mitigations

### Risk: Nested Subagent Limitation

**Problem:** Tool Runner can't spawn verse-processing subagents
**Mitigation:** Tool Runner processes verses sequentially in single context

### Risk: Context Window Exhaustion

**Problem:** 10 verses + reviews could exceed context
**Mitigation:**
- Use compact feature
- Write intermediate results to files
- Reload context as needed

### Risk: Hallucination in Generated YAML

**Problem:** LLMs may fabricate data
**Mitigation:**
- Web search for factual content
- Citation requirements in SCHEMA.md
- Reviewer validation step
- Human review flags

### Risk: Review Quality Variance

**Problem:** Different personas may give inconsistent feedback
**Mitigation:**
- Explicit evaluation criteria
- Structured review format
- Main agent synthesis to find signal vs noise

---

## Next Steps

1. Create agent directory structure
2. Write main orchestrator agent instructions
3. Write tool runner subagent instructions
4. Write reviewer subagent template
5. Test with simple experiment
6. Iterate based on learnings

---

## References

- [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Agent SDK - Anthropic](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Agent Skills - Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Subagents Documentation - Claude Docs](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Skills Documentation - Claude Docs](https://docs.claude.com/en/docs/claude-code/skills)
