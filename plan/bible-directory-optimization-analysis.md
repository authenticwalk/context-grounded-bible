# Bible Directory Optimization: Comprehensive Analysis

## Current Repository Status

**Repository Statistics (as of 2025-10-30):**
- Total bible directory size: 2.6GB
- Total files: 63,705 files
- Git repository (.git): 1.2GB
- Total commits: 90

**Data Breakdown:**
- `bible/commentary/`: 2.3GB (30,966 files)
- `bible/commentaries/`: 246MB (18,542 files)
- `bible/words/`: 63MB (14,197 files)
- Average file size: 136KB - 346KB (substantial YAML files)

**Current Growth Trajectory:**
The project is in early stages but already experiencing significant size issues. If this pattern continues to cover the entire Bible (31,102 verses), the repository could easily exceed 10-20GB.

---

## Solution Analysis

### 1. Git Sparse Checkout + Partial Clone

**How It Works:**
- **Sparse Checkout**: Allows you to check out only specific directories in your working tree
- **Partial Clone**: Uses filters to avoid downloading unnecessary objects from the repository
- Combined approach: `git clone --filter=blob:none --sparse` downloads only metadata, then you selectively checkout directories

**Implementation:**
```bash
# Clone with sparse checkout
git clone --filter=blob:none --sparse https://github.com/user/context-grounded-bible
cd context-grounded-bible

# Only checkout specific directories
git sparse-checkout init --cone
git sparse-checkout set bible/words bible/commentaries/PHP
```

**Pros:**
- Fastest initial clone (97% faster in some cases: 3m 49s → 6s)
- Reduces checkout size by 96% (1.3GB → 49MB)
- Native Git feature (no external tools needed)
- Users can selectively download only the data they need
- Still maintains full version control
- Excellent for CI/CD pipelines
- Free and no infrastructure required

**Cons:**
- Users must understand which directories they need
- Requires Git 2.25+ (cone mode requires 2.27+)
- Still downloads full history unless combined with shallow clone
- Complexity for non-technical users
- Each directory change requires git commands

**Bible Commentary Use Case:**
- **Excellent fit for tools/skills**: Tools could specify which Bible books they need
- **Natural organization**: Your existing `bible/{book}/{chapter}/{verse}` structure is perfect for sparse checkout
- **Researcher workflow**: Researchers studying specific books could checkout only those books
- **Example**: A tool studying Philippians only needs `bible/*/PHP/` directories

**How Tools Access Data:**
```python
# Tool would specify required books in configuration
REQUIRED_BOOKS = ['PHP', 'EPH', 'COL']

# Before running, checkout only required directories
subprocess.run(['git', 'sparse-checkout', 'set',
                'bible/words'] +
               [f'bible/commentaries/{book}' for book in REQUIRED_BOOKS])
```

**Recommended Implementation Path:**
1. Document sparse checkout patterns in tool READMEs
2. Create helper scripts for common patterns (NT only, OT only, specific books)
3. Update skills to declare required Bible books
4. CI/CD uses sparse checkout to test only affected books

---

### 2. Git LFS (Large File Storage)

**How It Works:**
- Replaces large files with pointer files in Git
- Stores actual file contents on a separate LFS server
- Downloads full files only when checking out

**Implementation:**
```bash
# Install git-lfs
git lfs install

# Track all YAML files
git lfs track "bible/**/*.yaml"

# Migrate existing files
git lfs migrate import --include="bible/**/*.yaml"
```

**Pros:**
- Reduces Git repository size dramatically
- Transparent to users (mostly)
- Works with GitHub, GitLab, Bitbucket
- Can track specific file patterns
- Good for binary files or files that change frequently

**Cons:**
- Requires LFS server (GitHub free tier: 1GB storage, 1GB bandwidth/month)
- Costs money at scale (GitHub: $5/month per 50GB storage pack)
- Still downloads ALL pointer files (63,705 small pointer files)
- Bound to single upstream provider
- More complex CI/CD setup
- Not ideal for text files (YAML) that compress well
- **Critical**: Your YAML files are text, not binary - Git LFS is overkill

**Bible Commentary Use Case:**
- **Poor fit**: YAML files are text-based and compress well in Git
- **Cost concern**: 2.6GB would require paid plan ($5-10/month)
- **Overhead**: Managing 63,705+ LFS pointers adds complexity
- **Better alternatives exist**: Sparse checkout or separate repos are simpler

**How Tools Access Data:**
- Transparent - tools access files normally
- But ALL pointer files still need to be present
- No selective download without sparse checkout

