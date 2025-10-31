#!/bin/bash
# Setup minimal bible data for tool testing and development
#
# This script clones only the essential data needed for bible tool development:
# - Test verses (Matthew 5, John 3, Genesis 1, Mark)
# - Strong's dictionary entries
# - Minimal footprint for fast development
#
# Reduces data clone from 2.6GB to ~100MB

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Minimal Bible Data Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

DATA_DIR="data"
DATA_REPO="https://github.com/authenticwalk/mybibletoolbox-data"

# Check if data directory already exists
if [ -d "$DATA_DIR" ]; then
    echo -e "${YELLOW}Data directory already exists at: $DATA_DIR${NC}"
    read -p "Do you want to remove it and start fresh? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        rm -rf "$DATA_DIR"
        echo "  Removed existing data directory"
    else
        echo "  Keeping existing data directory"
        exit 0
    fi
fi

echo -e "${GREEN}Cloning mybibletoolbox-data with sparse checkout...${NC}"
echo ""

# Clone with blobless filter for faster checkout
git clone --filter=blob:none --sparse "$DATA_REPO" "$DATA_DIR"

cd "$DATA_DIR"

echo ""
echo -e "${GREEN}Setting up minimal sparse checkout...${NC}"
echo ""

# Initialize sparse checkout with test verse data
# These are the verses commonly used for tool testing and development
git sparse-checkout set \
    bible/words/strongs \
    bible/commentary/MAT/5 \
    bible/commentary/JHN/3 \
    bible/commentary/GEN/1 \
    bible/commentaries

echo ""
echo -e "${GREEN}✓ Minimal bible data setup complete!${NC}"
echo ""
echo -e "${BLUE}What was installed:${NC}"
echo "  - Strong's dictionary (14,197 entries)"
echo "  - Matthew 5 commentary (Beatitudes)"
echo "  - John 3 commentary (includes 3:16)"
echo "  - Genesis 1 commentary"
echo "  - Commentary tools metadata"
echo ""
echo -e "${YELLOW}To add more books later:${NC}"
echo "  cd data"
echo "  git sparse-checkout add bible/commentary/MRK"
echo "  git sparse-checkout add bible/commentary/ROM"
echo ""
echo -e "${BLUE}========================================${NC}"
