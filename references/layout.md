# Layout — patterns, not rules

This document is a **menu**. Pick the pattern that fits the paper's
conceptual structure; do not force a paper into a pattern that
doesn't match its logic. Mix patterns when useful (e.g. a 3-column
phase outer with a side-by-side comparative inner panel).

## Read the paper first, then choose a pattern

Different conceptual structures suggest different patterns:

| Paper's logical shape | Layout pattern that often fits |
|---|---|
| Multi-step mechanism (input → transform → output) | 3-column phase, or single-row narrative with arrows |
| Comparative method vs baseline | Side-by-side, 2 vertical halves |
| Geometric / spatial story (manifold, embedding, decision boundary) | Centred large geometric panel + small annotation strips |
| Distributional claim (before / after) | Horizontal strip of paired distributions |
| Data flow with branching | T-shape with side outputs / inputs |
| Single continuous illustration (no natural panels) | One large panel, no sub-panels at all |
| Iterative / rollout (time evolution) | Horizontal time-axis with snapshots |
| Hierarchical / multi-scale | Vertical stack with nested boxes |
| **Training vs inference (shared learned object)** | **Two horizontal rows with shared element drawn identically in both; mid-figure colour legend doubles as row separator. See `exemplars/two-row-training-inference.md`.** |
| **Failure mechanism vs controlled fix** | **Two horizontal rows: a grouped failure loop above, then setup → iterative core → final readout below. See `exemplars/two-row-failure-fix-iterative-readout.md`.** |

The list is not exhaustive. Invent a layout when none of these fits.

## Sub-panels — `[A][B][C]` is one convention

The titled `[A]` / `[B]` / … sub-panel container (NeurIPS Fig. 1 norm
in many recent papers) is **one** convention. It works when:
- the figure has 3 + visually distinct elements that share an
  internal story;
- those elements deserve to be addressable by reference text.

It does **not** fit:
- single-panel figures;
- figures whose panels flow continuously and tagging them would
  visually fragment the flow;
- figures where the panel order is not the right reading order
  (rare; usually means the layout itself needs redesign).

`DrawioBuilder.sub_panel(x, y, w, h, tag, title)` is provided when
you want this convention — it returns the inner content rect.
`DrawioBuilder.cell(...)` plus your own bounding rounded-rect works
just as well when you want a different container style.

## Page geometry — pick from the paper's aspect

A wide-and-short main figure (~ 2.5 : 1) suits multi-step mechanism
papers. A taller canvas (~ 1 : 1) suits geometric / spatial papers.
A very wide strip (~ 4 : 1) suits time-evolution figures.

There is no default page size in the lib. The per-figure
`generate_figure.py` sets `page_w` and `page_h` on the
`DrawioBuilder` based on the figure's needs.

A common starting point for the multi-phase pattern is
~ 3400 × 1340 px (used by the EHCA-RPU reference). Treat as one
sample, not a default.

## Arrow corridors

Whatever pattern you pick, **reserve gutters between elements that
arrows route through**. ≥ 16 px is a common floor; pick more for
dense mechanism panels with many edges.

If an arrow has to cross an unrelated element to reach its target,
either the gutter is too narrow or the layout itself is wrong —
restructure rather than letting the arrow cross.

For iterative methods, do not let arrow grammar imply a one-pass
pipeline unless the method is actually one-pass. When two panels update
each other, wrap them as an iterative core or draw a clear return path.
Keep the final prediction / readout panel outside that core when it is
only valid after convergence.

## Square thumbnails

Class-identifier thumbnails, when used, must be square. The
`thumb_cell()` helper refuses non-square sources. Decoration
size ≥ 110 px on canvas; primary identifier ≥ 180 px. The class
label is always a separate drawio cell, never baked into the PNG.

## Aspect-ratio guard — firm

Every `image()` call passes at most one of `w` / `h`; the helper
derives the other. The build script terminates with
`verify_aspect_ratios(xml_path)`, which decodes each embedded PNG
IHDR and aborts on drift > 0.5 %.

This catches the common mistake of typing both `w` and `h` and
accidentally squashing the PNG. Applies to every layout pattern.

## Header / label sizing — firm

Every header / axis label / legend label measures ≥ 1.5 % of
`min(canvas_dim)` after final scaling. Below that, text becomes
unreadable in a printed reviewer copy. See `references/typography.md`.

## Legend — when used, keep it thin

If the figure has a colour legend, prefer a thin horizontal strip
between the title and the panels with ≤ 6 colour-coded bullets, not
a 2 × N notation grid. Bullet labels ≥ 22 pt.

Many figures don't need a legend at all — every concept is introduced
inline by a colour tag on its panel. That's often cleaner.
