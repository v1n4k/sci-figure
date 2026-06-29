# Quality Bar — strong defaults, not dogma

These defaults fit most AI/ML method figures. They are not a religion:
when a paper genuinely needs an exception, record the reason in
`requirements.md`, make the exception visually legible, and keep the
main message image-first. Anything not listed here (panel arrangement,
sub-panels, palette concepts, glyph types, page geometry, library
combinations) is a design choice you derive from the paper.

## 1. Math supports the picture, not the reverse

The forbidden pattern is a multi-line derivation chain, a manipulated
identity, or any equation block that the reader has to *parse* rather
than *recognise*.

What's allowed: **one-line definitions** of symbols the figure
introduces. A definition like `z = f(w)` placed next to where `z`
first appears, or a target like `v* = Δq/Δt` placed next to the
construct it defines — these *replace* what would otherwise be
verbose verbal labels and earn their place in the figure.

Practical guidance:

- Each equation is one line, defines exactly one new symbol the
  figure introduces, and sits adjacent to where that symbol first
  appears.
- Keep definitions rare. If the figure starts to look like a notation
  sheet, replace math with visual encoding or move detail to the paper.
- Avoid derivation chains. `a → b → c → d` developed across cells
  usually belongs in the paper text, not the figure.
- Avoid manipulated identities. No "= reduces to ... = simplifies
  to ..." unless the transformation itself is the visual claim.
- Single-symbol inline notation labels on arrows / glyphs / captions
  (`L_r`, `β_x`, `D_f`, `μ_{ℓ,c}`, `\tilde P`) are not equations and
  don't count toward the limit.

Why: a main figure is a poster, not a derivation. The 5-second skim
test fails when the eye has to parse a chained formula. A *single
line* defining a symbol can be recognised quickly and add explanatory
power; a *block* of math forces real reading and steals attention from
the visual story.

## 2. Prefer visual quantities over numeric labels

Avoid `0.62`, `α = 0.55`, axis-tick numbers on probability bars, and
percentages baked into glyphs when a visual encoding can carry the
magnitude. Prefer **bar height, line thickness, fill saturation, gauge
needle position, glyph length, position, or area**.

Use a number only when it is itself the visual claim or when removing
it would make the figure less honest.

Why: numbers often force the reader to compare digits across panels
instead of comparing visual quantities at a glance. They also imply a
precision that many illustrative figures do not have.

## 3. Avoid derivation chains

If a quantity is defined by 3 + chained intermediates (`a → b → c → d`),
collapse the chain to a single visual flow that lands on one summary
element. Intermediate symbols usually stay in the paper text.

## 4. Avoid notation glossaries or mechanics boxes

Avoid legend tables inside the figure body. Avoid labelled boxes for
operators that just name an operation: `softmax`, `normalize`,
`cosine`, `linear`. Show what an operator *produces* (a probability
bar, a similarity fan, a scalar gauge), not its name. Keep a name only
when omitting it would create a worse ambiguity.

Symbols introduced in the figure get a colour tag plus a one-line
semantic caption on the panel where they first appear.

## 5. Stable palette semantics within each figure

Pick the palette **from the paper's ontology** — the actual concepts
the paper distinguishes. Explore alternatives, then encode the chosen
mapping in the per-figure script's `COLORS` dict. Avoid reusing a
colour for unrelated concepts within the figure.

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
