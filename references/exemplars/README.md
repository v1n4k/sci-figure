# Exemplars — top-conference figures, annotated

This directory holds **annotated examples of figures that work**.
Each entry analyses *why* the figure lands at top-conference quality
so an agent generating layout candidates (Phase 2 of the workflow)
has concrete patterns to draw from rather than only abstract rules.

## How to use these

**During Phase 1 (Read & understand):** scan the exemplar list and
note which have a similar conceptual structure to the paper at hand
(mechanism vs comparison vs geometry vs training-vs-inference vs …).

**During Phase 2 (Design — explore):** the candidates you generate
should *reference patterns from these exemplars where applicable*.
"Candidate A: 3-column phase like exemplars/X" is a richer
description than "Candidate A: 3-column phase".

**Before showing the human candidates:** if your candidate looks
nothing like any exemplar pattern, that's not a bug — sometimes the
paper genuinely needs a new shape — but it's worth asking yourself
why no proven pattern fits. Often the answer is that you mis-read the
paper's conceptual structure in Phase 1.

## What each exemplar contains

- **Pattern provenance.** Public examples may cite a source; private or
  user-provided examples must be anonymized and reduced to style /
  layout grammar only.
- **What the pattern shows.** One paragraph: the reusable figure role
  and conceptual structure, not private claims or project semantics.
- **Why it works.** Concrete things the figure does right, mapped to
  the skill's invariants and patterns.
- **Patterns worth lifting.** Reusable design choices an agent can
  cite when proposing a candidate for a similar paper.
- **Things to be careful with.** Aspects that work for one conceptual
  structure but might not generalise.

## Adding new exemplars

If you find a figure that should be in this set, add a new
`.md` file here following the template above. Keep each entry under
~150 lines. The exemplar set is most useful when entries are
diverse — prefer adding a figure that demonstrates a *different*
pattern over one that's similar to existing entries.

For private or user-provided figures, do not copy source labels,
notation, task names, file paths, project names, or paper claims. Keep
only the transferable style and layout pattern.

## Current exemplars

- `numbered-modular-feedback-map.md` — wide modular system map with
  numbered panels, semantic containers, a right-side status column, and
  a bottom feedback / control strip.
- `two-row-training-inference.md` — TRAINING vs INFERENCE two-row
  split; shared learned-object across rows; mid-figure colour legend
  serving as row separator.
- `two-row-failure-fix-iterative-readout.md` — two-row failure/fix
  narrative; grouped failure loop above, iterative method core plus
  converged readout below.
