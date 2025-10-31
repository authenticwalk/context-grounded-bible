#!/bin/bash
# Split context-grounded-bible repository into 3 separate repositories
#
# This script creates:
# 1. mybibletoolbox-code - Tools, scripts, docs (everything except bible/)
# 2. mybibletoolbox-lexicon - Static reference data (bible/words/)
# 3. mybibletoolbox-commentary - Generated commentary (bible/commentary/ + bible/commentaries/)
#
# Prerequisites:
#   - git-filter-repo installed: pip install git-filter-repo
#   - Clean working directory (no uncommitted changes)
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
SPLIT_DIR="split-repos"
REPO_CODE_URL="https://github.com/authenticwalk/mybibletoolbox-code"
REPO_LEXICON_URL="https://github.com/authenticwalk/mybibletoolbox-lexicon"
REPO_COMMENTARY_URL="https://github.com/authenticwalk/mybibletoolbox-commentary"

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
echo "  1. Split into 3 separate repositories preserving git history"
echo "  2. Repositories will be created in: ./${SPLIT_DIR}/"
echo "  3. Push to GitHub:"
echo "     - ${REPO_CODE_URL}"
echo "     - ${REPO_LEXICON_URL}"
echo "     - ${REPO_COMMENTARY_URL}"
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
# Get current directory and create split directory
CURRENT_DIR=$(pwd)
mkdir -p "$SPLIT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 1: Creating mybibletoolbox-lexicon${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clone for lexicons repo
echo "Cloning repository for lexicons extraction..."
cd "$SPLIT_DIR"
git clone "$CURRENT_DIR" mybibletoolbox-lexicon
cd mybibletoolbox-lexicon

echo "Extracting bible/words/ subdirectory..."
git filter-repo --path bible/words/ --force

# Move bible/words/* to root
echo "Restructuring to root level..."
git filter-repo --path-rename bible/words/:words/ --force

echo -e "${GREEN}✓ mybibletoolbox-lexicon created (63MB)${NC}"
echo ""

cd "$CURRENT_DIR/$SPLIT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 2: Creating mybibletoolbox-commentary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clone for commentary repo
echo "Cloning repository for commentary extraction..."
git clone "$CURRENT_DIR" mybibletoolbox-commentary
cd mybibletoolbox-commentary

echo "Extracting bible/commentary/ and bible/commentaries/..."
git filter-repo \
    --path bible/commentary/ \
    --path bible/commentaries/ \
    --force

# Move bible/* to root
echo "Restructuring to root level..."
git filter-repo --path-rename bible/:/ --force

echo -e "${GREEN}✓ mybibletoolbox-commentary created (2.5GB)${NC}"
echo ""

cd "$CURRENT_DIR/$SPLIT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 3: Creating mybibletoolbox-code${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clone for main repo (tools/scripts)
echo "Cloning repository for main repo..."
git clone "$CURRENT_DIR" mybibletoolbox-code
cd mybibletoolbox-code

echo "Removing bible/ directory from code repo..."
git filter-repo --path bible/ --invert-paths --force

echo -e "${GREEN}✓ mybibletoolbox-code created${NC}"
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
echo "1. ${SPLIT_DIR}/mybibletoolbox-code/"
echo "   - Tools, skills, scripts, documentation"
echo "   - Size: ~10MB"
echo ""
echo "2. ${SPLIT_DIR}/mybibletoolbox-lexicon/"
echo "   - Static reference data (Strong's dictionary)"
echo "   - Size: ~63MB"
echo "   - Structure: words/strongs/"
echo ""
echo "3. ${SPLIT_DIR}/mybibletoolbox-commentary/"
echo "   - Generated commentary data"
echo "   - Size: ~2.5GB"
echo "   - Structure: commentary/ and commentaries/"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Next Steps${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "1. Review each repository:"
echo "   cd ${SPLIT_DIR}/mybibletoolbox-code && git log --oneline"
echo "   cd ${SPLIT_DIR}/mybibletoolbox-lexicon && git log --oneline"
echo "   cd ${SPLIT_DIR}/mybibletoolbox-commentary && git log --oneline"
echo ""
echo "2. Push to GitHub repositories:"
echo "   cd ${SPLIT_DIR}/mybibletoolbox-code"
echo "   git remote add origin ${REPO_CODE_URL}"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "   cd ../mybibletoolbox-lexicon"
echo "   git remote add origin ${REPO_LEXICON_URL}"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "   cd ../mybibletoolbox-commentary"
echo "   git remote add origin ${REPO_COMMENTARY_URL}"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Update documentation in code repo:"
echo "   - Update README to reference data repos"
echo "   - Add data repo URLs to configuration files"
echo "   - Update CLAUDE.md with new structure"
echo ""
echo "4. Team notification:"
echo "   - Notify all contributors about the split"
echo "   - Everyone must clone the new repositories"
echo "   - Update CI/CD configurations"
echo ""
echo -e "${BLUE}========================================${NC}"
