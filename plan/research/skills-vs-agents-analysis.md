# Skills vs Agents Analysis
**Date:** 2025-10-28
**Purpose:** Determine whether Bible Study Tool Creator should be a Skill or Agent

---

## Quick Answer

**RECOMMENDATION: AGENT-based system**

Primary reasons:
1. Complex multi-step workflow with state management
2. Requires parallel subagent execution
3. Needs iterative refinement loops
4. Explicit orchestration required
5. Large context and file generation

---

## What is a Skill?

### Definition
Modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources.

### Structure
```
.claude/skills/{skill-name}/
└── SKILL.md
    ├── YAML frontmatter (name, description)
    └── Markdown instructions
```

### Key Characteristics
- **Model-invoked:** Claude autonomously decides when to use
- **Stateless:** No context preservation between invocations
- **Focused:** Single, well-defined capability
- **Discoverable:** Description helps Claude find when relevant
- **Lightweight:** Small instructions, minimal resources

### When to Use Skills
- ✅ Simple, focused tasks
- ✅ Reusable across many contexts
- ✅ Stateless operations
- ✅ Model can decide when to invoke
- ✅ Small instruction set

### Examples of Good Skills
- Parse verse reference format
- Validate YAML against schema
- Format citations correctly
- Generate file paths from verse refs
- Check USFM book codes

---

## What is an Agent (via Task Tool)?

### Definition
Specialized AI assistant invoked via Task tool to handle specific complex tasks, with customized system prompts, tools, and separate context window.

### Structure
Task tool invocation with explicit instructions passed as prompt parameter.

### Key Characteristics
- **Explicitly invoked:** Developer/main agent decides when to delegate
- **Stateful:** Can maintain context within task execution
- **Complex:** Multi-step workflows
- **Orchestrated:** Explicit delegation and coordination
- **Resource-intensive:** Larger context, more tools

### When to Use Agents
- ✅ Multi-step workflows
- ✅ Needs state management
- ✅ Parallel execution required
- ✅ Iterative refinement
- ✅ Explicit orchestration needed
- ✅ Large context or complex operations

### Examples of Good Agents
- Research codebase for patterns
- Generate and refine complex documents
- Review code with specific persona
- Process batch of items with feedback loop
- Synthesize information from multiple sources

---

## Decision Matrix: Bible Study Tool Creator

### Requirement Analysis

| Requirement | Complexity | Favors |
|------------|------------|--------|
| Create directory structure | Simple | Either |
| Generate README.md | Moderate | Either |
| Generate LEARNINGS.md | Moderate | Either |
| Run experiment on 10 verses | **High** | **Agent** |
| Spawn 5 reviewer subagents | **High** | **Agent** |
| Iterate up to 7 refinement loops | **High** | **Agent** |
| Synthesize feedback | **High** | **Agent** |
| Track experiment state | **High** | **Agent** |
| Generate valid YAML per SCHEMA.md | Moderate | Either |
| Web search for factual data | Moderate | Either |

**Score: 6 High complexity (Agent) vs 4 Moderate/Simple (Either)**

### Workflow Complexity Analysis

**Current Requirements:**
1. Read README.md to understand tool
2. Load SCHEMA.md for structure
3. Build YAML for 10 specific verses:
   - John 1:1
   - Matthew 5:3
   - Colossians 3:1
   - John 11:35
   - Habakkuk 3:9
   - Job 38:36
   - Psalm 119:105
   - Daniel 9:25
   - 1 Samuel 15:3
   - Genesis 36:11
4. Spawn 5 reviewer subagents with different personas
5. Evaluate feedback, filter noise
6. Record learnings
7. Modify schema (rev2)
8. Repeat for problematic verses
9. Continue up to 7 iteration loops
10. Synthesize final learnings
11. Update tool README with stellar insights

**This is NOT a skill-appropriate workflow.**

### State Management Requirements

**Needs to track:**
- Current revision number (rev1, rev2, ... rev7)
- Which verses passed review
- Which verses need refinement
- Aggregated feedback across reviewers
- Iteration count
- Quality threshold status

**Conclusion:** State management complexity requires Agent.

### Parallel Execution Requirements

**Must execute in parallel:**
- 5 reviewer subagents simultaneously
- Each with different persona
- Same verses evaluated from multiple angles

**Skills cannot spawn subagents.**
**Conclusion:** Requires Agent with Task tool.

### Iteration Requirements

**Loop structure:**
```
WHILE (quality < threshold AND iterations < 7):
    1. Generate/regenerate YAML
    2. Spawn 5 reviewers
    3. Collect feedback
    4. Synthesize learnings
    5. Refine schema
    6. Increment iteration
```

**Skills are stateless and cannot maintain iteration loops.**
**Conclusion:** Requires Agent.

### Context Size Requirements

