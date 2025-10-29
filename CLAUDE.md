# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Context-Grounded Bible project - an initiative to create the largest AI-readable commentary on the entire Bible. The goal is to provide extensive context data for AI systems to ground their responses in truth when working with Biblical texts, especially for Bible translators, pastors, and students.

### The Problem Being Solved

AI text prediction models tend to be more confident than accurate when dealing with Biblical texts. While they perform well on commonly cited passages (like John 3:16) in popular translations (NIV, KJV), accuracy degrades significantly with:
- Lesser-quoted texts (minor prophets, Numbers, etc.)
- Rare or minority language translations
- Verses that lack extensive Internet training data

### The Solution

By providing extensive contextual data (essentially "a book's worth of information") for every verse broken into smaller task focused files, AI systems can be grounded in truth rather than relying solely on compressed training data.

## Repository Structure

### Data Organization

All generated commentary data follows this strict directory structure:

```
./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-{task}.yaml
```

Examples:
- `./bible/MAT/5/3/MAT-5-3-greek-words.yaml`
- `./bible/JHN/3/16/JHN-3-16-interpretations.yaml`

### File Formats

- All data files are in YAML format (both human and AI readable)
- Data is loosely structured to enable merging and filtering


## Development Notes

- The `.claude/` directory contains Claude Code configuration and slash commands
- The project is in early stages - the `bible/` directory structure will be created as data is generated
- Book codes follow standard 3-letter abbreviations (MAT, JHN, GEN, etc.) (USFM 3.0)
- Language codes follow (ISO-639-3)
- This is an open-source project under MIT License

## Writing Style for This Project

**Be Concise:** Trust AI agents to figure out details. Over-explanation increases confusion and token cost.
- ❌ "You must track tokens. Use the API response. Include all phases: research, generation, review. This is CRITICAL."
- ✅ "Track tokens_used from API response"

**No One-Off Summaries:** Don't create summary files like `CHANGES-SUMMARY.md` in root. Instead:
- Create plans in `/plan` directory
- Update plans with learnings as work progresses
- Plans evolve, summaries pollute

**Inline Relevant Content:** Don't create separate QUICK reference files. Put relevant parts directly in tool READMEs.

## Citations

Bible Verses: **Format:** Incremental specificity as needed: `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

