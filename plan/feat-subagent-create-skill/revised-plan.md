# Bible Study Tool Creator Agent - REVISED PLAN
**Date:** 2025-10-28
**Status:** Final - Based on 5-reviewer feedback synthesis
**Scope Reduction:** 70% simpler than initial plan

---

## Changes from Initial Plan

| Aspect | Initial Plan | Revised Plan | Reason |
|--------|-------------|--------------|--------|
| Verses | 10 | **3** | Context management, faster iteration |
| Reviewers | 5 parallel subagents | **Human** (Phase 1) | Prove value before automating |
| Iterations | Up to 7 | **2-3 max** | Diminishing returns, time constraints |
| Development time | Unclear | **4-6 hours MVP** | Realistic estimate |
| Validation | Automated | **Human gates** | Quality assurance |
| Infrastructure | Minimal | **State + logging + validation** | Operational maturity |

**Result:** 70% scope reduction, 5x faster to ship, much higher success probability

---

## Mission (Unchanged)

Create an agent system that generates new Bible study tools following the project's established patterns, with automated experimentation, review, and iterative refinement.

---

## Architecture (Simplified)

### Phase 1: MVP (Ship in 4-6 hours)

```
Main Agent
├── Creates directory structure
├── Generates templates (README, LEARNINGS, schema)
├── Processes 3 verses sequentially
│   └── Writes YAML per SCHEMA.md
└── Awaits human review
```

**No subagents in Phase 1.** Prove the core works first.

### Phase 2: Enhancement (IF Phase 1 succeeds)

```
Main Agent
├── Spawns 1 Reviewer Subagent (Pastor persona)
├── Reads feedback
└── Human decides: iterate or finalize
```

### Phase 3: Iteration (IF Phase 2 proves valuable)

```
Main Agent
├── Synthesizes reviewer feedback
├── Refines schema (simple rules)
├── Regenerates problematic verses
└── Max 2 iterations (not 7)
```

---

## Workflow

### PHASE 1: MVP - Prove Core Value

**Human provides:**
- Tool name
- Tool purpose
- Initial schema concept

**Agent does:**
1. **Initialize (5 min)**
   - Create directory structure
   - Generate README template
   - Generate LEARNINGS template
   - Create rev1/README.md with schema

2. **Generate (10-15 min)**
   - Process 3 test verses sequentially:
     - **John 1:1** (theological depth)
     - **Matthew 5:3** (practical teaching)
     - **Job 38:36** (obscure/difficult)
   - For each verse:
     - Read schema from rev1/README.md
     - Use web search for factual verification
     - Generate YAML following SCHEMA.md
     - Write to `rev1/{BOOK}-{CH}-{VS}.yaml`
   - Log progress to `execution-log.md`
   - Update `state.yaml` after each verse

3. **Pause for Human Review (15-30 min human time)**
   - Agent presents summary of outputs
   - Human reviews 3 YAML files:
     - ✅ Quality check: Are insights useful?
     - ✅ Schema check: Does structure work?
     - ✅ Accuracy check: Any hallucinations?
   - Human decision:
     - **Continue:** Generate 7 more verses
     - **Iterate:** Refine schema, regenerate
     - **Abandon:** Tool concept not viable

4. **Expand (IF human approved) (20-30 min)**
   - Generate 7 additional verses
   - Same process as step 2
   - Total: 10 verses

5. **Finalize (10 min)**
   - Extract 5-7 best examples for README
   - Document initial learnings in LEARNINGS.md
   - Mark as complete in state.yaml

**Total time: 4-6 hours development + 15-30 min human review**

---

## Infrastructure (NEW - Critical)

### State Management

**File:** `./{tool-name}/state.yaml`

