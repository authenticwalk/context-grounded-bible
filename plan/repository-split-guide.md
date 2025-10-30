# Repository Split Migration Guide

## Overview

This guide documents the process of splitting the `context-grounded-bible` repository into 3 separate repositories for better scalability and performance.

## Current Problem

- **Single repository**: 2.6GB, 63,705 files
- **Slow clones**: Several minutes to clone
- **Git performance**: Operations slow down with many files
- **Mixed concerns**: Code, static data, and generated data in one repo

## Solution: 3-Repository Architecture

### Repository Structure

```
┌─────────────────────────────────────┐
│  context-grounded-bible (main)      │
│  - Tools & scripts                  │
│  - .claude/ configuration           │
│  - Documentation                    │
│  - Size: ~10MB                      │
└─────────────────────────────────────┘
           │
           ├── References data from ──────┐
           │                               │
           │                               ▼
           │                    ┌────────────────────────────┐
           │                    │  bible-data-lexicons       │
           │                    │  - Strong's dictionary     │
           │                    │  - Word reference data     │
           │                    │  - Size: 63MB              │
           │                    │  - Rarely changes          │
           │                    └────────────────────────────┘
           │
           └── References data from ──────┐
                                          │
                                          ▼
                              ┌────────────────────────────┐
                              │  bible-data-commentary     │
                              │  - Generated commentary    │
                              │  - Active development      │
                              │  - Size: 2.5GB             │
                              │  - Frequently updated      │
                              └────────────────────────────┘
```

### Repository Details

#### 1. context-grounded-bible (Main Repository)

**Contains:**
- `.claude/` - Claude Code skills and configuration
- `bible-study-tools/` - Tool scripts
- `src/` - Source code
- `agents/` - Agent configurations
- `plan/` - Planning documents
- All documentation files
- Configuration files (requirements.txt, etc.)

**Size:** ~10MB
**Update Frequency:** Regular (code/tool development)
**Users:** Developers, contributors, tool users

#### 2. bible-data-lexicons

**Contains:**
- `words/strongs/` - Strong's Greek/Hebrew dictionary (14,197 files)
- Future: Other lexicon data

**Size:** 63MB
**Update Frequency:** Rare (static reference data)
**Users:** Tools needing word/lexicon data

#### 3. bible-data-commentary

**Contains:**
- `commentary/` - Generated verse commentary (2.3GB)
- `commentaries/` - Additional commentary data (246MB)

**Size:** 2.5GB
**Update Frequency:** Frequent (active generation)
**Users:** Tools needing verse commentary, researchers

## Benefits of Split

### Performance
- ✅ Main repo clones in seconds (10MB vs 2.6GB)
- ✅ Faster git operations (fewer files to scan)
- ✅ Users download only what they need
- ✅ CI/CD runs faster (smaller checkouts)

### Organization
- ✅ Clear separation of concerns
- ✅ Independent release cycles
- ✅ Different update frequencies respected
- ✅ Easier access control per repository

### Scalability
- ✅ Each repo can grow independently
- ✅ Commentary repo can scale to 10-20GB without affecting tools
- ✅ Can add more data repos as needed
- ✅ Sparse checkout per data repo

### Developer Experience
- ✅ Clone only tools repo to start developing
- ✅ Add data repos on demand
- ✅ Less context confusion
- ✅ Faster iteration cycles

## Migration Process

### Prerequisites

1. **Install git-filter-repo:**
   ```bash
   pip install git-filter-repo
   ```

2. **Clean working directory:**
   ```bash
   git status  # Should show "nothing to commit"
   ```

3. **Notify team members:**
   - All contributors must re-clone after migration
   - Update CI/CD pipelines
   - Update documentation links

### Step-by-Step Migration

#### Step 1: Backup

```bash
# Automatic backup created by script
./split-repository.sh
```

The script creates a timestamped backup: `context-grounded-bible-backup-YYYYMMDD-HHMMSS`

#### Step 2: Run Split Script

```bash
./split-repository.sh
```

This will:
1. Verify prerequisites
2. Create backup
3. Split into 3 repos in `split-repos/` directory
4. Preserve full git history for each repo

**Expected output:**
```
✓ context-grounded-bible-main created
✓ bible-data-lexicons created (63MB)
✓ bible-data-commentary created (2.5GB)
```

#### Step 3: Review Split Repositories

