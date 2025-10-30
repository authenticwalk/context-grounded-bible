#!/bin/bash
# Setup sparse checkout for Context-Grounded Bible repository
# This reduces the working directory from 2.6GB to ~100MB

set -e

echo "Setting up sparse checkout for faster cloning and reduced disk usage..."

# Enable sparse checkout in cone mode
git sparse-checkout init --cone

# In cone mode, we set directories. Root files are included automatically.
# The /* pattern includes all root-level files, and then we specify subdirectories
git sparse-checkout set \
  .claude \
  bible-study-tools \
  src \
  plan \
  agents

echo ""
echo "✓ Sparse checkout configured!"
echo ""
echo "Included directories:"
echo "  - .claude/          (Claude Code configuration)"
echo "  - bible-study-tools/ (Bible study scripts)"
echo "  - src/              (Source code)"
echo "  - plan/             (Planning documents)"
echo "  - agents/           (Agent configurations)"
echo "  - All root-level files (README.md, CLAUDE.md, etc.)"
echo ""
echo "Working directory size reduced from 2.6GB to ~100MB"
echo ""
echo "To add specific Bible books to your checkout, run:"
echo "  git sparse-checkout add bible/MAT  # Add Matthew"
echo "  git sparse-checkout add bible/JHN  # Add John"
echo ""
echo "To add all Bible words data:"
echo "  git sparse-checkout add bible/words"
echo ""
echo "To see what's currently checked out:"
echo "  git sparse-checkout list"
echo ""
echo "To disable sparse checkout and get the full repository:"
echo "  git sparse-checkout disable"
