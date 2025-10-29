# Token Optimization Plan

**Created:** 2025-10-29
**Status:** In Progress - Phase 1
**Goal:** Reduce Bible Tool token usage by 30-50%

---

## Problem Analysis

**Current Usage:** ~225,000 tokens per experiment cycle (9 agents × 25,000 avg)
**Waste Identified:** 32,000-43,000 tokens (25-30%)

### Key Issues
1. **Large files loaded early** - REVIEW-GUIDELINES (975 lines), SCHEMA (1,340 lines)
2. **Redundant documentation** in experiment READMEs
3. **WebSearch overuse** - searching for known URLs
4. **tokens_used not tracked** - can't measure improvements

---

## Solution Strategy

### Phase 1: Quick Wins
- [ ] Add web resources to ATTRIBUTION.md with calling formats
- [ ] Track tokens_used in metadata
- [ ] Update TEMPLATE.md: inline relevant validation/schema in tool READMEs
- [ ] Simplify bible-researcher.md
- [ ] Update CLAUDE.md with conciseness policy

**Expected:** 15-25% reduction

### Phase 2: Documentation Refactor
- [ ] Refactor existing tool READMEs (500 line max, relevant parts inline)
- [ ] Reduce experiment READMEs (150 line max)

**Expected:** 30-40% total reduction

### Phase 3: Advanced
- [ ] Analyze reviewer value
- [ ] Optimize prompts

**Target:** 35-50% total reduction

---

## Learnings

### 2025-10-29: Initial Implementation
**What worked:**
- Identifying token waste sources
- Understanding that experiments should optimize URLs, not researcher

**What didn't work:**
- Creating separate QUICK files - should be inline in tool READMEs
- web-resources.md - duplicates ATTRIBUTION.md
- CHANGES-SUMMARY.md in root - pollutes directory
- Verbose explanations in bible-researcher.md
- Optimizing researcher instead of experiment phase

**Course correction:**
- Put web resources in ATTRIBUTION.md with URL formats
- Inline relevant schema/validation in each tool README
- Keep bible-researcher.md simple
- Add conciseness policy to CLAUDE.md
- Experiments optimize URLs → researcher uses them

---

## Measurements

### Baseline
- tokens_used field: 0% populated
- Avg tokens/agent: ~25,000
- Total/cycle: ~225,000

### Phase 1 Target
- tokens_used field: 100% populated
- Avg tokens/agent: 17,000-19,000
- Total/cycle: 153,000-171,000
- Reduction: 24-32%

### Phase 2 Target
- Avg tokens/agent: 15,000-17,000
- Total/cycle: 135,000-153,000
- Reduction: 32-40%

### Phase 3 Target
- Avg tokens/agent: 12,000-15,000
- Total/cycle: 108,000-135,000
- Reduction: 40-52%

---

**Next update:** After Phase 1 implementation
