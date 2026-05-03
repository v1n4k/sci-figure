#!/usr/bin/env bash
# bootstrap_env.sh — set up a project's .venv with the sci-figure stack.
#
# Behaviour:
# - Ready-check first: if the existing .venv can already import every
#   required package, print "ready" and exit 0. No reinstall, no churn.
# - Otherwise: detect uv first (≈10× faster install); fall back to
#   ``python -m venv`` + pip if uv is missing.
# - Installs ``requirements.txt`` and the ``sci-figure-lib`` package
#   **non-editable** by default (avoids a known issue where some uv-
#   managed Pythons skip ``__editable__*.pth`` files as hidden).
#
# To develop the skill's lib in-place after bootstrap, install editable
# manually:
#   .venv/bin/python -m pip install -e .agents/skills/sci-figure/lib
#
# Usage:
#   bash .agents/skills/sci-figure/scripts/bootstrap_env.sh [project_root]
# Default project_root = $PWD.

set -euo pipefail

PROJECT_ROOT="${1:-$(pwd)}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REQS="$SKILL_DIR/requirements.txt"
LIB="$SKILL_DIR/lib"
VENV="$PROJECT_ROOT/.venv"

cd "$PROJECT_ROOT"

# ---------- 1. Ready-check ----------
# Cheap one-liner: if every required module imports, the env is good.
ready_check() {
  [[ -x "$VENV/bin/python" ]] || return 1
  "$VENV/bin/python" - <<'PY' 2>/dev/null
import sys
try:
    import sci_figure_lib  # noqa: F401
    import matplotlib, numpy, PIL  # noqa: F401
    import scipy, sklearn, seaborn  # noqa: F401
except Exception:
    sys.exit(1)
PY
}

if ready_check; then
  echo "[bootstrap] .venv already has every required module — skipping install."
  echo "[bootstrap] activate with: source .venv/bin/activate"
  exit 0
fi

echo "[bootstrap] environment not ready; installing…"

# ---------- 2. Create venv if missing, install deps + lib ----------
if command -v uv >/dev/null 2>&1; then
  echo "[bootstrap] using uv"
  if [[ ! -d "$VENV" ]]; then
    uv venv
  fi
  uv pip install -r "$REQS"
  uv pip install "$LIB"             # non-editable: copies into site-packages
else
  echo "[bootstrap] uv not found; falling back to python -m venv + pip"
  if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
  fi
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
  pip install --quiet --upgrade pip
  pip install --quiet -r "$REQS"
  pip install --quiet "$LIB"
fi

echo "[bootstrap] done. activate with: source .venv/bin/activate"
echo "[bootstrap] sci-figure-lib installed (non-editable) from $LIB"
echo "[bootstrap] to iterate on the lib in-place:"
echo "             .venv/bin/python -m pip install -e $LIB"
