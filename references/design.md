# Design — Explore Options Informed by the Paper

The hardest part of designing the paper's main figure is not drawing
— it's **deciding what shape the figure should take**, given the
paper's actual content. This document is permission and guidance to
explore.

## Principle

> The figure's layout is **derived from the paper's conceptual
> structure**, not picked from a template. Anything in this skill
> that looks like a "default" — 3-column phase layout, sub-panels
> `[A][B][C]`, specific palette concepts, specific glyphs, specific
> page geometry — is one option among many.

The strong defaults are in `quality-bar.md`. Everything else is yours,
and even those defaults can bend when the paper's visual argument
requires it.

## Read the paper deeply (before anything else)

If you skim the abstract and pick a layout, the figure will
communicate the abstract — not the actual contribution.

Specific things to extract before sketching:

1. **The single sentence of novelty.** Write it out. If it has more
   than ~ 25 words, you haven't compressed it yet. The figure must
   land that sentence visually.
2. **The conceptual structure.** Which of the following dominates,
   and which are secondary?
   - *Mechanism* — input transformed step-by-step into output.
   - *Comparison* — method A vs method B (or vs baseline).
   - *Geometry* — claims about a manifold, embedding, or decision
     boundary.
   - *Distribution* — claims about probability mass / density / shift.
   - *Hierarchy* — claims about multi-scale / multi-level structure.
   - *Time* — claims about evolution, training dynamics, rollouts.
   - *Data flow* — claims about how information moves through a
     system with branching / merging.
3. **The paper's ontology.** What are the *concepts* the paper
   distinguishes? "Retain / forget / target" is one ontology;
   "anchor / positive / negative" is another; "clean / noisy / score"
   is a third. The figure's palette comes from this list — no
   imported defaults.
4. **The notation that the figure must introduce.** Every symbol
   the figure shows needs to land somewhere a panel owns. Write the
   list out and assign each to a future panel as you sketch.

## Match the layout to the structure

Some heuristics (none mandatory):

| Conceptual structure | Layout patterns that often fit |
|---|---|
| Mechanism (input → … → output) | 3-column phase, single-row narrative with arrows |
| Comparison | Side-by-side, 2 vertical halves, before / after strip |
| Geometry | Centred large geometric panel + small annotation strips, or single panel |
| Distribution | Horizontal strip of paired distributions, density-stack |
| Hierarchy | Vertical stack with nested boxes |
| Time evolution | Horizontal time-axis with snapshots |
| Data flow with branches | T-shape, fork-and-join, side outputs |
| Pure illustration (no flow) | One continuous panel, no sub-panels |

Mix patterns when the paper warrants it. A multi-step mechanism with
a comparative inset is two patterns nested. A single-panel figure
with one annotated geometric story is sometimes the right answer.

## Sketch candidates, present them, let the human pick

Phase 2 is a **human-in-the-loop** step. The agent does not pick the
winner. For a new main figure or ambiguous redesign, the agent's job
is breadth (generate genuinely different candidates and surface their
trade-offs); the human's job is taste (decide which one fits the paper,
the audience, the venue). For a targeted revision to an already chosen
figure, breadth is usually waste: keep the current design and propose
the smallest coherent change unless the human asks to reopen layout
exploration.

### Generate ≥ 3 candidates for new or ambiguous designs

1. Pick three (or more) **different** layout patterns from the table
   above. Three near-identical 3-column variants is not exploration.
2. **Cross-reference `exemplars/`**: scan the entries there for
   figures whose conceptual structure resembles the paper at hand.
   When you propose a candidate, *cite* the exemplar that pattern
   came from — the reviewer (the human picking) can then anchor on
   a known-good figure rather than reasoning purely about your
   description.
3. For each candidate, write the rough composition: which patterns,
   how many panels, where the focal point lands, what trade-offs it
   makes, and which exemplar (if any) it draws from.
4. Self-audit each candidate against the invariants in
   `quality-bar.md`:
   - Does the focal point align with the novelty?
   - Does each panel pass the 5-second skim test?
   - Are arrow corridors clear?
   - Does the candidate need sub-panels at all?
   - Are the asset combinations (`asset-strategy.md`) feasible?

If a candidate fails an invariant in a way that can't be fixed
without changing the pattern, drop it and generate another.

