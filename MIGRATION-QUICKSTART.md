# Repository Split - Quick Start Guide

## TL;DR

We're splitting this repo into 3 for better performance:
1. **mybibletoolbox-code** (10MB) - Tools & scripts
2. **mybibletoolbox-lexicon** (63MB) - Reference data
3. **mybibletoolbox-commentary** (2.5GB) - Generated data

**Result:** 97% faster clones for developers

## Before You Start

1. **Commit all changes** - Clean working directory required
2. **Install git-filter-repo**: `pip install git-filter-repo`
3. **GitHub repos created** - All 3 repos should exist (already done!)

## Run the Migration

```bash
# From repository root
./split-repository.sh
```

Follow the prompts. Script will:
- ✅ Create timestamped backup
- ✅ Split into 3 repos in `split-repos/` directory
- ✅ Preserve full git history
- ✅ Provide next steps

## After Split

### Review the Split

```bash
cd split-repos

# Check each repo
ls -lh mybibletoolbox-code/
ls -lh mybibletoolbox-lexicon/
ls -lh mybibletoolbox-commentary/
```

### Push to GitHub

```bash
# Code repo
cd split-repos/mybibletoolbox-code
git remote add origin https://github.com/authenticwalk/mybibletoolbox-code
git branch -M main
git push -u origin main

# Lexicon repo
cd ../mybibletoolbox-lexicon
git remote add origin https://github.com/authenticwalk/mybibletoolbox-lexicon
git branch -M main
git push -u origin main

# Commentary repo
cd ../mybibletoolbox-commentary
git remote add origin https://github.com/authenticwalk/mybibletoolbox-commentary
git branch -M main
git push -u origin main
```

## Using the New Structure

### For Developers (Tools/Scripts)

```bash
# Just clone code repo
git clone https://github.com/authenticwalk/mybibletoolbox-code
```

**That's it!** 10MB clone in seconds.

### For Data Users

```bash
# Clone code repo
git clone https://github.com/authenticwalk/mybibletoolbox-code
cd mybibletoolbox-code

# Clone lexicon (if needed)
git clone https://github.com/authenticwalk/mybibletoolbox-lexicon data/lexicon

# Clone commentary with sparse checkout (recommended)
git clone --filter=blob:none --sparse \
  https://github.com/authenticwalk/mybibletoolbox-commentary \
  data/commentary

# Add only books you need
cd data/commentary
git sparse-checkout set commentary/MAT commentary/JHN
```

## What Goes Where?

| Repository | Contents | Size | Update Frequency |
|------------|----------|------|------------------|
| **mybibletoolbox-code** | Tools, scripts, .claude/, docs | 10MB | Regular |
| **mybibletoolbox-lexicon** | Strong's dictionary, word data | 63MB | Rare |
| **mybibletoolbox-commentary** | Generated verse commentary | 2.5GB | Frequent |

## Troubleshooting

### "git-filter-repo not found"
```bash
pip install git-filter-repo
```

### "uncommitted changes"
```bash
git status
git add . && git commit -m "save work"
# Then run split script
```

### Need to rollback?
```bash
# Just delete split-repos directory and start over
rm -rf split-repos
# Original repo is unchanged until you push
```

## Help

- **Full guide**: [plan/repository-split-guide.md](plan/repository-split-guide.md)
- **Issues**: https://github.com/authenticwalk/mybibletoolbox-code/issues

## The Why

**Before:**
- Single 2.6GB repo
- 3-5 minute clones
- Slow git operations
- Mixed concerns

**After:**
- Main repo: 10MB (99.6% smaller)
- 5-10 second clones
- Fast git operations
- Clean separation

Developers work with tools without downloading gigabytes of data they don't need.
