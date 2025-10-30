# Learnings: Sermon Illustrations

## Round 1: Initial Broad Experiments (2025-10-29)

### Thesis/Goal

Test three fundamentally different approaches to generating sermon illustrations:
- **Experiment A (Preacher-Transcripts):** Extract from actual sermon transcripts
- **Experiment B (Cultural-Artifacts):** Find illustrations in films, books, history, art
- **Experiment C (Web-Databases):** Mine established sermon illustration databases

### What Worked Well

- **Cultural-Artifacts approach (Experiment B):**
  - 100% data extraction success across all verses
  - Consistently high quality (8.5/10) for popular and obscure verses
  - All sources accessible (IMDB, Wikipedia, historical records)
  - Cross-generational appeal with vivid, memorable content

- **Parallel execution:** 9 agents running simultaneously provided rapid comparative data

- **Diverse test verses:** John 3:16 (well-known), Matthew 5:3 (moderate), Habakkuk 3:9 (obscure) exposed different challenges

### What Worked Poorly

- **Preacher-Transcripts approach (Experiment A):**
  - Complete failure - 100% of web access blocked (403 errors)
  - **Root cause:** Missing WebFetch permissions in sandbox (not website blocking)
  - 0 transcripts extracted despite identifying 15+ sermon sources

- **Web-Databases approach (Experiment C):**
  - Required workarounds - direct database access blocked
  - Had to pivot to Google Search as intermediary
  - Methodology deviation from intended design

- **README bloat:** Experiment READMEs averaged 350 lines, consuming excessive tokens

- **No failure handling:** Schemas didn't account for "found but inaccessible" data

### Key Insights

1. **Web access restrictions must be anticipated upfront** - 67% of experiments encountered systematic 403/SSL errors

2. **Cultural touchstones are highly effective** - Great stories embody universal truths that resonate across generations

3. **Verse obscurity impacts different approaches differently:**
   - Cultural-artifacts: Works consistently regardless of verse popularity
   - Web-databases: Works best for well-known verses
   - Preacher-transcripts: Failed universally due to access issues

4. **Shorter instructions = better results** - Agents spent 15-20% of token budget just reading instructions

### Helpful Resources

**Accessible sources (Experiment B success):**
- IMDB for film information and scenes
- Wikipedia for historical events and cultural context
- Public domain literature databases
- Art history archives

**Blocked sources (experiments failed):**
- SermonCentral, PreachingToday, Preceptaustin (403 errors)
- YouTube sermon transcripts (requires API integration)
- Most church websites with sermon archives

### Source/Method Optimization

| Experiment | Access Method | URL Pattern | Predictability | Scalability | Notes |
|------------|---------------|-------------|----------------|-------------|-------|
| Preacher-Transcripts | WebFetch | Various sermon sites | Low | Poor | 403 errors, no predictable URL schema |
| Cultural-Artifacts | WebSearch + WebFetch | IMDB, Wikipedia | High | Excellent | Predictable patterns, reliable access |
| Web-Databases | WebSearch | Search snippets | Medium | Good | Search-based discovery works well |

**Decision:** Cultural-Artifacts chosen for predictable access methods and scalability

### Review Committee Evolution

**Round 1 (Initial):**
- 8 reviewers with 64 total questions (broad net to catch all issue types)
- All reviewers active to understand problem space

**Rounds 2-3 (To be conducted):**
- Track which reviewers find which issues
- Track which questions catch real problems
- Document effectiveness metrics

**Rounds 7-8 (To be optimized):**
- Target: 3-4 reviewers with 12-15 focused questions
- Keep only reviewers who consistently find issues
- Refine questions based on what actually caught problems

### Recommended Approach

**Winner: Cultural-Artifacts (Experiment B)**
- Ready for refinement phase
- Score: 9.3/10 weighted across all criteria
- Immediately usable outputs for pastors
- **Optimal access method:** WebSearch for discovery + WebFetch for verification (predictable patterns)

**Future consideration:** Retest Preacher-Transcripts with proper WebFetch permissions and API access

### Schema Evolution

#### Round 1 (rev1-rev3)
- Initial schemas in `experiments/{experiment-name}/README-rev1.md`
- Added `source_access`, `verification_status`, `quality_warning` fields
- Evolved from 300+ line READMEs to ~150 line target

### Prompt Engineering Lessons

**What worked:**
- "Document challenges rather than fabricate content" - led to honest failure reporting
- Systematic web verification before writing descriptions
- "Top 3 Insights / Challenges & Fixes / Quality Metrics" structure

**What to avoid:**
- Assuming "publicly available" = "programmatically accessible"
- Long, complex multi-phase instructions
- Required source lists without pre-validation
- Forcing direct fetch when search-based discovery works better

### Stellar Insights

Best examples added to README.md:

1. **John 3:16** - Parent-child sacrifice pattern creates strongest emotional resonance (Mufasa→Simba, Yondu→Peter Quill, Sydney Carton)

2. **Matthew 5:3** - Cultural artifacts refuse to romanticize poverty; kingdom blessing manifests as transformative agency (Valjean, Scrooge)

3. **Habakkuk 3:9** - "Unveiling moment" pattern is universal across cultures (Gladiator's "unleash hell," Aragorn's charge at Black Gate)

### Next Steps for Round 2

- [ ] Refine cultural-artifacts approach with 5-7 additional verses
- [ ] Test cultural diversity expansion (non-Western artifacts)
- [ ] Experiment with contemporary examples (2015-2025)
- [ ] Optimize schema (remove unnecessary fields while maintaining quality)
- [ ] Retest preacher-transcripts if WebFetch permissions confirmed

---

*For detailed experiment analysis, see LEARNINGS-round1.md*
