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

## Working Preferences

### File Organization
- **NO summary files in root directory** - Do not create CHANGES-SUMMARY.md, COMPLETION-SUMMARY.md, PR-DESCRIPTION.md, or similar files in the project root
- **Use `/plan` directory** - For planning and tracking work, create files in `/plan/{task-name}.md` and update them as you learn and progress
- **Keep root clean** - Root should only contain permanent project documentation

### Documentation Philosophy
- **Prefer concise over comprehensive** - Simple instructions let AI figure things out; verbose explanations create confusion
- **Don't over-explain mechanics** - Avoid detailed explanations of "how to use tokens" or basic processes unless solving a specific issue
- **Inline key info, reference details** - Summarize essential standards in tool READMEs; link to full docs for edge cases with "see {doc} for details"
- **Avoid redundancy** - Don't create "-quick" versions of docs; extract relevant parts directly into tool READMEs

### Tool Development Process
- **Experiments optimize, researchers execute** - Tool experimentation phase should test sources and optimize lookups; researchers should use the optimized approach directly
- **Document sources, not tools** - In tool READMEs, list helpful webpages, not the obvious fact that WebSearch/WebFetch exist
- **Tailored standards** - Tools dealing with words need word standards; tools without words don't need them. Include only relevant standards.

## Git Commit Guidelines

When committing changes to this repository, follow these guidelines:

### Separate Data and Code Commits

**IMPORTANT:** Data files must be committed separately from code files. This allows for easier cherry-picking and repository management.

**Two-commit workflow:**
1. **First commit:** Code/script files only (e.g., Python scripts, configuration files)
2. **Second commit:** Data files only (all generated YAML files in `./bible/` directory)

**Example:**
```bash
# Commit 1: Code changes
git add strongs-fetcher.py
git commit -m "feat: add Strong's dictionary fetcher script"

# Commit 2: Generated data
git add bible/words/strongs
git commit -m "data: add Strong's dictionary entries (14,197 files)"
```

**Why this matters:**
- Enables cherry-picking data updates without code changes
- Keeps git history clean and organized
- Makes it easier to revert data without affecting code
- Reduces merge conflicts between data and code changes

## Citations

Bible Verses: **Format:** Incremental specificity as needed: `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