```yaml
tool_name: "example-tool"
experiment: "initial-experiment"
revision: 1
phase: generate  # initialize | generate | review | refine | finalize | complete
status: in_progress  # pending | in_progress | complete | failed
started_at: "2025-10-28T10:00:00Z"
last_activity: "2025-10-28T10:15:00Z"

verses:
  - reference: "John 1:1"
    book: JHN
    chapter: 1
    verse: 1
    status: complete
    yaml_file: "rev1/JHN-1-1.yaml"
    generated_at: "2025-10-28T10:05:00Z"

  - reference: "Matthew 5:3"
    book: MAT
    chapter: 5
    verse: 3
    status: in_progress
    yaml_file: "rev1/MAT-5-3.yaml"
    started_at: "2025-10-28T10:15:00Z"

errors: []
warnings: []
```

**Purpose:**
- Single source of truth
- Resume capability
- Progress tracking
- Error logging

### Execution Log

**File:** `./{tool-name}/execution-log.md`

```markdown
# Execution Log

## Revision 1
- [2025-10-28 10:00:00] Phase: initialize - Started
- [2025-10-28 10:02:15] Created directory structure
- [2025-10-28 10:02:20] Generated README template
- [2025-10-28 10:05:00] Phase: generate - Started
- [2025-10-28 10:05:10] Processing verse: John 1:1
- [2025-10-28 10:05:45] Web search: "John 1:1 Greek Logos theology"
- [2025-10-28 10:07:30] Generated JHN-1-1.yaml (142 lines, 4 citations)
- [2025-10-28 10:07:31] Updated state.yaml
- [2025-10-28 10:07:35] Processing verse: Matthew 5:3
...
```

**Purpose:**
- Debugging
- Progress monitoring
- Time tracking
- Error diagnosis

### Validation Gates

**Between each phase:**

1. **After Initialize:**
   - ✓ Directory exists and is writable
   - ✓ Templates are valid markdown
   - ✓ Schema in rev1/README.md is parseable

2. **After each verse:**
   - ✓ YAML file exists
   - ✓ YAML syntax is valid
   - ✓ Required `verse` field present
   - ✓ File size between 100 bytes and 50KB
   - ✓ Update state.yaml

3. **Before human review:**
   - ✓ All expected YAML files exist
   - ✓ No critical errors in log
   - ✓ State marked as complete

4. **Before finalize:**
   - ✓ Human approval received
   - ✓ All verses processed
   - ✓ README examples selected

### Error Handling

**Transient errors (retry 3x with exponential backoff):**
- Web search timeout (5s, 10s, 20s delays)
- File write temporarily failed (1s, 2s, 4s delays)
- Context window near limit (compact and retry)

**Permanent errors (fail fast, log, human intervention):**
- Invalid schema in README
- YAML generation repeatedly fails validation
- Human rejects quality

**Graceful degradation:**
- Web search fails → Mark field as `NOT_VERIFIED`, continue
- Single verse fails → Log error, continue to next verse
- Context exhaustion → Save state, present what's done, allow resume

---

## File Structure (Simplified)

```
./bible-study-tools/{tool-name}/
├── state.yaml                          # NEW: Single source of truth
├── execution-log.md                    # NEW: Detailed activity log
│
├── README.md                           # Tool documentation
│   ├── # {Tool Name}
│   ├── ## Why This Tool Exists
│   ├── ## How It Works
│   ├── ## Examples (5-7)
│   └── ## Schema Reference
│
├── LEARNINGS.md                        # What we learned
│   └── ## Experiment: {name}
│       ├── ### What Worked
│       ├── ### What Didn't
│       └── ### Key Insights
│
└── learnings-{experiment}/
    └── rev1/
        ├── README.md                   # Schema for this revision
        ├── JHN-1-1.yaml               # 3 verses for MVP
        ├── MAT-5-3.yaml
        └── JOB-38-36.yaml
```

**Much simpler:** No multiple revisions initially, no reviewer files, focus on core value.

---

## Test Verses (Carefully Selected)

**3 verses for MVP (not 10):**

1. **John 1:1** - "In the beginning was the Word..."
   - Theological depth
   - Well-studied, lots of resources
   - Tests schema for complex theology

