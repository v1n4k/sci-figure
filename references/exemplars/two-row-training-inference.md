# Two-row TRAINING / INFERENCE split · pattern exemplar

## What this exemplar covers

A figure pattern for any paper whose method has two distinct
conceptual stages — typically **training** and **inference** — that
share a learned object (e.g. the same network used both to learn a
target and later to roll out predictions). The pattern is common in
generative modelling, sampling / rollout methods, and many RL papers.

The analysis below is generic — it describes the design pattern
itself, not any particular paper.

## Why the pattern works

### Layout: two horizontal rows with stage labels

The paper has two distinct conceptual stages that share a learned
object. The natural layout is **two horizontal rows**, one per stage,
with the shared object visually appearing in both. Stage labels at
the left margin (`TRAINING`, `INFERENCE`) make the split unmistakable.

This is *not* a 3-column phase layout (which would suggest a single
linear pipeline) and *not* a comparative side-by-side (which would
suggest two competing methods). The two-row stages-of-life pattern
is genuinely distinct and deserves a name in the layout menu.

### Focal point alignment with the novelty

The most visually prominent panel — typically the visual centre of
the dominant top row — should host the paper's actual contribution.
That panel earns its weight by being:

- the visual centre of the dominant row,
- the most-explained (the densest cluster of inline asides and
  one-line equations),
- the only panel that explicitly shows whatever dual relationship
  the contribution is built on.

A reviewer's eye lands there first. That panel *is* the contribution.

### Shared visual element across rows

The learned object (the network, the operator, the policy — whatever
the paper has just one of) is rendered **identically** in both rows.
This is the single most powerful design move in the pattern: the
figure says *"the same learned object handles both stages"* visually,
before the reader reads any text. Most method-overview figures fail
to do this — they redraw each stage's network as a separate box and
the reader has to verify equivalence by name-matching.

### Color discipline

A small, fixed semantic palette — typically four concept colours plus
neutrals — encoded in three reinforcing places:

1. A mid-figure legend strip naming each colour's concept.
2. The border colour of every embedded thumbnail / heatmap (a thumbnail
   of concept *X* wears concept *X*'s colour as its border).
3. The arrow / equation colour in the relevant panel.

This triple reinforcement is why the figure reads at a glance:
seeing a coloured thumbnail already triggers the concept before any
label is read.

### Mid-figure legend strip as row separator

The colour legend sits *between* the two rows, not at the top of the
figure. Structurally clever:

- It physically separates the two rows, helping the eye parse the
  two-row structure.
- It documents the palette at the boundary where it's most needed —
  both rows reference the same colours.
- It substitutes for a horizontal divider line, which would feel
  more bureaucratic.

### Equation density: short definitions only

Every displayed equation in the figure should be **a one-line
definition of a symbol the figure introduces** — never a derivation,
never a manipulated identity. The equations *replace* what would
otherwise be verbose verbal labels. Each equation sits next to where
the symbol first appears.

The rule is qualitative rather than a fixed quota: *no derivation
walls; one-line definitions of newly introduced notation are fine when
they help the visual story land faster than a prose label would*.

### In-panel italic asides instead of mechanics boxes

Short coloured italic phrases inside panels do the job of mechanics
labels but without the "labelled box" feel. They orient the eye,
identify what's being shown visually, and stay out of the way. They
describe *the visual element* (a curve, a line, a behaviour), not
the operation that produced it.

### Encoding consistency

A small typographic / linework code, applied consistently across both
rows. A representative code:

| Visual property | Meaning |
|---|---|
| Solid coloured arrow | data flow in that semantic stream |
| Dashed coloured arrow | "same as" / cross-stream reference |
| Curved dashed line | notional / abstract relationship |
| Coloured border on thumbnail | semantic role of the field |
| Star marker | unique identifier (e.g. an unseen-time query) |

The code stays consistent across both rows.

### Sub-panel containers

The skill's `sub_panel(x, y, w, h, "[A]", "title")` helper produces
the right style for this pattern: bold square `[A]` tag, italic
title to its right, thin grey separator beneath, rounded grey frame.

## Patterns worth lifting

For papers with **training vs inference** structure (most generative
modelling papers, most rollout / sampling papers, many RL papers):

- **Two-row split** with stage labels at the left margin.
- **Mid-figure legend** doubling as row separator.
- **Shared learned object** rendered identically in both rows.
- **Colour-coded thumbnail borders** to reinforce semantic role.

For **any paper introducing new notation**:

- **One-line displayed definitions** anchored where each symbol first
  appears. Keep them sparse; never use a derivation chain.
- **Italic in-panel asides** in the relevant semantic colour to
  orient the eye, replacing mechanics-naming boxes.

For **any paper with a clear single contribution**:

- Place the contribution panel at the **visual centre of the
  dominant row** (not at an edge, not in a smaller secondary panel).
- Give it more ink, more captions, and the densest equation
  population — to mark it as the focal point.

## Things to be careful with

- The two-row pattern only works when the paper genuinely has two
  parallel stages with a shared object. Don't force it onto a
  sequential pipeline (use 3-column phase) or a comparative claim
  (use side-by-side).
- The shared-object trick only works when the *same* learned object
  literally appears in both stages. If training and inference use
  different networks, redrawing the same box in both rows would
  mislead.
- Around six displayed equations is a *lot*. Each is justified only
  if it defines one symbol the figure introduces; if any symbol
  could be omitted, its equation should go too.
- This pattern relies on data-looking thumbnails (heatmaps, fields,
  rendered samples). For a paper without natural thumbnail content
  (e.g. a tabular-data paper), the asset territory is different.

## ASCII layout sketch

```
TRAINING                                  "<paper title> · overview"  →
┌─[A] <setup panel>──┐ ┌─[B] <contribution panel>─┐ ┌─[C] <objective panel>────────┐
│                    │ │                          │ │                              │
│  thumbnail ──→     │ │  contribution shown      │ │  shared object ─→ predicted  │
│                    │ │  as the dual relation    │ │                  output      │
│  one-line def      │ │  (curve above,           │ │                              │
│  of a new symbol   │ │   line below, etc.)      │ │       ┌─ loss box ─┐         │
│                    │ │  one-line defs anchored  │ │       │            │         │
└────────────────────┘ └──────────────────────────┘ └───────└────────────┘─────────┘

         ● concept-1   ● concept-2   ● concept-3   ● concept-4    [legend separates rows]

INFERENCE
┌─[D] <init panel>──┐ ┌─[E] <generator panel>────┐ ┌─[F] <rollout panel>───────────┐
│                   │ │                          │ │                               │
│  initial state    │ │  shared learned object   │ │  t_0 ─ t_1 ─ ★ ─ t_q          │
│  thumbnail        │ │  (rendered identically   │ │                               │
│                   │ │   to the panel above)    │ │  one-line def of the          │
│  one-line def     │ │                          │ │  rollout map                  │
│                   │ │  step labels k1..k4      │ │                               │
└───────────────────┘ └──────────────────────────┘ └───────────────────────────────┘
```
