# Two-row failure/fix with iterative core readout · pattern exemplar

## What this exemplar covers

A dense landscape figure pattern for papers whose main story is best
shown as **a failure mechanism followed by a controlled fix**. Use it
when the paper needs the reader to first understand why a naive feedback
process fails, then understand how the proposed method controls that
feedback through an iterative core and reads out a final distribution or
decision only after convergence.

This is a **style-only abstraction** from a user-provided local figure.
Do not copy source labels, notation, domain objects, paper claims, file
paths, or icon meanings.

## Why the pattern works

### Layout: two rows, failure above fix

The figure uses two wide horizontal rows:

- the top row shows the failure context and a grouped failure loop,
- the bottom row shows the corrected method with an iterative core and
  a final readout panel.

This lets the reviewer compare "what goes wrong" and "what the method
controls" without treating the fix as a long one-way pipeline.

### Failure context is not drawn as a causal source

The top row separates a sparse or weak-evidence context from the actual
failure mechanism. A visible amplifier badge between them says "this
context magnifies the loop" without implying that the context itself
creates the error mode. The loop panels are wrapped in one tinted group,
so the reader sees them as one mechanism before reading each label.

### Iterative core is wrapped, final readout is outside

In the bottom row, the controlled inference panel and the parameter /
state-update panel are enclosed in a light wrapper. The wrapper says
these panels iterate together. The final output panel sits outside that
wrapper and reads from the converged state, rather than receiving a
direct arrow from the update panel.

This prevents a common mistake: drawing an iterative method as if each
panel simply produces the next panel once.

### Colour semantics stay concept-local

The palette is concept-driven:

- red for failure, overconfidence, blocked feedback, or warning paths;
- blue for local / controlled evidence;
- amber for shared state or parameter components;
- purple for global or final readout distributions;
- neutral grey for structural grouping, priors, and repeated items.

The key discipline is negative: do not reuse amber for unrelated
"shared item" markers if amber already means shared model components,
and do not let blue become the colour for the entire method if it means
only one local stream.

### Stroke hierarchy reduces clutter

The row containers have the strongest outlines, major conceptual panels
use medium outlines, and inner histogram boxes / grouping marks use thin
outlines. This hierarchy lets a dense figure stay readable without
needing large empty margins.

### Bars represent different semantic levels

Multiple bar-strip glyphs can coexist if their labels distinguish the
levels:

- evidence summaries are labelled as evidence, not posteriors;
- local and global distributions inside the iterative core are labelled
  as iterative quantities;
- the final readout distribution is labelled as converged.

This matters because identical-looking histograms can otherwise imply
that every intermediate bar chart is already a final prediction.

### Assets are semantic thumbnails, not containers

Raster assets are tightly cropped and contain only the visual content:
grids, heatmaps, scatter fields, or similar thumbnails. Titles,
notation, panel frames, arrows, legends, and callouts stay in drawio so
they can be edited and aligned after the layout is built.

## Patterns worth lifting

- **Two-row failure/fix narrative**: top row demonstrates the pathology;
  bottom row demonstrates the controlled method.
- **Amplifier badge** between context and mechanism when the context
  magnifies but does not cause the failure mode.
- **Grouped failure loop**: several failure panels in one tinted wrapper
  with a dashed return hint.
- **Iterative-core wrapper** around the panels that update each other,
  with the final readout kept outside the wrapper.
- **Converged readout panel**: no internal arrow tangle; use a clean
  `uses:` list or aligned chips for final uses.
- **Stacked-card effect** only for quantities that genuinely have many
  instances, such as block-local or sample-local objects.
- **Aligned component positions** when a lower panel visualizes weights
  over the same components shown above.
- **Drawio-native math labels** for notation, with PNG assets kept free
  of text and frames.

## Things to be careful with

- Do not use this pattern for a simple feed-forward architecture; the
  iterative wrapper will overcomplicate the story.
- The failure row must not overclaim causality. Use visual grammar to
  distinguish "amplifies" from "causes".
- Keep the final readout outside the iterative core. If it sits inside
  the wrapper, readers may think the prediction is available before
  convergence.
- Do not stack a card just because there are multiple conceptual
  sources. Stack only when the represented quantity itself has multiple
  instances.
- Watch for dead space in wide panels. Shrink the panel or move content;
  do not let invisible PNG whitespace create layout margins.

## ASCII layout sketch

```
                                 <short figure title>

[A] <weak evidence amplifies a self-reinforcing failure loop>
+----------------------+   +-------------------------------------------------------------+
| context / sparse     | + | grouped failure mechanism                                  |
| evidence thumbnail   |-->| panel 1 -> panel 2 -> panel 3                              |
|                      |   |       ^ . . . . . . . . . . . . . . . . . . . . . . . . . |
+----------------------+   +-------------------------------------------------------------+

[B] <method controls feedback and reads out only after convergence>
+----------------------+   +-------------------------------------------------------------+  +------------------+
| setup / partition    |-->| iterative core wrapper                                     |->| final readout    |
| graph-like thumbnail |   | +-----------------------+  <=>  +-------------------------+ |  | converged dist.  |
| aligned block rows   |   | | controlled inference  |       | parameter / state update | |  | uses:            |
+----------------------+   | | local + global bars   |       | shared components        | |  | [decision]       |
                           | +-----------------------+       +-------------------------+ |  | [soft target]    |
                           +-------------------------------------------------------------+  +------------------+
```
