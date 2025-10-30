# Repository Split - Quick Start Guide

## TL;DR

We're splitting this repo into 3 for better performance:
1. **Main repo** (10MB) - Tools & scripts
2. **Lexicons** (63MB) - Reference data
3. **Commentary** (2.5GB) - Generated data

**Result:** 97% faster clones for developers

## Before You Start

1. **Commit all changes** - Clean working directory required
2. **Install git-filter-repo**: `pip install git-filter-repo`
3. **Backup important work** - Script creates backup automatically

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
ls -lh context-grounded-bible-main/
ls -lh bible-data-lexicons/
ls -lh bible-data-commentary/
```

### Create GitHub Repos

**Option 1 - Web Interface:**
1. Go to https://github.com/new
2. Create `bible-data-lexicons`
3. Create `bible-data-commentary`

**Option 2 - CLI:**
```bash
gh repo create authenticwalk/bible-data-lexicons --public
gh repo create authenticwalk/bible-data-commentary --public
```

### Push to GitHub

```bash
# Main repo (update existing)
cd split-repos/context-grounded-bible-main
git remote set-url origin https://github.com/authenticwalk/context-grounded-bible
git push -f origin main

# Lexicons repo
cd ../bible-data-lexicons
git remote add origin https://github.com/authenticwalk/bible-data-lexicons
git push -u origin main

# Commentary repo
cd ../bible-data-commentary
git remote add origin https://github.com/authenticwalk/bible-data-commentary
git push -u origin main
```

## Using the New Structure

### For Developers (Tools/Scripts)

```bash
# Just clone main repo
git clone https://github.com/authenticwalk/context-grounded-bible
```

**That's it!** 10MB clone in seconds.

### For Data Users

```bash
# Clone main repo
git clone https://github.com/authenticwalk/context-grounded-bible
cd context-grounded-bible

# Clone lexicons (if needed)
git clone https://github.com/authenticwalk/bible-data-lexicons data/lexicons

# Clone commentary with sparse checkout (recommended)
git clone --filter=blob:none --sparse \
  https://github.com/authenticwalk/bible-data-commentary \
  data/commentary

# Add only books you need
cd data/commentary
git sparse-checkout set commentary/MAT commentary/JHN
```

## What Goes Where?

| Repository | Contents | Size | Update Frequency |
|------------|----------|------|------------------|
| **main** | Tools, scripts, .claude/, docs | 10MB | Regular |
| **lexicons** | Strong's dictionary, word data | 63MB | Rare |
| **commentary** | Generated verse commentary | 2.5GB | Frequent |

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
# Backup is at parent directory
cd ..
mv context-grounded-bible-backup-YYYYMMDD-HHMMSS context-grounded-bible
```

## Help

- **Full guide**: [plan/repository-split-guide.md](plan/repository-split-guide.md)
- **Issues**: https://github.com/authenticwalk/context-grounded-bible/issues

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
