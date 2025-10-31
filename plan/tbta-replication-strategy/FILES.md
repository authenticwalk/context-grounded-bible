# TBTA Replication Strategy - File Inventory

## Confirmed Files in `/plan/tbta-replication-strategy/`

### ✅ Core Strategy & Research

- **MASTER-STRATEGY.md** - Complete replication strategy (Opus-based approach)
- **complete-field-taxonomy.md** - All 41 TBTA fields cataloged (926 lines)
- **reproduction-guide-95-percent.md** - Step-by-step guide to 95% accuracy (726 lines)
- **comprehensive-language-research.md** - Language examples for every feature (821 lines)
- **blind-discovery-test.md** - Independent discovery validation (794 lines)
- **blind-test-comparison.md** - 8.2/10 baseline analysis (543 lines)

### 📁 To Be Created

#### Field Documentation (41 files needed)
Create: `/plan/tbta-replication-strategy/fields/{field-name}.md`

Each must have:
- Field definition
- 7+ confirmed languages
- 7+ real translation examples
- Coverage assessment

**Priority fields to document first:**
1. `trial-number.md`
2. `clusivity.md`
3. `dual-number.md`
4. `participant-tracking.md`
5. `time-granularity.md`
6. `speaker-demographics.md`
7. `proximity-systems.md`
8. `illocutionary-force.md`

#### Tracking Files
- `debug-log.md` - Iteration tracking per verse
- `improvements.md` - TBTA gaps and additions to consider

#### Test Results Directory
- `test-results/` - Store generated annotations and comparisons

---

## Key Data Sources (External)

### TBTA Data
- Location: `./bible/commentaries/{BOOK}/{chapter}/{verse}/*-tbta.yaml`
- Example: `./bible/commentaries/GEN/001/026/GEN-001-026-tbta.yaml`
- Coverage: 11,649 verses across 34 books

### eBible Corpus
- Location: `./bible/commentary/{BOOK}/{chapter}/*.translations-ebible.yaml`
- Example: `./bible/commentary/GEN/1/GEN_1_001.translations-ebible.yaml`
- Coverage: 1000+ translations in 1000+ languages

---

## Status Summary

**✅ Phase 1 Research:** Complete (6 files)
**⏳ Field Documentation:** Not started (0/41 files)
**⏳ Testing Infrastructure:** Not started
**⏳ Opus Subagent Prompt:** Not started

**Ready to proceed:** Yes - All foundational research complete