```bash
# Review main repo
cd split-repos/context-grounded-bible-main
git log --oneline --graph
ls -lh

# Review lexicons repo
cd ../bible-data-lexicons
git log --oneline --graph
ls -lh

# Review commentary repo
cd ../bible-data-commentary
git log --oneline --graph
ls -lh
```

**Verify:**
- [ ] All expected files present in each repo
- [ ] Git history preserved
- [ ] No unexpected files
- [ ] Sizes match expectations

#### Step 4: Create GitHub Repositories

**Option A: Via GitHub Web Interface**
1. Go to https://github.com/new
2. Create `bible-data-lexicons` (Public or Private)
3. Create `bible-data-commentary` (Public or Private)
4. Do NOT initialize with README (we're pushing existing repos)

**Option B: Via GitHub CLI**
```bash
gh repo create authenticwalk/bible-data-lexicons --public --source=split-repos/bible-data-lexicons --push
gh repo create authenticwalk/bible-data-commentary --public --source=split-repos/bible-data-commentary --push
```

#### Step 5: Push to GitHub

**Main repository (keep existing):**
```bash
cd split-repos/context-grounded-bible-main
git remote set-url origin https://github.com/authenticwalk/context-grounded-bible
git branch -M main
git push -f origin main
```

**Lexicons repository:**
```bash
cd ../bible-data-lexicons
git remote add origin https://github.com/authenticwalk/bible-data-lexicons
git branch -M main
git push -u origin main
```

**Commentary repository:**
```bash
cd ../bible-data-commentary
git remote add origin https://github.com/authenticwalk/bible-data-commentary
git branch -M main
git push -u origin main
```

#### Step 6: Update Main Repository Documentation

Update the main repo's README.md to reference the data repositories:

```markdown
## Data Repositories

This repository contains tools and scripts. Bible data is stored separately:

- **Lexicons & Reference Data**: [bible-data-lexicons](https://github.com/authenticwalk/bible-data-lexicons)
  - Strong's Greek/Hebrew dictionary
  - Size: 63MB

- **Commentary Data**: [bible-data-commentary](https://github.com/authenticwalk/bible-data-commentary)
  - Generated verse commentary
  - Size: 2.5GB
  - Use sparse checkout for specific books

## Quick Start

```bash
# Clone main repo
git clone https://github.com/authenticwalk/context-grounded-bible
cd context-grounded-bible

# Clone data repos (as needed)
git clone https://github.com/authenticwalk/bible-data-lexicons data/lexicons
git clone https://github.com/authenticwalk/bible-data-commentary data/commentary
```
```

#### Step 7: Update Tool Configurations

Update tools to reference the new data repository structure:

**Example: config.yaml**
```yaml
data_repositories:
  lexicons:
    url: "https://github.com/authenticwalk/bible-data-lexicons"
    path: "data/lexicons"
    required: true

  commentary:
    url: "https://github.com/authenticwalk/bible-data-commentary"
    path: "data/commentary"
    required: false
    sparse_checkout:
      - "commentary/MAT"
      - "commentary/JHN"
```

**Example: Tool loader script**
```python
# tools/load_data.py
import os
import subprocess

def ensure_data_repo(name, url, path, sparse_patterns=None):
    """Clone data repository if not present."""
    if os.path.exists(path):
        return

    if sparse_patterns:
        # Clone with sparse checkout
        subprocess.run(['git', 'clone', '--filter=blob:none', '--sparse', url, path])
        subprocess.run(['git', 'sparse-checkout', 'set'] + sparse_patterns, cwd=path)
    else:
        # Full clone
        subprocess.run(['git', 'clone', url, path])

# Usage
ensure_data_repo(
    'lexicons',
    'https://github.com/authenticwalk/bible-data-lexicons',
    'data/lexicons'
)

ensure_data_repo(
    'commentary',
    'https://github.com/authenticwalk/bible-data-commentary',
    'data/commentary',
    sparse_patterns=['commentary/MAT', 'commentary/JHN']
)
```

#### Step 8: Update .gitignore

Add data directories to main repo's `.gitignore`:

```gitignore
# Data repositories (cloned separately)
data/
bible/
```

#### Step 9: Team Migration

**Send to all contributors:**

> **Action Required: Repository Split Migration**
>
> We've split the context-grounded-bible repository into 3 separate repositories for better performance:
>
> 1. **Main repo** (tools/scripts): https://github.com/authenticwalk/context-grounded-bible
> 2. **Lexicons** (reference data): https://github.com/authenticwalk/bible-data-lexicons
> 3. **Commentary** (generated data): https://github.com/authenticwalk/bible-data-commentary
>
> **What you need to do:**
>
> 1. Delete your local `context-grounded-bible` directory
> 2. Clone the new main repository
> 3. Clone data repositories as needed (see README)
>
> **Benefits:**
> - 97% faster clones (2.6GB → 10MB for main repo)
> - Work on tools without downloading all data
> - Better organization
>
> Questions? See the [migration guide](./plan/repository-split-guide.md)

#### Step 10: Update CI/CD

Update GitHub Actions, CI/CD pipelines:

**Before:**
```yaml
- uses: actions/checkout@v3
```

**After:**
```yaml
- uses: actions/checkout@v3
  with:
    repository: authenticwalk/context-grounded-bible

# Only checkout data if tests need it
- name: Checkout commentary data
  uses: actions/checkout@v3
  with:
    repository: authenticwalk/bible-data-commentary
    path: data/commentary
    sparse-checkout: |
      commentary/MAT
      commentary/JHN
```

## Rollback Plan

If something goes wrong:

```bash
# Delete split repos
rm -rf split-repos

# Restore from backup
cd ..
mv context-grounded-bible context-grounded-bible-failed
mv context-grounded-bible-backup-YYYYMMDD-HHMMSS context-grounded-bible
cd context-grounded-bible
```

## Post-Migration Verification

### Checklist

- [ ] All 3 repositories pushed to GitHub
- [ ] Main repo README updated with data repo links
- [ ] Tool configurations updated
- [ ] .gitignore updated
- [ ] CI/CD pipelines updated
- [ ] Team members notified
- [ ] Documentation links updated
- [ ] Test cloning all 3 repos
- [ ] Test tools can access data
- [ ] Backup verified and stored safely

### Testing

```bash
# Test main repo clone
git clone https://github.com/authenticwalk/context-grounded-bible
cd context-grounded-bible
ls -lh  # Should NOT contain bible/ directory
du -sh  # Should be ~10MB

# Test lexicons repo
git clone https://github.com/authenticwalk/bible-data-lexicons
cd bible-data-lexicons
ls -lh  # Should contain words/
du -sh  # Should be ~63MB

# Test commentary repo with sparse checkout
git clone --filter=blob:none --sparse https://github.com/authenticwalk/bible-data-commentary
cd bible-data-commentary
git sparse-checkout set commentary/MAT
ls -lh  # Should only contain Matthew commentary
```

## Future Optimizations

After the split, consider:

### Phase 3: External Storage for Static Data

Move lexicons to CDN/GitHub Releases:
- Strong's dictionary → GitHub Release asset
- Tools download once and cache locally
- Further reduces git repository overhead

### Phase 4: DVC for Commentary

If you need experiment tracking:
- Track commentary generation pipelines
- Compare different data generation approaches
- Requires S3/cloud storage (~$5/month)

## Troubleshooting

### Issue: git-filter-repo not found

```bash
pip install git-filter-repo
# Or: brew install git-filter-repo (macOS)
```

### Issue: "not a valid object name"

Ensure you're on the correct branch:
```bash
git checkout main
git pull origin main
```

### Issue: Large push rejected by GitHub

For very large pushes:
```bash
git config http.postBuffer 524288000  # 500MB
```

Or use GitHub CLI:
```bash
gh repo create --source=. --push
```

### Issue: Missing files after split

Verify the filter-repo command:
```bash
# Check what would be kept
git filter-repo --path bible/words/ --dry-run --force
```

## Cost Analysis

### Before Split

- **Single repo**: 2.6GB
- **Clone time**: 3-5 minutes
- **Disk usage per developer**: 2.6GB minimum
- **CI/CD**: Full 2.6GB clone every run

### After Split

- **Main repo**: 10MB (99.6% reduction)
- **Clone time**: 5-10 seconds
- **Disk usage**: 10MB (or 10MB + 63MB + 2.5GB if all cloned)
- **CI/CD**: Only 10MB for most builds

**Estimated savings:**
- Developer time: 5 minutes → 10 seconds per clone
- Disk space: Can work with just 10MB
- CI/CD: 97% faster for tests that don't need data

## Support

- **Documentation**: See main [README.md](../README.md)
- **Issues**: https://github.com/authenticwalk/context-grounded-bible/issues
- **Questions**: Create a GitHub Discussion

## References

- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo)
- [Git Sparse Checkout Guide](https://github.blog/open-source/git/bring-your-monorepo-down-to-size-with-sparse-checkout/)
- [Original Analysis](./bible-directory-optimization-analysis.md)
