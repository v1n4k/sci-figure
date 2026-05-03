#!/usr/bin/env bash
# refresh_drawio_skill.sh — pull the latest drawio-skill SKILL.md from upstream.
#
# Upstream: https://github.com/Agents365-ai/drawio-skill
# Default behaviour: refresh only SKILL.md (the most likely-to-change file).
# Pass --bundle to re-download the entire skill via git clone.
#
# Usage:
#   bash .agents/skills/sci-figure/scripts/refresh_drawio_skill.sh [--bundle]

set -euo pipefail

REPO="Agents365-ai/drawio-skill"
TARGET_DIR=".agents/skills/drawio-skill"
RAW_BASE="https://raw.githubusercontent.com/$REPO/main"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "[refresh] target dir $TARGET_DIR not found" >&2
  exit 1
fi

mode="${1:-skill-md}"

if [[ "$mode" == "--bundle" ]]; then
  echo "[refresh] cloning entire bundle from $REPO into a temp dir"
  TMP="$(mktemp -d)"
  git clone --depth 1 "https://github.com/$REPO.git" "$TMP/drawio-skill"
  echo "[refresh] sync new files into $TARGET_DIR (excluding .git)"
  rsync -a --delete --exclude=.git "$TMP/drawio-skill/" "$TARGET_DIR/"
  rm -rf "$TMP"
else
  echo "[refresh] fetching latest SKILL.md only"
  curl -fsSL "$RAW_BASE/SKILL.md" -o "$TARGET_DIR/SKILL.md.new"
  if diff -q "$TARGET_DIR/SKILL.md.new" "$TARGET_DIR/SKILL.md" >/dev/null 2>&1; then
    echo "[refresh] SKILL.md already up to date"
    rm "$TARGET_DIR/SKILL.md.new"
  else
    mv "$TARGET_DIR/SKILL.md.new" "$TARGET_DIR/SKILL.md"
    echo "[refresh] SKILL.md updated"
  fi
fi

# Show the version stamp from the YAML metadata for confirmation.
grep -oE '"version":"[^"]+"' "$TARGET_DIR/SKILL.md" | head -1 || true