**2025 Update:**
Git itself is moving toward native large file support, potentially making LFS obsolete. The `--filter=blob:limit` feature provides similar benefits without external servers.

---

### 3. Separate Data Repositories

**How It Works:**
- Split into multiple repositories:
  - `context-grounded-bible` (main code/tools repo)
  - `bible-data-words` (Strong's dictionary, lexicons)
  - `bible-data-commentary` (commentary data)
  - Or by category: `bible-data-greek`, `bible-data-hebrew`, `bible-data-interpretations`

**Implementation:**
```bash
# Option A: Split by type
context-grounded-bible/          # Tools, skills, documentation
bible-data-words/                # All word-related data
bible-data-commentary/           # All commentary data

# Option B: Split by language/domain
context-grounded-bible/          # Tools, skills
bible-data-greek/                # Greek word studies
bible-data-hebrew/               # Hebrew word studies
bible-data-english-commentary/   # English commentaries
```

**Pros:**
- Clean separation of concerns (code vs data)
- Users can clone only what they need
- Smaller, faster clones for each repository
- Independent release cycles for data vs code
- Different access controls per repository
- Easier to manage GitHub free tier limits per repo
- Can use different storage strategies per repo
- Natural "microservices" architecture for data

**Cons:**
- More repositories to manage (coordination overhead)
- Tools need to access multiple repositories
- Versioning across repositories is complex
- Dependency management required
- More complex CI/CD setup
- Risk of version mismatches between repos
- Contributors need to clone multiple repos

**Bible Commentary Use Case:**
- **Good fit for domain separation**: Words vs Commentary are logically separate
- **Good fit for language separation**: Greek, Hebrew, English are independent
- **Reduces barrier to entry**: Users interested in tools don't need data
- **Scales well**: Each data repo can grow independently
- **Organizational clarity**: Clear ownership and purpose per repo

**How Tools Access Data:**
```python
# Option 1: Git submodules (auto-fetched)
# Tools repository includes submodules for data

# Option 2: Dependency declaration
# pyproject.toml or requirements.txt
dependencies = [
    "bible-data-words @ git+https://github.com/user/bible-data-words",
]

# Option 3: Configuration-based
# config.yaml
data_repositories:
  words: "https://github.com/user/bible-data-words"
  commentary: "https://github.com/user/bible-data-commentary"

# Tool clones on first use
if not os.path.exists('data/words'):
    git.clone('https://github.com/user/bible-data-words', 'data/words')
```

**Recommended Split Structure:**
```
context-grounded-bible/           # Main repo (tools, skills, docs)
├── .claude/                      # Claude config
├── tools/                        # Bible study tools
├── skills/                       # Claude skills
└── README.md

bible-data-static/               # Reference data (rarely changes)
└── words/
    └── strongs/                  # Strong's dictionary

bible-data-generated/            # Generated commentary (frequently updated)
├── commentary/
└── commentaries/
```

---

### 4. Git Submodules

**How It Works:**
- Embeds other Git repositories as subdirectories
- Main repository stores references to specific commits of submodule repos
- Users explicitly update submodules

**Implementation:**
```bash
# In main repository
git submodule add https://github.com/user/bible-data-words bible/words
git submodule add https://github.com/user/bible-data-commentary bible/commentary

# Users clone with submodules
git clone --recursive https://github.com/user/context-grounded-bible

# Or initialize after cloning
git submodule update --init --recursive
```

**Pros:**
- Native Git feature (no external tools)
- Clear versioning (main repo pins submodule commits)
- Can update submodules independently
- Works well with sparse checkout
- Good for separating stable vs frequently-updated data

**Cons:**
- Notorious for being confusing to users
- "Poor man's Git LFS" - often considered a hack
- Requires explicit initialization
- Easy to forget to update submodules
- Merge conflicts when submodule references diverge
- Not transparent - users see empty directories if not initialized

**Bible Commentary Use Case:**
- **Moderate fit**: Works if you split into separate repos
- **Complexity warning**: Submodules are famously confusing
- **Better combined with sparse checkout**: Submodule + sparse = selective data
- **Alternative exists**: Direct cloning might be simpler

**How Tools Access Data:**
- Same as separate repos, but with submodule awareness
- Need to ensure `git submodule update --init` before accessing

**Best Practice:**
If using submodules, provide helper scripts:
```bash
# setup-data.sh
#!/bin/bash
git submodule update --init bible/words
git submodule update --init bible/commentaries
```

---

### 5. Git Shallow Clone

**How It Works:**
- Clone only recent history (e.g., last N commits)
- Uses `--depth=N` flag

**Implementation:**
```bash
# Clone only latest commit
git clone --depth 1 https://github.com/user/context-grounded-bible

# Clone last 10 commits
git clone --depth 10 https://github.com/user/context-grounded-bible
```

**Pros:**
- Dramatically faster clones (11-year codebase: 4m 24s → 29.5s)
- Smaller disk usage
- Perfect for CI/CD builds
- Smaller .git directory

**Cons:**
- No history available
- Cannot see old commits or branches
- Difficult to contribute (need to unshallow)
- Fetches are computationally expensive for server
- GitHub discourages except for temporary builds
- Not useful for development work

**Bible Commentary Use Case:**
- **Poor fit for primary solution**: Tools need full data, not just recent
- **Good fit for CI/CD**: Temporary test environments
- **Doesn't solve core problem**: Still downloads all 63,705 files
- **Better for code repos**: History matters less for data

**How Tools Access Data:**
- No change - files are present in working directory
- But git operations are limited

**Recommendation:**
- Use in CI/CD only: `git clone --depth 1`
- Not a solution for development or tool usage

---

### 6. DVC (Data Version Control)

**How It Works:**
- Tracks data files with `.dvc` files (like Git LFS pointers)
- Stores actual data in remote storage (S3, Azure, GCP, local)
- Designed for ML/data science workflows
- Provides pipeline management and experiment tracking

**Implementation:**
```bash
# Install DVC
pip install dvc[s3]

# Initialize
dvc init

# Track data directory
dvc add bible/commentary
dvc add bible/words

# Configure remote storage
dvc remote add -d storage s3://my-bucket/bible-data

# Push data to remote
dvc push

# Git tracks only .dvc files
git add bible/commentary.dvc bible/words.dvc .dvc/config
git commit -m "Add bible data tracking with DVC"
```

**Pros:**
- Purpose-built for large datasets
- Flexible storage (S3, GCS, Azure, SSH, local)
- Only download files you need (selective pull)
- Built for reproducibility and experimentation
- Better than Git LFS for text data
- Can track directories, not just files
- Pipeline management features
- Deduplication across versions

**Cons:**
- Additional tool to learn (steeper curve than Git)
- Requires running DVC commands alongside Git
- Not transparent (separate `dvc pull` command)
- Infrastructure cost (S3 storage)
- More complex CI/CD setup
- Overhead of maintaining DVC configuration
- Might be overkill for your use case

**Bible Commentary Use Case:**
- **Moderate fit**: Designed for exactly this problem (large data)
- **Cost**: S3 storage ~$0.023/GB/month (2.6GB = $0.06/month + transfer)
- **Selective download**: Users pull only needed books
- **Experiment tracking**: Could track which commentary source performed better
- **Overhead concern**: DVC is ML-focused, might be too heavy for YAML files

**How Tools Access Data:**
```python
# Tools would use DVC API or command
import dvc.api

# Pull specific data before using
subprocess.run(['dvc', 'pull', 'bible/commentary/PHP'])

# Or use DVC API to read directly from storage
with dvc.api.open('bible/commentary/PHP/1/1.yaml', repo='user/context-grounded-bible') as f:
    data = yaml.safe_load(f)
```

**When DVC Makes Sense:**
- You want to track data provenance (which tool generated what)
- You need to compare different data generation approaches
- You want pipeline management (data generation workflows)
- You're already using ML workflows

**When DVC is Overkill:**
- Simple read-only reference data
- No need for experiment tracking
- Team is not familiar with ML tools

---

### 7. External Storage Solutions

**How It Works:**
- Store data outside Git entirely
- Use cloud storage (S3, GCS, Azure Blob)
- Git repository contains only download scripts and metadata

**Implementation Options:**

**Option A: Cloud Storage (S3)**
```bash
# Git repository structure
context-grounded-bible/
├── tools/
├── skills/
├── scripts/
│   └── download-data.py      # Downloads from S3
└── data/                     # .gitignored

# download-data.py
import boto3
s3 = boto3.client('s3')
s3.download_file('bible-data-bucket', 'words/strongs.tar.gz', 'data/strongs.tar.gz')
```

**Option B: GitHub Releases**
```bash
# Upload data as release assets
gh release create v1.0 bible-data.tar.gz

# Tools download from releases
curl -L https://github.com/user/context-grounded-bible/releases/latest/download/bible-data.tar.gz | tar xz
```

**Option C: CDN/Static Hosting**
```bash
# Host on GitHub Pages, Netlify, Vercel
https://context-grounded-bible.netlify.app/data/bible-commentary.tar.gz
```

**Pros:**
- Git repository stays tiny (only code)
- Unlimited storage capacity (only pay for what you use)
- Fast downloads (CDN distribution)
- No Git performance issues
- Simple versioning (timestamped or versioned URLs)
- Can use compression effectively
- No Git learning curve for data

**Cons:**
- No version control for data
- Separate infrastructure to maintain
- Costs money (though minimal)
- Tools need internet connection
- No atomic versioning (code + data)
- Manual upload/download processes
- Dependency on external service

**Bible Commentary Use Case:**
- **Excellent for static data**: Strong's dictionary rarely changes
- **Good for large datasets**: Cost-effective for TB-scale data
- **Poor for active development**: Harder to iterate on data
- **Hybrid approach possible**: Static data external, generated data in Git

**How Tools Access Data:**
```python
# Check if data exists locally
if not os.path.exists('data/strongs'):
    print("Downloading Strong's dictionary...")
    download_from_s3('strongs')

# Use cached data
with open('data/strongs/G1234.yaml') as f:
    data = yaml.safe_load(f)
```

**Cost Estimate (AWS S3):**
- Storage: 2.6GB @ $0.023/GB/month = $0.06/month
- Transfer: 100 downloads/month @ 2.6GB = 260GB @ $0.09/GB = $23.40/month
- Total: ~$23.46/month (high estimate)

**Free Alternatives:**
- GitHub Releases: Free, but 2GB per file limit
- Netlify: 100GB bandwidth/month free
- Cloudflare R2: 10GB storage free, zero egress costs

---

### 8. Git Filter-Repo (Monorepo Cleanup)

**How It Works:**
- Rewrites Git history to remove or reorganize files
- 100x faster than `git filter-branch`
- Can move files to subdirectories, remove large files, etc.

**Implementation:**
```bash
# Install
pip install git-filter-repo

# Remove accidentally committed large files
git filter-repo --path bible/large-file.bin --invert-paths

# Remove files larger than 10MB
git filter-repo --strip-blobs-bigger-than 10M

# Reorganize structure
git filter-repo --path-rename bible/old:bible/new
```

**Pros:**
- Very fast (10 seconds vs 25+ minutes)
- Can rescue a bloated repository
- Useful for restructuring
- Recommended by Git project over filter-branch

**Cons:**
- Rewrites history (all users must re-clone)
- Destructive operation (backup required)
- Resets Git configuration
- One-time operation, not an ongoing strategy
- All contributors must coordinate

**Bible Commentary Use Case:**
- **Not a solution, but a tool**: Doesn't solve ongoing growth
- **Useful for cleanup**: If you've committed test files accidentally
- **Use before splitting**: Clean history before creating separate repos
- **One-time migration**: Restructure before implementing new strategy

**When to Use:**
- Before implementing separate repos (clean history first)
- After discovering large files were committed by mistake
- When restructuring directory organization

**Warning:**
After running filter-repo, all team members must re-clone:
```bash
# After filter-repo
git push --force origin main

# Team members must:
rm -rf context-grounded-bible
git clone https://github.com/user/context-grounded-bible
```

---

## Performance Considerations: Many Small Files

**The Hidden Problem:**
Your repository has 63,705 small files. Research shows that many small files cause performance issues:

**Git's Bottleneck:**
- Git itself handles many files well
- The bottleneck is the operating system (filesystem enumeration)
- Operations like `git status` scan all files with stat() calls
- Windows particularly struggles with many files

**Real-World Examples:**
- Canva: 500,000 files → `git status` takes 10 seconds, `git fetch` takes minutes
- Scientific computing: 100,000 files → tens of minutes for operations
- 10,000 files on disk: 5 minutes to commit

**Your Situation:**
- 63,705 files currently
- Growing to potentially 200,000+ files (full Bible coverage)
- Each operation will slow down significantly

**Solutions:**
1. **Reduce file count**: Combine related files into archives
2. **Use Git optimizations**: Enable `feature.manyFiles` config
3. **Filesystem monitoring**: Use `fsmonitor` with Watchman
4. **Separate repos**: Split data to keep file counts manageable
5. **External storage**: Move data outside Git entirely

**Git Configuration for Many Files:**
```bash
# Enable many files optimizations
git config feature.manyFiles true
git config core.untrackedCache true
git config index.version 4
```

---

## Recommendation Matrix

### For Your Bible Commentary Project

| Solution | Setup Complexity | Ongoing Maintenance | Cost | Performance | Best For |
|----------|-----------------|---------------------|------|-------------|----------|
| **Sparse Checkout + Partial Clone** | Low | Low | Free | Excellent | Primary solution |
| **Separate Repos** | Medium | Medium | Free | Excellent | Data organization |
| **External Storage (S3/CDN)** | Medium | Low | ~$25/month | Excellent | Static reference data |
| **DVC** | High | Medium | ~$5/month | Good | ML workflows, experimentation |
| **Git LFS** | Low | Medium | $5-10/month | Poor | Not recommended |
| **Shallow Clone** | Low | Low | Free | Good | CI/CD only |
| **Git Submodules** | Medium | High | Free | Good | If splitting repos |
| **Filter-Repo** | High | N/A | Free | N/A | One-time cleanup |

---

## Recommended Approach: Hybrid Strategy

Based on your requirements and current state, I recommend a **hybrid approach**:

### Phase 1: Immediate Relief (Sparse Checkout + Git Config)

**Why:**
- No infrastructure required
- Native Git features
- Immediate 90%+ improvement
- Zero cost

**Implementation:**
```bash
# Enable many files optimizations
git config feature.manyFiles true
git config core.untrackedCache true
git config index.version 4

# Document sparse checkout patterns in README
git sparse-checkout init --cone
git sparse-checkout set bible/words bible/commentaries/PHP
```

**For Tools/Skills:**
- Each skill declares required Bible books
- Helper scripts setup sparse checkout for common patterns
- CI/CD uses sparse checkout to test only affected books

### Phase 2: Repository Split (Separate Repos)

**Why:**
- Clean separation of concerns
- Independent scaling
- Better organization
- Still free

**Structure:**
```
context-grounded-bible/              # Main repository (tools, skills)
├── .claude/
├── tools/
├── skills/
└── README.md                        # Points to data repos

bible-data-lexicons/                 # Static reference data
└── strongs/
    ├── greek/
    └── hebrew/

bible-data-commentary/               # Generated commentary
├── commentary/
└── commentaries/
```

**How Tools Access:**
```python
# config.yaml in each tool
data_sources:
  lexicons: "https://github.com/user/bible-data-lexicons"
  commentary: "https://github.com/user/bible-data-commentary"

# Auto-clone on first use
def ensure_data(source_name):
    if not os.path.exists(f'data/{source_name}'):
        git.clone(config['data_sources'][source_name],
                  f'data/{source_name}',
                  sparse=['relevant/paths'])
```

### Phase 3: Static Data to CDN (Optional)

**Why:**
- Strong's dictionary and lexicons rarely change
- Reduces data repo size
- Faster downloads via CDN
- Zero egress costs with Cloudflare R2

**Implementation:**
- Move `bible/words/strongs` to Cloudflare R2 or GitHub Releases
- Keep generated commentary in Git (actively developed)
- Tools download lexicons on first run, cache locally

### Phase 4: DVC for Experimentation (Future)

**When:**
- You start comparing different commentary generation approaches
- You need pipeline management for data generation
- You want reproducible experiments

**Why:**
- Purpose-built for this workflow
- Tracks which tool generated which data
- Enables A/B testing of commentary approaches

---

## Implementation Checklist

### Immediate Actions (This Week)

- [ ] Enable Git many-files optimizations
  ```bash
  git config feature.manyFiles true
  git config core.untrackedCache true
  git config index.version 4
  ```

- [ ] Document sparse checkout patterns in README
  ```markdown
  ## Working with Large Data

  To reduce clone time, use sparse checkout:

  # Clone only metadata
  git clone --filter=blob:none --sparse https://github.com/user/context-grounded-bible

  # Checkout specific books
  git sparse-checkout set bible/words bible/commentaries/PHP
  ```

- [ ] Create helper scripts for common patterns
  ```bash
  # scripts/checkout-new-testament.sh
  git sparse-checkout set bible/words \
    bible/commentaries/{MAT,MRK,LUK,JHN,ACT,ROM,1CO,2CO,...}
  ```

- [ ] Update CI/CD to use sparse checkout

### Near-Term (Next Month)

- [ ] Analyze data split boundaries
  - Which data changes frequently vs rarely?
  - Which data is independent vs interconnected?
  - Which data is large vs small?

- [ ] Plan repository split
  - Decide on 2-3 separate data repos
  - Design inter-repo dependencies
  - Document migration plan

- [ ] Use git filter-repo to clean history if needed
  ```bash
  # Backup first!
  git clone --mirror context-grounded-bible context-grounded-bible-backup

  # Clean any accidentally committed large files
  git filter-repo --strip-blobs-bigger-than 100M
  ```

- [ ] Create separate repositories
  - Extract data with preserved history
  - Update tool configurations
  - Add submodules or documentation for data repos

### Long-Term (Future)

- [ ] Evaluate external storage for static data
  - Strong's dictionary to CDN
  - Rare language translations to storage

- [ ] Consider DVC if doing experimentation
  - Compare different commentary sources
  - Track data generation pipelines

- [ ] Monitor and optimize
  - Track clone times
  - Monitor repo sizes
  - Gather user feedback

---

## Specific Recommendations by Data Type

### Strong's Dictionary (`bible/words/strongs/`)
- **Current**: 14,197 files, 63MB
- **Status**: Static reference data (rarely changes)
- **Recommendation**: Move to external storage (GitHub Releases or CDN)
- **Reason**: No need for version control, reduces repo size
- **Access**: Download once, cache locally

### Generated Commentary (`bible/commentary/`, `bible/commentaries/`)
- **Current**: 49,508 files, 2.5GB
- **Status**: Actively generated, frequently updated
- **Recommendation**: Separate repository with sparse checkout
- **Reason**: Needs version control, but separate from code
- **Access**: Sparse checkout by Bible book

### Tools and Skills
- **Recommendation**: Keep in main repository
- **Reason**: Lightweight, code-focused, needs full history

---

## Measuring Success

After implementing optimizations, track these metrics:

**Performance Metrics:**
- [ ] Initial clone time: Target < 30 seconds (vs current minutes)
- [ ] Working directory size: Target < 100MB (vs current 2.6GB)
- [ ] `git status` time: Target < 2 seconds
- [ ] `git fetch` time: Target < 5 seconds

**User Experience:**
- [ ] Contributors can clone and start working in < 1 minute
- [ ] CI/CD builds complete in reasonable time
- [ ] Tools can access needed data without manual steps
- [ ] Clear documentation for data access patterns

**Organizational:**
- [ ] Clear separation between code and data
- [ ] Independent release cycles for data repos
- [ ] Manageable file counts per repository (< 10,000)
- [ ] Sustainable growth pattern for full Bible coverage

---

## Conclusion

Your Bible commentary project faces a common challenge: **Git was designed for code, not large datasets**. While your 2.6GB and 63,705 files are manageable now, the growth trajectory will cause significant problems.

**The winning combination:**

1. **Sparse Checkout + Partial Clone** (immediate, free, native)
2. **Repository Split** (organizational clarity, sustainable growth)
3. **External Storage for Static Data** (optional, for reference data)
4. **DVC** (future, if you need experimentation tracking)

**Start simple, evolve as needed.** Sparse checkout gives you immediate relief. Split repositories when you start feeling organizational pain. Add external storage or DVC only if you need their specific benefits.

**The key insight:** Your data has different characteristics (static reference vs generated commentary vs code), and they deserve different strategies. Don't force everything into one Git repository just because that's where you started.

---

## Additional Resources

### Git Sparse Checkout
- [GitHub Blog: Sparse Checkout](https://github.blog/open-source/git/bring-your-monorepo-down-to-size-with-sparse-checkout/)
- [Git Documentation: git-sparse-checkout](https://git-scm.com/docs/git-sparse-checkout)

### Git Performance
- [Atlassian: Big Repositories](https://www.atlassian.com/git/tutorials/big-repositories)
- [Microsoft: Git Performance](https://github.com/microsoft/git/blob/HEAD/Documentation/technical/gvfs.md)

### DVC
- [DVC Documentation](https://dvc.org/doc)
- [DVC vs Git LFS](https://dvc.org/doc/user-guide/related-technologies#git-lfs)

### Git Filter-Repo
- [Git Filter-Repo](https://github.com/newren/git-filter-repo)
- [Git Tower Tutorial](https://www.git-tower.com/learn/git/faq/git-filter-repo)

### Repository Organization
- [GitOps Directory Structure](https://developers.redhat.com/articles/2022/09/07/how-set-your-gitops-directory-structure)
- [Monorepo vs Multirepo](https://www.harness.io/harness-devops-academy/best-code-repository-for-microservices)
