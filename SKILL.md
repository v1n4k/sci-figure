---
name: sci-figure
description: Use when producing or revising a single publication-quality main figure for an AI/ML manuscript at NeurIPS / ICML / ICLR quality — typically the method / pipeline / architecture overview, but any single figure the user wants designed. Triggers on "make a figure", "method diagram", "pipeline figure", "main figure", "architecture diagram", "drawio figure for the paper". One invocation = one figure. If the user wants help with a secondary / auxiliary figure they will say so explicitly. Skip for slide decks, schematic sketches, or non-paper diagrams.
---

# sci-figure — semantic conference-figure workflow

## Goal

**One single figure** — typically the main method / pipeline / concept
overview the user is currently designing — that explains the
manuscript's *idea*, not its derivations, and is parseable in
**5 seconds per panel**.

The authoring interface is semantic: requirements, layout patterns,
asset boundaries, wrappers, glyphs, and readouts. The `.drawio` XML is
only the compiled editable target, not the design language.

If the user invokes this skill they want **one** figure designed in
this session. Don't try to plan or design secondary figures unless
the user explicitly asks.

## File / folder structure

One figure = one `<name>` triple:

```
scripts/<name>/{generate_assets,generate_figure}.py + Makefile
scripts/<name>/requirements.md
assets/<name>/*.png
artifacts/<name>.drawio + <name>_review.png
```

Don't mix multiple figures inside one subdir; don't dump shared
helpers into `scripts/<name>/` (they belong in the skill's `lib/`);
don't keep stale debug PNGs in `assets/` or `artifacts/`. Full
folder-hygiene rules: `references/anti-patterns.md`.

## Deliverable

Two files per figure, no more:

- `artifacts/<figure>.drawio` — the editable source. The user opens
  this in the drawio desktop app for fine-tuning, takes screenshots,
  exports to whatever format they need downstream. **The skill does
  not produce paper-ready PDFs**; how the figure ends up in the
  manuscript is the user's choice and outside scope.
- `artifacts/<figure>_review.png` — one bounded raster (default
  longest-side 1500 px, hard bounds 800–1800 px enforced by
  `make_review_png`). For agent and human review of layout, palette,
  typography, and the 5-second skim test. Math notation renders
  correctly in this PNG (CLI export rasterizes drawio's MathJax for
  PNG / PDF — see `references/notation.md` for the delimiter rules).

Auxiliary PNG assets in `assets/<figure>/` are intermediate inputs
to the drawio file, not deliverables in their own right.

## Quick start

```bash
# Once per project
bash <SKILL>/scripts/bootstrap_env.sh
# This also clones .agents/skills/drawio-skill/ if the backend bundle is missing.

# Once per new figure (replace <name>)
bash <SKILL>/scripts/new_figure.sh <name>

# Iterate
cd scripts/<name>
make assets    # only when asset PNGs need re-rendering
make xml       # build .drawio only; no drawio CLI export
make figure    # only when drawio layout changes
make all       # both, then writes <name>_review.png for agent review
```

`<SKILL>` resolves to the skill's path on disk (typically
`.agents/skills/sci-figure/`).

### Known drawio export failure

If `make figure` or `make all` fails with drawio `SIGABRT`, empty
output, or other Electron startup symptoms inside a sandbox, run
`make xml` first. If the `.drawio` builds and `verify_aspect_ratios`
passes, treat the issue as an export-environment problem, not figure
corruption. Rerun export with escalation / outside the sandbox only
when a PNG review file is required.

## Workflow (5 phases)

1. **Read & understand** — read the manuscript carefully *before*
   drawing. Pull out the single novelty, the conceptual structure
   (mechanism, comparison, geometry, distribution, evolution, …),
   and every notation symbol the figure must introduce. The figure's
   layout will be **derived from this**, not picked from a template.
2. **Design — explore, then human selects.** Treat the conventions
   in `references/layout.md` as a *menu of patterns* and the entries
   in `references/exemplars/` as concrete top-conference figures
   demonstrating those patterns. This phase is **explicitly
   human-in-the-loop**: the agent generates ≥ 3 distinct layout
   candidates (different patterns from the menu, ideally each citing
   an exemplar with a similar conceptual structure), presents them
   in a comparable per-candidate spec with focal-point alignment +
   trade-offs, and asks the human to pick. The agent does **not**
   pick the winner — design taste belongs to whoever knows the
   paper, the audience, and the venue. The human picks one, asks
   for a hybrid, or asks for another round; the agent implements
   the chosen design. Format and example responses:
   `references/design.md`. The only fixed inputs are the invariants
   in *Quality bar* below; everything else (panel count, arrangement,
   sub-panels, palette, page geometry, glyph repertoire, asset
   combinations) the human chooses.
3. **Implement** — two independent scripts plus a requirements log:
   - `requirements.md` records palette semantics, arrow meanings,
     asset vs drawio territory, and handoff notes.
   - `generate_assets.py` produces PNGs in `assets/<figure>/`.
   - `generate_figure.py` reads those PNGs and compiles semantic
     layout helpers into the `.drawio`.
   They share no in-process state. Each can be re-run alone during
   audit / iteration.
4. **Audit / Review** — open `artifacts/<figure>.drawio` in the drawio
   app at 100 / 50 / 25 % zoom. Cover one panel at a time and verify
   the 5-second skim test for that panel. Use the bounded
   `<figure>_review.png` (≤ 1500 px) when an agent does the review.
5. **Refine** — drawio cells tweak by hand or via the script;
   PNG assets re-render only when the underlying data story changes.

## Quality bar — these are the only invariants

