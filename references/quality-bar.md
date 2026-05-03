# Quality Bar — the only invariants

These survive across every paper, every layout, every asset
combination. Anything not listed here (panel arrangement, sub-panels,
palette concepts, glyph types, page geometry, library combinations)
is a design choice you derive from the paper.

## 1. No derivation walls in the figure body

The forbidden pattern is a multi-line derivation chain, a manipulated
identity, or any equation block that the reader has to *parse* rather
than *recognise*.

What's allowed: **one-line definitions** of symbols the figure
introduces. A definition like `z = f(w)` placed next to where `z`
first appears, or a target like `v* = Δq/Δt` placed next to the
construct it defines — these *replace* what would otherwise be
verbose verbal labels and earn their place in the figure. The
exemplar `exemplars/two-row-training-inference.md` uses around six
such definitions and reads cleanly because none is a derivation.

Practical limits:

- Each equation is one line, defines exactly one new symbol the
  figure introduces, and sits adjacent to where that symbol first
  appears.
- Across the whole figure, ≤ 6 such definitions. If you're tempted
  past that, you're probably trying to land too much in one figure
  (see `anti-patterns.md` figure-bloat).
- **Zero derivation chains.** `a → b → c → d` developed across cells
  belongs in the paper text, never in the figure.
- **Zero manipulated identities.** No "= reduces to ... = simplifies
  to ...". One side of an equals sign at most.
- Single-symbol inline notation labels on arrows / glyphs / captions
  (`L_r`, `β_x`, `D_f`, `μ_{ℓ,c}`, `\tilde P`) are not equations and
  don't count toward the limit.

Why: a main figure is a poster, not a derivation. The 5-second skim
test fails immediately when the eye has to parse a chained formula.
A *single line* defining a symbol is recognisable in under a second
and adds explanatory power; a *block* of math forces real reading and
loses the skim.

## 2. No specific numeric values

No `0.62`, no `α = 0.55`, no axis-tick numbers on probability bars,
no percentages baked into a glyph. **Bar height, line thickness, fill
saturation, gauge needle position, glyph length** carry magnitude.

Why: numbers force the reader to compare digits across panels instead
of comparing visual quantities at a glance. They also imply a
precision that an illustrative figure does not have.

## 3. No derivation chains

If a quantity is defined by 3 + chained intermediates (`a → b → c → d`),
collapse the chain to a single visual flow that lands on one summary
element. Intermediate symbols stay in the paper text.

## 4. No notation glossaries or mechanics boxes

No legend table inside the figure body. No labelled boxes for
operators that just name an operation: `softmax`, `normalize`,
`cosine`, `linear`. Show what an operator *produces* (a probability
bar, a similarity fan, a scalar gauge), not its name.

Symbols introduced in the figure get a colour tag plus a one-line
semantic caption on the panel where they first appear.

## 5. Fixed palette per figure with no colour reuse

Pick the palette **from the paper's ontology** — the actual concepts
the paper distinguishes. Encode it once in the per-figure script's
`COLORS` dict and never reuse a colour for an unrelated concept
within the figure.

Examples of paper-driven ontologies (each picks its own colours, none
of these is a default):
- An unlearning paper distinguishes *retain / forget / frozen-original
  / unlearned / target* concepts.
- A contrastive-learning paper distinguishes *anchor / positive /
  negative / projection*.
- A diffusion paper distinguishes *clean / noisy / score-network /
  reverse-process / sample*.
- A knowledge-distillation paper distinguishes *teacher / student /
  soft-target / hard-target*.

Do **not** import a palette from another paper's figure as if it were
universal. The colours mean what *this* paper says they mean.

## 6. Single visual focal point

Every figure has **one element the eye lands on first**, and it must
be the paper's novelty. Multiple equally-weighted regions confuse the
reading order; a reviewer who skims for 200 ms before deciding
whether to read on must register the contribution from the focal
element alone.

Make the focal element win on ≥ 2 of: size, contrast, saturation,
border weight, central position. Supporting infrastructure (frozen
models, retain pipelines, baseline branches, reference distributions)
must read as quieter than the contribution.

If a reviewer covering the rest of the figure for 200 ms can't
identify "what this paper is doing" from the focal region alone, the
visual hierarchy is broken — even if every other invariant passes.

## 7. Visual encoding consistency

Within one figure, **the same visual property always means the same
thing**. Establish the code once and follow it everywhere:

- *Stroke style* — solid arrow = forward data flow; dashed arrow =
  supervision / cross-phase reference / precomputed; thin grey =
  ancillary / auxiliary connection.
- *Stroke weight* (px) encodes salience: punchline / final output ≥ 4;
  primary mechanism flow 3; secondary connection 2; ancillary 1–1.5.
- *Arrowhead shape* — pick one (block / open / classic) per figure;
  a second shape is reserved for a deliberately distinct edge type
  (e.g. backward gradient).
- *Glyph idiom* — if thumbnails are square, all thumbnails are square;
  if model glyphs are stacked rectangles, every model is stacked
  rectangles.

A figure that uses dashed for "ancillary" in one panel and dashed for
"supervision" in another is broken even if every other invariant
passes — the reviewer learns the code panel-by-panel and gets
contradictory signals.

## 8. The 5-second skim test (per panel and reverse)

**Forward.** Cover all but one panel; a fresh reviewer (or an agent
reviewer reading the bounded review PNG) must articulate that panel's
single visual message **without reading any equation**. If they
cannot, the panel is too dense — split, simplify, or remove elements.

**Reverse.** Show the *whole* figure for 5 seconds, then cover it.
What does the reviewer remember? *That* is the figure's actual
signal. If they remember the prettiest asset rather than the
contribution, the visual hierarchy (invariant 6) is wrong.

## 9. Demonstration over numeric calculation

Visual encoding (height, thickness, saturation, position, area)
always beats annotated numbers. If you find yourself wanting to write
"= 0.78" anywhere on a bar / glyph / arrow, redesign so the visual
encoding alone communicates the magnitude.
