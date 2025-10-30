#!/bin/bash
# Split context-grounded-bible repository into 3 separate repositories
#
# This script creates:
# 1. context-grounded-bible (main) - Tools, scripts, docs (everything except bible/)
# 2. bible-data-lexicons - Static reference data (bible/words/)
# 3. bible-data-commentary - Generated commentary (bible/commentary/ + bible/commentaries/)
#
# Prerequisites:
#   - git-filter-repo installed: pip install git-filter-repo
#   - Clean working directory (no uncommitted changes)
#   - Backup of original repository recommended
#
# WARNING: This script rewrites git history. All contributors must re-clone.

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ORIGINAL_REPO="context-grounded-bible"
BACKUP_DIR="context-grounded-bible-backup-$(date +%Y%m%d-%H%M%S)"
SPLIT_DIR="split-repos"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Repository Split Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo -e "${RED}ERROR: git-filter-repo not found${NC}"
    echo "Install with: pip install git-filter-repo"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}ERROR: Not in a git repository${NC}"
    echo "Run this script from the root of context-grounded-bible repository"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}ERROR: You have uncommitted changes${NC}"
    echo "Please commit or stash your changes before running this script"
    git status
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"
echo ""

# Confirm action
echo -e "${YELLOW}This will:${NC}"
echo "  1. Create a backup of your current repository"
echo "  2. Split into 3 separate repositories preserving git history"
echo "  3. Repositories will be created in: ./${SPLIT_DIR}/"
echo ""
echo -e "${YELLOW}Current repository sizes:${NC}"
du -sh bible/words bible/commentaries bible/commentary 2>/dev/null || true
echo ""
echo -e "${RED}WARNING: This operation rewrites git history.${NC}"
echo -e "${RED}All team members will need to re-clone the new repositories.${NC}"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 1: Creating backup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get current directory
CURRENT_DIR=$(pwd)
PARENT_DIR=$(dirname "$CURRENT_DIR")

# Create backup
echo "Creating backup at: ${PARENT_DIR}/${BACKUP_DIR}"
cd "$PARENT_DIR"
cp -r "$ORIGINAL_REPO" "$BACKUP_DIR"
echo -e "${GREEN}✓ Backup created${NC}"
echo ""

# Create split directory
cd "$CURRENT_DIR"
mkdir -p "$SPLIT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 2: Creating bible-data-lexicons${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clone for lexicons repo
echo "Cloning repository for lexicons extraction..."
cd "$SPLIT_DIR"
git clone "$CURRENT_DIR" bible-data-lexicons
cd bible-data-lexicons

echo "Extracting bible/words/ subdirectory..."
git filter-repo --path bible/words/ --force

# Move bible/words/* to root
echo "Restructuring to root level..."
git filter-repo --path-rename bible/words/:words/ --force

echo -e "${GREEN}✓ bible-data-lexicons created (63MB)${NC}"
echo ""

cd "$CURRENT_DIR/$SPLIT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 3: Creating bible-data-commentary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clone for commentary repo
echo "Cloning repository for commentary extraction..."
git clone "$CURRENT_DIR" bible-data-commentary
cd bible-data-commentary

echo "Extracting bible/commentary/ and bible/commentaries/..."
git filter-repo \
    --path bible/commentary/ \
    --path bible/commentaries/ \
    --force

# Move bible/* to root
echo "Restructuring to root level..."
git filter-repo --path-rename bible/:/ --force

echo -e "${GREEN}✓ bible-data-commentary created (2.5GB)${NC}"
echo ""

cd "$CURRENT_DIR/$SPLIT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 4: Creating main repository${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clone for main repo (tools/scripts)
echo "Cloning repository for main repo..."
git clone "$CURRENT_DIR" context-grounded-bible-main
cd context-grounded-bible-main

echo "Removing bible/ directory from main repo..."
git filter-repo --path bible/ --invert-paths --force

echo -e "${GREEN}✓ context-grounded-bible-main created${NC}"
echo ""

cd "$CURRENT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${GREEN}✓ Repository split complete!${NC}"
echo ""
echo "New repositories created in: ${SPLIT_DIR}/"
echo ""
echo "1. ${SPLIT_DIR}/context-grounded-bible-main/"
echo "   - Tools, skills, scripts, documentation"
echo "   - Size: ~10MB"
echo ""
echo "2. ${SPLIT_DIR}/bible-data-lexicons/"
echo "   - Static reference data (Strong's dictionary)"
echo "   - Size: ~63MB"
echo "   - Structure: words/strongs/"
echo ""
echo "3. ${SPLIT_DIR}/bible-data-commentary/"
echo "   - Generated commentary data"
echo "   - Size: ~2.5GB"
echo "   - Structure: commentary/ and commentaries/"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Next Steps${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "1. Review each repository:"
echo "   cd ${SPLIT_DIR}/context-grounded-bible-main && git log --oneline"
echo "   cd ${SPLIT_DIR}/bible-data-lexicons && git log --oneline"
echo "   cd ${SPLIT_DIR}/bible-data-commentary && git log --oneline"
echo ""
echo "2. Create new GitHub repositories:"
echo "   - authenticwalk/context-grounded-bible (rename existing)"
echo "   - authenticwalk/bible-data-lexicons (new)"
echo "   - authenticwalk/bible-data-commentary (new)"
echo ""
echo "3. Push to new remotes:"
echo "   cd ${SPLIT_DIR}/context-grounded-bible-main"
echo "   git remote set-url origin https://github.com/authenticwalk/context-grounded-bible"
echo "   git push -f origin main"
echo ""
echo "   cd ${SPLIT_DIR}/bible-data-lexicons"
echo "   git remote add origin https://github.com/authenticwalk/bible-data-lexicons"
echo "   git push -u origin main"
echo ""
echo "   cd ${SPLIT_DIR}/bible-data-commentary"
echo "   git remote add origin https://github.com/authenticwalk/bible-data-commentary"
echo "   git push -u origin main"
echo ""
echo "4. Update documentation:"
echo "   - Update main repo README to reference data repos"
echo "   - Add data repo URLs to configuration files"
echo "   - Update CLAUDE.md with new structure"
echo ""
echo "5. Team notification:"
echo "   - Notify all contributors about the split"
echo "   - Everyone must re-clone repositories"
echo "   - Update CI/CD configurations"
echo ""

echo -e "${GREEN}Backup location: ${PARENT_DIR}/${BACKUP_DIR}${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
