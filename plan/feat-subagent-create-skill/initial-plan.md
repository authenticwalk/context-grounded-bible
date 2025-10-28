# Bible Study Tool Creator Agent - Initial Plan
**Date:** 2025-10-28
**Status:** Draft for Review

---

## Mission

Create an agent system that generates new Bible study tools following the project's established patterns, with automated experimentation, multi-perspective review, and iterative refinement.

---

## Architecture Overview

### Components

```
1. Main Orchestrator Agent (entry point)
   - Creates tool directory structure
   - Generates initial README.md and LEARNINGS.md
   - Spawns experiment runner
   - Coordinates review process
   - Synthesizes learnings

2. Tool Runner Subagent
   - Processes 10 specific verses
   - Generates YAML output per SCHEMA.md
   - Records all outputs in revision directory
   - One at a time to manage context

3. Reviewer Subagent (5 parallel instances)
   - Evaluates outputs from specific persona
   - Identifies valuable insights
   - Flags noise and inaccuracies
   - Produces structured feedback

4. Synthesis Process (Main Agent)
   - Aggregates reviewer feedback
   - Filters signal from noise
   - Refines schema for next revision
   - Determines if iteration needed
```

---

## Workflow

### Phase 1: Initialization

**Main Agent Actions:**
1. Create directory structure:
   ```
   ./bible-study-tools/{tool-name}/
   ├── README.md
   ├── LEARNINGS.md
   └── learnings-{experiment-name}-log/
       └── rev1/
           └── README.md
   ```

2. Generate README.md with:
   - Human-readable title
   - Overview (Why this tool must exist + How it works)
   - 7 placeholder examples (to be filled from experiments)
   - Schema reference

3. Generate LEARNINGS.md with:
   - Experiment name header
   - Thesis/goal placeholder
   - Analysis placeholders

4. Create rev1/README.md with initial schema

### Phase 2: Experiment Execution

**Tool Runner Subagent:**
1. Read tool README.md to understand purpose
2. Read schema from rev1/README.md
3. For each verse (sequentially):
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

4. Generate YAML following schema
   - Use web search for factual verification
   - Include all required citations
   - Follow SCHEMA.md standards

5. Write to: `learnings-{exp}-log/rev{N}/{BOOK}-{CH}-{VS}.yaml`

### Phase 3: Review

**5 Parallel Reviewer Subagents:**

**Personas:**
1. Doctor of Theology
2. Veteran Translator (20+ years field experience)
3. Principal Database Engineer (data structure focus)
4. 1st year Bible college student
5. Pastor working on a sermon

**Each Reviewer:**
1. Read tool README.md for context
2. Read all YAML files in current revision
3. Evaluate each file:
   - Which insights are genuinely helpful?
   - Which sections could be removed as noise?
   - What looks inaccurate or fabricated?
   - What would make a meaningful difference?

4. Write feedback to:
   `{persona-slug}-round{N}.md`

5. Aggregate findings into short summary
6. Return summary to main agent

### Phase 4: Synthesis

**Main Agent:**
1. Read all 5 reviewer files
2. Identify common themes:
   - Consistent praise → keep/amplify
   - Consistent criticism → fix/remove
   - Divergent views → investigate further

3. Determine most important improvements:
   - Filter noise from valid critique
   - Prioritize high-impact changes
   - Focus on simplicity

4. Record analysis in LEARNINGS.md

5. Decide: iterate or finalize?
   - If major issues AND iterations < 7: Continue
   - If minor issues OR iterations >= 7: Finalize

### Phase 5: Iteration (if needed)

**Main Agent:**
1. Create rev{N+1}/ directory
2. Copy and modify schema in rev{N+1}/README.md
3. Identify problematic verses + potentially similar verses
4. Re-run Tool Runner Subagent for those verses
5. Re-run Reviewers
6. Repeat synthesis
7. Continue until quality threshold or max 7 iterations

### Phase 6: Finalization

**Main Agent:**
1. Read all LEARNINGS.md from each revision
2. Synthesize into tool's LEARNINGS.md:
   - What worked really well
   - What worked poorly
   - Helpful websites
   - Helpful techniques
   - Schema fields that were valuable
   - Prompt engineering lessons

3. Identify stellar insights from verse outputs
4. Add best examples to tool README.md (up to 7)

---

## File Structure