For small revisions, skip this candidate-generation step. State the
local issue, the intended patch, and any trade-off it creates; then
implement after the human agrees or when the request is already
specific.

### Present to the human in a comparable format

Use a tight per-candidate spec — about six lines each — so the human
can compare side by side at a glance:

```
Candidate A — 3-column phase
  Structure  : input → mechanism → output
  Layout     : Phase1 (1 panel) | Phase2 (4 sub-panels) | Phase3 (1 panel)
  Focal pt   : the central mechanism panel [E] (β_x dial)
  Exemplar   : (no direct match in exemplars/; standard mechanism layout)
  Strengths  : matches sequential-method papers; clear reading order
  Trade-offs : feels busy when mechanism has > 4 sub-steps

Candidate B — Centered geometric
  Structure  : single large geometric panel + small annotation strips
  Layout     : one large square panel; 3 small captioned strips below
  Focal pt   : the geometric panel itself (the manifold)
  Exemplar   : (no direct match yet)
  Strengths  : powerful for spatial / embedding stories
  Trade-offs : poor fit if the contribution is sequential or branching

Candidate C — Training vs inference, two rows
  Structure  : training row (3 sub-panels) | inference row (3 sub-panels)
               with shared learned object drawn identically in both
  Layout     : two horizontal rows, mid-figure colour legend separates
  Focal pt   : the bridge / construction panel in the training row
  Exemplar   : exemplars/two-row-training-inference.md
  Strengths  : ideal when training and inference are the two stages
               that share a learned object; the cross-row repeat
               communicates "same network, two stages" without text
  Trade-offs : only fits papers with two parallel stages; a sequential
               pipeline paper would feel forced into this shape
```

Then ask: *"Pick A / B / C, request a hybrid (e.g. 'A's outer + B's
geometric centerpiece'), or tell me what's still missing and I'll
regenerate with that constraint."*

### Common human responses and what the agent does

- *"A"* → proceed with A as-is, move to Phase 3.
- *"B but with C's centre"* → produce one hybrid spec, confirm, proceed.
- *"None — the focal point must be X"* → regenerate with that
  constraint, present another round.
- *"A, but show me one more variant where Phase 2 is simpler"* → keep
  A, generate a refinement, re-present.

The agent does not push back on the human's choice. The agent does
flag if the choice will make some invariant hard to satisfy ("with
this layout the β_x focal point is ~30 % of canvas; want me to
proceed or adjust?") — but the decision still belongs to the human.

### Symptoms of bad candidates the agent should self-filter before presenting

- Need text on a panel to explain what it shows (visual encoding
  failed; redesign before showing).
- Arrows fan out everywhere (the layout is fighting the flow;
  restructure).
- One giant central panel surrounded by small "explanation" panels
  (the central panel is doing too many jobs; split or simplify).
- The novelty isn't the focal point (invariant 6 violation).
- A panel fails the 5-second skim by inspection.

Don't waste the human's attention on candidates that already fail
invariants; surface only candidates worth a real decision between.

## Combine plotting libraries to fit the asset

Inside an asset, **compose** the installed libraries (matplotlib,
scipy, sklearn, seaborn, plus any Tier 2 / 3 you've installed) —
don't restrict yourself to a single backend per asset.

The composition examples in `asset-strategy.md` are seeds, not the
full set. New combinations are valid as long as:
- the resulting PNG passes the 5-second skim alone;
- it has no leaked axis chrome / numerics / operator labels;
- it stays under ~ 2 s per render (cache UMAP / TSNE if needed).

## Choose the palette from the paper

Once you know the paper's ontology (Phase 1, item 3), assign one
colour per concept. Put it in `COLORS = {...}` in
`scripts/<figure>/generate_figure.py`. Use only those colours; the
skill ships **no** default ML palette.

Suggestions for picking colours:
- Pastel / mid-saturation works at conference scale; very-saturated
  hurts contrast against asset content.
- Dark red is the standard for "the thing being suppressed" but pick
  what the paper's ontology demands.
- Greens are easy to confuse with blues at small sizes; pick one.
- Test under colour-blind simulation (one common: deuteranopia) if
  the figure relies on red / green distinction.

## When in doubt, fewer elements

Every additional panel, glyph, arrow, label is a 5-second tax on the
reviewer. Strip until the visual story is the *minimum sufficient*
to land the paper's novelty sentence. Then stop.
