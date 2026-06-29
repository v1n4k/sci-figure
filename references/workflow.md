# Workflow — 5 phases

## Phase 1 — Read & Understand

Before drawing anything:
- Read the manuscript carefully. Mark the **single novelty** the
  figure must communicate. If you can't state it in one sentence,
  you don't yet understand the paper well enough to design the figure.
- Characterise the paper's **conceptual structure**. Some examples:
  multi-step mechanism, comparative claim, geometric / spatial story,
  distributional change, hierarchical decomposition, time evolution,
  data-flow with branching. The figure's layout will be derived from
  this — not picked from a template.
- List every notation symbol the figure must introduce.
- Decide what is **asset territory** (data geometry, distributions,
  feature spaces, density / score landscapes — anything matplotlib /
  sklearn / scipy / seaborn can produce honestly) vs **drawio
  territory** (boxes, arrows, glyphs, captions, math notation, the
  reading order between elements).
- Start `scripts/<figure>/requirements.md` as soon as the figure name
  exists. Treat it as the decision log for palette semantics, arrow
  meanings, asset/drawio territory, stacked quantities, final readout
  semantics, and handoff status.

## Phase 2 — Design (explore, then human selects)

Treat the conventions in `layout.md` as a **menu**. Different papers
want different shapes.

This phase is **explicitly human-in-the-loop**. The agent's job is to
**generate** several layout candidates and **present** them; the
human's job is to **select** which to develop. The agent does not
pick the winner — design taste belongs to the person who knows the
paper, the audience, and the venue.

### Step A. Agent generates ≥ 3 layout candidates

Each candidate is a *rough* design sketch (text + ASCII layout, not
implementation), informed by the paper's conceptual structure from
Phase 1. Spread the candidates across genuinely different patterns
from `layout.md` — three near-identical 3-column phase variants does
not count as exploration.

For each candidate the agent works out internally:
- Conceptual structure (mechanism / comparison / geometry / …)
- Rough sub-element bounding boxes + arrow corridors
- Where the visual focal point lands (must align with the novelty —
  see `quality-bar.md` invariant 6)
- Per-panel 5-second skim verdict
- What asset combinations it needs (`asset-strategy.md`)
- What the candidate trades off (e.g. "scales for complex methods
  but feels busy", "clean for single-thread stories but bad for
  branching")

### Step B. Agent presents candidates to the human

Use the format below. Keep each candidate to ~6 lines so the human
can compare them at a glance. Include the trade-offs honestly — the
agent's job is to surface the real choices, not to advocate.

```
Candidate A — <pattern name>
  Structure  : <one line>
  Layout     : <ASCII sketch or 2-line description>
  Focal pt   : <which element; why it aligns with the novelty>
  Strengths  : <what this lands well>
  Trade-offs : <what this gives up>

Candidate B — <pattern name>
  …

Candidate C — <pattern name>
  …
```

Then ask: *"Pick A / B / C, request a hybrid (e.g. 'A's outer + B's
[F]'), or describe what's still missing and I'll regenerate."*

### Step C. Human selects (or rejects all and asks for another round)

The human chooses. Common responses:
- "B" → proceed with B as-is
- "B but with C's geometric centerpiece" → produce a hybrid
- "None of these — the focal point should be X, try again with that
  constraint" → regenerate with the new constraint
- "B, but try one more variant where Phase 2 is simpler" → keep B,
  refine

The agent does **not** push back on the choice; it implements.

### Step D. Agent commits the chosen design

Lock in:
- the rough sub-element bounding boxes (with arrow corridors);
- the equation budget (default = 0 displayed equations);
- notation rendering: `tex_cell()` (drawio MathJax — default; renders
  in both app view and CLI PNG export) or `math_cell()` (HTML +
  Unicode escape hatch). See `notation.md` for delimiter rules.
- a short per-figure requirements checklist. This should capture
  decisions that are easy to lose during refinement: palette semantics,
  what each arrow means, which quantities are evidence vs posterior vs
  final readout, what should be stacked, and which glyphs are assets
  rather than drawio containers.
- whether the method should be shown as a one-pass pipeline, an
  iterative core, or a converged final readout. Do not leave this for
  implementation to infer from arrows.

Move to Phase 3 (implement).

The only firm layout rules across every candidate:
aspect-ratio guard on every embedded image, asset typography floor,
header / label size ≥ 1.5 % of `min(canvas_dim)`. Everything else is
the human's to compose.

## Phase 3 — Implement

Two scripts, both in `scripts/<figure>/`, both standalone:

### `generate_assets.py`
- Imports matplotlib + scipy + sklearn + seaborn as needed.
- **No drawio import.**
- Reads no PNGs from `assets/<figure>/` — it writes them.
- Each helper renders one PNG at 300 dpi.
- **Every random source is seeded.** Asset helpers that draw synthetic
  clusters / scatter samples / random offsets must take a seed
  (`np.random.default_rng(seed)`) and store it as a named module-level
  constant (`SEED_FEATURE_SPACE = 11`, `SEED_FAN_LAYER3 = 7`, …) so
  every rebuild reproduces the same geometry. Without this, "the
  figure I sent reviewer 3 weeks ago" no longer reproduces, and asset
  re-renders silently change the published artefact.

### `generate_figure.py`
- Imports `sci_figure_lib` only.
- **No matplotlib import.**
- Reads PNGs from `assets/<figure>/`; if none exist, exits with a
  message telling the user to run `generate_assets.py` first.
- Uses semantic layout helpers (`Rect`, `panel_box`, `wrapper_box`,
  `block_arrow`, distribution/readout glyphs) so the script reads like
  a figure plan rather than raw XML coordinates.
- Builds the `.drawio`, runs `verify_aspect_ratios`, then either:
  `SCI_FIGURE_SKIP_EXPORT=1 make xml` for structure-only validation, or
  `make figure` for CLI export + bounded review PNG.

The two scripts share no in-process state. Re-running either alone
exercises one stage of the pipeline.

## Phase 4 — Audit / Review

Open `artifacts/<figure>.drawio` in the drawio app, or open
`artifacts/<figure>_review.png` in Preview. Both render math
notation correctly when `tex_cell()` was used (the `\(...\)`
delimiter wrapping is what makes the CLI export render math too).

For each sub-panel, in 5 seconds, answer:
1. What is the single visual message?
2. Is any cell overlapping an adjacent cell?
3. Does any arrow cross an unrelated cell?
4. Are there blank dead regions an asset should fill, or should the
   panel itself shrink?
5. Are sub-panel header / axis / legend labels readable at 25 % zoom?

Then run the **reverse 5-second test on the whole figure**: glance
at the full review PNG for 5 seconds, then look away. What did you
remember? If you remembered the prettiest asset rather than the
paper's contribution, the focal point is wrong (see invariant 6 in
`quality-bar.md`); the supporting infrastructure is shouting louder
than the novelty. Restructure visual weight (size, contrast,
saturation, border weight, central position) until the focal point
IS the contribution.