```
./bible-study-tools/{tool-name}/
├── README.md
│   ├── # {Tool Name}
│   ├── ## Why This Tool Exists
│   ├── ## How It Works
│   ├── ## Examples of Insights
│   │   ├── ### Insight 1: {Title}
│   │   │   └── {5-line description with what/why}
│   │   ├── ... (7 total)
│   └── ## Schema
│       └── See SCHEMA.md section {X}
│
├── LEARNINGS.md
│   ├── # Learnings
│   ├── ## Experiment: {name}
│   ├── ### Thesis/Goal
│   ├── ### What Worked Well
│   ├── ### What Worked Poorly
│   ├── ### Key Techniques
│   ├── ### Helpful Resources
│   └── ### Schema Evolution
│
└── learnings-{experiment-name}-log/
    ├── rev1/
    │   ├── README.md (schema v1)
    │   ├── JHN-1-1.yaml
    │   ├── MAT-5-3.yaml
    │   ├── ... (10 verses)
    │   ├── theologian-round1.md
    │   ├── translator-round1.md
    │   ├── engineer-round1.md
    │   ├── student-round1.md
    │   └── pastor-round1.md
    ├── rev2/
    │   ├── README.md (refined schema)
    │   ├── {problematic verses}.yaml
    │   ├── theologian-round2.md
    │   └── ... (5 reviewers)
    └── ... (up to rev7)
```

---

## Key Design Decisions

### 1. Sequential Verse Processing

