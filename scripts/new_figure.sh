#!/usr/bin/env bash
# new_figure.sh — scaffold a new figure project layout.
#
# Copies only the per-figure stubs (generate_assets.py, generate_figure.py,
# Makefile, requirements.md) into scripts/<name>/. The DrawioBuilder, glyphs, render
# helpers, and matplotlib styling primitives stay in the skill's lib/
# and are imported via the editable install — no copy-and-customise of
# the lib here.
#
# Usage:
#   bash .agents/skills/sci-figure/scripts/new_figure.sh <figure_name>

set -euo pipefail

NAME="${1:?usage: new_figure.sh <figure_name>}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="$(pwd)"

# Validate name (no slashes, no shell metacharacters)
if [[ ! "$NAME" =~ ^[A-Za-z0-9_-]+$ ]]; then
  echo "[new_figure] error: name must match [A-Za-z0-9_-]+, got: $NAME" >&2
  exit 1
fi

mkdir -p "scripts/$NAME" "assets/$NAME" "artifacts"

for f in generate_assets.py generate_figure.py Makefile requirements.md; do
  src="$SKILL_DIR/templates/${f}.tmpl"
  dst="scripts/$NAME/$f"
  if [[ ! -f "$src" ]]; then
    echo "[new_figure] error: missing template $src" >&2
    exit 1
  fi
  cp "$src" "$dst"
done

# Token replacement
sed -i.bak "s/__FIGURE_NAME__/$NAME/g" "scripts/$NAME"/*
rm "scripts/$NAME"/*.bak

echo "[new_figure] scaffolded scripts/$NAME/{generate_assets.py,generate_figure.py,Makefile,requirements.md}"
echo "[new_figure] iterate with:"
echo "    cd scripts/$NAME && make assets && make xml"
