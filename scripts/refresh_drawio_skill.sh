#!/usr/bin/env bash
# refresh_drawio_skill.sh — pull the latest drawio-skill backend adapter.
#
# Upstream: https://github.com/Agents365-ai/drawio-skill
# Default behaviour: refresh only the nested skills/drawio-skill/SKILL.md.
# Pass --bundle to overlay the entire repository without deleting local files.
#
# Usage:
#   bash .agents/skills/sci-figure/scripts/refresh_drawio_skill.sh [--bundle]

set -euo pipefail

REPO="Agents365-ai/drawio-skill"
TARGET_DIR=".agents/skills/drawio-skill"
NESTED_SKILL="skills/drawio-skill/SKILL.md"
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
  COMMIT="$(git -C "$TMP/drawio-skill" rev-parse --short HEAD)"
  echo "[refresh] overlay new files into $TARGET_DIR (excluding .git; no delete)"
  rsync -a --exclude=.git "$TMP/drawio-skill/" "$TARGET_DIR/"
  rm -rf "$TMP"
  echo "[refresh] upstream commit $COMMIT"
else
  echo "[refresh] fetching latest nested $NESTED_SKILL only"
  mkdir -p "$(dirname "$TARGET_DIR/$NESTED_SKILL")"
  curl -fsSL "$RAW_BASE/$NESTED_SKILL" -o "$TARGET_DIR/$NESTED_SKILL.new"
  if diff -q "$TARGET_DIR/$NESTED_SKILL.new" "$TARGET_DIR/$NESTED_SKILL" >/dev/null 2>&1; then
    echo "[refresh] SKILL.md already up to date"
    rm "$TARGET_DIR/$NESTED_SKILL.new"
  else
    mv "$TARGET_DIR/$NESTED_SKILL.new" "$TARGET_DIR/$NESTED_SKILL"
    echo "[refresh] SKILL.md updated"
  fi
fi

# Show the version stamp from the YAML metadata for confirmation.
grep -E '^version:' "$TARGET_DIR/$NESTED_SKILL" | head -1 || true
grep -oE '"version":"[^"]+"' "$TARGET_DIR/$NESTED_SKILL" | head -1 || true
