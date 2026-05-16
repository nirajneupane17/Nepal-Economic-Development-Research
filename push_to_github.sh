#!/bin/bash
# ============================================================
#  Nepal Economic Development Research — Git Push Script
#  Run this from inside the unzipped repo folder
# ============================================================

set -e   # stop on any error

REPO_URL="https://github.com/nirajneupane17/Nepal-Economic-Development-Research.git"
BRANCH="main"

echo "============================================================"
echo "  Nepal Economic Development Research — GitHub Push"
echo "============================================================"
echo ""
echo "Repo : $REPO_URL"
echo "Branch: $BRANCH"
echo ""

# ── Check git is installed ──────────────────────────────────
if ! command -v git &> /dev/null; then
    echo "✗ git is not installed."
    echo "  Install: https://git-scm.com/downloads"
    exit 1
fi

# ── Option A: Clone existing repo and copy files into it ────
echo "Choose an option:"
echo "  [1] Push INTO existing repo (recommended)"
echo "  [2] Create fresh local repo and push"
echo ""
read -p "Enter 1 or 2: " CHOICE

if [ "$CHOICE" = "1" ]; then
    # Clone existing repo
    echo ""
    echo "Cloning existing repo..."
    TMPDIR=$(mktemp -d)
    git clone "$REPO_URL" "$TMPDIR/repo"

    echo "Copying new files..."
    # Copy everything from current directory into cloned repo
    # (excluding .git folder)
    rsync -av --exclude='.git' --exclude='push_to_github.sh' \
          ./ "$TMPDIR/repo/"

    cd "$TMPDIR/repo"

    git config user.name  "Niraj Neupane"
    git config user.email "nirajneupane17@gmail.com"

    git add .

    # Check if there's anything to commit
    if git diff --cached --quiet; then
        echo ""
        echo "Nothing new to commit — all files already up to date."
    else
        git commit -m "Add District 01 Bhojpur — full economic development framework

- README with national macro context (GDP, remittances, electricity, debt)
- Macro: development indicators across political regimes (1960-2026)
- Policy recommendations 2026 (governance, jobs, energy, agriculture)
- District 01 Bhojpur: income sources, infrastructure gaps, 7 interventions,
  market opportunities (chili, khukuri, cardamom, tourism), 1600-2900 jobs,
  7 financing sources (ADB, federal grants, SJVN LAD, NIFRA, 3% loans)
- Animated GIFs: English + Nepali (6 slides, Pango-rendered Devanagari)
- Master dataset: 77 districts + 165 constituencies
- Data sources: World Bank NDU Apr 2026, MoF Apr 2026, CBS Nepal 2021"

        echo ""
        echo "Pushing to GitHub..."
        git push origin "$BRANCH"
        echo ""
        echo "✓ Done! View at: https://github.com/nirajneupane17/Nepal-Economic-Development-Research"
    fi

    # Cleanup
    rm -rf "$TMPDIR"

elif [ "$CHOICE" = "2" ]; then
    # Init fresh repo here
    echo ""
    git init
    git config user.name  "Niraj Neupane"
    git config user.email "nirajneupane17@gmail.com"
    git branch -m main

    git remote add origin "$REPO_URL" 2>/dev/null || \
        git remote set-url origin "$REPO_URL"

    git add .
    git commit -m "Initial commit: Nepal Economic Development Research

District 01 Bhojpur — complete economic development profile
Sources: World Bank NDU Apr 2026, MoF Apr 2026, CBS Nepal Census 2021"

    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main --force
    echo ""
    echo "✓ Done! View at: https://github.com/nirajneupane17/Nepal-Economic-Development-Research"

else
    echo "Invalid choice. Exiting."
    exit 1
fi