**Decision:** Tool Runner processes verses one at a time
**Rationale:**
- Nested subagents not supported (can't spawn 10 parallel verse processors)
- Sequential processing manageable within single context
- Can reload context if compression occurs

**Alternative Considered:** Spawn 10 parallel Tool Runner instances
**Rejected:** Would require main agent to manage 10 subagents, increasing complexity

### 2. Parallel Reviewers

**Decision:** Spawn all 5 reviewers simultaneously
**Rationale:**
- Different personas provide diverse perspectives
- Parallel execution faster than sequential
- No dependencies between reviewers
- Maximum 10 parallel tasks supported, 5 is safe

**Alternative Considered:** Sequential reviews
**Rejected:** Slower, no benefit from sequential processing

### 3. File-Based Communication

**Decision:** All data exchange via files
**Rationale:**
- Subagents have separate contexts
- Files persist beyond context window
- Enables context reloading
- Matches project's YAML-centric approach

**Alternative Considered:** Return data in subagent response
**Rejected:** Limited by response size, no persistence

### 4. Max 7 Iterations

**Decision:** Hard limit of 7 refinement loops
**Rationale:**
- Prevents infinite iteration
- Diminishing returns after multiple refinements
- Practical limit for human oversight
- Biblical significance (7 = completeness)

**Alternative Considered:** Iterate until perfect
**Rejected:** No clear "perfect" threshold, resource intensive

### 5. Explicit Success Criteria

**Decision:** Main agent determines quality threshold
**Rationale:**
- Flexible based on tool complexity
- Human judgment still valuable
- Can tighten over time with experience

**Alternative Considered:** Automated quality metrics
**Rejected:** Hard to quantify "insight value" algorithmically

---

## Risk Analysis

### Risk 1: Context Window Exhaustion

**Problem:** 10 verses + 5 reviews could exceed context
**Likelihood:** Medium
**Impact:** High
**Mitigation:**
- Use compact feature for auto-summarization
- Write intermediate results to files
- Reload context as needed from files
- Process verses sequentially to manage size

### Risk 2: Reviewer Feedback Quality Variance

**Problem:** Different personas may give inconsistent or low-quality feedback
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Explicit evaluation criteria in reviewer instructions
- Structured feedback format
- Main agent synthesis filters noise
- Iterate on reviewer prompts if needed

### Risk 3: Hallucination in Generated YAML

**Problem:** LLMs may fabricate data despite instructions
**Likelihood:** Medium
**Impact:** High
**Mitigation:**
- Require web search citations
- SCHEMA.md citation requirements
- Reviewer validation step
- Flag uncertain data for human review
- Match existing tool's "NO HALLUCINATION" principle

### Risk 4: Infinite Iteration Loop

**Problem:** System might never reach quality threshold
**Likelihood:** Low
**Impact:** Medium
**Mitigation:**
- Hard limit of 7 iterations
- Clear exit criteria
- Human can intervene at any point
- Log all iterations for analysis

### Risk 5: Subagent Spawning Failures

**Problem:** Subagents might fail to execute properly
**Likelihood:** Low
**Impact:** High
**Mitigation:**
- Error handling in main agent
- Retry logic for transient failures
- Fallback to sequential if parallel fails
- Comprehensive logging

---

## Success Metrics

### Must-Have (MVP)

1. ✅ Creates valid directory structure
2. ✅ Generates README.md with all required sections
3. ✅ Generates LEARNINGS.md template
4. ✅ Processes all 10 verses with valid YAML
5. ✅ Spawns 5 reviewers successfully
6. ✅ Produces reviewer feedback files
7. ✅ Synthesizes learnings into LEARNINGS.md
8. ✅ Adds examples to README.md

### Nice-to-Have (Enhancements)

1. ⭐ Iterates to improve quality
2. ⭐ Identifies truly stellar insights
3. ⭐ Helpful schema refinements
4. ⭐ Clear, actionable learnings
5. ⭐ Reusable for future tools

### Stretch Goals

1. 🚀 Automated quality scoring
2. 🚀 Web search integration for all facts
3. 🚀 Cross-reference to existing tools
4. 🚀 Template extraction for reuse

---

## Implementation Plan

### Step 1: Create Directory Structure (Main Agent)

**Input:** Tool name, experiment name
**Output:** Empty directory tree
**Time:** < 1 minute

### Step 2: Generate Templates (Main Agent)

**Tasks:**
- README.md with placeholders
- LEARNINGS.md with structure
- rev1/README.md with initial schema

**Time:** 2-3 minutes

### Step 3: Build Tool Runner Instructions

**Create:** Clear, comprehensive prompt for subagent
**Include:**
- Tool purpose from README
- Schema from rev1/README
- Verse list
- Output file naming
- Quality standards

**Time:** 5 minutes setup (reusable)

### Step 4: Build Reviewer Instructions

**Create:** Parameterized prompt with persona variable
**Include:**
- Persona description
- Evaluation criteria
- Output format
- Examples of good feedback

**Time:** 5 minutes setup (reusable)

### Step 5: Execute Experiment

**Sequence:**
1. Spawn Tool Runner → Wait for completion
2. Spawn 5 Reviewers in parallel → Wait for all
3. Synthesize feedback
4. Decide on iteration
5. If iterate: Refine schema, go to step 1

**Time:** 30-60 minutes per iteration

### Step 6: Finalize

**Tasks:**
- Synthesize all learnings
- Extract best examples
- Update README.md
- Commit changes

**Time:** 10-15 minutes

---

## Open Questions

### Q1: How specific should initial schema be?

**Option A:** Very detailed schema based on SCHEMA.md
**Option B:** Minimal schema, let experimentation reveal needs
**Recommendation:** Option A - leverage existing standards, iterate from solid base

### Q2: Should reviewers see each other's feedback?

**Option A:** Sequential reviews (later reviewers see earlier feedback)
**Option B:** Parallel reviews (independent perspectives)
**Recommendation:** Option B - avoid groupthink, get diverse views

### Q3: What defines "quality threshold"?

**Option A:** All reviewers satisfied
**Option B:** Majority satisfied
**Option C:** No critical issues flagged
**Recommendation:** Option C - practical, measurable, achievable

### Q4: Should we test with one verse first?

**Option A:** Full experiment (10 verses)
**Option B:** Test with 1-2 verses, then scale
**Recommendation:** Option B for first tool creation, then Option A for subsequent tools

### Q5: How to handle web search requirements?

**Option A:** Tool Runner does all web searches
**Option B:** Flag items needing research, human follows up
**Option C:** Best effort, cite LLM when web search not feasible
**Recommendation:** Option C - practical, maintains velocity

---

## Next Steps

1. Get feedback on this plan from multiple perspectives
2. Refine based on feedback (focus on simplicity)
3. Implement main agent orchestrator
4. Implement tool runner subagent template
5. Implement reviewer subagent template
6. Test with simple experiment
7. Iterate based on learnings
8. Document patterns in AGENTS.md

---

## Request for Review

**Reviewers, please evaluate:**

1. **Feasibility:** Can this actually work with current Claude Code capabilities?
2. **Simplicity:** Are we over-engineering? Where can we simplify?
3. **Risks:** What risks are we missing?
4. **Value:** Will this actually produce useful Bible study tools?
5. **Alternatives:** What different approaches should we consider?

**Specific personas:**
- Software Architect: System design, scalability, maintainability
- DevOps Engineer: Reliability, error handling, monitoring
- UX Researcher: User value, clarity, practical utility
- Project Manager: Scope, timeline, success criteria
- Skeptical Engineer: What will go wrong? What are we assuming incorrectly?