Everything below survives across every paper, every layout, every
asset combination. Anything *not* listed here (panel count,
arrangement, sub-panels, palette concepts, glyph types, page geometry,
library combinations) is a design choice you make from the paper.

- **Math stays subordinate to the picture.** Single-symbol labels and
  short one-line definitions are fine when they reduce text or anchor
  a visual element. Avoid derivation blocks, equation chains, and math
  whose main job is to be read rather than recognised.
- **Zero specific numeric values** anywhere. Bar height, line
  thickness, fill saturation, glyph length carry magnitude.
- **Zero derivation chains.** Collapse 3 + chained intermediates into
  a single visual flow that lands on one summary element.
- **Zero notation glossaries** or mechanics boxes (`softmax`,
  `normalize`, …). Show what an operator *produces*, not its name.
- **Fixed palette per figure with no colour reuse across concepts.**
  Pick the palette from the paper's ontology (the actual concepts the
  paper distinguishes); do not import a generic palette.
- **5-second skim test** passes per panel.
- **Demonstration over numeric calculation** — visual encoding always
  beats annotated numbers.

Details and rationale: `references/quality-bar.md`.

## Asset strategy

The two scripts are independent on purpose:

- `generate_assets.py` uses any combination of the installed plotting
  libraries (matplotlib, scipy, sklearn, seaborn — and any Tier 2 / 3
  the figure happens to need). No drawio imports. Writes PNGs to
  `assets/<figure>/`.
- `generate_figure.py` uses `sci_figure_lib` (DrawioBuilder + glyphs +
  render helpers). No matplotlib imports. Reads PNGs from
  `assets/<figure>/`, writes `.drawio` to `artifacts/`.

If you only changed the layout, run `make figure`; PNGs untouched.

**Compose libraries freely.** A single asset may pair `sklearn.make_blobs`
with `scipy.gaussian_kde` overlays and `seaborn.kdeplot` shading; another
asset might be pure `matplotlib` because that's all it needs. The
"data not layout" + "cheap at one-shot runtime" rules in
`references/asset-strategy.md` are constraints; the *combination*
within those constraints is open.

## Notation

Math can render via drawio's built-in MathJax in **both** the app view
and the CLI PNG / PDF export. Use `tex_cell()` whenever possible: it
wraps raw LaTeX with delimiters that have worked reliably in drawio
exports. If you hand-write math inside HTML cells, prefer `\(...\)`
for inline math or `$$...$$` for display math, then verify the review
PNG rather than assuming every MathJax delimiter behaves the same.

Use `tex_cell()` in `sci_figure_lib`; it wraps with the right
delimiter automatically. For HTML + Unicode (no MathJax dependency)
use `math_cell()`. Full guidance + symbol cheat sheet:
`references/notation.md`.

## Layout — patterns, not rules

`references/layout.md` is a **menu of patterns** (3-column phase, single-
row narrative, T-shape with side outputs, vertical stack, side-by-side
comparison, geometric / spatial, distributional / strip, …). Pick what
fits the paper's conceptual structure; don't force a 3-column phase
layout onto a paper that's a comparative study, or a sub-panel grid
onto a figure that's really a single continuous story.

The only **firm** layout rules:
- Aspect-ratio guard on every embedded image (`image()` helper enforces).
- Asset typography floor (`apply_pub_rcparams()` once at script top).
- Headers / labels measure ≥ 1.5 % of `min(canvas_dim)` after final
  scaling — see `references/typography.md`.

## Pre-export QA

Before showing a figure as done:

- `verify_aspect_ratios()` exits 0
- Math use is visually justified: no derivation chains, no equation
  walls, and any one-line definition sits next to the visual element it
  names.
- Rendered math was checked in the review PNG. If bare `$...$` appears
  in the produced `.drawio`, inspect the PNG and switch to `tex_cell()`
  or `\(...\)` if it renders literally. See `references/notation.md`.
- Every header / label measures ≥ 1.5 % of `min(canvas_dim)` after
  final scaling
- Forward 5-second skim per panel passes
- **Reverse 5-second skim on the whole figure** — what does the
  reviewer remember? Must be the contribution, not the prettiest
  asset (visual hierarchy / focal point — `references/quality-bar.md`)
- All asset random sources are seeded (`np.random.default_rng(...)`
  with named module-level constants) — figure reproduces deterministically
- The bounded `<figure>_review.png` is between 800 and 1800 px on
  longest side (`make_review_png` enforces this)
- After the build, no orphan drawio Electron processes:
  `pgrep -f "draw.io.app" | wc -l` returns 0

Full checklist: `references/workflow.md`.

## drawio-skill backend adapter

This skill **references** the sibling drawio-skill bundle at
`.agents/skills/drawio-skill/` as a backend knowledge adapter: CLI
resolution, export flags, MathJax/export quirks, shape search,
fallback URLs, and troubleshooting. Do not copy its general
box-and-arrow workflow into scientific figure design.

To refresh that backend adapter from upstream:

```bash
bash <SKILL>/scripts/refresh_drawio_skill.sh
```

The default refresh updates the nested `skills/drawio-skill/SKILL.md`.
Use `--bundle` to overlay the full upstream bundle without deleting
local files. During first deployment, `bootstrap_env.sh` clones the
bundle automatically when `.agents/skills/drawio-skill/` is missing.

## Anti-patterns

See `references/anti-patterns.md`.

## Repo-agnostic guarantee

The skill mentions no project-specific filename, no manuscript title,
no class names, no notation symbols beyond conventional Greek (α, β,
μ, …). Per-figure decisions live in `scripts/<figure>/` only.
