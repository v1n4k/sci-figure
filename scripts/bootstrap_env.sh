#!/usr/bin/env bash
# bootstrap_env.sh — set up a project's .venv with the sci-figure stack.
#
# Behaviour:
# - Best-effort installs the optional sibling
#   ``.agents/skills/drawio-skill/`` backend bundle. If missing, try to
#   clone it from upstream. Set ``SCI_FIGURE_REFRESH_DRAWIO=1`` to
#   overlay-refresh an existing bundle. Set
#   ``SCI_FIGURE_REQUIRE_DRAWIO_BACKEND=1`` to make backend setup
#   fail-fast instead of warning and continuing.
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
DRAWIO_REPO="https://github.com/Agents365-ai/drawio-skill.git"
DRAWIO_DIR="$PROJECT_ROOT/.agents/skills/drawio-skill"
DRAWIO_SKILL_MD="$DRAWIO_DIR/skills/drawio-skill/SKILL.md"
REQUIRE_DRAWIO_BACKEND="${SCI_FIGURE_REQUIRE_DRAWIO_BACKEND:-0}"

cd "$PROJECT_ROOT"

# ---------- 1. Backend adapter check ----------
drawio_backend_problem() {
  local message="$1"
  if [[ "$REQUIRE_DRAWIO_BACKEND" == "1" ]]; then
    echo "[bootstrap] error: $message" >&2
    exit 1
  fi
  echo "[bootstrap] warning: $message" >&2
  echo "[bootstrap] continuing without optional drawio-skill backend; figure XML generation still works." >&2
  return 0
}

ensure_drawio_backend() {
  if [[ -f "$DRAWIO_SKILL_MD" ]]; then
    echo "[bootstrap] drawio-skill backend present at $DRAWIO_DIR"
    if [[ "${SCI_FIGURE_REFRESH_DRAWIO:-0}" == "1" ]]; then
      echo "[bootstrap] SCI_FIGURE_REFRESH_DRAWIO=1 — refreshing drawio backend"
      if ! bash "$SKILL_DIR/scripts/refresh_drawio_skill.sh" --bundle; then
        drawio_backend_problem "failed to refresh optional drawio-skill backend."
      fi
    fi
    return 0
  fi

  if ! command -v git >/dev/null 2>&1; then
    drawio_backend_problem "drawio-skill backend missing and git is not installed; install git or clone $DRAWIO_REPO into $DRAWIO_DIR manually for export-troubleshooting references."
    return 0
  fi

  if [[ -e "$DRAWIO_DIR" ]]; then
    drawio_backend_problem "drawio backend directory exists but nested SKILL.md is missing at $DRAWIO_SKILL_MD; fix/remove the directory or run refresh manually for backend references."
    return 0
  fi

  echo "[bootstrap] drawio-skill backend missing; cloning $DRAWIO_REPO"
  mkdir -p "$(dirname "$DRAWIO_DIR")"
  if ! git clone --depth 1 "$DRAWIO_REPO" "$DRAWIO_DIR"; then
    drawio_backend_problem "failed to clone optional drawio-skill backend from $DRAWIO_REPO."
    return 0
  fi
  if [[ ! -f "$DRAWIO_SKILL_MD" ]]; then
    drawio_backend_problem "clone completed but nested drawio SKILL.md was not found at $DRAWIO_SKILL_MD."
    return 0
  fi
}

ensure_drawio_backend

# ---------- 2. Ready-check ----------
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

# ---------- 3. Create venv if missing, install deps + lib ----------
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