Common regressions to look for:
- **Overlap** — neighbour cards / glyphs whose bounding boxes touch.
- **Blank dead space** — large empty interiors that should hold an
  asset or be removed.
- **Arrow tangle** — edges that cross other cells because no corridor
  was reserved.
- **Asset chrome** — axis ticks / titles baked into a PNG when a
  drawio TeX cell would be cleaner.

Semantic regressions to look for during later refinement:
- **Palette drift** — a colour starts meaning two unrelated concepts,
  or one concept is split across unrelated colours.
- **Arrow drift** — a convenience arrow implies causality, one-pass
  production, or availability before convergence.
- **Stacking drift** — stacked-card effects are applied to quantities
  that are not actually multi-instance.
- **Distribution drift** — evidence summaries, iterative posteriors,
  and final readouts are drawn with similar bars but not labelled at
  their correct semantic level.
- **Over-assetization** — PNG assets contain frames, titles, notation,
  or callouts that should remain editable drawio cells.

For agent review, use the **bounded review PNG**
(`<figure>_review.png`, ≤ 1500 px) — see `review-render.md`. The
full-resolution `<figure>.drawio.png` is for human inspection at 100 %.

## Phase 5 — Refine

- **drawio cells = tweakable post-hoc** — move, recolour, resize by
  hand in the drawio app, or by re-running `generate_figure.py` before
  final handoff.
- **Handoff boundary is explicit** — once the user starts hand-tuning
  the `.drawio`, record that state in `requirements.md`. Do not blindly
  regenerate and overwrite hand-tuned arrows, spacing, or labels. If a
  scripted change is still needed, fold the human edits back into
  `generate_figure.py` first or clearly agree that the hand-tuned state
  will be replaced.
- **PNG assets = locked images** — they cannot be edited after the
  fact. Therefore every asset must hit publication quality on the
  first render: cluster ellipsoids, white-haloed prototype markers,
  round-cap stroked lines, ≥ 24 pt tick labels, ≥ 28 pt axis labels,
  no spurious axis chrome. See `typography.md`.
- If an asset still feels rough at 100 % zoom in Preview,
  re-render it. Asset re-renders are cheap; a rough PNG embedded at
  conference scale is not.

## Pre-export QA Checklist

Run before showing a figure as "done":

- `verify_aspect_ratios(<drawio>)` exits 0
- `make xml` succeeds before any slower CLI export attempt
- Equation count in the figure body matches budget (default 0)
- No HTML `<sub>` / `<sup>` leaked into a Path-A figure (grep the
  `.drawio` source — those should be `$..._x$` instead)
- Every sub-panel header, axis label, and legend label measures
  ≥ 1.5 % of `min(canvas_dim)` after final scaling
- Sub-panel count is deliberate (3–6 per dense phase, 1–3 per simple
  phase)
- The bounded review PNG (≤ 1500 px) is legible at 25 % zoom
- 5-second skim test passes for each panel independently
- After `cli_export`, no orphan drawio Electron processes:
  `pgrep -f "draw.io.app" | wc -l` returns 0

If any of these fail, fix before proceeding.