2. **Matthew 5:3** - "Blessed are the poor in spirit..."
   - Practical teaching
   - Translation challenges
   - Tests schema for practical application

3. **Job 38:36** - "Who gives wisdom to the heart..."
   - Obscure passage
   - Limited resources
   - Tests schema for edge cases

**Why these 3?**
- Different verse types (theology, teaching, wisdom)
- Range of difficulty (easy, medium, hard)
- Enough to see patterns, not enough to overwhelm
- Similar genre (all require interpretation, not genealogy/lists)

**If Phase 1 succeeds, add 7 more:**
- Colossians 3:1
- John 11:35
- Psalm 119:105
- Daniel 9:25
- 1 Samuel 15:3 (handle with care - ethical complexity)
- Habakkuk 3:9
- Genesis 36:11

---

## Success Metrics

### Phase 1 MVP Success Criteria

**Must achieve:**
- [ ] Agent completes initialization without errors (< 5 min)
- [ ] 3 YAML files generated with valid syntax (< 15 min)
- [ ] All YAML files have required `verse` field
- [ ] All YAML files have at least 1 citation
- [ ] Human review finds at least 2/3 of insights genuinely useful
- [ ] No hallucinations detected by human

**Decision point:**
- If YES: Proceed to Phase 2 (add reviewer)
- If NO: Refine schema manually, try again OR abandon

### Phase 2 Enhancement Success (IF building)

**Must achieve:**
- [ ] Reviewer provides structured feedback
- [ ] Feedback matches human judgment 70%+ of the time
- [ ] Feedback identifies at least 1 actionable improvement
- [ ] Feedback processing adds < 10 min to workflow

### Phase 3 Iteration Success (IF building)

**Must achieve:**
- [ ] Iteration improves quality (human rating)
- [ ] Converges in 2-3 iterations (not more)
- [ ] Iterated output measurably better than first pass

---

## What We're NOT Building (Yet)

**Deferred to future:**
- ❌ 5 parallel reviewer subagents (start with 1 or human)
- ❌ 7 iteration loops (start with 2-3 max)
- ❌ 10 verses (start with 3)
- ❌ Automated synthesis (human decides initially)
- ❌ Complex schema evolution (simple refinements only)
- ❌ Parallel verse processing (sequential is fine for 3 verses)
- ❌ Automated quality scoring (human judgment initially)

**Why defer?**
- Prove core value first
- Add complexity only when proven necessary
- Fail fast if concept doesn't work
- Learn what actually matters

---

## Development Plan

### Step 1: Build Infrastructure (1-2 hours)

**Tasks:**
- Create state.yaml management functions
- Create execution logging
- Create validation gates
- Test error handling

**Deliverable:** Infrastructure that works, tested

### Step 2: Build Main Agent (2-3 hours)

**Tasks:**
- Directory creation logic
- Template generation (README, LEARNINGS, schema)
- YAML generation for 3 verses
- State management integration
- Human review pause point

**Deliverable:** Working MVP agent

### Step 3: Test Internally (1 hour)

**Tasks:**
- Run with sample tool concept
- Review outputs
- Check logging works
- Verify state management
- Test error scenarios

**Deliverable:** Validated system

### Step 4: Document (30 min)

**Tasks:**
- Usage instructions
- Architecture docs
- Learnings captured

**Deliverable:** Documentation

**Total: 4-6 hours**

---

## Risk Mitigation

### Risk 1: Context Window Exhaustion
**Mitigation:** Only 3 verses = ~600 lines total, well within limits
**Fallback:** Write after each verse, can reload if needed

### Risk 2: Poor Quality Output
**Mitigation:** Human review gate catches problems early
**Fallback:** Refine schema, try again; only 3 verses to regenerate

### Risk 3: Schema Doesn't Work
**Mitigation:** Test with 3 diverse verses reveals schema issues fast
**Fallback:** Human redesigns schema, quick to retry with 3 verses