**Must hold in context:**
- SCHEMA.md (1281 lines)
- Tool README template
- 10 verse outputs (variable size)
- 5 reviewer feedbacks
- Previous revision learnings
- Iteration state

**Estimated:** Several thousand lines of context
**Skills have minimal context.**
**Conclusion:** Requires Agent with context management.

---

## Pros and Cons Analysis

### Option 1: Skill-based Approach

**Pros:**
- ✅ Simple to create (single SKILL.md file)
- ✅ Claude can auto-invoke when appropriate
- ✅ Reusable across conversations
- ✅ Low context footprint

**Cons:**
- ❌ Cannot spawn subagents
- ❌ Cannot maintain state across iterations
- ❌ Cannot execute parallel operations
- ❌ Cannot handle complex multi-step workflows
- ❌ Limited context for large schemas
- ❌ No explicit orchestration control
- ❌ Cannot iterate with feedback loops

**Verdict:** Skill approach cannot meet requirements.

### Option 2: Agent-based Approach

**Pros:**
- ✅ Can spawn multiple subagents in parallel
- ✅ Maintains state across iterations
- ✅ Explicit orchestration control
- ✅ Large context window for complex operations
- ✅ Supports feedback loops and refinement
- ✅ Can use TodoWrite for progress tracking
- ✅ Separate context per subagent
- ✅ File-based state persistence

**Cons:**
- ❌ More complex to set up
- ❌ Requires explicit invocation (not auto-discovered)
- ❌ Higher token usage
- ❌ More difficult to reuse across contexts

**Verdict:** Agent approach meets all requirements.

### Option 3: Hybrid Approach

**Structure:**
- Main orchestrator: Agent
- Utility functions: Skills

**Example Skills:**
- Parse verse reference
- Validate YAML schema
- Format citations
- Generate file paths

**Main Agent:**
- Orchestrate workflow
- Spawn subagents
- Manage iterations
- Synthesize learnings

**Pros:**
- ✅ Best of both worlds
- ✅ Reusable utilities
- ✅ Complex orchestration
- ✅ Efficient context usage

**Cons:**
- ❌ More components to maintain
- ❌ Increased setup complexity

**Verdict:** Good long-term approach, but may be over-engineering for initial implementation.

---

## Final Recommendation

### Primary Approach: **AGENT-based System**

**Architecture:**
```
Main Orchestrator Agent
├── Spawns: Tool Runner Subagent
│   └── Processes 10 verses sequentially
├── Spawns: 5 Reviewer Subagents (parallel)
│   ├── Theologian
│   ├── Translator
│   ├── Engineer
│   ├── Student
│   └── Pastor
└── Synthesizes feedback and iterates
```

### Rationale

1. **Requirements-driven:**
   - Parallel subagent execution: ✅
   - Iteration loops: ✅
   - State management: ✅
   - Complex workflows: ✅

2. **Best practices alignment:**
   - Research and planning first
   - Explicit delegation
   - Structured workflows with roles
   - TodoWrite for state tracking

3. **Project methodology fit:**
   - Matches semantic-clusters pattern
   - Iterative refinement is core
   - Multi-perspective review
   - Learning capture

4. **Practical considerations:**
   - Can't achieve requirements with Skills
   - Agent limitations are manageable
   - File-based state persistence works
   - Context management is sufficient

### Future Enhancements

**After initial implementation succeeds, consider:**
1. Extract utility functions as Skills
2. Create reusable reviewer templates
3. Standardize agent patterns in AGENTS.md
4. Build agent scaffolding tools

**But for now:** Keep it simple, use Agents.

---

## Implementation Strategy

### Phase 1: Core Agent System (Current Task)

**Components:**
1. Main orchestrator agent instructions
2. Tool runner subagent template
3. Reviewer subagent template
4. File structure scaffolding

**Deliverables:**
- Working agent that creates tool structure
- Executes experiment on 10 verses
- Spawns reviewers
- Iterates based on feedback
- Documents learnings

### Phase 2: Refinement (Future)

**Based on Phase 1 learnings:**
- Optimize prompts
- Reduce context usage
- Improve reviewer quality
- Streamline iteration logic

### Phase 3: Utility Skills (Future)

**Extract common patterns:**
- Verse reference parser skill
- YAML validator skill
- Citation formatter skill
- File path generator skill

**Benefits:**
- Reduce main agent complexity
- Reusable across tools
- Cleaner separation of concerns

---

## Conclusion

**Decision: Build as AGENT system**

The Bible Study Tool Creator requires:
- Complex multi-step workflows ✅
- Parallel subagent execution ✅
- Iterative refinement loops ✅
- State management ✅
- Large context handling ✅

These requirements cannot be met with Skills alone. An Agent-based architecture is the only viable approach.

Future optimization can extract utilities as Skills, but the core orchestration must be Agent-based.

---

## References

- [Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Subagents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Project files: SCHEMA.md, CLAUDE.md, bible-study-tools/grouping-semantic-clusters/