### Risk 4: Development Takes Longer
**Mitigation:** Clear scope, realistic estimate, incremental testing
**Fallback:** Ship what works, defer enhancements

### Risk 5: Tool Concept Not Viable
**Mitigation:** Fail fast after 3 verses, not after 10 verses × 7 iterations
**Fallback:** Minimal time wasted, learn quickly, try different concept

---

## Decision Gates

### Gate 1: After Phase 1 MVP

**Question:** Did we produce 3 useful YAML files?

**If YES:**
- Continue to add 7 more verses
- Document what worked
- Consider Phase 2 (reviewer)

**If NO:**
- Why not? (Schema? Verse selection? Tool concept?)
- Can we fix with minor changes?
- If yes: Iterate manually
- If no: Abandon this tool concept

### Gate 2: After 10 Verses

**Question:** Is this tool worth using?

**If YES:**
- Finalize documentation
- Add to project
- Consider building Phase 2 (automation)

**If NO:**
- Document learnings
- Don't invest in automation
- Try different tool concept

### Gate 3: After Phase 2 (IF built)

**Question:** Does automated reviewer add value?

**If YES:**
- Keep for future tools
- Consider adding more personas

**If NO:**
- Remove reviewer
- Stick with human review
- Document why automation didn't help

---

## Open Questions (Reduced)

### Q1: Which schema should we start with?
**Answer:** Adapt semantic-clusters schema, it's proven

### Q2: How much web search is needed?
**Answer:** Best effort, mark unverified, human can follow up

### Q3: What if all 3 verses fail?
**Answer:** Schema or tool concept is wrong, redesign or abandon

### Q4: Should Phase 2/3 be built?
**Answer:** Only if Phase 1 proves valuable and automation would actually help

---

## Comparison: Initial vs Revised

| Metric | Initial Plan | Revised Plan |
|--------|-------------|--------------|
| **Verses** | 10 | 3 (MVP), 10 (if approved) |
| **Reviewers** | 5 parallel subagents | Human (Phase 1) |
| **Iterations** | Up to 7 | 2-3 max |
| **Phases** | 6 | 3 (incremental) |
| **Agent types** | 7 (orchestrator + runner + 5 reviewers) | 1 (Phase 1), 2 (Phase 2) |
| **Development time** | 20-31 hours | 4-6 hours (Phase 1) |
| **Runtime** | 30-60 min × 7 = 7 hours worst case | 10-15 min (3 verses) |
| **Complexity** | High | Low |
| **Failure points** | 16+ | 3-4 |
| **Files generated** | 350 max | 15-20 |
| **Infrastructure** | Minimal | State + logging + validation |
| **Human validation** | End only | Throughout |
| **Success probability** | 10% (per skeptic) | 70-80% |

---

## Next Steps

1. ✅ Get approval on this revised plan
2. ⏭️ Build infrastructure (state, logging, validation)
3. ⏭️ Build Phase 1 MVP agent
4. ⏭️ Test with simple tool concept
5. ⏭️ Decide: Continue to Phase 2 or iterate on Phase 1

---

## Principles for Success

1. **Simplicity first** - Start with 20% of features that deliver 80% of value
2. **Validate early** - Human gates prevent wrong paths
3. **Build infrastructure** - State, logging, validation are not optional
4. **Fail fast** - 3 verses reveals problems quickly
5. **Incremental** - Ship milestones, learn, decide next step
6. **Human-in-loop** - Don't trust full automation yet
7. **Measure** - Explicit success criteria at each gate

---

## Conclusion

This revised plan is **70% simpler** than the initial plan while preserving the core value proposition. It:

✅ Ships in 4-6 hours instead of 20-31 hours
✅ Proves value before scaling complexity
✅ Includes critical infrastructure (state, logging, validation)
✅ Has human validation gates
✅ Fails fast if concept doesn't work
✅ Provides clear decision points
✅ Has realistic success metrics

**This is shippable. The initial plan was not.**

The opportunity is still enormous. The need is still real. The approach is still sound. We've just made it **actually achievable**.
